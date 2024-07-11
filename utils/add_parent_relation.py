from neo4j import GraphDatabase


def main():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "ceosdb_scraper"))
    print("hmm")
    with driver.session() as session:
        result = session.run('MATCH p=(a:Sensor)-[r:INSTANCE_OF]->(b:SensorType)'
        'CREATE (b)-[:PARENT_OF]->(a)',)
        print(result)

if __name__ == "__main__":
    main()