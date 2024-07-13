import os
import shutil
import csv

import utils.add_parent_relation as add_parent_relation
import utils.measurement_type_rule as measurement_type_rule
import utils.test_neo4j_connection as test_neo4j_connection
import utils.print_kg_csv as print_kg_csv
import utils.restore_kg as restore_kg
import utils.ukge.create_tsvs as create_tsvs
import utils.ukge.add_ukge_relations as add_ukge_relations

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
        create_tsvs.main(user,password,"3D_CHESS_det")
        shutil.copyfile("./utils/ukge/run_ukge.py", "./UKGE/run/run_ukge.py")
        shutil.copyfile("./utils/ukge/ukge_src/data.py", "./UKGE/src/data.py")
        shutil.copyfile("./utils/ukge/ukge_src/models.py", "./UKGE/src/models.py")
        shutil.copyfile("./utils/ukge/ukge_src/testers.py", "./UKGE/src/testers.py")
        shutil.copyfile("./utils/ukge/ukge_src/trainer.py", "./UKGE/src/trainer.py")
        os.chdir("./UKGE")
        os.system("python ./run/run_ukge.py --data 3D_CHESS_det --model rect --batch_size 1024 --dim 128 --epoch 100 --reg_scale 5e-4")
        os.chdir("..")
        add_ukge_relations.main(user,password)
        print_kg_csv.main(user,password,"after_ukge")
        plain_entities, plain_relations = load_kg_from_csv("plain")
        aug_entities, aug_relations = load_kg_from_csv("augmented")
        ukge_entities, ukge_relations = load_kg_from_csv("after_ukge")
        print("Plain KG has "+str(len(plain_entities))+" connected entities, and "+str(len(plain_relations))+" relations.")
        print("Augmented KG has "+str(len(aug_entities))+" connected entities, and "+str(len(aug_relations))+" relations.")
        print("UKGE KG has "+str(len(ukge_entities))+" connected entities, and "+str(len(ukge_relations))+" relations.")
        print("Augmented KG has "+str(len(aug_entities)-len(plain_entities))+" more entities than the plain KG.")
        print("Augmented KG has "+str(len(aug_relations)-len(plain_relations))+" more relations than the plain KG.")
        print("UKGE KG has "+str(len(ukge_relations)-len(plain_relations))+" more relations than the plain KG.")
        print("UKGE KG has "+str(len(ukge_relations)-len(aug_relations))+" more relations than the augmented KG.")
    else:
        print("Neo4j connection not working.")

if __name__ == "__main__":
    main()