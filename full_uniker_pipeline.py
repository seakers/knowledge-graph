import os
import shutil

import utils.add_parent_relation as add_parent_relation
import utils.uniker.add_uniker_relations as add_uniker_relations
import utils.measurement_type_rule as measurement_type_rule
import utils.test_neo4j_connection as test_neo4j_connection
import utils.print_kg_csv as print_kg_csv
import utils.uniker.print_kg_csv_uniker as print_kg_csv_uniker
import utils.uniker.create_uniker_files as create_uniker_files
import utils.restore_kg as restore_kg

def main():
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "ceosdb_scraper"
    if test_neo4j_connection.test_neo4j_connection(uri,user,password):
        if os.path.isfile("./kg_plain.csv"):
            restore_kg.main("plain")
        else:
            print_kg_csv.main("plain")
        measurement_type_rule.main()
        add_parent_relation.main()
        print_kg_csv.main("augmented")
        create_uniker_files.main()
        shutil.rmtree("./UniKER/record/3dchess_model/")
        os.chdir("./UniKER")
        os.system("python run.py 3dchess 0 3dchess_model TransE 1 0.0 0.2")
        os.chdir("..")
        print_kg_csv_uniker.main()
        add_uniker_relations.main()
        print_kg_csv.main("after_uniker")
    else:
        print("huh")

if __name__ == "__main__":
    main()