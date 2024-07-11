import os

def main():
    head_names = []
    relation_names = []
    tail_names = []
    head_ids = []
    relation_ids = []
    tail_ids = []

    with open("/home/ben/repos/UKGE/KG raw data/prob_kg.csv", "r") as kg_file:
        next(kg_file)
        for line in kg_file.readlines():
            line.rstrip()
            tokens = line.split(",")
            if float(tokens[3]) == 1.0:
                head_names.append(tokens[0])
                relation_names.append(tokens[1])
                tail_names.append(tokens[2])

    for i in range(len(head_names)):
        with open("/home/ben/repos/UKGE/KG processed data/en2id.txt", "r") as entity_file:
            for line in entity_file.readlines():
                line.rstrip()
                tokens = line.split("\t")
                if str(head_names[i]) == tokens[0].rstrip():
                    head_id = tokens[1].rstrip()
                    head_ids.append(head_id)
                    break

    for i in range(len(relation_names)):
        with open("/home/ben/repos/UKGE/KG processed data/rel2id.txt", "r") as entity_file:
            for line in entity_file.readlines():
                line.rstrip()
                tokens = line.split("\t")
                if str(relation_names[i]) == tokens[0].rstrip():
                    relation_id = tokens[1].rstrip()
                    relation_ids.append(relation_id)
                    break

    for i in range(len(tail_names)):
        with open("/home/ben/repos/UKGE/KG processed data/en2id.txt", "r") as entity_file:
            for line in entity_file.readlines():
                line.rstrip()
                tokens = line.split("\t")
                if str(tail_names[i]) == tokens[0].rstrip():
                    tail_id = tokens[1].rstrip()
                    tail_ids.append(tail_id)
                    break

    num_relations = len(relation_ids)
    train_split = int(0.8*num_relations)
    test_split = int(0.9*num_relations)
    print(num_relations)

    os.mkdir("./UKGE/data/3D_CHESS_det")

    train_filename = './UKGE/data/3D_CHESS_det/train.tsv'
    with open(train_filename, "w") as query_file:
        for i in range(0,train_split):
            head_id = head_ids[i]
            tail_id = tail_ids[i]
            relation_id = relation_ids[i]
            query_file.write(head_id + "\t" + relation_id + "\t" + tail_id + "\t" + "1.00000" + "\n")

    test_filename = './UKGE/data/3D_CHESS_det/test.tsv'
    with open(test_filename, "w") as query_file:
        for i in range(train_split,test_split):
            head_id = head_ids[i]
            tail_id = tail_ids[i]
            relation_id = relation_ids[i]
            query_file.write(head_id + "\t" + relation_id + "\t" + tail_id + "\t" + "1.00000" + "\n")

    val_filename = './UKGE/data/3D_CHESS_det/val.tsv'
    with open(val_filename, "w") as query_file:
        for i in range(test_split,num_relations):
            head_id = head_ids[i]
            tail_id = tail_ids[i]
            relation_id = relation_ids[i]
            query_file.write(head_id + "\t" + relation_id + "\t" + tail_id + "\t" + "1.00000" + "\n")

if __name__ == "__main__":
    main()