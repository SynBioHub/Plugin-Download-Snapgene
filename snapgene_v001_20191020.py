# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:32:39 2019

@author: JVM
"""

#CREATE ZIP RETURN

import xml.etree.ElementTree as ET 
import requests
from zipfile import ZipFile

#%%
#uri = "https://synbiohub.org/public/igem/BBa_E0240_sequence/1"
#xmlfile = "C:\\Users\\JVM\\Downloads\\BBa_E0240.xml"
#
## create element tree object 
#tree = ET.parse(xmlfile) 
#  
## get root element 
#root = tree.getroot() 
#
##get displayID and set as partname
#displayIDs = []
#for item in root.findall('./{http://sbols.org/v2#}ComponentDefinition/{http://sbols.org/v2#}displayId'):
#    displayIDs.append(item.text)
#partname = displayIDs[0]
#
##get sequence
#for item in root.findall('./{http://sbols.org/v2#}Sequence'):
#    if uri == item.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']:
#        for child in item:
#            if child.tag == '{http://sbols.org/v2#}elements':
#                sequence = child.text
#
##find if part is circular
#linear = True
#for item in root.findall('./{http://sbols.org/v2#}ComponentDefinition'):
#    if uri == item.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']:
#        for child in item:
#            if child.tag == '{http://sbols.org/v2#}type':
#                types = child.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
#                if types == 'http://identifiers.org/so/SO:0000988':
#                    linear = False
                                 
#%%              
def snapgeneseq(sequence, uri, partname, detectfeatures = True, linear = True):
    newtext_url = "http://song.ece.utah.edu/examples/pages/acceptNewText.php" #link to post to
    get_url = "http://song.ece.utah.edu/dnafiles/"+partname
    
    #setting linearity and detect features parameters
    if linear:
        linearity = "linear"
    else:
        linearity = "circular"
        
    if detectfeatures:
        decfeat = "true"
    else:
        decfeat = "false"
    
    #data to send
    data = {"textToUpload": sequence,
            "detectFeatures": decfeat,
            "textId": partname,
            "textName": partname,
            "topology": linearity} 
    #parameters to send
    params ={} 
    
    #post data to snapgene server
    requests.post(newtext_url, data = data, params = params,  headers = {"Accept":"text/plain"})
    
    #get the genebank file generated
    s = requests.get(f"{get_url}.gb")
    genebank = s.text
    print(genebank, file=open(partname+".gb", "w"))
    
    #get the png map generated
    t = requests.get(f"{get_url}.png")
    with open(partname+".png", 'wb') as f:
            f.write(t.content)
    
    return(genebank, partname+".png")

#%%
def snapgenefile(partname, filename, detectfeatures = False, linear = True):    
    newfile_url = "http://song.ece.utah.edu/examples/pages/acceptNewFile.php"
    get_url = "http://song.ece.utah.edu/dnafiles/"+partname
    
    #linearity and detectFeatures works on presence so set those parameters
    data = {}
    if detectfeatures:
        data["detectFeatures"] = "True"
    if linear:
        data["linear"]="True"
    
    #file to open
    gbfile = requests.get(filename).content
    files = {'fileToUpload': gbfile}
    
    #parameters
    params = {} 
    
    #upload file
    requests.post(newfile_url, files=files, data = data, params = params,
                      headers = {"Accept":"text/plain"})

    #request genebank
    s = requests.get(f"{get_url}.gb")
    genebank = s.content
    
    
    with open(partname+".gb", 'wb') as f:
        f.write(genebank)
    
    
    #request png map
    t = requests.get(f"{get_url}.png")
    with open(partname+".png", 'wb') as f:
            f.write(t.content)
       
    with ZipFile(partname+'.zip', 'w') as myzip:
        myzip.write(partname+'.png')
        myzip.write(partname+'.gb')

    return(partname+".zip")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#FLASK_APP=app.py flask run
from flask import Flask, request, abort, send_file
#from Full_v004_20190506 import *
app = Flask(__name__)


#flask run --host=0.0.0.0
@app.route("/gbAnnotate/status")
def imdoingfine():
    return("Not dead Jet")


@app.route("/gbAnnotate/evaluate")
def alliswell():
    return("All is well")


@app.route("/gbAnnotate/run", methods=["POST"])
def wrapper():
    data = request.json
    gburl = data['genbank']
    displayid = data['top_level'].split('/')[-2]
    print(displayid,gburl)
    try:
        #instance = "synbiohub.org"
        zipname = snapgenefile(displayid, gburl, detectfeatures = False, linear = linear)
        return send_file(zipname, attachment_filename=zipname)
    except Exception as e:
        print(e)
        abort(404)






