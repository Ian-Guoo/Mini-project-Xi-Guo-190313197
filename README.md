# Mini-project-Xi-Guo-190313197
Cloud Computing Coursework

## COVID19 Application: 
This application is a prototype of a Cloud application developed in Python and Flask where one can use GET, POST, PUT and DELETE methods to interact with the application.

1.It is a REST-based service interface and makes use of an external REST service being the Coronavirus API (https://covid19api.com/)

2.It makes use of a Cloud database in Apache Cassandra.

3.The application is served over HTTPS.

4.Kubernetes based load balancing

## 1.REST API Requests

### @app.route('/', methods =['GET'])
The home page show the data of global covid19. And extract the data from the Coronavirus API (https://covid19api.com/summary). These data are stored to the Cassandra Database.
Shom instructions of this application are shown in the home page.

### @app.route('/countrylist', methods=['GET'])
Show all the county existed in the Cassandra Database.

### @app.route('/country', methods=['GET'])
Show covid19 data of each country in the Cassandra Database.

### @app.route('/country/<name>',  methods=['GET'])
Search the covid19 data by country name.

### @app.route('/country',  methods=['POST'])
Insert new country' covid19 data to the Cassandra Database.
```curl
curl -i -H "Content-Type: application/json" -X POST -d '{"country":"a","newconfirmed":1,"totalconfirmed":1,"newdeaths":1,"totaldeaths":1,"newrecovered":1,"totalrecovered":1}' http://54.89.254.114:80/country
```

### @app.route('/country',  methods=['PUT'])
Change the covid19 data of one country existed in database.
```curl
curl -i -H "Content-Type: application/json" -X PUT -d '{"country":"a","newconfirmed":2,"totalconfirmed":2,"newdeaths":2,"totaldeaths":2,"newrecovered":2,"totalrecovered":2}' http://54.89.254.114:80/country
```

### @app.route('/country',  methods=['DELETE'])
Delete the covid19 data of one country existed in database.
```curl
curl -X "DELETE" http://54.89.254.114:80/country/a
```



## 2.Deploying Cassandra via Docker

Pull the Cassandra Docker Image:

```
sudo apt update
sudo apt install docker.io
sudo docker pull cassandra:latest
```

Run a Cassandra instance within docker:

```
sudo docker run --name cassandra-project -p 9042:9042 -d cassandra:latest
```

Interact with Cassandra via its native command line shell client called ‘cqlsh’ using CQL:

```
  sudo docker exec -it cassandra-project cqlsh
```

 Within the Cassandra terminal, create a keyspace for the data to be inserted into:

```CQL
CREATE KEYSPACE covid19 WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
```

Create the table inside of the keyspace, specifying all column names and types, firstly create a database table for global stats:

```CQL
CREATE TABLE covid19.global (Key text PRIMARY KEY,NewConfirmed int, TotalConfirmed int, NewDeaths int, TotalDeaths int, NewRecovered int, TotalRecovered int);
```
Secondly create a database table for summary stats:

```CQL
CREATE TABLE covid19.summary (Country text PRIMARY KEY,NewConfirmed int, TotalConfirmed int, NewDeaths int, TotalDeaths int, NewRecovered int, TotalRecovered int);
```


## 3.Serving the application over https.

Creat requirments.txt
```
pip
Flask
cassandra-driver
requests
requests_cache
```

Create the Dockerfile.
```
FROM python:3.7-alpine
WORKDIR /myapp
COPY . /myapp
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python","app.py"]
```

Bulit imgae and run
```
sudo docker build . --tag=covid19:v1
sudo docker run -p 80:80 covid19:v1
```
## 4.Kubernetes based load balancing

Install Kubernetes
```
sudo snap install microk8s -classic
```

Develop an nginx application,listening on port 80, and names the deployment "covid19-web"
```
sudo microk8s.kubectl run covid19-web --image==nginx --port=80
```
See the pods created:
```
sudo microk8s.kubectl get pods
```
Expose cluster to the external world
```
sudo microk8s.kubectl expose deployment covid19-web --type=LoadBalancer
```
Scaling up application
```
sudo microk8s.kubectl scale deployment covid19-web --replicas=5
```
Check the replias
```
sudo microk8s.kubectl get pods
```
### cleaning up 
Delete the load-balancing service:
```
sudo microk8s.kubectl delete service covid19-web
```
