import csv

from neo4j import GraphDatabase


def main(user,password,flag):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(user,password))

    with open('kg_'+flag+'.csv', 'w', newline='') as csvfile:
        fieldnames = ['head', 'head_id', 'relation', 'relation_id', 'tail', 'tail_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with driver.session() as session:
            results = session.run("MATCH (h)-[r]->(t) RETURN h, r, t")
            for result in results:
                head = result["h"]["name"]
                head_id = result["h"].element_id
                relation = result["r"].type
                relation_id = result["r"].element_id
                tail = result["t"]["name"]
                tail_id = result["t"].element_id
                writer.writerow({
                    'head': head,
                    'head_id': head_id,
                    'relation': relation,
                    'relation_id': relation_id,
                    'tail': tail,
                    'tail_id': tail_id
                })


if __name__ == "__main__":
    main("neo4j","ceosdb_scraper","plain")
