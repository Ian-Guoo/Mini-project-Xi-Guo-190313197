# Mini-project-Xi-Guo-190313197
Cloud Computing Coursework

## COVID19 Application: 
This application is a prototype of a Cloud application developed in Python and Flask where one can use GET, POST, PUT and DELETE methods to interact with the application.
1.It is a REST-based service interface and makes use of an external REST service being the Coronavirus API (https://covid19api.com/)
2.It makes use of a Cloud database in Apache Cassandra.
3.The application is served over HTTPS.

## REST API Requests


## Deploying Cassandra via Docker

Pull the Cassandra Docker Image:

```
sudo docker pull cassandra:latest
```

Run a Cassandra instance within docker:

```
sudo docker run --name cassandra-miniproject -p 9042:9042 -d cassandra:latest
```

Interact with Cassandra via its native command line shell client called ‘cqlsh’ using CQL:

```
  sudo docker exec -it cassandra-Miniproject cqlsh
```

 Within the Cassandra terminal, create a keyspace for the data to be inserted into:

```CQL
CREATE KEYSPACE rickandmortycharacters WITH REPLICATION =
{'Country' : 'SimpleStrategy', 'replication_factor' : 1};
```

Create the table inside of the keyspace, specifying all column names and types, firstly for the catalogue of characters and secondly for the users who sign up as part of the community:

```CQL
CREATE TABLE rickandmortycharacters.catalogue (ID int, Name text, Gender text, Species text, Status text, Image_url text, PRIMARY KEY ((ID), Name));
```

```CQL
CREATE TABLE rickandmortycharacters.users (Username text PRIMARY KEY, Password text);
```

Then populate `rickandmortycharacters.catalogue` using the curl command stated in the section above:

```
curl -i -H "Content-Type: application/json" -X POST https://www.rickandmortyapp.co.uk/populate_catalogue
```
