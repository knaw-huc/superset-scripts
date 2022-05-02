# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from datetime import date
import pprint
import re
import requests
import sys


class Superset():

    url = ''
    token = ''
    csrf_token = ''
    username = ''
    password = ''
    session = None

    def __init__(self, url, username='admin', password='admin'):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.session()
        self.login()

    def login(self):
        http = f'{self.url}api/v1/security/login'
        headers = { 'Content-type': 'application/json', }
        data = {
            "password": self.password,
            "provider": "db",
            "refresh": False,
            "username": self.username
        }
        pprint.pprint(data)
        response = self.session.post(url=http, headers=headers, json=data)
        pprint.pprint(response.json())
        self.token = response.json()['access_token']

        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        csrf_url = f'{self.url}/api/v1/security/csrf_token'
        response = self.session.get(url=csrf_url, headers=headers)
        pprint.pprint(response.json())
        self.csrf_token = response.json()['result']
#        pprint.pprint(response.json()['result'])

    def get_database(self):
        http = f'{self.url}api/v1/database'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.get(http, headers=headers)
        return response

    def create_database(self,schema):
        http = f'{self.url}api/v1/database'
        # this doesn't work
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'X-CSRFToken': self.csrf_token}
        data = { 'schema': schema }
        response = requests.post(http, headers=headers, data=data)
        return response

    def get_datasets(self):
        http = f'{self.url}api/v1/dataset'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.get(http, headers=headers)
        return response

    def create_dataset(self, data):
        http = f'{self.url}api/v1/dataset'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.post(http, headers=headers, data=data)
        return response

    def get_queries(self):
        http = f'{self.url}/api/v1/query/'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.get(http, headers=headers)
        return response

    def get_reports(self, data):
        http = f'{self.url}api/v1/report'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.get(http, headers=headers, schema=data)
        return response

    def create_reports(self, data):
        http = f'{self.url}api/v1/dataset'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.post(http, header=headers, schema=data)
        return response

 

def arguments():
    ap = argparse.ArgumentParser(description='Readhtml and convert to xhtml"')
    ap.add_argument('-u', '--url',
                    help="superset site",
                    default = 'http://localhost:8088/')
    args = vars(ap.parse_args())
    return args

if __name__ == "__main__":

    args = arguments()
    url = args['url']
    
    superset = Superset(url)


    result = superset.get_database()

    print("Get database")
    print(result.status_code)
    print(result.headers)
#    pprint.pprint(result.json())

    datasets = superset.get_datasets()

    print("Get datasets")
    print(datasets.status_code)
    if datasets.status_code!=200:
        print(dataset.message)
    else:
        pass
#        pprint.pprint(datasets.json())

        # dit moet nog wat anders:
        schema = { "id": 0,
                "result": {
               "allow_ctas": True,
               "allow_cvas": True,
               "allow_dml": True,
               "allow_file_upload": True,
               "allow_multi_schema_metadata_fetch": True,
               "allow_run_async": True,
               "cache_timeout": 0,
               "configuration_method": "sqlalchemy_form",
               "database_name": "postgres_2",
               "encrypted_extra": "string",
               "engine": "Postgresql",
               "expose_in_sqllab": True,
               "external_url": "string",
               "extra": "string",
               "force_ctas_schema": "string",
               "impersonate_user": True,
               "is_managed_externally": True,
               "parameters": {
                 "additionalProp1": "string",
                 "additionalProp2": "string",
                 "additionalProp3": "string"
               },
               "server_cert": "string",
               "sqlalchemy_uri": "string"
             }
           }
        result = superset.create_database(schema)

        print("Create database")
        print(result.status_code)
        print(result.headers)
        pprint.pprint(result.json())

    result = superset.get_queries()
    print('Queries:')
    print(result.status_code)
    print(result.headers)
    pprint.pprint(result.json())


