from flask import Flask, render_template, request, jsonify
import json
from cassandra.cluster import Cluster
import requests
import requests_cache

cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
session = cluster.connect()
requests_cache.install_cache('covid19_cache', backend='sqlite', expire_after=36000)
app = Flask(__name__)

covid_url_sum = 'https://api.covid19api.com/summary'
covid_url_country = 'https://api.covid19api.com/countries'

@app.route('/', methods =['GET'])
def home():
    resp = requests.get(covid_url_sum)
    if resp.ok:
        response = resp.json()
        response_g = response['Global']
        response_c = response['Countries']
        k = 'Global'
        NewConfirmed_global = int(response_g['NewConfirmed'])
        TotalConfirmed_global = int(response_g['TotalConfirmed'])
        NewDeaths_global = int(response_g['NewDeaths'])
        TotalDeaths_global = int(response_g['TotalDeaths'])
        NewRecovered_global = int(response_g['NewRecovered'])
        TotalRecovered_global = int(response_g['TotalRecovered'])

        session.execute('''Insert INTO covid19.global(Key, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths ,NewRecovered, TotalRecovered) \
        VALUES( '{}', {}, {}, {}, {}, {}, {})'''.format(k,NewConfirmed_global,TotalConfirmed_global,NewDeaths_global,TotalDeaths_global,NewRecovered_global,TotalRecovered_global))

        for i in range(0,len(response_c)):

            countries_data = response_c[i]
            if str(countries_data['Country']) != "":
                Country = countries_data['Slug']
                NewConfirmed = int(countries_data['NewConfirmed'])
                TotalConfirmed = int(countries_data['TotalConfirmed'])
                NewDeaths = int(countries_data['NewDeaths'])
                TotalDeaths = int(countries_data['TotalDeaths'])
                NewRecovered = int(countries_data['NewRecovered'])
                TotalRecovered = int(countries_data['TotalRecovered'])

                session.execute('''Insert INTO covid19.summary(Country, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths ,NewRecovered, TotalRecovered) \
                        VALUES( '{}', {}, {}, {}, {}, {}, {})'''.format(Country,NewConfirmed,TotalConfirmed,NewDeaths,TotalDeaths,NewRecovered,TotalRecovered))

        rows = session.execute("""Select * From covid19.global""")
        result = []
        for r in rows:
            result.append({"Newconfirmed": r.newconfirmed, "Totalconfirmed": r.totalconfirmed,
                           "Newdeaths": r.newdeaths, "Totaldeaths": r.totaldeaths, "Newrecovered": r.newrecovered,
                           "Totalrecovered": r.totalrecovered})
        result = str(result)
        return 'Until Now, the global data is'+result+'<br/>'+'<br/> /countrylist  Show all the county existed in the Cassandra Database.'+ '<br/>'+'<br/> /country  Show covid19 data of each country in the Cassandra Database.'+ '<br/>'+ '<br/> /country/country_name  Search the covid19 data by country name.' +'<br/>'+ '<br/> /country POST Insert new country covid19 data to the Cassandra Database.'+'<br/>'+ '<br/> /country PUT Change the covid19 data of one country existed in database.'+ '<br/>'+ '<br/> /country DELETE Delete the covid19 data of one country existed in database.'

    else:
        print(resp.reason)

@app.route('/countrylist', methods=['GET'])
def list():
    resp = requests.get(covid_url_country)
    response = resp.json()
    result = []
    for i in range(0,len(response)):
        country= response[i]
        result.append(country)
    return jsonify(result)

@app.route('/country', methods=['GET'])
def summary_country():
    rows = session.execute("""Select * From covid19.summary""")
    result = []
    for r in rows:
        result.append({"Country":r.country,
                       "Newconfirmed":r.newconfirmed,
                       "Totalconfirmed":r.totalconfirmed,
                       "Newdeaths":r.newdeaths,
                       "Totaldeaths":r.totaldeaths,
                       "Newrecovered":r.newrecovered,
                       "Totalrecovered":r.totalrecovered})
    return jsonify(result)

@app.route('/country/<name>',  methods=['GET'])
def country(name):
    rows = session.execute("""Select * from covid19.summary WHERE Country = '{}'""".format(name))
    result = []
    for r in rows:
        result.append({"Country": r.country,
                       "Newconfirmed": r.newconfirmed,
                       "Totalconfirmed": r.totalconfirmed,
                       "Newdeaths": r.newdeaths,
                       "Totaldeaths": r.totaldeaths,
                       "Newrecovered": r.newrecovered,
                       "Totalrecovered": r.totalrecovered})
    if len(result)==0:
        return jsonify({'error':'country name not found'}),404
    else:
        return jsonify(result),200

@app.route('/country',  methods=['POST'])
def create_country():
    if not request.json or not 'Country' in request.json:
        return jsonify({'error':'the new record needs to have a country'}),200
    name = request.json['Country']
    rows = session.execute("""Select * from covid19.summary WHERE Country = '{}'""".format(name))
    result = []
    for r in rows:
        result.append({"Country": r.country,
                       "Newconfirmed": r.newconfirmed,
                       "Totalconfirmed": r.totalconfirmed,
                       "Newdeaths": r.newdeaths,
                       "Totaldeaths": r.totaldeaths,
                       "Newrecovered": r.newrecovered,
                       "Totalrecovered": r.totalrecovered})
    if len(result) != 0:
        return jsonify({'error': 'The country already exists'}), 409
    else:
        session.execute( """INSERT INTO COVID19.summary(Country,NewConfirmed,TotalConfirmed,NewDeaths,TotalDeaths,NewRecovered,TotalRecovered) \ 
            VALUES('{}', {}, {}, {},{}, {}, {})""".format(request.json['Country'],int(request.json['NewConfirmed']),int(request.json['TotalConfirmed']),int(request.json['NewDeaths']),int(request.json['TotalDeaths']),int(request.json['NewRecovered']),int(request.json['TotalRecovered'])))
        return jsonify({'message': 'created: /country/{}'.format(request.json['Country'])}), 201

@app.route('/country',  methods=['PUT'])
def update_country():
    if not request.json or not 'Country' in request.json:
        return jsonify({'error':'the new record needs to have a country'}),200
    name = request.json['Country']
    rows = session.execute("""Select * from covid19.summary WHERE Country = '{}'""".format(name))
    result = []
    for r in rows:
        result.append({"Country": r.country,
                       "Newconfirmed": r.newconfirmed,
                       "Totalconfirmed": r.totalconfirmed,
                       "Newdeaths": r.newdeaths,
                       "Totaldeaths": r.totaldeaths,
                       "Newrecovered": r.newrecovered,
                       "Totalrecovered": r.totalrecovered})
    if len(result) == 0:
        return jsonify({'error': 'The country not exists'}), 409
    else:
        session.execute("""UPDATE COVID19.summary SET NewConfirmed= {}, TotalConfirmed= {}, NewDeaths= {}, TotalDeaths= {},NewRecovered= {},TotalRecovered= {} WHERE Country= '{}'""".format(int(request.json['NewConfirmed']),int(request.json['TotalConfirmed']),int(request.json['NewDeaths']),int(request.json['TotalDeaths']),int(request.json['NewRecovered']),int(request.json['TotalRecovered']),request.json['Country']))
        return jsonify({'message': 'updated: /country/{}'.format(request.json['Country'])}), 200

@app.route('/country',  methods=['DELETE'])
def delete_country():
    if not request.json or not 'Country' in request.json:
        return jsonify({'error':'the new record needs to have a country'}),200
    name = request.json['Country']
    rows = session.execute("""Select * from covid19.summary WHERE Country = '{}'""".format(name))
    result = []
    for r in rows:
        result.append({"Country": r.country,
                       "Newconfirmed": r.newconfirmed,
                       "Totalconfirmed": r.totalconfirmed,
                       "Newdeaths": r.newdeaths,
                       "Totaldeaths": r.totaldeaths,
                       "Newrecovered": r.newrecovered,
                       "Totalrecovered": r.totalrecovered})
    if len(result) == 0:
        return jsonify({'error': 'The country not exists'}), 409
    else:
        session.execute("""DELETE FROM COVID19.summary WHERE Country= '{}'""".format(request.json['Country']))
        return jsonify({'message': 'deleted: /country/{}'.format(request.json['Country'])}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

