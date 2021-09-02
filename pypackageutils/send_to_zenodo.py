"""send_to_zenodo  This is function sends up files to the JGCRI community on zenodo.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import requests
import json


def send_to_zenodo(access_token = None,
                   delete = False,
                   id = None,
                   metadata = None):
    """Get the sum from a list of values.

    :param access_token:                  Access token to Zenodo Community
    :type access_token:                   str

    :param delete:                  Delete a given id number deposition on Zenodo
    :type delete:                   bool

    :param delete:                  id of Zenodo deposition to edit or delete
    :type delete:                   str

    :param metadata:                 metadata as a python dictionary or path to .csv file
    :type metadata:                  dict

    """

    # Connect to Zenodo
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}
    id_orig = id
    doi = None

    # Create new entry
    if (delete == False) and (id==None):
        r = requests.post('https://zenodo.org/api/deposit/depositions',
                          params=params,
                          json={},
                          headers=headers)

        print(r.status_code)

        # Get id and doi from temporary upload
        id = str(r.json()["id"])
        doi = str(r.json()["metadata"]["prereserve_doi"]["doi"])


    # Add metadata
    if (metadata != None) and (id_orig != None):
        # If metadata is a path to csv file then read in and convert to dictionary first
        # Add some checks to make sure metadata entries match allowed keys

        # Get existing metadata for id provided
        r_existing = requests.get('https://zenodo.org/api/deposit/depositions/%s' % id,
                         params = {'access_token': access_token})
        metadata_existing = r_existing.json()['metadata']

        # Keys: "title", "upload_type" and "description" are required for updating metadata
        # if metadata does not have title set defaults
        if "title" not in list(metadata.keys()):
            if "title" not in list(metadata_existing.keys()):
                metadata['title']='Untitled'
            else:
                metadata['title']=metadata_existing['title']

        # if metadata does not have upload_type set defaults
        if "upload_type" not in list(metadata.keys()):
            if "upload_type" not in list(metadata_existing.keys()):
                metadata['upload_type']='other'
            else:
                metadata['upload_type']=metadata_existing['upload_type']

        # if metadata does not have description set defaults
        if "description" not in list(metadata.keys()):
            if "description" not in list(metadata_existing.keys()):
                metadata['description'] = 'Description.'
            else:
                metadata['description'] = metadata_existing['description']

        # Check that title and description are not blank
        # Check that output_type is one of the valid entries

        # If it is a dictionary append the elements to params
        data = {
            'metadata': metadata
        }

        print("data")
        print(data)

        # Now update the metadata for the deposition id
        r = requests.put('https://zenodo.org/api/deposit/depositions/%s' % id,
                         params = {'access_token': access_token},
                         data = json.dumps(data),
                         headers = headers)

        print(f'Updating deposition id#: {id} with given metadata.')
        print(r.status_code)

    # If delete == TRUE & id != NONE
    if (delete == True) and (id != None):
        r = requests.delete('https://zenodo.org/api/deposit/depositions/' + id,
                            params=params)
        print(f'Deleted object with id#: {id}')

    # Create return dictionary
    return_dict = dict()
    return_dict['id'] = id
    return_dict['doi'] = doi

    return return_dict