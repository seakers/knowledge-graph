import os
import shutil
import csv
from neo4j import GraphDatabase

import utils.add_parent_relation as add_parent_relation
import utils.measurement_type_rule as measurement_type_rule
import utils.test_neo4j_connection as test_neo4j_connection
import utils.print_kg_csv as print_kg_csv
import utils.restore_kg as restore_kg

def load_kg_from_csv(flag):
    entities = []
    relations = []
    with open('kg_'+flag+'.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        i = 0
        for row in spamreader:
            if i < 1:
                i=i+1
                continue
            entities.append(row[1])
            entities.append(row[5])
            relations.append((row[0],row[2],row[4]))
    entities = set(entities)
    entities = list(entities)
    return entities, relations

def add_manual_entries(user,password,manual_entity_filename,manual_relation_filename):
    entity_names = []
    entity_types = []
    extra_infos = []
    with open(manual_entity_filename, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        i = 0
        for row in spamreader:
            if i < 1:
                i=i+1
                continue
            entity_names.append(row[0])
            entity_types.append(row[1])
            extra_infos.append(row[2])

    head_names = []
    relation_names = []
    tail_names = []
    with open(manual_relation_filename, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        i = 0
        for row in spamreader:
            if i < 1:
                i=i+1
                continue
            head_names.append(row[0])
            relation_names.append(row[1])
            tail_names.append(row[2])

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(user,password))
    with driver.session() as session:
        for i, entity_name in enumerate(entity_names):
            entity_type = entity_types[i]
            extra_info = extra_infos[i]
            cypher_query_string = f"MERGE (n:{entity_type} {{name: \"{entity_name}\",{extra_info}}})"
            print(cypher_query_string)
            result = session.run(cypher_query_string)
                
            
    with driver.session() as session:
        for i, head_name in enumerate(head_names):
            relation = relation_names[i]
            tail_name = tail_names[i]
            if relation == "TYPE_OF":
                result = session.run('MATCH (h:ObservableProperty),(t:ObservablePropertyCategory) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:TYPE_OF]-(t) )'
                    'CREATE (h)-[:TYPE_OF]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "INCLUDES":
                result = session.run('MATCH (h:ObservablePropertyCategory),(t:ObservableProperty) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:INCLUDES]-(t) )'
                    'CREATE (h)-[:INCLUDES]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "BUILT":
                result = session.run('MATCH (h:Agency),(t:Sensor) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:BUILT]-(t) )'
                    'CREATE (h)-[:BUILT]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "PARENT_OF":
                result = session.run('MATCH (h:SensorType),(t:Sensor) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:PARENT_OF]-(t) )'
                    'CREATE (h)-[:PARENT_OF]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "BUILT_BY":
                result = session.run('MATCH (h:Sensor),(t:Agency) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:BUILT_BY]-(t) )'
                    'CREATE (h)-[:BUILT_BY]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "IS_HOSTED_BY":
                result = session.run('MATCH (h:Sensor),(t:Platform) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:IS_HOSTED_BY]-(t) )'
                    'CREATE (h)-[:IS_HOSTED_BY]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "INSTANCE_OF":
                result = session.run('MATCH (h:Sensor),(t:SensorType) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:INSTANCE_OF]-(t) )'
                    'CREATE (h)-[:INSTANCE_OF]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "HOSTS":
                result = session.run('MATCH (h:Platform),(t:Sensor) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:HOSTS]-(t) )'
                    'CREATE (h)-[:HOSTS]->(t)',
                    head_name=head_name,
                    tail_name=tail_name)
            elif relation == "OBSERVES":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head_name AND t.name = $tail_name AND NOT EXISTS( (h)-[:OBSERVES]-(t) )'
                    'CREATE (h)-[:OBSERVES]->(t) RETURN h',
                    head_name=head_name,
                    tail_name=tail_name)
    

            

def main():
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "ceosdb_scraper"
    if test_neo4j_connection.test_neo4j_connection(uri,user,password):
        if os.path.isfile("./kg_plain.csv"):
            restore_kg.main(user,password,"plain")
        else:
            print_kg_csv.main(user,password,"plain")
        measurement_type_rule.main(user,password)
        add_parent_relation.main(user,password)
        print_kg_csv.main(user,password,"augmented")
        manual_entity_filename = "./manual_entities.csv"
        manual_relation_filename = "./manual_relations.csv"
        add_manual_entries(user,password,manual_entity_filename,manual_relation_filename)
        print_kg_csv.main(user,password,"after_manual")
        plain_entities, plain_relations = load_kg_from_csv("plain")
        aug_entities, aug_relations = load_kg_from_csv("augmented")
        manual_entities, manual_relations = load_kg_from_csv("after_manual")
        print("Plain KG has "+str(len(plain_entities))+" connected entities, and "+str(len(plain_relations))+" relations.")
        print("Augmented KG has "+str(len(aug_entities))+" connected entities, and "+str(len(aug_relations))+" relations.")
        print("Manual KG has "+str(len(manual_entities))+" connected entities, and "+str(len(manual_relations))+" relations.")
        print("Augmented KG has "+str(len(aug_entities)-len(plain_entities))+" more entities than the plain KG.")
        print("Augmented KG has "+str(len(aug_relations)-len(plain_relations))+" more relations than the plain KG.")
        print("Manual KG has "+str(len(manual_relations)-len(plain_relations))+" more relations than the plain KG.")
        print("Manual KG has "+str(len(manual_relations)-len(aug_relations))+" more relations than the augmented KG.")
    else:
        print("Neo4j connection not working.")

if __name__ == "__main__":
    main()