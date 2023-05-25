from usdm_excel import USDMExcel
from py2neo import Graph
import pandas as pd
from pandas import DataFrame

graph = Graph("bolt://localhost:7687", auth=("neo4j", "analysisconcept"))
param_list=[{'study':'H2Q-MC-LZZT'}]

def get_data(bcName):
 query="match(a:Activity)<-[:activityIds]-(sia)-[:scheduledInstanceEncounterId]->(ec),(a)-[:biomedicalConceptIds]->(bc:BiomedicalConcept),(dc)-[:derivationConceptParameterType]->(pt:ParameterType)-[:dcParameterValue]->(pv:ParameterValue)-[r:derivedFrom]->(bc),(dc)-[:derivationConceptAction]->(m:Method)-[:derivationConceptInput]->(a),(a)-[:derivationConceptIds]->(dc),(pv:ParameterValue)-[l]->(pvprop:ResultValue),(bc)-[:bcProperties]-(prop)<-[:dataPointBiomedicalConcept]-(dp)-[:dataPointCapturedFrom]->(subj:StudySubject),(dp)-[:dataPointScheduledInstanceEncounter]->(sia) where bc.bcName ='"+bcName+"' return subj.studySubjectIdentifier as USUBJID, pv.label as PARAM, ec.encounterName as ENCOUNTER_NAME, sia.scheduledInstanceId as scheduledInstanceId, dp.DataValue as VALUE order by USUBJID, scheduledInstanceId"
 
 result = graph.run(query).data() 
 # convert result into pandas dataframe 
 df = DataFrame(result)
 return(df)
 
def CHG_num_find(df,baseline):
    #get baseline records
    print(baseline)
    bl=df[["USUBJID","PARAM","VALUE"]].loc[df['ENCOUNTER_NAME']==baseline]
    bl.rename(columns = {'VALUE':'BL'}, inplace = True)
    df=df.merge(bl, on=['USUBJID','PARAM'], how='left')
    df['CHG'] = df.apply(lambda x: x['VALUE'] - x['BL'], axis=1)
    df.drop('BL', axis=1, inplace=True)
    print(df.head())
    return(df)

def save_derived_to_dc(df,dcName):
    filtered_df = df[df['CHG'].notnull()]
    for p in param_list:
        for index, row in filtered_df.iterrows():
            result=str(row['CHG'])
            query="MATCH(subj:StudySubject{studySubjectIdentifier:'"+row['USUBJID']+"'}),(a:Activity)<-[:activityIds]-(sia)-[:scheduledInstanceEncounterId]->(ec),(a)-[:biomedicalConceptIds]->(bc:BiomedicalConcept),(dc)-[:derivationConceptParameterType]->(pt:ParameterType)-[:dcParameterValue]->(pv:ParameterValue)-[r:derivedFrom]->(bc),(dc)-[:derivationConceptAction]->(m:Method)-[:derivationConceptInput]->(a),(a)-[:derivationConceptIds]->(dc),(pv:ParameterValue)-[l]->(pvprop:ResultValue) where pv.label ='"+dcName+"' and ec.encounterName='"+row['ENCOUNTER_NAME']+"'  MERGE(ddp:DerivedDataPoint{derivedDataValue :toFloat('"+result+"'),uri:'"+p['study']+"'+'/"+row['USUBJID']+"/'+pt.parameterTypeLabel+' '+pv.label+'/'+ec.encounterName}) MERGE(pvprop)<-[:dataPointDerivationConcept]-(ddp) MERGE(ddp)-[:dataPointScheduledInstanceEncounter]->(sia) MERGE(subj)<-[:subjectDerivedDataPoint]-(ddp)"
            graph.run(query) 



df= get_data('Sodium Measurement')
df= CHG_num_find(df,'Screening 1')
print(df.head())
save_derived_to_dc(df,'Sodium Measurement')

