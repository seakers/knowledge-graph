import csv
from neo4j import GraphDatabase

def main(username,password):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(username,password))

    head_ids = []
    tail_ids = []
    relation_ids = []
    valid_ukge_filename = './valid_ukge_relations.csv'
    with open(valid_ukge_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        # printing data line by line
        i = 0
        for line in csv_reader:
            if i < 1:
                i=i+1
                continue
            head_ids.append(line[0])
            tail_ids.append(line[2])
            relation_ids.append((line[1]))

    relation_types = []
    with driver.session() as session:
        results = session.run("MATCH ()-[r]->() RETURN r")
        for result in results:
            relation_type = result["r"].type
            relation_types.append(relation_type)
        relation_types_set = set(relation_types)
        relation_types_set = list(relation_types_set)
        relation_types_set.sort()

        
        for i, head_id in enumerate(head_ids):
            tail_id = tail_ids[i]
            relation = relation_types_set[int(relation_ids[i])]
            tail_id = int(tail_id)
            head_id = int(head_id)
            ### THIS IS STUPID BUT CYPHER DOESN'T ACCEPT RELATIONSHIP TYPES AS PARAMETERS ###
            if relation == "TYPE_OF":
                result = session.run('MATCH (h:ObservableProperty),(t:ObservablePropertyCategory) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:TYPE_OF]-(t) )'
                    'CREATE (h)-[:TYPE_OF]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "INCLUDES":
                result = session.run('MATCH (h:ObservablePropertyCategory),(t:ObservableProperty) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:INCLUDES]-(t) )'
                    'CREATE (h)-[:INCLUDES]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "BUILT":
                result = session.run('MATCH (h:Agency),(t:Sensor) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:BUILT]-(t) )'
                    'CREATE (h)-[:BUILT]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "PARENT_OF":
                result = session.run('MATCH (h:SensorType),(t:Sensor) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:PARENT_OF]-(t) )'
                    'CREATE (h)-[:PARENT_OF]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "BUILT_BY":
                result = session.run('MATCH (h:Sensor),(t:Agency) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:BUILT_BY]-(t) )'
                    'CREATE (h)-[:BUILT_BY]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "IS_HOSTED_BY":
                result = session.run('MATCH (h:Sensor),(t:Platform) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:IS_HOSTED_BY]-(t) )'
                    'CREATE (h)-[:IS_HOSTED_BY]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "INSTANCE_OF":
                result = session.run('MATCH (h:Sensor),(t:SensorType) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:INSTANCE_OF]-(t) )'
                    'CREATE (h)-[:INSTANCE_OF]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "HOSTS":
                result = session.run('MATCH (h:Platform),(t:Sensor) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:HOSTS]-(t) )'
                    'CREATE (h)-[:HOSTS]->(t)',
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "OBSERVES":
                result = session.run('MATCH (h),(t) '
                    'WHERE ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:OBSERVES]-(t) )'
                    'CREATE (h)-[:OBSERVES]->(t) RETURN h',
                    head_id=head_id,
                    tail_id=tail_id)
                
if __name__ == "__main__":
    main("neo4j","ceosdb_scraper")