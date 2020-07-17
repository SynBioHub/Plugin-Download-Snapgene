# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:32:39 2019

@author: JVM
"""

#FLASK_APP=app.py flask run
from flask import Flask, request, abort, send_from_directory
import sbol2
from snapgene import find_sequence, find_partname, islinear, snapgeneseq, snapgenefile
app = Flask(__name__)


#flask run --host=0.0.0.0
@app.route("/<detectfeatures>/<return_type>/status")
def status():
    return("The Download Test Plugin Flask Server is up and running")
    return("Not dead Jet")


@app.route("/<detectfeatures>/<return_type>/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)
    rdf_type = data['type']
    
    ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
    #uses rdf types
    accepted_types = {'ComponentInstance', 'Sequence'}
    
    acceptable = rdf_type in accepted_types
    ################## END SECTION ####################################
    
    if acceptable:
        return f'The type sent ({rdf_type}) is an accepted type', 200
    else:
        return f'The type sent ({rdf_type}) is NOT an accepted type', 415
    return("All is well")


@app.route("/<detectfeatures>/<return_type>/run", methods=["POST"])
def run(return_type, detectfeatures):






