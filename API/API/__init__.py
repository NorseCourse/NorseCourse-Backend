from flask import Flask
from flask.ext.restplus import Api

import mysql.connector
import mysql.connector.pooling

import config

db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

app = Flask(__name__)
NorseCourse = Api(app)
API = NorseCourse.namespace("api", "Root namespace for NorseCourse APIs")

# Adds "Access-Control-Allow-Origin": "*" to the response header
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

from API import courses, departments, divisions, genEds, schedules, sections, terms, recommendations