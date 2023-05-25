from py2neo import Graph
import os
import sys

print(sys.getdefaultencoding())

graph = Graph("bolt://localhost:7687", auth=("neo4j", "analysisconcept"))

#find the ttl files that are based on SKOS concepts
directory = os.listdir('source_data/dafs_ttl')
skos_list=[]
non_skos_list=[]
for fname in directory:
    with open('source_data/dafs_ttl/'+fname, 'r', encoding='utf-8') as f:
        if 'skos:Concept' in f.read():
         skos_list.append(fname)
        else:
         non_skos_list.append(fname)
    f.close() 
print('SKOS files %s' % skos_list)
print('NON-SKOS files %s' % non_skos_list)

for fname in directory:
    f = open('source_data/dafs_ttl/'+fname,'r')
    filedata = f.read()
    f.close()
    if "'" in filedata and not "\\'" in filedata:
        print('found an apstrophe in %s' % fname)
        newdata = filedata.replace("'", "\\'")
        f = open('source_data/dafs_ttl/'+fname,'w')
        f.write(newdata)
        f.close()
    """ if "'t" in filedata and not "\\'t" in filedata:
        print('found an apstrophe t in %s' % fname)
        newdata2 = filedata.replace("'t", "\\'t")
        f = open('source_data/dafs_ttl/'+fname,'w')
        f.write(newdata2)
        f.close()
    if "s'" in filedata and not "s\\'" in filedata:
        print('found an s apstrophe  in %s' % fname)
        newdata3 = filedata.replace("s'", "s\\'")
        f = open('source_data/dafs_ttl/'+fname,'w')
        f.write(newdata3)
        f.close()       
         """
    
for f in skos_list:
    with open('source_data/dafs_ttl/'+f, 'r', encoding='utf-8') as file:
        data = file.read()
        init_query='CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE'
        query_skos="CALL n10s.onto.import.inline('"+data+"','Turtle')"
        #graph.run(init_query)
        graph.run(query_skos)
    with open('queries/query_'+f, 'w',encoding='utf-8') as file2:
        file2.write(query_skos)
        file2.close()