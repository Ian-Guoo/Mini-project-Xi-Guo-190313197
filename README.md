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
sudo apt update
sudo apt install docker.io
sudo docker pull cassandra:latest
```

Run a Cassandra instance within docker:

```
sudo docker run --name cassandra-miniproject -p 9042:9042 -d cassandra:latest
```

Interact with Cassandra via its native command line shell client called ‘cqlsh’ using CQL:

```
  sudo docker exec -it cassandra-miniproject cqlsh
```

 Within the Cassandra terminal, create a keyspace for the data to be inserted into:

```CQL
CREATE KEYSPACE covid19 WITH REPLICATION = {'Type' : 'SimpleStrategy', 'replication_factor' : 1};
```

Create the table inside of the keyspace, specifying all column names and types, firstly create a database table for global stats:

```CQL
CREATE TABLE covid19.global (Key text PRIMARY KEY,NewConfirmed int, TotalConfirmed int, NewDeaths int, TotalDeaths int, NewRecovered int, TotalRecovered int);
```
Secondly create a database table for summary stats:

```CQL
CREATE TABLE covid19.summary (Country text PRIMARY KEY,NewConfirmed int, TotalConfirmed int, NewDeaths int, TotalDeaths int, NewRecovered int, TotalRecovered int);
```


