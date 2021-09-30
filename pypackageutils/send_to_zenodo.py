"""send_to_zenodo  This is function sends up files to the JGCRI community on zenodo.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import requests
import json
import csv

def upload_zenodo_record(access_token = None,
                         path_to_data = None,
                         metadata = None):
    """Get the sum from a list of values.

    :param access_token:                  Access token to Zenodo Community
    :type access_token:                   str

    :param path_to_data:                  Path to file or folder to upload
    :type path_to_data:                   str

    :param metadata:                      metadata as a python dictionary or path to .csv file
    :type metadata:                       dict

    """

    # Connect to Zenodo
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}

    #Create new upload
    r1 = requests.post('https://zenodo.org/api/deposit/depositions',
                       params=params,
                       json={},
                       headers=headers)

    if r1.status_code > 210:
        print("Error happened during submission, status code: " + str(r1.status_code))
        return 

    # Get id and doi from temporary upload
    id = str(r1.json()["id"])
    doi = str(r1.json()["metadata"]["prereserve_doi"]["doi"])

    # Upload the file and add metadata
    if (metadata != None):
        # If metadata is a path to csv file then read in and convert to dictionary first
        if type(metadata) == str and "csv" in metadata: #Check if path to csv
            csv_file = open(metadata, "r") # return a file object that has been opened for reading
            dict_reader = csv.DictReader(csv_file) # return a csv.DictReader object
            ordered_dict_from_csv = list(dict_reader)[0] # Convert the csv.DictReader object to a list and extract the first element to return an csv.OrderedDict object
            metadata = dict(ordered_dict_from_csv) # Use dict() to convert the csv.OrderedDict object to a dictionary.

            # Append the elements to params
            data = {
                'metadata': metadata
            }
        elif type(metadata) == dict: 
            data = {
                'metadata': metadata
            } 
        else: 
            print("Wrong metadata format. Needs to be path to csv or dictionary")
            return
    else: 
        # Set default metadata
        data = {
                "metadata": {'title': 'Untitled', 'description': 'Description.', 'upload_type': 'other'} 
        } 

    # Get files to upload: 
    if path_to_data is not None: 
        files = {'file': open(path_to_data, 'rb')}

        # Upload the file or folder
        r2 = requests.post('https://zenodo.org/api/deposit/depositions/%s/files' % id,
                        params=params,
                        data = data, 
                        files = files)
        # put in status code check
                        
    # Add metadata
    r3 = requests.put('https://zenodo.org/api/deposit/depositions/%s' % id,
                      params=params, data=json.dumps(data),
                      headers=headers) 
    # put in status code check

    # Create return dictionary
    return_dict = dict()
    return_dict['id'] = id
    return_dict['doi'] = doi

    return return_dict


def delete_zenodo_record(access_token = None, 
                         id = None):

    params = {'access_token': access_token}

    r = requests.delete('https://zenodo.org/api/deposit/depositions/' + id,
                        params=params)
    if r.status_code == 204:
        print(f'Deleted object with id#: {id}')
    #Add error if status code not 204
        return


def update_zenodo_record(access_token = None, 
                         id = None, 
                         metadata = None, 
                         path_to_data = None):

    # how do file updates work? 

    # Connect to Zenodo
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}
    
    # Get existing metadata for id provided
    r_existing = requests.get('https://zenodo.org/api/deposit/depositions/%s' % id,
                              params = {'access_token': access_token})
    metadata_existing = r_existing.json()['metadata']

    # If new metadata is path to csv file, convert it to python dictionary
    if type(metadata) == str and "csv" in metadata: #Check if path to csv
        csv_file = open(metadata, "r") # return a file object that has been opened for reading
        dict_reader = csv.DictReader(csv_file) # return a csv.DictReader object
        ordered_dict_from_csv = list(dict_reader)[0] # Convert the csv.DictReader object to a list and extract the first element to return an csv.OrderedDict object
        metadata = dict(ordered_dict_from_csv) # Use dict() to convert the csv.OrderedDict object to a dictionary.

    # Keys: "title", "upload_type" and "description" are required for updating metadata
    # If new or old metadata does not have title set defaults
    if "title" not in list(metadata.keys()):
        if "title" not in list(metadata_existing.keys()):
            metadata['title']='Untitled'
        else:
            metadata['title']=metadata_existing['title']
        # Check that title is not blank
    else:
        if metadata['title']=='':
            metadata['title']='Untitled'

    # If metadata does not have upload_type set defaults
    if "upload_type" not in list(metadata.keys()):
        if "upload_type" not in list(metadata_existing.keys()):
            metadata['upload_type']='other'
        else:
            metadata['upload_type']=metadata_existing['upload_type']
    # Check that output_type is one of the valid entries
    else:
        # List of valid upload types: https://developers.zenodo.org/#representation
        upload_type_valid = ['publication','poster','presentation','dataset','image',
                             'video','software','lesson','physicalobject','other']
        if metadata['upload_type'] not in upload_type_valid:
            print(f'upload_type must be one of #: {upload_type_valid} with given metadata.')
            print(f'Changing upload_type to other.')
            metadata['upload_type']='other'

    # if metadata does not have description set defaults
    if "description" not in list(metadata.keys()):
        if "description" not in list(metadata_existing.keys()):
            metadata['description'] = 'Description.'
        else:
            metadata['description'] = metadata_existing['description']
    # Check that description is not blank
    else:
        if metadata['description'] == '':
            metadata['description'] = 'Untitled'

    # Append the elements to params
    data = {
        'metadata': metadata
    }

    # Now update the metadata for the deposition id
    r1 = requests.put('https://zenodo.org/api/deposit/depositions/%s' % id,
                     params = {'access_token': access_token},
                     data = json.dumps(data),
                     headers = headers)

    # Get id and doi
    id = str(r1.json()["id"])
    doi = str(r1.json()["metadata"]["prereserve_doi"]["doi"])

    # Get files to upload: 
    if path_to_data is not None: 
        files = {'file': open(path_to_data, 'rb')}

        # Upload the file or folder
        r2 = requests.post('https://zenodo.org/api/deposit/depositions/%s/files' % id,
                        params=params,
                        data = data, 
                        files = files)
        # put in status code check

     # Create return dictionary
    return_dict = dict()
    return_dict['id'] = id
    return_dict['doi'] = doi

    return return_dict

#def publish_zenodo_record(access_token = None, 
#                           id = None):
