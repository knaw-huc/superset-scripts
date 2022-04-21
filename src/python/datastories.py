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

    def __init__(self, url):
        self.url = url
        self.login()

    def login(self):
        http = f'{self.url}api/v1/security/login'
        headers = { 'Content-type': 'application/json', }
        data = '{ "password": "admin", "provider": "db",  "refresh": true,  "username": "admin"}'
        response = requests.post(http, headers=headers, data=data)
#        print(response.json())
        self.token = response.json()['access_token']

    def get_database(self):
        http = f'{self.url}api/v1/database'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.get(http, headers=headers)
        return response

    def get_datasets(self):
        http = f'{self.url}api/v1/dataset'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.get(http, headers=headers)
        return response

    def get_queries(self):
        http = f'{self.url}/api/v1/query/'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}'}
        response = requests.get(http, headers=headers)
        return response

    def create_database(self,schema):
        http = f'{self.url}api/v1/database'
        # this doesn't work
        csrf_url = f'{self.url}/api/v1/security/csrf_token'
        headers = { 'Content-type': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'X-CSRFToken': csrf_url}
        data = { 'schema': schema }
        response = requests.post(http, headers=headers, data=data)
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
        pprint.pprint(datasets.json())

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

#    result = create_database(url,token,schema)

#    print("Create database")
#    print(result.status_code)
#    print(result.headers)
#    pprint.pprint(result.json())

    result = superset.get_queries()
    print('Queries:')
    print(result.status_code)
    print(result.headers)
    pprint.pprint(result.json())


