import csv


def main():
    with open('./UniKER/record/3dchess_model/1/fc_train.txt') as file:
        lines = [line.rstrip() for line in file]

    with open('./UniKER/data/3dchess/test.txt') as file:
        lines.extend([line.rstrip() for line in file])

    with open('./UniKER/data/3dchess/valid.txt') as file:
        lines.extend([line.rstrip() for line in file])

    with open('./UniKER/data/3dchess/entity_names.dict') as file:
        entity_lines = [line.rstrip() for line in file]

    entity_dict = {}    
    for line in entity_lines:
        tokens = line.split("\t")
        entity_dict[tokens[0]] = tokens[1]


    head_ids = []
    relations = []
    tail_ids = []
    for line in lines:
        tokens = line.split("\t")
        head_ids.append(tokens[0])
        relations.append(tokens[1])
        tail_ids.append(tokens[2])
    
    heads = []
    tails = []
    for head in head_ids:
        heads.append(entity_dict[head])
    for tail in tail_ids:
        tails.append(entity_dict[tail])


    with open('kg_uniker.csv', 'w', newline='') as csvfile:
        fieldnames = ['head', 'relation', 'tail']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, head in enumerate(heads):
            writer.writerow({
                    'head': head,
                    'relation': relations[i],
                    'tail': tails[i]
                })


if __name__ == "__main__":
    main()
