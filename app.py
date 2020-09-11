# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:32:39 2019

@author: JVM
"""
#for detectfeatures use: "annotate" or "plain", for return type use: "zip", "png", or "gb"

#FLASK_APP=app.py flask run
from flask import Flask, request, abort, send_from_directory, send_file
import sbol2, tempfile, os, shutil
from snapgene import find_sequence, find_partname, islinear, snapgeneseq, snapgenefile
app = Flask(__name__)


#flask run --host=0.0.0.0
@app.route("/<detectfeatures>/<return_type>/status")
def status(detectfeatures, return_type):
    return("The Download Test Plugin Flask Server is up and running")



@app.route("/<detectfeatures>/<return_type>/evaluate", methods=["POST"])
def evaluate(detectfeatures,return_type):
    #FOR SOME SNAPGENE RELATED REASON UNANOTATED PNGS OF SEQUENCES ARE IMPOSSIBLE
    #THUS THE UNANOTATED SEQUENCE ENDPOINT IS HIDDEN
    
    data = request.get_json(force=True)
    rdf_type = data['type']
    
    ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
    #uses rdf types
    if detectfeatures == 'plain':
        accepted_types = {'Component'}
    elif detectfeatures == 'annotate':
       accepted_types = {'Component', 'Sequence'} 
    
    acceptable = rdf_type in accepted_types
    ################## END SECTION ####################################
    
    if acceptable:
        return f'The type sent ({rdf_type}) is an accepted type', 200
    else:
        return f'The type sent ({rdf_type}) is NOT an accepted type', 415
    return("All is well")


@app.route("/<detectfeatures>/<return_type>/run", methods=["POST"])
def run(return_type, detectfeatures):
    #FOR SOME SNAPGENE RELATED REASON UNANOTATED PNGS OF SEQUENCES ARE IMPOSSIBLE
    #THUS THE UNANOTATED SEQUENCE ENDPOINT IS HIDDEN
    
    #create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    
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
            snapgenefile(genbank_url, partname, temp_dir.name, detectfeatures = detectfeat, linear = linear)
        elif rdf_type == "Sequence":
            seq = find_sequence(doc)
            snapgeneseq(seq, partname, temp_dir.name, detectfeatures = detectfeat, linear = linear)

        #return outfile  based on url param
        if return_type == "png":
            download_file_name =  f"{partname}.png"
            return send_from_directory(temp_dir.name, download_file_name,
                                       attachment_filename=f"{partname}_{detectfeatures}.png",
                                       as_attachment=True)
        elif return_type == "gb":
            download_file_name =  f"{partname}.gb"
            return send_from_directory(temp_dir.name, download_file_name,
                                       as_attachment=True,
                                       attachment_filename=f"{partname}_{detectfeatures}.gb")
        elif return_type == "zip":
            with tempfile.NamedTemporaryFile() as temp_file:
                #create zip file of converted files and manifest
                shutil.make_archive(temp_file.name, 'zip', temp_dir.name)
                
                #return zip file
                return send_file(f"{temp_file.name}.zip", as_attachment=True,
                                 attachment_filename=f"{partname}_{detectfeatures}.zip")
        else:
            abort(421)    
        
    except Exception as e:
        print(e)
        abort(400)





