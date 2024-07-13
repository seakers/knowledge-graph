import os
import time
from neo4j import GraphDatabase

# Get Neo4j server details from environment variables
# uri = "bolt://localhost:7687"
# user = "neo4j"
# password = "ceosdb_scraper"
def test_neo4j_connection(uri, user, password):
    worked = False
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session() as session:
            result = session.run("RETURN 1")
            for record in result:
                print("Connection successful, query result:", record)
                worked = True
    except Exception as e:
        print("Connection failed:", e)
    finally:
        driver.close()
    return worked

# if __name__ == "__main__":
#     print(f"Connecting to Neo4j at {uri} with user {user}")
#     test_neo4j_connection(uri, user, password)