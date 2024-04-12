import csv
import os

from neo4j import GraphDatabase


def main():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "ceosdb_kg"))
    kg = []
    entities = []
    relations = []
    with driver.session() as session:
        results = session.run("MATCH (a)-[r]->(b) RETURN a, r, b")
        for result in results:
            a = result["a"]
            r = result["r"]
            b = result["b"]
            entities.append(a)
            entities.append(b)
            relations.append(r)
            kg.append((a,r,b))

    entities = set(entities)
    entities = list(entities)

    relations = set(relations)
    relations = list(relations)

    kg_w_indices = []
    for entry in kg:
        kg_w_indices.append((entities.index(entry[0]),entry[1],entities.index(entry[2])))

    train_percentage = 0.7
    test_percentage = 0.2
    valid_percentage = 0.1

    rules = ["OBSERVES","PARENT_OF","OBSERVES"]
    if not os.path.exists('./UniKER/data/3dchess/'):
        os.mkdir('./UniKER/data/3dchess/')
    file1 = open("./UniKER/data/3dchess/relations.dict","w")
    for i, relation in enumerate(relations):
        file1.write(str(i)+"\t"+relation+"\n")
    file1.close()
    file2 = open("./UniKER/data/3dchess/entity_names.dict","w")
    for i, entity in enumerate(entities):
        file2.write(str(i)+"\t"+entity+"\n")
    file2.close()
    file3 = open("./UniKER/data/3dchess/entities.dict","w")
    for i, entity in enumerate(entities):
        file3.write(str(i)+"\t"+entities.index(entity)+"\n")
    file3.close()
    file4 = open("./UniKER/data/3dchess/train.txt","w")
    for i, fact in enumerate(kg_w_indices[0:int(len(kg_w_indices)*train_percentage)]):
        file4.write(fact[0]+"\t"+fact[1]+"\t"+fact[2]+"\n")
    file4.close()
    file5 = open("./UniKER/data/3dchess/test.txt","w")
    for i, fact in enumerate(kg_w_indices[int(len(kg_w_indices)*train_percentage):int(len(kg_w_indices)*(train_percentage+test_percentage))]):
        file5.write(fact[0]+"\t"+fact[1]+"\t"+fact[2]+"\n")
    file5.close()
    file6 = open("./UniKER/data/3dchess/valid.txt","w")
    for i, fact in enumerate(kg_w_indices[int(len(kg_w_indices)*(train_percentage+test_percentage)):]):
        file6.write(fact[0]+"\t"+fact[1]+"\t"+fact[2]+"\n")
    file6.close()
    file7 = open("./UniKER/data/3dchess/MLN_rule.txt","w")
    for i, rule in enumerate(rules):
        file7.write("1.0\t"+rule[0]+"\t"+rule[1]+"\t"+rule[2]+"\n")
    file7.close()

    


if __name__ == "__main__":
    main()
