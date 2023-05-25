from usdm_excel import USDMExcel
from py2neo import Graph
import pandas as pd

graph = Graph("bolt://localhost:7687", auth=("neo4j", "analysisconcept"))

#prepare collected data to load
datapath='/Users/kwl/Documents/CDISC/CDISC Pilot Study/updated-pilot-submission-package/900172/m5/datasets/cdiscpilot01/tabulations/sdtm/'
lb_coll = pd.read_sas(datapath+'lb.xpt',format='xport', encoding='utf-8')
dm = pd.read_sas(datapath+'dm.xpt',format='xport', encoding='utf-8')
#select arm for each subject
dm=dm[["USUBJID","ARM"]].loc[dm["ARM"]!='Screen Failure']
#Select the rows for Albumin and Sodium
#Select the relevant columns
lb= lb_coll[["USUBJID","VISIT","LBTEST","LBTESTCD","LBSTRESN","LBSTRESU"]].loc[lb_coll['LBTESTCD'].isin(["ALB","SODIUM"])].loc[lb_coll['VISIT'].isin(["SCREENING 1","WEEK 2","WEEK 4","WEEK 6","WEEK 8","WEEK 12","WEEK 16","WEEK 20","WEEK 24","WEEK 26"])]

param_list=[{'study':'H2Q-MC-LZZT'}]
for p in param_list:
    for index, row in dm.iterrows():
        #create subjects and link to study
        query1="match(sid:StudyIdentifier)<-[:studyIdentifiers]-(s:Study) where sid.studyIdentifier='"+p['study']+"' MERGE(subj:StudySubject{studySubjectIdentifier:'"+row['USUBJID']+"'}) MERGE (subj)-[:enrolledInStudy]->(s)"
           
        #create link form study arm to subject
        query2="match(arm:StudyArm),(subj:StudySubject{studySubjectIdentifier:'"+row['USUBJID']+"'}) where arm.studyArmName='"+row['ARM']+"' MERGE(arm)<-[:subjectRandomisedToArm]-(subj)" 
        graph.run(query1)
        graph.run(query2)
        
    for index, row in lb.iterrows():
        result=str(row['LBSTRESN'])
        #link datapoint to bc result node
        query3="MATCH(subj:StudySubject{studySubjectIdentifier:'"+row['USUBJID']+"'}) MATCH(bc:BiomedicalConcept)<-[:biomedicalConceptIds]-(a:Activity)<-[:activityIds]-(sia)-[:scheduledInstanceEncounterId]->(ec) where bc.bcName contains '"+row['LBTEST']+"' and toUpper(ec.encounterName)='"+row['VISIT']+"'  match(bc:BiomedicalConcept)-[:bcProperties]->(bcprop:BiomedicalConceptProperty) where (bc.bcName contains '"+row['LBTEST']+"') and toLower(bcprop.bcPropertyName) contains 'result' MERGE(dp:DataPoint{dataValue :toFloat('"+result+"'),uri:'"+p['study']+"'+'/"+row['USUBJID']+"/'+bc.bcName+'/'+ec.encounterName}) MERGE(dp)-[:dataPointBiomedicalConcept]->(bcprop) MERGE(subj)<-[:dataPointCapturedFrom]-(dp) MERGE(dp)-[:dataPointScheduledInstanceEncounter]->(sia)" 
        print(query3)
        #link collected unit to BC unit property
        query4="match(bc:BiomedicalConcept)-[:bcProperties]->(bcprop:BiomedicalConceptProperty) where (bc.bcName contains '"+row['LBTEST']+"') and toLower(bcprop.bcPropertyName) contains 'unit' MERGE(dpu:DataPointUnit{dataUnit:'"+row['LBSTRESU']+"'}) MERGE (dpu)-[:dataPointUnitBiomedicalConcept]->(bcprop)"
        graph.run(query3)
        graph.run(query4)