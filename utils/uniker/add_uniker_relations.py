from neo4j import GraphDatabase

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
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "ceosdb_scraper"))

    with driver.session() as session:
        for i, head in enumerate(heads):
            relation = relations[i]
            tail = tails[i]
            ### THIS IS STUPID BUT CYPHER DOESN'T ACCEPT RELATIONSHIP TYPES AS PARAMETERS ###
            if relation == "TYPE_OF":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:TYPE_OF]-(t) )'
                    'CREATE (h)-[:TYPE_OF]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "INCLUDES":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:INCLUDES]-(t) )'
                    'CREATE (h)-[:INCLUDES]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "BUILT":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:BUILT]-(t) )'
                    'CREATE (h)-[:BUILT]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "PARENT_OF":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:PARENT_OF]-(t) )'
                    'CREATE (h)-[:PARENT_OF]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "BUILT_BY":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:BUILT_BY]-(t) )'
                    'CREATE (h)-[:BUILT_BY]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "IS_HOSTED_BY":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:IS_HOSTED_BY]-(t) )'
                    'CREATE (h)-[:IS_HOSTED_BY]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "INSTANCE_OF":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:INSTANCE_OF]-(t) )'
                    'CREATE (h)-[:INSTANCE_OF]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "HOSTS":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:HOSTS]-(t) )'
                    'CREATE (h)-[:HOSTS]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)
            elif relation == "OBSERVES":
                result = session.run('MATCH (h),(t) '
                    'WHERE h.name = $head AND t.name = $tail AND NOT EXISTS( (h)-[:OBSERVES]-(t) )'
                    'CREATE (h)-[:OBSERVES]->(t)',
                    head=head,
                    relation=relation,
                    tail=tail)

# " python run.py 3dchess 0 3dchess_model TransE 5 0.0 0.2 "

if __name__ == "__main__":
    main()
