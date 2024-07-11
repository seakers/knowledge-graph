import csv
from neo4j import GraphDatabase

def main(flag):
    heads = []
    head_ids = []
    relations = []
    relation_ids = []
    tails = []
    tail_ids = []

    with open('kg_'+flag+'.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        i = 0
        for row in spamreader:
            if i < 1:
                i=i+1
                continue
            heads.append(row[0])
            head_ids.append(row[1])
            relations.append(row[2])
            relation_ids.append(row[3])
            tails.append(row[4])
            tail_ids.append(row[5])

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "ceosdb_scraper"))

    with driver.session() as session:
        result = session.run('MATCH ()-[r]->() DELETE r;')
        for i, head in enumerate(heads):
            # if tail_ids[i] == '':
            #     print(head)
            #     print(tail)
            #     continue
            head_id = int(head_ids[i])
            tail_id = int(tail_ids[i])
            relation = relations[i]
            tail = tails[i]
            ### THIS IS STUPID BUT CYPHER DOESN'T ACCEPT RELATIONSHIP TYPES AS PARAMETERS ###
            if relation == "TYPE_OF":
                result = session.run('MATCH (h:ObservableProperty),(t:ObservablePropertyCategory) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:TYPE_OF]-(t) )'
                    'CREATE (h)-[:TYPE_OF]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "INCLUDES":
                result = session.run('MATCH (h:ObservablePropertyCategory),(t:ObservableProperty) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:INCLUDES]-(t) )'
                    'CREATE (h)-[:INCLUDES]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "BUILT":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:BUILT]-(t) )'
                    'CREATE (h)-[:BUILT]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "PARENT_OF":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:PARENT_OF]-(t) )'
                    'CREATE (h)-[:PARENT_OF]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "BUILT_BY":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:BUILT_BY]-(t) )'
                    'CREATE (h)-[:BUILT_BY]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "IS_HOSTED_BY":
                result = session.run('MATCH (h:Sensor),(t:Platform) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:IS_HOSTED_BY]-(t) )'
                    'CREATE (h)-[:IS_HOSTED_BY]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "INSTANCE_OF":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:INSTANCE_OF]-(t) )'
                    'CREATE (h)-[:INSTANCE_OF]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "HOSTS":
                result = session.run('MATCH (h:Platform),(t:Sensor) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:HOSTS]-(t) )'
                    'CREATE (h)-[:HOSTS]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)
            elif relation == "OBSERVES":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND ID(h) = $head_id AND ID(t) = $tail_id AND NOT EXISTS( (h)-[:OBSERVES]-(t) )'
                    'CREATE (h)-[:OBSERVES]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail,
                    head_id=head_id,
                    tail_id=tail_id)

# " python run.py 3dchess 0 3dchess_model TransE 5 0.0 0.2 "

if __name__ == "__main__":
    main("plain")
