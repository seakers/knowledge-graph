from neo4j import GraphDatabase


def main():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "ceosdb_scraper"))
    with driver.session() as session:
        result = session.run('MATCH p=()-[r:INSTANCE_OF]->() DETACH DELETE r')

if __name__ == "__main__":
    main()