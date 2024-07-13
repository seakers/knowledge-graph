# knowledge-graph

First install Docker Desktop (insert link here). Have it running before the next step.

Next, run 
```
docker-compose up
```
in the docker_setup directory with the docker-compose.yml. This should start the scraping process and you will have the database available at localhost:7474 with username neo4j and password ceosdb_scraper. Takes me ~15 minutes on my machine.

Then you can run the manual, UKGE, and UniKER pipelines with full_manual_pipeline.py, full_ukge_pipeline.py, and full_uniker_pipeline.py respectively.