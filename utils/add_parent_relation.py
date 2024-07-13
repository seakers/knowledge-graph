from neo4j import GraphDatabase

def main(user,password):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(user,password))
    with driver.session() as session:
        result = session.run('MATCH p=(a:Sensor)-[r:INSTANCE_OF]->(b:SensorType)'
        'CREATE (b)-[:PARENT_OF]->(a)',)

if __name__ == "__main__":
    main("neo4j", "ceosdb_scraper")