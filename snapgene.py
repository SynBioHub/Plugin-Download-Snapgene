# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:32:39 2019

@author: JVM
"""

import requests, os, shutil

def find_sequence(doc):
    """
    Finds the sequence of an sbol component given a document containing full sbol
    
    Requires
    --------
    None.

    Parameters
    ----------
    doc : object of sbol2.document module
        a full depth sbol document

    Returns
    -------
    seq: string
        series of atgc all lowercase representing the component sequence
        
    Example
    -------
    file_in = "https://synbiohub.programmingbiology.org/public/UWYeast_AND_gate/plasmid_0/1/sbol"
    doc = sbol2.Document()
    doc.read(file_in)
    seq = find_sequence(doc)
    """
    max_seq = 0
    seq = ""
    for top_level in doc:
        if top_level.type == "http://sbols.org/v2#Sequence":
            if len(top_level.elements) > max_seq:
                max_seq = len(top_level.elements)
                seq = top_level.elements.lower()
    return(seq)
    
def find_partname(doc_shallow):
    """
    Given shallow sbol find display_id
    
    Requires
    --------
    None
    
    Parameters
    ----------
    doc_shallow: sbol document.Document object
        a shallow doc created using sbol2
    
    Returns
    -------
    part_name: string
        the display id of the part
        
    Example
    -------
    file_in = "https://synbiohub.programmingbiology.org/public/UWYeast_AND_gate/plasmid_0/1/sbolnr"
    doc_shallow = sbol2.Document()
    doc_shallow.read(file_in)
    part_name1 = find_partname(file_in, doc_shallow)
    print(part_name1)
    
    """
    
    for top_level in doc_shallow:
        part_name = top_level.displayId
        
    return (part_name)

def islinear(doc):
    """
    Given sbol document (shallow or full) find linearness
    
    Requires
    --------
    None

    Parameters
    ----------
    doc: sbol document.Document object
        a shallow or full doc created using sbol2

    Returns
    -------
    linear: boolean
        if the file is linear True, if the file is circular (a plasmid) False
        
    Example
    -------
    file_in = "https://synbiohub.programmingbiology.org/public/UWYeast_AND_gate/plasmid_0/1/sbol"
    doc = sbol2.Document()
    doc.read(file_in)
    circular = islinear(doc)

    """
    
    linear = True
    for top_level in doc:
        if top_level.type == "http://sbols.org/v2#ComponentDefinition":    
            #create a set of types for every top_level component definition
            type_set = set(top_level.types)
            if "http://identifiers.org/so/SO:0000988" in type_set:
                linear = False
                
    return(linear)
        
def snapgeneseq(sequence, partname, out_dir, detectfeatures = True, linear = True):
    """
    Takes in a sequence string and generates genebank, plasmid map, and archive of both
    in the directory out_dir
    
    Requires
    --------
    import requests, os, shutil
    get_converted
    
    Parameters
    ----------
    sequence : string
        A series of atgc etc of the sbol that you want annotated/a plasmid map of
        
    partname : string
        The part name that will be used to name files etc
        
    out_dir : string, file path
        The directory where the output will be written to
        
    detectfeatures : Boolean, optional
        Whether or not features should be detected. The default is True.
        
    linear : boolean, optional
        Whether or not the given part is linear. The default is True.

    Returns
    -------
    None. But outputs partname.gb, partname.png, 
    and Zip.zip (containing gb and png) to out_dir

    """
    
    newtext_url = "http://song.ece.utah.edu/examples/pages/acceptNewText.php" #link to post to
    
    data = {}
    if detectfeatures:
        data["detectFeatures"] = "True"
    if linear:
        data["linear"]="True"

    
    #data to send
    data["textToUpload"] = sequence
    data["textId"] = partname
    data["textName"] = partname

    params ={} 
    
    #post data to snapgene server
    requests.post(newtext_url, data = data, params = params,  headers = {"Accept":"text/plain"})

    get_converted(partname, out_dir)
    
    return

def snapgenefile(filename, partname, out_dir, detectfeatures = False, linear = True):
    """
    Takes in a file name and generates genebank, plasmid map, and archive of both
    in the directory out_dir
    
    Requires
    --------
    import requests, os, shutil
    get_converted
    
    Parameters
    ----------
    filename : string
        a genbank file to upload for conversion
        
    partname: string
        The part name that will be used to name files etc
        
    out_dir : string, file path
        The directory where the output will be written to
        
    detectfeatures : Boolean, optional
        Whether or not features should be detected. The default is True.
        
    linear : boolean, optional
        Whether or not the given part is linear. The default is True.

    Returns
    -------
    None. But outputs partname.gb, partname.png, 
    and Zip.zip (containing gb and png) to out_dir
    """
    
    newfile_url = "http://song.ece.utah.edu/examples/pages/acceptNewFile.php"
    
    #linearity and detectFeatures works on presence so set those parameters
    data = {}
    if detectfeatures:
        data["detectFeatures"] = "True"
    if linear:
        data["linear"]="True"
    
    #file to open
    gbfile = requests.get(filename).content
    files = {'fileToUpload': (partname, gbfile)}
    
    #upload file
    requests.post(newfile_url, files=files, data = data, params = {},
                      headers = {"Accept":"text/plain"})

    get_converted(partname, out_dir)
    
    return

def get_converted(partname, out_dir):
    """
    Gets files from the snapgene server at song.ece.utah.edu and writes
    them to a local folder specified by out_dir
    
    Parameters
    ----------
    partname : string
        Name of part
        
    out_dir : string, filepath
        The file path where files should be output to

    Returns
    -------
    None.

    """
    
    get_url = "http://song.ece.utah.edu/dnafiles/"+partname
    
    #request genebank
    s = requests.get(f"{get_url}.gb")
    genbank = s.content
    
    #write out genbank
    gb_out_path = os.path.join(out_dir, f"{partname}.gb")
    with open(gb_out_path,'wb') as gb_file:
        gb_file.write(genbank)


    #get the png map generated
    t = requests.get(f"{get_url}.png")
    
    #output map generated
    png_out_path = os.path.join(out_dir, f"{partname}.png")
    with open(png_out_path, 'wb') as f:
            f.write(t.content)
    
    return
