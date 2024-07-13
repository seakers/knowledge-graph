# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

ENV NEO4J_URI=bolt://neo4j:7687
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=ceosdb_scraper

RUN apt-get update && apt-get install -y git


# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY test_neo4j_connection.py /app/

# Set the default command to run the Python script
#CMD ["python", "test_neo4j_connection.py"]
#RUN python test_neo4j_connection.py

RUN git clone https://github.com/seakers/historical_db.git

# Change directory to the cloned repository
WORKDIR /app/historical_db
RUN git pull
#RUN pip install -r requirements.txt
RUN pip install scrapy
RUN pip install rdflib
RUN pip install dateparser
RUN pip install sqlalchemy
#RUN pip install neo4j
#RUN pip install Twisted==22.10.0
WORKDIR /app/historical_db/scraper
CMD ["scrapy", "crawl", "ceosdb_scraper"]
#RUN scrapy crawl ceosdb_scraper

# # Use the official Python image from the Docker Hub
# FROM python:3.8-slim

# # Set the working directory inside the container
# WORKDIR /app

# ENV NEO4J_URI=bolt://neo4j:7687
# ENV NEO4J_USER=neo4j
# ENV NEO4J_PASSWORD=ceosdb_scraper

# RUN apt-get update && apt-get install -y python3 python3-pip git

# # Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the Python script into the container
# COPY test_neo4j_connection.py /app/

# # Set the default command to run the Python script
# CMD ["python", "test_neo4j_connection.py"]
# RUN python test_neo4j_connection.py

# RUN git clone https://github.com/seakers/historical_db.git

# # Change directory to the cloned repository
# WORKDIR /app/historical_db
# RUN git pull
# #RUN pip install -r requirements.txt
# RUN pip install scrapy
# RUN pip install rdflib
# RUN pip install dateparser
# RUN pip install sqlalchemy
# #RUN pip install neo4j
# #RUN pip install Twisted==22.10.0
# WORKDIR /app/historical_db/scraper
# RUN scrapy crawl ceosdb_scraper