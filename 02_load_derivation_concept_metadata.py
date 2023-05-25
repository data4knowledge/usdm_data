from usdm_excel import USDMExcel
from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "analysisconcept"))

activity_list=[{'activity':"Vital signs /Temperature",
                'endpoint':"Laboratory evaluations (Change from Baseline)",
                'definition':"The change from baseline of observations of activity Vital Sign.",'dcConceptName':"Change from Baseline in Vital Signs Values",
                'dcType':"Numeric Finding"},
               {'activity':"Chemistry",
                'endpoint':'Laboratory evaluations (Change from Baseline)',
                'definition':"The change from baseline of observations of category Chemistry.",
                'dcConceptName':"Change from Baseline in Chemistry Laboratory Values",
                'dcType':"Numeric Finding"}]
for a in activity_list:
    # creates the definition,derivation concept, method and parameter type nodes. Adds the links to activity and the scheduledActivityInstance (Timepoints)
    query1='MATCH(a:Activity {activityName:"'+a['activity']+'"})MERGE(def:DerivationDefinition {term:"'+a['definition']+'"})MERGE(dc:DerivationConcept {derivationConceptName:"'+a['dcConceptName']+'",DerivationConceptClass:"'+a['dcType']+'"}) MERGE (pt:ParameterType {parameterTypeShortLabel: "CHG", parameterTypeLabel: "Change from Baseline"}) MERGE(m:Method {scriptName: "CHG_num_find"})MERGE(a)-[r:derivationConceptIds]->(dc) MERGE(def)<-[:derivationConceptDefinition]-(dc) MERGE(dc)-[:derivationConceptAction]->(m) MERGE(m)-[:derivationConceptInput]->(a) MERGE (dc)-[:derivationConceptParameterType]->(pt) with m MATCH(a)<-[:activityIds]-(sai:ScheduledActivityInstance) MERGE(m)-[:derivationConceptInput]->(sai)'

    #creates the next level of the derivation concept: Parameter value, Result Value, Result Unit and their lins to BC and Method. 
    query2='MATCH(a:Activity {activityName:"'+a['activity']+'"})-[:biomedicalConceptIds]->(bc:BiomedicalConcept)-[:bcProperties]->(bcprop) with bc, bc.bcName as bcname, bcprop, bcprop.bcPropertyName as bcunit where bcunit contains "Unit" or bcunit contains "Count" with bc, bcname, bcunit MATCH(a:Activity {activityName:"'+a['activity']+'"})-[:biomedicalConceptIds]->(bc:BiomedicalConcept)-[:bcProperties]->(bcprop) where bc.bcName=bcname with bc, bcunit, bcname, bcprop.bcPropertyDatatype as bcdatatype, replace(bcprop.bcPropertyId,\'Biomedical\',\'Derivation\') as propId where bcprop.bcPropertyName contains "Result" with bc, bcname, bcunit, bcdatatype, propId call apoc.cypher.doIt(\"MATCH (m:Method{scriptName: \'CHG_num_find\'}) MATCH(pt:ParameterType{parameterTypeShortLabel:\'CHG\'}) MERGE(pv:ParameterValue {label:\'\"+bcname+\"\'}) MERGE(rv:ResultValue {dcPropertyId:\'\"+propId+\"\',dataType:\'\"+bcdatatype+\"\'}) MERGE(rv)<-[:derivationConceptOutput]-(m) MERGE(pv)-[:dcValue]->(rv) MERGE(pv)-[:derivedFrom]->(bc) MERGE (pv)-[:dcUnit]->(:ResultUnit{reportingUnit:\'\"+bcunit+\"\'}) MERGE (pt)-[:dcParameterValue]->(pv) return pv,rv,m\",{bc:bc}) YIELD value return value'
    
    #Create link to endpoint
    query3='MATCH (e:Endpoint{endpointDescription:"'+a['endpoint']+'"}),(dc:DerivationConcept {derivationConceptName:"'+a['dcConceptName']+'"}) MERGE (e)-[:endpointDerivationConcepts]->(dc)'
  
    graph.run(query1)
    graph.run(query2)
    graph.run(query3)


