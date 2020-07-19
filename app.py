# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:32:39 2019

@author: JVM
"""
#for detectfeatures use: "annotate" or "plain", for return type use: "zip", "png", or "gb"

#FLASK_APP=app.py flask run
from flask import Flask, request, abort, send_from_directory
import sbol2, shutil, os
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
    cwd = os.getcwd()
    
    temp_dir = os.path.join(cwd, "temp_dir")
    
    #remove to temp directory if it exists
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except:
        print("No temp_dir exists currently")
    
    #make temp_dir directory
    os.makedirs(temp_dir)
    
    data = request.get_json(force=True)
    
    top_level_url = data['top_level']
    complete_sbol = data['complete_sbol']
    instance_url = data['instanceUrl']
    genbank_url = data['genbank']
    size = data['size']
    rdf_type = data['type']
    shallow_sbol = data['shallow_sbol']
    
    url = complete_sbol.replace('/sbol','')
    
    try:
        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
        doc_shallow = sbol2.Document()
        doc_shallow.read(shallow_sbol)
        
        doc = sbol2.Document()
        doc.read(complete_sbol)
        
        partname = find_partname(doc_shallow)
        linear = islinear(doc)
        
        #check detect features set in url param
        if detectfeatures == "annotate":
            detectfeat = True
        elif detectfeatures == "plain":
            detectfeat = False
        else:
            abort(421)

        #if it is a sequnce page use sequence, if it is a componentdef page use gb
        if rdf_type == "Component":
            snapgenefile(genbank_url, partname, temp_dir, detectfeatures = detectfeat, linear = linear)
        elif rdf_type == "Sequence":
            seq = find_sequence(doc)
            snapgeneseq(seq, partname, temp_dir, detectfeatures = detectfeat, linear = linear)

        #return outfile  based on url param
        if return_type == "png":
            download_file_name =  f"{partname}.png"
        elif return_type == "gb":
            download_file_name =  f"{partname}.gb"
        elif return_type == "zip":
            download_file_name =  "Zip.zip"
        
        ################## END SECTION ####################################
        
        return send_from_directory(temp_dir, download_file_name, as_attachment=True)
        
        #clear temp_dir directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    except Exception as e:
        print(e)
        abort(400)





