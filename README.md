# knowledge-graph

First install Docker Desktop (insert link here). Have it running before the next step.

Next, run 
```
docker-compose up
```
in the directory with the docker-compose.yml. This should start the scraping process and you will have the database available at localhost:7474 with username neo4j and password ceosdb_scraper.



First you will need to download the ceosdb.dump file from the 3D-CHESS Google Drive. Then you will need to 

To run UniKER, first run create_uniker_files.py.
Then run
```
python ./UniKER/run.py ceosdb 0 ceosdb_model TransE 8 0.0 0.2
```

To run the UKGE, 