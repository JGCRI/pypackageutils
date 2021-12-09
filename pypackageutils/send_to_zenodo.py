""" send_to_zenodo

This script allows users to send up files to the JGCRI community on Zenodo.

:author:   Zarrar Khan and Ellie Lochner
:email:    zarrar.khan@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

# TODO
    # Check if we can upload multiple files
    # path_to_data and metadata are optional in upload function. Need to specify this?
        # test w/ making access token a requirement
            # is this a requirement in get function
    # upload function: If metadata upload (r2) fails should we bail out of function?
    # Delete and update functions: Should ID be str? if statement if an integer 

import requests
import json
import csv
import os 
import shutil

def upload_zenodo_record(access_token = None,
                         path_to_data = None,
                         metadata = None):
    """Upload deposition to Zenodo.

    If data to upload is a directory, this function will zip it first, 
    otherwise just upload the single file with the corresponding metadata

    :param access_token: Access token to Zenodo Community
    :type access_token: str

    :param path_to_data: Path to file or folder to upload
    :type path_to_data: str

    :param metadata: metadata as a python dictionary or path to .csv file
    :type metadata: dict or str

    """

    # Connect to Zenodo and create new empty upload
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}
    r1 = requests.post('https://zenodo.org/api/deposit/depositions',
                       params=params,
                       json={},
                       headers=headers)
                       
    # Check that upload worked
    if r1.status_code > 210:
        print("Error happened during submission") # Print error messages and status code
        r1.json() 
        return  # If we can't do the initial upload, exit function

    # Get ID and DOI from successful upload
    id = str(r1.json()["id"])
    doi = str(r1.json()["metadata"]["prereserve_doi"]["doi"])

    # Process metadata if it exists
    if (metadata != None):
        # If metadata is a path to csv file, read it in and convert to dictionary
        if type(metadata) == str and "csv" in metadata: # Check if path to csv
            csv_file = open(metadata, "r") # Return a file object that has been opened for reading
            dict_reader = csv.DictReader(csv_file) # Return a csv.DictReader object
            ordered_dict_from_csv = list(dict_reader)[0] # Convert csv.DictReader object to a list and extract the first element to return an csv.OrderedDict object
            metadata = dict(ordered_dict_from_csv) # Use dict() to convert the csv.OrderedDict object to a dictionary.

        # Return error if metadata exists but is not a path to a CSV or dictionary 
        elif type(metadata) != dict: 
            print("Wrong metadata format. Needs to be path to csv or dictionary")
            # Delete existing record that we made earlier and exit function
            delete_zenodo_record(access_token, id)
            return
            
    # If metadata was not provided, set default metadata
    else: 
        metadata = {'title': 'Untitled', 'description': 'Description.', 'upload_type': 'other'} 
        print("No metadata provided. Setting to default metadata.")

    # Append metadata to data object
    data = {'metadata': metadata}
                    
    # Add metadata to initial upload
    r2 = requests.put('https://zenodo.org/api/deposit/depositions/%s' % id,
                      params=params, 
                      data=json.dumps(data),
                      headers=headers) 

    # Check that upload worked. If it did not, print error message but continue function
    if r2.status_code > 210:
        print("Error: Metadata not uploaded correctly")
        r2.json()

    # Get files to upload if provided
    if path_to_data is not None: 
        # If path_to_data is a file, read it in
        if os.path.isfile(path_to_data):
            files = {'file': open(path_to_data, 'rb')} 
        # If path_to_data is a directory, zip it first and then read it in
        elif os.path.isdir(path_to_data): 
            def make_archive(source, destination):
                base = os.path.basename(destination)
                name = base.split('.')[0]
                format = base.split('.')[1]
                archive_from = os.path.dirname(source)
                archive_to = os.path.basename(source.strip(os.sep))
                shutil.make_archive(name, format, archive_from, archive_to)
                #shutil.move('%s.%s'%(name,format), destination)

            destination = os.getcwd() + '/' + os.path.basename(path_to_data) + '.zip'
            make_archive(source = path_to_data, destination = destination)
            files = {'file': open(destination, 'rb')}
        # If path_to_data is neither a file or directory, delete initial upload and exit function
        else:
            print("Data in path_to_data must be either a file or folder")
            # Delete existing record that we made earlier and exit function
            delete_zenodo_record(access_token, id)
            return

        # Upload the file or zipped folder
        r2 = requests.post('https://zenodo.org/api/deposit/depositions/%s/files' % id,
                            params=params,
                            data = data,
                            files = files)

        # Check that upload worked
        if r2.status_code > 210:
            print("Error happened during submission, status code: " + str(r2.status_code))
            # Delete existing record that we made earlier and exit function
            delete_zenodo_record(access_token, id)
            return

    # If no data provided, print a message but continue with function because users can add data to deposition later
    else:
        print("No upload data provided")

    # Create return dictionary
    return_dict = dict()
    return_dict['id'] = id
    return_dict['doi'] = doi

    print("upload_zenodo_record complete.")

    return return_dict


def delete_zenodo_record(access_token = None, 
                         id = None):
    """Delete existing Zenodo record.

    Can only delete unpublished records

    :param access_token: Access token to Zenodo Community
    :type access_token: str

    :param id: Unique zenodo record ID (can be found in URL)
    :type id: str


    """
    params = {'access_token': access_token}

    # Delete record based on ID provided
    r = requests.delete('https://zenodo.org/api/deposit/depositions/' + id,
                        params=params)

    # Check status code to see if record was successfully deleted
    # If incorrect code, exit function
    if r.status_code == 204:
        print(f'Deleted object with id#: {id}')
    else:
        print("Could not delete record")
        return
    
    print("delete_zenodo_record complete.")
    return


def update_zenodo_record(access_token = None, 
                         id = None, 
                         metadata = None, 
                         path_to_data = None):

    # Connect to Zenodo
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}
    
    # Get existing metadata for id provided
    r_existing = requests.get('https://zenodo.org/api/deposit/depositions/%s' % id,
                              params = {'access_token': access_token})
    metadata_existing = r_existing.json()['metadata']
    if (metadata == None):
        metadata = metadata_existing

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
    # Check that upload worked. If it did not, print error message but continue function
    if r1.status_code > 210:
        print("Error: Metadata not uploaded correctly")
        r1.json()


    # This adds new files. Does not replace existing files
    if path_to_data is not None: 
        if os.path.isfile(path_to_data):
            files = {'file': open(path_to_data, 'rb')} 
        # If path is a folder, zip it first
        elif os.path.isdir(path_to_data): 
            def make_archive(source, destination):
                base = os.path.basename(destination)
                name = base.split('.')[0]
                format = base.split('.')[1]
                archive_from = os.path.dirname(source)
                archive_to = os.path.basename(source.strip(os.sep))
                shutil.make_archive(name, format, archive_from, archive_to)
                #shutil.move('%s.%s'%(name,format), destination)

            destination = os.getcwd() + '/' + os.path.basename(path_to_data) + '.zip'
            make_archive(source = path_to_data, destination = destination)
            files = {'file': open(destination, 'rb')}
        else:
            print("Not valid data")

        r2 = requests.post('https://zenodo.org/api/deposit/depositions/%s/files' % id,
                           params=params,
                           data = data, 
                           files = files)
        r2.json()
        # Check that upload worked
        if r2.status_code > 210:
            print("Error happened during data upload")


    # Get id and doi
    id = str(r1.json()["id"])
    doi = str(r1.json()["metadata"]["prereserve_doi"]["doi"])

     # Create return dictionary
    return_dict = dict()
    return_dict['id'] = id
    return_dict['doi'] = doi

    return return_dict

#def publish_zenodo_record(access_token = None, 
#                          id = None):

def get_zenodo_record(access_token = None,
                      queries = None,
                      id = None):

    r = requests.get('https://zenodo.org/api/deposit/depositions',
                     params={'access_token': access_token, 
                              'q' : queries})

    print(json.dumps(r.json(), indent=2))