# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from datetime import date
import pprint
import re
import requests
import sys


def login(url):
    http = f'{url}api/v1/security/login'
    headers = { 'Content-type': 'application/json', }
    data = '{ "password": "admin", "provider": "db",  "refresh": true,  "username": "admin"}'
    response = requests.post(http, headers=headers, data=data)
    print(response.json())
    return response.json()['access_token']

def get_database(url,token):
    http = f'{url}api/v1/database'
    headers = { 'Content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.get(http, headers=headers)
    return response

def get_datasets(url,token):
    http = f'{url}api/v1/dataset'
    headers = { 'Content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.get(http, headers=headers)
    return response

def get_queries(url,token):
    http = f'{url}/api/v1/query/'
    headers = { 'Content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.get(http, headers=headers)
    return response

def create_database(url,token,schema):
    http = f'{url}api/v1/database'
    csrf_url = f'{url}/api/v1/security/csrf_token'
    headers = { 'Content-type': 'application/json', 'Authorization': f'Bearer {token}',
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
    
    token = login(url)
    print("Get token")
    print (f'access token: {token}')

    result = get_database(url,token)

    print("Get database")
    print(result.status_code)
    print(result.headers)
#    pprint.pprint(result.json())

    datasets = get_datasets(url, token)

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

    result = get_queries(url,token)
    print('Queries:')
    print(result.status_code)
    print(result.headers)
    pprint.pprint(result.json())


