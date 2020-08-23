from database import Database
from table import createTable
import requests
import json
import pprint
import threading
import time
import re


API_KEY = "tfA5-hX-EHFT"
PROJECT_TOKEN = "tkAYM1OPy9vX"
RUN_TOKEN = "tZM8cxGo1uTB"
db = Database('store.db')
graph_result = {}
class DataAPI:

    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key":self.api_key
        }

        self.data = self.get_data()
        
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)

        data = json.loads(response.text)
        return data

    def get_country(self):
        countries = []

        for country in self.data['country']:

            countries.append(country['name'])
        
        return countries
    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', data=self.params)
        old_data = self.data
        def pull_data():
            time.sleep(0.1)

            while True:

                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data are now Updated")
                    break
                else:
                    print('Not updated yet')
                time.sleep(5)

        t = threading.Thread(target=pull_data)
        t.start()
        t.join()
    def get_country_data(self, country):

        country_data = self.data['country']

        for content in country_data:

            if content['name'].lower() == country.lower():
                return content
    
    def get_total_cases(self):
        datas = self.data['total']

        for data in datas:

            if data['name'] == 'Coronavirus Cases:':
                return data['value']
    def get_total_deaths(self):
        
        datas = self.data['total']

        for data in datas:

            if data['name'] == 'Deaths:':
                return data['value']
    def get_total_recovered(self):

        datas = self.data['total']

        for data in datas:

            if data['name'] == 'Recovered:':
                return data['value']

class ConnectToDatabase:

    def __init__(self):
        pass
    def insert_country_data(self, data):

        for country_info in data['country']:
            
            name = country_info['name']
            total_cases = country_info['total_cases'].replace(",","")
            num_total_cases = int(total_cases)

            try:
                total_death = country_info['total_death'].replace(",","")
                num_total_death = int(total_death)
            except KeyError:
                num_total_death = 0

            db.insert_country_info(name, num_total_cases, num_total_death)
        
        print("Successfully Insert Country Data")

    def insert_total_data(self, data):
        
        for total_info in data['total']:

            name = total_info['name'].replace(":","")

            try:
                total_cases = total_info['value'].replace(",","")
                num_total_cases = int(total_cases)
            except KeyError:
                continue

            db.insert_total_info(name, num_total_cases)
        
        print("Successfully Insert Total Data")
    
    def fetch_country_data(self):

        country_list_info = []
        country_dict = {}

        for row in db.fetch_country_info():
            country_dict = {
                'Name':row[0],
                'Total_Cases':row[1],
                'Total_Deaths':row[2]
            }
            #print(row)
            country_list_info.append(country_dict)
        
        print("Successfully fetch Country")
        return country_list_info

    def fetch_total_data(self):

        total_list_info = []
        total_dict = {}
        for row in db.fetch_total_info():
            total_dict = {
                'Name':row[0],
                'Value':row[1]
            }
            #print(row)
            total_list_info.append(row)

        print("Successfully fetch Total")
        return total_list_info

    def update_country_data(self,data):

        for country_info in data['country']:

            name = country_info['name']
            total_cases = country_info['total_cases'].replace(",","")
            num_total_cases = int(total_cases)

            try:
                total_death = country_info['total_death'].replace(",","")
                num_total_death = int(total_death)
            
            except KeyError:
                continue
            
            db.update_country_info(name, num_total_cases, num_total_death)
        
        print("Successfully Updated Country")
    def update_total_data(self, data):
        
        for total_info in data['total']:
            name = total_info['name'].replace(":","")
            try:
                total_cases = total_info['value'].replace(",","")
                num_total_cases = int(total_cases)
                
            except KeyError:
                continue
            db.update_total_info(name, num_total_cases)

        print("Successfully Updated Total")

def run_data(user_input,topFrame):
    global graph_result
    country_input = user_input
    tracker_data = DataAPI(API_KEY, PROJECT_TOKEN)
    connect = ConnectToDatabase()
    country_list = tracker_data.get_country()
    result = None
    another_frame = topFrame

    UPDATE_COMMAND = "update"

    TOTAL_PATTERN = {
        re.compile(r"[\w\s]+ total [\w\s]+ cases"): tracker_data.get_total_cases,
        re.compile(r"[\w\s]+ total cases([\w\s]+|)"): tracker_data.get_total_cases,
        re.compile(r"[\w\s]+ total [\w\s]+ deaths?"): tracker_data.get_total_deaths,
        re.compile(r"[\w\s]+ total deaths?([\w\s]+|)"): tracker_data.get_total_deaths,
        re.compile(r"[\w\s]+ total [\w\s]+ recovered"): tracker_data.get_total_recovered,
        re.compile(r"[\w\s]+ total recovered([\w\s]+|)"): tracker_data.get_total_recovered
    }

    COUNTRY_PATTERN = {
        re.compile(r"[\w\s]+ cases([\w\s]+|)"): lambda country: tracker_data.get_country_data(country)['total_cases'],
        re.compile(r"[\w\s]+ deaths([\w\s]+|)"): lambda country: tracker_data.get_country_data(country)['total_death']
    }
        
    for pattern, func in COUNTRY_PATTERN.items():

        if pattern.match(country_input):
            words = set(country_input.split(" "))
            copy_word = words.copy()

            for copy in copy_word:
                copy_word.remove(copy)
                copy_word.add(copy.capitalize())
            
            for country in country_list:
                
                if country in copy_word:
                    data = tracker_data.get_data()
                    graph_result.setdefault("Past-Country-Result", connect.fetch_country_data())
                    graph_result.setdefault("Past-Total-Result", connect.fetch_total_data())

                    result = func(country)
                    return f"{country}: {result}"
    
    for pattern, func in TOTAL_PATTERN.items():
    
        if pattern.match(country_input):
            data = tracker_data.get_data()
            graph_result.setdefault("Past-Country-Result", connect.fetch_country_data())
            graph_result.setdefault("Past-Total-Result", connect.fetch_total_data())

            result = func()
            return result
    

    if country_input.lower() == UPDATE_COMMAND:
        print("It is being updated now")
        tracker_data.update_data()

        data = tracker_data.get_data()
        connect.update_country_data(data)
        connect.update_total_data(data)
        graph_result.setdefault("Present-Country-Result", connect.fetch_country_data())
        graph_result.setdefault("Present-Total-Result", connect.fetch_total_data())
        return "The Data is Now Updated"
    
    if country_input.lower() == "show table":

        if len(graph_result) == 4:
            create_table = createTable(another_frame, graph_result)    
            return "Showing Table....."
        else:
            return "Incomplete Data"

    return "None"