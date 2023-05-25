from usdm_excel import USDMExcel
from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "analysisconcept"))

class DictWithoutQuotedKeys(dict):
    def __repr__(self):
        s = "{"
        for key in self:
            s += "{0}:".format(key)
            # if isinstance(self[key], str):
            #     # String values still get quoted
            #     s += "\"{0}\", ".format(self[key])
            # if isinstance(self[key], int):
            #     # String values still get quoted
            #     s += "\'{0}\', ".format(self[key])

            if isinstance(self[key], dict):
                # Apply formatting recursively
                s += "{0}, ".format(DictWithoutQuotedKeys(self[key]))
            else:
                # Quote all the values
                s += "\'{0}\', ".format(self[key])
        if len(s) > 1:
            s = s[0: -2]
        s += "}"
        return s



""" studies = [
  'Roche Phase 3 NCT04320615',
  'cycles_1',
  'simple_1',
  'simple_2',
  'profile_1'
]  """

studies = [
  'CDISC Pilot Study'
] 
for study in studies:
  print ("Processing study %s ..." % (study))
  file_path = "source_data/%s.xlsx" % (study)
  file_graphml = "source_data/%s.graphml" % (study)
  x = USDMExcel(file_path)
  nodes, edges = x.to_nodes_and_edges()
  
  #First make all the nodes
  for n in nodes:
    #adding the study_temp property - to be deleted later for those labels where they need to be study specific
    n['properties']["study_temp"]= study
    res = DictWithoutQuotedKeys(n['properties'])
    node_prop=str(res).replace('None','Null').replace("'[","[").replace("]'","]") 
    query_node="MERGE(a:"+n['properties']['_type']+node_prop+")"
    graph.run(query_node)
   #Then for all edges find the start and the end node and the the label and properties to match on. 
    for e in edges : 
      for n in nodes:
        if e['start'] == n['id']:
         start_node=n
         start_res = DictWithoutQuotedKeys(start_node['properties'])
         start_node_prop=str(start_res).replace('None','Null').replace("'[","[").replace("]'","]") 
         start_node_label=n['properties']['_type']
        
        if e['end'] == n['id']:
         end_node=n
         end_res = DictWithoutQuotedKeys(end_node['properties'].items())
         end_node_prop=str(end_res).replace('None','Null').replace("'[","[").replace("]'","]")
         end_node_label= n['properties']['_type']
      # Then create the relationship
      query = "MATCH(a:"+start_node_label+"),(b:"+end_node_label+") where properties(a) ="+start_node_prop+" and properties(b)="+end_node_prop+" MERGE(a)-[:"+e['properties']['label']+"]->(b)"
      #print(query)
      graph.run(query)