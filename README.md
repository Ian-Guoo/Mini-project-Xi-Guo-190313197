# Mini-project-Xi-Guo-190313197
Cloud Computing Coursework

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
  sudo docker exec -it cassandra-miniproject cqlsh
```

 Within the Cassandra terminal, create a keyspace for the data to be inserted into:

```CQL
CREATE KEYSPACE rickandmortycharacters WITH REPLICATION =
{'class' : 'SimpleStrategy', 'replication_factor' : 1};
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
