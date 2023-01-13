# Owlready2
# Copyright (C) 2021 Jean-Baptiste LAMY
# LIMICS (Laboratoire d'informatique médicale et d'ingénierie des connaissances en santé), UMR_S 1142
# University Paris 13, Sorbonne paris-Cité, Bobigny, France

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys, os
from owlready2 import *

"""

Not supported:

ASK
DESCRIBE
LOAD, ADD, MOVE, COPY, CLEAR, DROP

GRAPH, FROM, FROM NAMED

CONSTRUCT

SERVICE

INSERT DATA, DELETE DATA, DELETE WHERE (use INSERT or DELETE instead)

VALUES

MINUS

"""

from owlready2.sparql.parser import *
from owlready2.sparql.func   import register_python_function, FuncSupport


class Translator(object):
  def __init__(self, world, error_on_undefined_entities = True):
    self.world                         = world
    self.error_on_undefined_entities   = error_on_undefined_entities
    self.prefixes                      = { "rdf:" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdfs:" : "http://www.w3.org/2000/01/rdf-schema#", "owl:" : "http://www.w3.org/2002/07/owl#", "xsd:" : "http://www.w3.org/2001/XMLSchema#", "obo:" : "http://purl.obolibrary.org/obo/", "owlready:" : "http://www.lesfleursdunormal.fr/static/_downloads/owlready_ontology.owl#" }
    self.base_iri                      = ""
    self.current_anonynous_var         = 0
    self.current_parameter             = 0
    self.main_query                    = None
    self.preliminary_selects           = []
    self.recursive_preliminary_selects = {}
    self.escape_mark                   = "@@@ESCAPE@@@"
    
    if not getattr(world.graph, "_has_sparql_func", False):
      register_python_function(world)
      world.graph._has_sparql_func = True
      
  def parse(self, sparql):
    while self.escape_mark in sparql:
      self.escape_mark += "ç"
    CURRENT_TRANSLATOR.set(self)
    self.main_query = PARSER.parse(LEXER.lex(sparql))
    
    sql = ""
    if self.preliminary_selects:
      sql += "WITH "
      if max(prelim.recursive for prelim in self.preliminary_selects): sql += "RECURSIVE "
      sql += ",\n\n".join(prelim.sql() for prelim in self.preliminary_selects)
      sql += "\n\n"
    sql += self.main_query.sql()
    
    if self.solution_modifier[0]:
      sql += " GROUP BY %s" % ", ".join(self.main_query.parse_expression(x) for x in self.solution_modifier[0])
    if self.solution_modifier[1]:
      sql += " HAVING %s" % self.main_query.parse_expression(self.solution_modifier[1])
    if self.solution_modifier[2]:
      sql += " ORDER BY %s" % ", ".join(self.main_query.parse_expression(x) for x in self.solution_modifier[2])
    if self.solution_modifier[3]:
      sql += " LIMIT %s"  % self._to_sql(self.solution_modifier[3])
    if self.solution_modifier[4]:
      if not self.solution_modifier[3]: sql += " LIMIT -1" # SQLite requires a LIMIT clause before the OFFSET clause
      sql += " OFFSET %s" % self._to_sql(self.solution_modifier[4])
      
    nb_parameter = self.current_parameter
    parameter_2_parameter_datatypes = {}
    parameter_datatypes = []
    if self.escape_mark in sql:
      def sub(m):
        escape = m.group(0)[len(self.escape_mark):]
        if escape.startswith("TypeOfParam?"):
          number = int(escape[12:])
          r = parameter_2_parameter_datatypes.get(number)
          if r is None:
            r = parameter_2_parameter_datatypes[number] = self.new_parameter()
            parameter_datatypes.append(number - 1)
        return "?%s" % r
      sql = re.sub("%s[^ ]*" % self.escape_mark, sub, sql)
      
    if   self.main_query.type == "select":
      return PreparedSelectQuery(self.world, sql, [column.var for column in self.main_query.columns if not column.name.endswith("d")], [column.type for column in self.main_query.columns], nb_parameter, parameter_datatypes)
    
    elif self.main_query.type == "modify":
      select_param_indexes = [i - 1 for i in self.main_query.select_param_indexes]
      return PreparedModifyQuery(self.world, sql, [column.var for column in self.main_query.columns if not column.name.endswith("d")], [column.type for column in self.main_query.columns], nb_parameter, parameter_datatypes, self.world.get_ontology(self.main_query.ontology_iri.value) if self.main_query.ontology_iri else None, self.parse_inserts_deletes(self.main_query.deletes, self.main_query.columns), self.parse_inserts_deletes(self.main_query.inserts, self.main_query.columns), select_param_indexes)
    
  def parse_inserts_deletes(self, triples, columns):
    var_2_column = { column.var : column for column in self.main_query.columns if not column.name.endswith("d") }
    r = []
    for triple0 in triples:
      triple = []
      for x in triple0:
        if   hasattr(x, "storid"):
          triple.append(("objs", x.storid))
        elif x.name == "VAR":
          if x.value.startswith("??anon") or x.value.startswith("_:"): # a new blank node
            triple.append(("bn", x.value))
          else: # a normal var
            column = var_2_column[x.value]
            triple.append(("vars", column.index))
            if len(triple) == 3: # in 'o' position => can be objs or datas!
              if column.index + 1 < len(columns):
                next_column = columns[column.index]
                if next_column.name.endswith("d"):
                  triple.append(("vars", next_column.index))
        elif x.name == "PARAM":
          triple.append(("param", x.number - 1))
          if len(triple) == 3: # in 'o' position => can be datas!
            triple.append(("paramdatatype", x.number - 1))
        else:
          if   isinstance(x.value, locstr):
            triple.append(("datas", x.value[1:-1]))
            triple.append(("datas", "@%s" % x.value.lang))
          else:
            if isinstance(x.value, str): v, d = self.world._to_rdf(x.value[1:-1])
            else:                        v, d = self.world._to_rdf(x.value)
            d2 = getattr(x, "datatype", None) or d
            triple.append(("datas", v))
            triple.append(("datas", d2))
            
      r.append(triple)
    return r
  
  def new_sql_query(self, name, block, selects = None, distinct = None, solution_modifier = None, preliminary = False, extra_binds = None, nested_inside = None):
    if preliminary and not name: name = "prelim%s" % (len(self.preliminary_selects) + 1)

    if isinstance(block, UnionBlock) and block.simple_union_triples: block = SimpleTripleBlock(block.simple_union_triples)
    
    if   isinstance(block, SimpleTripleBlock):
      s = SQLQuery(name)
      
    elif isinstance(block, OptionalBlock):
      s = SQLQuery(name)
      s.optional = True
      
    elif isinstance(block, UnionBlock):
      s = SQLCompoundQuery(name)
      if selects is None: selects = block.get_ordered_vars()
      
    elif isinstance(block, FilterBlock):
      s = SQLNestedQuery(name)
      if isinstance(block, ExistsBlock): s.extra_sql = "IS NOT NULL"
      else:                              s.extra_sql = "IS NULL"
      s.next_table_id = nested_inside.next_table_id
      s.vars = nested_inside.vars
      preliminary = False
      
    elif isinstance(block, NotExistsBlock):
      s = SQLCompoundQuery(name)
      
    elif isinstance(block, SubQueryBlock):
      s = block.parse()
      s.name = "prelim%s" % (len(self.preliminary_selects) + 1)
      
    else:
      raise ValueError("Unknown block type '%s'!" % block)
    
    if preliminary:
      s.preliminary = True
      self.preliminary_selects.append(s)
      
    extra_binds = extra_binds or []
    if isinstance(selects, list): # Otherwise, it is "SELECT *"
      for i, select in enumerate(selects):
        if isinstance(select, list): # ( expression AS var )
          selects[i] = select[2]
          bind = Bind(select[0], select[2])
          extra_binds.append(bind)
          
          
    if   isinstance(block, (SimpleTripleBlock, OptionalBlock, FilterBlock)):
      s.parse_distinct(distinct)
      
      for i in block:
        if isinstance(i, Bind): s.prepare_bind(i)
      for bind in extra_binds: s.prepare_bind(bind)
      
      s.parse_selects(selects)
      
      s.parse_triples(block)
      for bind in extra_binds: s.parse_bind(bind)
      
      s.finalize_columns()
      
    elif isinstance(block, UnionBlock):
      for alternative in block:
        query = self.new_sql_query(None, alternative, selects, distinct, None, False, extra_binds)
        s.append(query, "UNION")
      s.finalize_compounds()
      
      
    if isinstance(block, FilterBlock):
      nested_inside.next_table_id = s.next_table_id
      
    if (not preliminary) and solution_modifier: self.solution_modifier = solution_modifier
    return s

  def expand_prefix(self, prefix):
    expanded = self.prefixes.get(prefix)
    if expanded: return expanded
    prefix0 = prefix[:-1] # Remove trailing :
    for ontology in self.world.ontologies.values():
      if prefix0 == ontology.name:
        self.prefixes[prefix] = ontology.base_iri
        return ontology.base_iri
    raise ValueError("Undefined prefix '%s'!" % prefix)

  def abbreviate(self, entity):
    if self.error_on_undefined_entities:
      r = self.world._abbreviate(entity, False)
      if r is None: raise ValueError("No existing entity for IRI '%s'! (use error_on_undefined_entities=False to accept unknown entities in SPARQL queries)" % entity)
      return r
    else:
      return self.world._abbreviate(entity)
  
  def _to_sql(self, x):
    if x.name == "PARAM": return "?%s" % x.number
    return x.value
    
  def new_var(self):
    self.current_anonynous_var += 1
    return "??anon%s" % self.current_anonynous_var

  def new_parameter(self):
    self.current_parameter += 1
    return self.current_parameter
  
  def get_recursive_preliminary_select(self, triple, fixed, fixed_var, prelim_triples):
    prelim = self.recursive_preliminary_selects.get((triple, fixed, fixed_var, tuple(prelim_triples)))
    if not prelim:
      self.recursive_preliminary_selects[triple, fixed, fixed_var, tuple(prelim_triples)] = prelim = SQLRecursivePreliminaryQuery("prelim%s" % (len(self.preliminary_selects) + 1), triple, fixed, fixed_var)
      self.preliminary_selects.append(prelim)
      prelim.build(triple, prelim_triples)
    return prelim


class PreparedQuery(object):
  def __init__(self, world, sql, column_names, column_types, nb_parameter, parameter_datatypes):
    self.world               = world
    self.sql                 = sql
    self.column_names        = column_names
    self.column_types        = column_types
    self.nb_parameter        = nb_parameter
    self.parameter_datatypes = parameter_datatypes
  
  def execute(self, params = ()):
    self.world._nb_sparql_call += 1
    sql_params = [self.world._to_rdf(param)[0] for param in params]
    for i in self.parameter_datatypes: sql_params.append(self.world._to_rdf(params[i])[1])
    return self.world.graph.execute(self.sql, sql_params)
  
class PreparedSelectQuery(PreparedQuery):
  def execute(self, params = ()):
    for l in PreparedQuery.execute(self, params):
      l2 = []
      i = 0
      while i < len(l):
        if self.column_types[i] == "objs":
          if l[i] is None: l2.append(None)
          else:            l2.append(self.world._to_python(l[i], None) or l[i])
          i += 1
        else:
          if l[i + 1] is None:
            if l[i] is None: l2.append(None)
            else:            l2.append(self.world._to_python(l[i], None) or l[i])
          else:
            l2.append(self.world._to_python(l[i], l[i + 1]))
          i += 2
      yield l2
      
class PreparedModifyQuery(PreparedQuery):
  def __init__(self, world, sql, column_names, column_types, nb_parameter, parameter_datatypes, ontology, deletes, inserts, select_param_indexes):
    PreparedQuery.__init__(self, world, sql, column_names, column_types, nb_parameter, parameter_datatypes)
    
    column_name_2_index = { column_name : i for (i, column_name) in enumerate(column_names) }
    self.ontology = ontology
    self.deletes  = deletes
    self.inserts  = inserts
    self.select_param_indexes = select_param_indexes
    
  def execute(self, params = ()):
    nb_match = 0
    if self.sql: resultss = PreparedQuery.execute(self, [params[i] for i in self.select_param_indexes])
    else:        resultss = [[]]
    for results in list(resultss):
      nb_match += 1
      
      for delete in self.deletes:
        triple = []
        for type, value in delete:
          if   type == "vars":          triple.append(results[value])
          elif type == "param":         triple.append(self.world._to_rdf(params[value])[0])
          elif type == "paramdatatype": triple.append(self.world._to_rdf(params[value])[1])
          else:                         triple.append(value)
        #print("DEL", triple)
        self.world._del_triple_with_update(*triple)
        
      bns = {}
      for insert in self.inserts:
        triple = []
        for type, value in insert:
          if   type == "vars":          triple.append(results[value])
          elif type == "bn":            triple.append(bns.get(value) or bns.setdefault(value, self.world.new_blank_node()))
          elif type == "param":         triple.append(self.world._to_rdf(params[value])[0])
          elif type == "paramdatatype": triple.append(self.world._to_rdf(params[value])[1])
          else:                         triple.append(value)
        #print("ADD", triple)
        self.world._add_triple_with_update(self.ontology, *triple)
        
    return nb_match
  
    
class Column(object):
  def __init__(self, var, type, binding, name, index):
    self.var         = var
    self.type        = type
    self.binding     = binding
    self.name        = name
    self.index       = index
    
  def __repr__(self):
    return """<Column #%s %s %s %s %s>""" % (self.index, self.var, self.type, self.binding, self.name)
    
class Variable(object):
  def __init__(self, name):
    self.name           = name
    self.type           = "quads"
    self.fixed_datatype = None
    self.prop_type      = "quads" # Type when the variable is used as a property
    self.bindings       = []
    self.bind           = None
    self.initial_query  = None
    
  def __repr__(self): return """<Variable %s type %s, %s bindings>""" % (self.name, self.type, len(self.bindings))
  
  def update_type(self, type):
    if   self.type == "quads": self.type = type
    elif (type != self.type) and (type != "quads") :
      raise ValueError("Variable %s cannot be both %s and %s!" % (self.name, self.type, type))
    
class Table(object):
  def __init__(self, name, type = "quads", index = None, join = ",", join_conditions = None):
    self.name            = name
    self.type            = type
    self.index           = index
    self.join            = join
    self.join_conditions = join_conditions or []
    self.query           = None
    
  def __repr__(self): return "<Table '%s %s'>" % (self.type, self.name)
    
  def sql(self):
    return """%s %s%s%s""" % (self.type, self.name, self.index and (" INDEXED BY %s" % self.index) or "", self.join_conditions and (" ON (%s)" % " AND ". join(self.join_conditions)) or "")
  
  
class SQLQuery(FuncSupport):
  def __init__(self, name):
    self.name                    = name
    self.preliminary             = False
    self.recursive               = False
    self.translator              = CURRENT_TRANSLATOR.get()
    self.distinct                = False
    self.raw_selects             = None
    self.next_table_id           = 1
    self.tables                  = []
    self.name_2_table            = {}
    self.columns                 = []
    self.conditions              = []
    self.triples                 = []
    self.vars_needed_for_select  = set()
    self.vars                    = {}
    self.extra_sql               = ""
    self.select_simple_union     = False
    self.optional                = False
    
  def __repr__(self): return "<%s '%s'>" % (self.__class__.__name__, self.sql())
  
  def sql(self):
    if self.tables:
      sql = """SELECT """
      if self.distinct: sql += "DISTINCT "
      sql += """%s FROM """ % (", ".join(str(column.binding) for column in self.columns))
      for table in self.tables:
        if not table is self.tables[0]: sql += " %s " % table.join
        sql += table.sql()
      if self.conditions:
        sql += """ WHERE %s""" % (" AND ".join(str(condition) for condition in self.conditions))
    else:
      if not self.columns: return ""
      if self.select_simple_union:
        for i, column in enumerate(self.columns):
          if isinstance(column.binding, list): break
        l = []
        for j in range(len(self.columns[i].binding)):
          l.append([])
          for k, column in enumerate(self.columns):
            if k == i: l[-1].append(column.binding[j])
            else:      l[-1].append(column.binding)
        sql = """VALUES %s""" % ",".join("(%s)" % ",".join(str(k) for k in j) for j in l)
      else:
        sql = """VALUES (%s)""" % (",".join(str(column.binding) for column in self.columns))
        
    if self.extra_sql: sql += " %s" % self.extra_sql
    if self.preliminary: return """%s(%s) AS (%s)""" % (self.name, ", ".join(column.name for column in self.columns), sql)
    return sql
    
  def set_column_names(self, names):
    for column, name in zip(self.columns, names): column.name = name
    
  def parse_distinct(self, distinct):
    if isinstance(distinct, rply.Token): self.distinct = distinct and (distinct.value.upper() == "DISTINCT")
    else:                                self.distinct = distinct
    
  def parse_var(self, x):
    if isinstance(x, rply.Token): name = x.value
    else:                         name = x
    var = self.vars.get(name)
    if not var:
      self.vars[name] = var = Variable(name)
    return var
  
  def parse_selects(self, selects):
    if selects is None:
      self.raw_selects = "*"
    else:
      self.raw_selects = selects
      vars_needed_for_select = { self.parse_var(select) for select in selects if (isinstance(select, rply.Token) and (select.name == "VAR")) or (isinstance(select, str)) }
      for var in vars_needed_for_select:
        self.expand_referenced_vars(var, self.vars_needed_for_select)
        
  def expand_referenced_vars(self, var, r):
    r.add(var)
    if var.bind:
      for var_name in var.bind.referenced_var_names:
        self.expand_referenced_vars(self.parse_var(var_name), r)
        
  def prepare_bind(self, bind):
    var      = self.parse_var(bind.var)
    var.bind = bind
    
  def parse_bind(self, bind):
    var      = self.parse_var(bind.var)
    var.bind = bind
    var.bindings.insert(0, self.parse_expression(bind.expression))
    
    fixed_type, fixed_datatype = self.infer_expression_type(bind.expression, accept_zero = True)
    if fixed_type is None: fixed_type = "quads"
    var.update_type(fixed_type)
    if fixed_type != "objs":  var.fixed_datatype = fixed_datatype
    
  def parse_filter(self, filter):
    sql = self.parse_expression(filter.constraint)
    self.conditions.append(sql)
    
  def add_subqueries(self, sub):
    if isinstance(sub, SQLNestedQuery):
      self.conditions.append(sub)
    else:
      table = Table("p%s" % self.next_table_id, sub.name)
      table.query = sub
      self.next_table_id += 1
      self.tables.append(table)
      self.name_2_table[table.name] = table
      if sub.optional:
        table.join = "LEFT JOIN"
        conditions = table.join_conditions
      else:
        conditions = self.conditions
        
      for column in sub.columns:
        var = self.parse_var(column.var)
        var.update_type(column.type)
        if not column.name.endswith("d"):
          self.create_conditions(conditions, table, column.name, var)
          
          
  def parse_triples(self, triples):
    if self.triples: raise ValueError("Cannot parse triples twice!")
    self.block = triples
    self.triples.extend(triples)
    
    if self.raw_selects is None: raise ValueError("Need to call parse_selects() before finalizing triples!")
    
    if self.raw_selects == "*":
      self.vars_needed_for_select = { self.parse_var(var_name) for var_name in self.block.get_ordered_vars() }         
      
    for i, triple in enumerate(self.triples): # Pass 0: Simple union blocks
      if isinstance(triple, UnionBlock) and triple.simple_union_triples:
        self.triples[i:i+1] = triple.simple_union_triples
        
    remnant_triples = set(self.triples)
        
    for triple in list(self.triples): # Pass 1: Determine var type and prop type
      if isinstance(triple, (Bind, Filter, Block)): continue
      s, p, o = triple
      
      triple.local_table_type = triple.table_type
      if s.name == "VAR":
        var = self.parse_var(s)
        var.update_type("objs")
        if (p.name == "IRI") and (p.storid == rdfs_subpropertyof) and (o.name == "IRI"):
          parent_prop = self.translator.world._get_by_storid(o.storid)
          if   isinstance(parent_prop, ObjectPropertyClass): var.prop_type = "objs"
          elif isinstance(parent_prop, DataPropertyClass):   var.prop_type = "datas"
      if p.name == "VAR": self.parse_var(p).update_type("objs")
      if o.name == "VAR": self.parse_var(o).update_type(triple.local_table_type)
      
    for triple in list(self.triples): # Pass 2: Determine var type, which may be changed due to prop type
      if isinstance(triple, (Bind, Filter, Block)): continue
      s, p, o = triple
      if (triple.local_table_type == "quads") and (o.name == "VAR"): triple.local_table_type = self.parse_var(o).type
      if (triple.local_table_type == "quads") and (p.name == "VAR"): triple.local_table_type = self.parse_var(p).prop_type # Repeat (table.type == "quads") condition, since table.type may have been changed by the previous if block
      if o.name == "VAR": self.parse_var(o).update_type(triple.local_table_type)
      
    non_preliminary_triples = []
    for triple in list(self.triples): # Pass 3: Create recursive preliminary selects
      if isinstance(triple, Block): continue
      if isinstance(triple, (Bind, Filter)):
        non_preliminary_triples.append(triple)
        continue
      s, p, o = triple
      triple.consider_s = triple.consider_p = triple.consider_o = True
      
      if p.modifier:
        if   (s.name != "VAR"): fixed = "s"
        elif (o.name != "VAR"): fixed = "o"
        else:
          # nb_s = nb_o = 0
          # for triple2 in self.triples:
          #   for x in triple2.var_names:
          #     if x == s.value: nb_s += 1
          #     if x == o.value: nb_o += 1
          # if   nb_s == 1:    fixed = "o"
          # elif nb_o == 1:    fixed = "s"
          # elif nb_s <= nb_o: fixed = "s"
          # else:              fixed = "o"
          # print("NB", nb_s, nb_o)
          fix_levels = self.get_fix_levels([self.parse_var(s), self.parse_var(o)], triple)
          if fix_levels[self.parse_var(s)] >= fix_levels[self.parse_var(o)]: fixed = "s"
          else:                                                              fixed = "o"
          
        non_fixed = "o" if fixed == "s" else "s"
        vars = []
        if   (s.name == "VAR") and (fixed == "s"): fixed_var = s
        elif (o.name == "VAR") and (fixed == "o"): fixed_var = o
        else:                                      fixed_var = None
        if fixed_var: vars.append(self.parse_var(fixed_var))
        if  p.name == "VAR": vars.append(self.parse_var(p))
        
        prelim_triples = self.extract_triples(self.triples, vars, triple)
        
        remnant_triples.remove(triple)
        remnant_triples.difference_update(prelim_triples)
        prelim = self.translator.get_recursive_preliminary_select(triple, fixed, fixed_var, prelim_triples)
        triple.local_table_type = prelim.name
        triple.consider_p = False
        if not(fixed_var and prelim_triples):
          if fixed == "s": triple.consider_s = False
          else:            triple.consider_o = False
          
      else:
        non_preliminary_triples.append(triple)
        
    selected_non_preliminary_triples = frozenset(self.extract_triples(non_preliminary_triples, self.vars_needed_for_select))
    selected_non_preliminary_triples = selected_non_preliminary_triples | remnant_triples

    for triple in self.triples: # Pass 4: create triples tables and conditions
      if   isinstance(triple, Bind):
        self.parse_bind(triple)
        continue
      elif isinstance(triple, Filter):
        self.parse_filter(triple)
        continue
      elif isinstance(triple, Block):
        if   isinstance(triple, SimpleTripleBlock) and len(triple) == 0: # Empty
          continue
        elif isinstance(triple, FilterBlock):
          sub = self.translator.new_sql_query(None, triple, nested_inside = self)
          self.add_subqueries(sub)
          continue
        else:
          sub = self.translator.new_sql_query(None, triple, preliminary = True)
          self.add_subqueries(sub)
          continue
        
      s, p, o = triple
      if (not p.modifier) and (not triple in selected_non_preliminary_triples): continue
      
      table = Table("q%s" % self.next_table_id, triple.local_table_type)
      if triple.optional:
        table.join = "LEFT JOIN"
        conditions = table.join_conditions
      else:
        conditions = self.conditions
      self.next_table_id += 1
      self.tables.append(table)
      self.name_2_table[table.name] = table
      
      s_fixed = triple.consider_s and self.is_fixed(s)
      o_fixed = triple.consider_o and self.is_fixed(o)
      if   s_fixed and o_fixed: # Favor index SP over index OP, because there are usually more diversity in the values of S than in O
        if   table.type == "objs":  table.index = "index_objs_sp"
        elif table.type == "datas": table.index = "index_datas_sp"
      elif s_fixed: # Favor index SP over SQLite3 partial covering index, because benchmark suggests better performances
        if   table.type == "objs":  table.index = "index_objs_sp"
        elif table.type == "datas": table.index = "index_datas_sp"
        
      if triple.consider_s: self.create_conditions(conditions, table, "s", s)
      if triple.consider_p: self.create_conditions(conditions, table, "p", p)
      if triple.consider_o: self.create_conditions(conditions, table, "o", o)
      
      if p.modifier == "+": conditions.append("%s.nb>0"  % table.name)
      

  def get_fix_levels(self, vars0, exclude_triple = None):
    vars0_names = { var.name for var in vars0 }
    fix_levels  = defaultdict(float)
    fix_triples = {}
    
    def fix(var, triple, via_vars, w = 1.0):
      nonlocal changed
      
      w0 = min((0.5 * fix_levels[via_var] for via_var in via_vars), default = 1.0)
      w  = w * w0
      
      if w > fix_levels[var]:
        changed          = True
        fix_levels [var] = w
        fix_triples[var] = l = { triple }
        for via_var in via_vars: l.update(fix_triples[via_var])
        
    def scan_triple(triples, w = 1):
      for triple in self.triples:
        if triple is exclude_triple: continue
        
        if   isinstance(triple, Triple):
          if   len(triple.var_names) == 1:
            var = self.parse_var(tuple(triple.var_names)[0])
            fix(var, triple, [], w)
            
          elif len(triple.var_names) == 2:
            if triple.var_names != vars0_names:
              vars = [self.parse_var(var_name) for var_name in triple.var_names]
              for v1, v2 in [(vars[0], vars[1]), (vars[1], vars[0])]:
                fix(v1, triple, [v2], w)
                
        elif isinstance(triple, Filter):
          pass
        elif isinstance(triple, Bind):
          var = self.parse_var(triple.var)
          fix(var, triple, [self.parse_var(var_name) for var_name in triple.var_names], w)
          
        elif isinstance(triple, UnionBlock):
          for alternative in triple: scan_triple(alternative, w / len(triple))
          
    while True:
      changed = False
      scan_triple(self.triples)
      if not changed: break
      for var in vars0:
        if not var in fix_levels: break
      else:
        break
      
    return fix_levels
      
  def extract_triples(self, triples, vars, except_triple = None):
    var_names = { var.name for var in vars }
    while True:
      r = [triple for triple in triples if (not triple == except_triple) and isinstance(triple, (Triple, Filter, Bind)) and (not triple.var_names.isdisjoint(var_names))]
      var_names2 = { var_name for triple in r for var_name in triple.var_names }
      if var_names2 == var_names: return r
      var_names = var_names2
      
  def create_conditions(self, conditions, table, n, x):
    if isinstance(x, SpecialCondition):
      x.create_conditions(conditions, table, n)
    else:
      sql, sql_type, sql_d, sql_d_type = self._to_sql(x)
      
      if table.query: # If datatype is 0 (=auto), disable datatype conditions and replace it by IS NOT NULL
        for column in table.query.columns:
          if column.name == "%sd" % n[:-1]:
            if str(column.binding) == "0":
              sql_d = None
              conditions.append("%s.%sd IS NOT NULL" % (table.name, n[:-1])) # Datatype part
            break
          
      if not sql   is None: conditions.append("%s.%s=%s"  % (table.name, n,      sql))
      if not sql_d is None: conditions.append("%s.%sd=%s" % (table.name, n[:-1], sql_d)) # Datatype part
      
      if x.name == "VAR": x = self.vars[x.value]
      if   isinstance(x, Variable):
        if not x.bindings: x.initial_query = self
        x.bindings.append("%s.%s" % (table.name, n))

  def is_fixed(self, x):
    if x.name != "VAR": return True
    x = self.parse_var(x)
    if x.initial_query and (x.initial_query is not self): return True
    if x.bindings: return True
    return False
  
  def finalize_columns(self):
    selected_parameter_index = 0
    i = j = 0
    if self.raw_selects == "*": selects = [self.vars[var] for var in self.block.get_ordered_vars() if not var.startswith("??")]
    else:                       selects = self.raw_selects
    
    def do_select(select):
      nonlocal selected_parameter_index
      if isinstance(select, str) and select.startswith("?"): select = self.vars[select]
      sql, sql_type, sql_d, sql_d_type = self._to_sql(select)
      
      if   isinstance(select, rply.Token) and (select.name == "VAR"): var_name = select.value
      elif isinstance(select, Variable):                              var_name = select.name
      else:                                                           var_name = None
      
      if sql == "?":
        self.parameters.insert(selected_parameter_index, select.number)
        selected_parameter_index += 1

      return var_name, sql, sql_type, sql_d, sql_d_type
    
    for select in selects:
      i += 1
      if isinstance(select, SimpleUnion):
        self.select_simple_union = True
        sql = []
        for select_item in select.items:
          var_name, sql_i, sql_type, sql_d, sql_d_type = do_select(select_item)
          sql.append(sql_i)
        sql_d = None # SimpleUnion is only supported for object here
        
      else:
        var_name, sql, sql_type, sql_d, sql_d_type = do_select(select)
        
      if sql is None: raise ValueError("Cannot select '%s'!" % select)
      self.columns.append(Column(var_name, sql_type,   sql,   "col%s_o" % i, j)); j += 1
      if not sql_d is None: self.columns.append(Column(var_name, sql_d_type, sql_d, "col%s_d" % i, j)); j += 1
        
  def _to_sql(self, x):
    if isinstance(x, rply.Token) and (x.name == "VAR"): x = self.parse_var(x)

    if   isinstance(x, str): return x, "value", None, None
    elif isinstance(x, Variable):
      if not x.bindings: return None, None, None, None
      binding = x.bindings[0]
      
      if   x.type == "objs":  return binding, "objs", None, None
      else:
        if not x.fixed_datatype is None:
          if isinstance(x.fixed_datatype, Variable):
            dropit, dropit, other_sql_d, other_sql_d_type = self._to_sql(x.fixed_datatype)
            return binding, "datas", other_sql_d, other_sql_d_type
          else:
            return binding, "datas", x.fixed_datatype, "datas"
        type = "datas" if x.type == "datas" else "quads"
        return binding, type, "%sd" % binding[:-1], type
    elif x.name == "IRI":   return x.storid, "objs", None, None
    elif x.name == "PARAM": return "?%s" % x.number, "objs", None, None # XXX data parameter
    else:
      if   x.name == "DATA":            return x.value, "value", x.datatype, "value"
      elif isinstance(x.value, locstr): return x.value, "value", "'@%s'" % x.value.lang, "value"
      else:                             return x.value, "value", None, None
      
    
class SQLCompoundQuery(object):
  recursive = False
  def __init__(self, name):
    self.name                    = name
    self.translator              = CURRENT_TRANSLATOR.get()
    self.queries                 = []
    self.preliminary             = False
    self.optional                = False
    
  def __repr__(self): return "<%s '%s'>" % (self.__class__.__name__, self.sql())

  def append(self, query, operator = ""):
    query.operator = operator
    self.queries.append(query)
    
  def sql(self):
    sql = ""
    for i, query in enumerate(self.queries):
      if i != 0: sql += "\n%s\n" % query.operator
      sql += query.sql()
    if self.preliminary: return """%s(%s) AS (%s)""" % (self.name, ", ".join(column.name for column in self.columns), sql)
    return sql
  
  def finalize_compounds(self):
    has_d = set()
    for query in self.queries:
      for column in query.columns:
        if column.name.endswith("d"):
          has_d.add(column.name.split("_", 1)[0])
          
    for query in self.queries:
      for i, column in enumerate(query.columns):
        if column.name.endswith("o") and (column.name.split("_", 1)[0] in has_d):
          column.type = "quads"
          if (column is query.columns[-1]) or (not query.columns[i+1].name.endswith("d")):
            query.columns.insert(i + 1, Column(column.var, "quads", "NULL", "%sd" % column.name[:-1], i + 1))
      for i, column in enumerate(query.columns): # Re-index columns
        column.index = i
    self.columns = self.queries[0].columns
    
    
class SQLNestedQuery(SQLQuery):
  def __init__(self, name):
    SQLQuery.__init__(self, name)
    
  def finalize_columns(self):
    self.columns = [Column(None, "datas", "1", "col1_o", 1)]
    
  def sql(self):
    extra_sql = self.extra_sql
    self.extra_sql = ""
    
    sql = "(%s)" % SQLQuery.sql(self)
    
    if extra_sql: sql += " %s" % extra_sql
    self.extra_sql = extra_sql
    return sql
  
  def __str__(self): return self.sql()
  

class SQLRecursivePreliminaryQuery(SQLQuery):
  def __init__(self, name, triple, fixed, fixed_var):
    s, p, o = triple
    translator = CURRENT_TRANSLATOR.get()
    self.fixed        = fixed
    self.fixed_var    = fixed_var
    self.non_fixed    = "o" if fixed == "s" else "s"
    
    if isinstance(p, NegatedPropSetPath): self.need_d = True
    else:                                 self.need_d = (p.modifier == "?") and not isinstance(triple.Prop, ObjectPropertyClass)
    
    self.need_orig    = not self.fixed_var is None # XXX Optimizable
    self.need_nb      = p.modifier != "*"
    
    SQLQuery.__init__(self, "%s_%s" % (name, "quads" if self.need_d else "objs"))
    self.recursive    = True
    self.preliminary  = True
    
  def build(self, triple, prelim_triples):
    s, p, o = triple
    column_names = [self.non_fixed] + ["d"] * self.need_d + [self.fixed] * self.need_orig + ["nb"] * self.need_nb
    if self.fixed_var and prelim_triples: value = self.fixed_var
    else:                                 value = s if self.fixed == "s" else o
    self.parse_selects([value] + ["NULL"] * self.need_d + [value] * self.need_orig + ["0"] * self.need_nb)
    self.parse_triples(prelim_triples)
    self.finalize_columns()
    self.set_column_names(column_names)
    
    p_conditions = []
    self.create_conditions(p_conditions, Table("q", "quads" if self.need_d else "objs"), "p", p)
    self.extra_sql = """
UNION
SELECT q.%s%s%s%s FROM %s q, %s rec WHERE %s %sAND q.%s=rec.%s""" % (
  self.non_fixed,
  ", q.d"                 if self.need_d    else "",
  ", rec.%s" % self.fixed if self.need_orig else "",
  ", rec.nb+1"            if self.need_nb   else "",
  "quads"                 if self.need_d    else "objs",
  self.name, " AND ".join(p_conditions),
  "AND rec.nb=0 " if p.modifier == "?" else "",
  self.fixed, self.non_fixed)
  
  
