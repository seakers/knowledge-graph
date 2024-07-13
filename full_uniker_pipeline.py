import os
import shutil
import csv

import utils.add_parent_relation as add_parent_relation
import utils.uniker.add_uniker_relations as add_uniker_relations
import utils.measurement_type_rule as measurement_type_rule
import utils.test_neo4j_connection as test_neo4j_connection
import utils.print_kg_csv as print_kg_csv
import utils.uniker.create_uniker_files as create_uniker_files
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
        create_uniker_files.main(user,password)
        shutil.rmtree("./UniKER/record/3dchess_model/")
        os.chdir("./UniKER")
        os.system("python run.py 3dchess 0 3dchess_model TransE 1 0.0 0.2")
        os.chdir("..")
        add_uniker_relations.main(user,password)
        print_kg_csv.main(user,password,"after_uniker")
        plain_entities, plain_relations = load_kg_from_csv("plain")
        aug_entities, aug_relations = load_kg_from_csv("augmented")
        uniker_entities, uniker_relations = load_kg_from_csv("after_uniker")
        print("Plain KG has "+str(len(plain_entities))+" connected entities, and "+str(len(plain_relations))+" relations.")
        print("Augmented KG has "+str(len(aug_entities))+" connected entities, and "+str(len(aug_relations))+" relations.")
        print("UniKER KG has "+str(len(uniker_entities))+" connected entities, and "+str(len(uniker_relations))+" relations.")
        print("Augmented KG has "+str(len(aug_entities)-len(plain_entities))+" more entities than the plain KG.")
        print("Augmented KG has "+str(len(aug_relations)-len(plain_relations))+" more relations than the plain KG.")
        print("UniKER KG has "+str(len(uniker_relations)-len(plain_relations))+" more relations than the plain KG.")
        print("UniKER KG has "+str(len(uniker_relations)-len(aug_relations))+" more relations than the augmented KG.")
    else:
        print("Neo4j connection not working.")

if __name__ == "__main__":
    main()