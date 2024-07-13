import os
from neo4j import GraphDatabase
from tqdm import tqdm

def main(username,password,model_name):
    head_ids = []
    relation_ids = []
    tail_ids = []

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(username, password))
    relation_types = []
    with driver.session() as session:
        results = session.run("MATCH (h)-[r]->(t) RETURN h, r, t")
        for result in results:
            head_id = result["h"].element_id
            relation_type = result["r"].type
            tail_id = result["t"].element_id
            head_ids.append(head_id)
            tail_ids.append(tail_id)
            relation_types.append(relation_type)
    relation_types_set = set(relation_types)
    relation_types_set = list(relation_types_set)
    relation_types_set.sort()
    relation_ids = []
    for relation_type in relation_types:
        relation_ids.append(relation_types_set.index(relation_type))

    num_relations = len(relation_ids)
    train_split = int(0.8*num_relations)
    test_split = int(0.9*num_relations)
    #print(num_relations)
    if not os.path.isdir("./UKGE/data/"+model_name):
        os.mkdir("./UKGE/data/"+model_name)

    train_filename = './UKGE/data/'+model_name+'/train.tsv'
    with open(train_filename, "w") as query_file:
        for i in range(0,train_split):
            head_id = str(head_ids[i])
            tail_id = str(tail_ids[i])
            relation_id = str(relation_ids[i])
            query_file.write(head_id + "\t" + relation_id + "\t" + tail_id + "\t" + "1.00000" + "\n")

    test_filename = './UKGE/data/'+model_name+'/test.tsv'
    with open(test_filename, "w") as query_file:
        for i in range(train_split,test_split):
            head_id = str(head_ids[i])
            tail_id = str(tail_ids[i])
            relation_id = str(relation_ids[i])
            query_file.write(head_id + "\t" + relation_id + "\t" + tail_id + "\t" + "1.00000" + "\n")

    val_filename = './UKGE/data/'+model_name+'/val.tsv'
    with open(val_filename, "w") as query_file:
        for i in range(test_split,num_relations):
            head_id = str(head_ids[i])
            tail_id = str(tail_ids[i])
            relation_id = str(relation_ids[i])
            query_file.write(head_id + "\t" + relation_id + "\t" + tail_id + "\t" + "1.00000" + "\n")
    sensors = []
    sensor_ids = []
    observables = []
    observable_ids = []
    with driver.session() as session:
        results = session.run("MATCH (s:Sensor) RETURN s")
        for result in results:
            sensor = result["s"]["name"]
            sensor_id = result["s"].element_id
            sensors.append(sensor)
            sensor_ids.append(sensor_id)
    with driver.session() as session:
        results = session.run("MATCH (o:ObservableProperty) RETURN o")
        for result in results:
            observable = result["o"]["name"]
            observable_id = result["o"].element_id
            observables.append(observable)
            observable_ids.append(observable_id)
    with driver.session() as session:
        results = session.run("MATCH (o:ObservablePropertyCategory) RETURN o")
        for result in results:
            observable = result["o"]["name"]
            observable_id = result["o"].element_id
            observables.append(observable)
            observable_ids.append(observable_id)

    query_filename = './UKGE/data/'+model_name+'/query.tsv'
    with open(query_filename, "w") as query_file:
        for sensor_id in sensor_ids:
            if sensor_id in head_ids or sensor_id in tail_ids:
                for observable_id in observable_ids:
                    if observable_id in head_ids or observable_id in tail_ids:
                        head_id = str(sensor_id)
                        tail_id = str(observable_id)
                        relation_id = str(relation_types_set.index("OBSERVES"))
                        query_file.write(head_id + "\t" + relation_id + "\t" + tail_id + "\t" + "1.00000" + "\n")


if __name__ == "__main__":
    main("neo4j","ceosdb_scraper","3D_CHESS_det")