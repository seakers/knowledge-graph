import csv
import os
import random

from neo4j import GraphDatabase


def main(user,password):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(user,password))
    kg = []
    entity_pairs = []
    entity_ids = []
    relations = []
    with driver.session() as session:
        results = session.run("MATCH (a)-[r]->(b) RETURN a, r, b")
        for result in results:
            a = result["a"].get('name')
            a_id = result["a"].element_id
            r = result["r"].type
            b = result["b"].get('name')
            b_id = result["b"].element_id
            entity_pairs.append((a_id,a))
            entity_pairs.append((b_id,b))
            entity_ids.append(a_id)
            entity_ids.append(b_id)
            relations.append(r)
            kg.append((a_id,r,b_id))
    entity_pairs = set(entity_pairs)
    entity_pairs = list(entity_pairs)

    entity_ids = set(entity_ids)
    entity_ids = list(entity_ids)

    relations = set(relations)
    relations = list(relations)

    kg_w_indices = kg

    random.shuffle(kg_w_indices)

    train_percentage = 0.7
    test_percentage = 0.2
    valid_percentage = 0.1

    rules = [["OBSERVES","PARENT_OF","OBSERVES"]]
    if not os.path.exists('./UniKER/data/3dchess/'):
        os.mkdir('./UniKER/data/3dchess/')
    file1 = open("./UniKER/data/3dchess/relations.dict","w")
    for i, relation in enumerate(relations):
        file1.write(str(i)+"\t"+str(relation)+"\n")
    file1.close()
    file2 = open("./UniKER/data/3dchess/entity_pairs.dict","w")
    for i, entity_pair in enumerate(entity_pairs):
        file2.write(str(entity_pair[0])+"\t"+str(entity_pair[1])+"\n")
    file2.close()
    file3 = open("./UniKER/data/3dchess/entities.dict","w")
    for i, entity_id in enumerate(entity_ids):
        file3.write(str(i)+"\t"+str(entity_id)+"\n")
    file3.close()
    file4 = open("./UniKER/data/3dchess/train.txt","w")
    for i, fact in enumerate(kg_w_indices[0:int(len(kg_w_indices)*train_percentage)]):
        file4.write(str(fact[0])+"\t"+str(fact[1])+"\t"+str(fact[2])+"\n")
    file4.close()
    file5 = open("./UniKER/data/3dchess/test.txt","w")
    for i, fact in enumerate(kg_w_indices[int(len(kg_w_indices)*train_percentage):int(len(kg_w_indices)*(train_percentage+test_percentage))]):
        file5.write(str(fact[0])+"\t"+str(fact[1])+"\t"+str(fact[2])+"\n")
    file5.close()
    file6 = open("./UniKER/data/3dchess/valid.txt","w")
    for i, fact in enumerate(kg_w_indices[int(len(kg_w_indices)*(train_percentage+test_percentage)):]):
        file6.write(str(fact[0])+"\t"+str(fact[1])+"\t"+str(fact[2])+"\n")
    file6.close()
    file7 = open("./UniKER/data/3dchess/MLN_rule.txt","w")
    for i, rule in enumerate(rules):
        file7.write("1.0\t"+rule[0]+"\t"+rule[1]+"\t"+rule[2]+"\n")
    file7.close()

    


if __name__ == "__main__":
    main("neo4j","ceosdb_scraper")
