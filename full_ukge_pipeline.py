import os
import shutil

import utils.add_parent_relation as add_parent_relation
import utils.measurement_type_rule as measurement_type_rule
import utils.test_neo4j_connection as test_neo4j_connection
import utils.print_kg_csv as print_kg_csv
import utils.restore_kg as restore_kg
import utils.ukge.create_tsvs as create_tsvs

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
        create_tsvs.main()
        shutil.copyfile("./utils/ukge/ben_test.py", "./UKGE/run/ben_test.py")
        os.chdir("./UKGE")
        os.system("python ./run/ben_test.py --data 3D_CHESS --model rect --batch_size 1024 --dim 128 --epoch 100 --reg_scale 5e-4")
        os.chdir("..")
        print_kg_csv.main("after_ukge")
    else:
        print("huh")

if __name__ == "__main__":
    main()