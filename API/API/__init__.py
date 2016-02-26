# Imports
#Teset 2

from flask import Flask
from flask.ext.restplus import Api

import mysql.connector
import mysql.connector.pooling

from API import config

# Grab database properties from the config file
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)


# Instantiate the Flask applicaation and specify properties for Swagger.io.
app = Flask(__name__)
version = "0.0"
title = "NorseCourse"
description = "The NorseCourse API"
terms_url = "We need to figuure these out!"
license = "The MIT License (MIT)"
license_url = "https://opensource.org/licenses/MIT"
contact = "Blaise Schaeffer & Grant Barnes"
contact_url = "https://github.com/NorseCourse"
contact_email = "schabl01@luther.edu,barngr01@luther.edu"
security_definitions = "Security Definitions go here!"
security = [{"S1": [{"description": "desc"}, {"issues": "None"}]}, {"S2": [{"description": "desc"}, {"issues": ["I1", "I2", "Everything under secirity is currently for testing!"]}]}]


# Initialize with swagger definitions.
NorseCourse = Api(app, version, title, description, terms_url, license, license_url, contact, contact_url, contact_email, security_definitions, security)
API = NorseCourse.namespace("api", "Root namespace for NorseCourse APIs")

# Adds "Access-Control-Allow-Origin": "*" to the response header.
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Import files responsible for each API.
from API import courses, departments, divisions, genEds, schedules, sections, terms, recommendations, new_schedules