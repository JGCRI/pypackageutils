"""send_to_zenodo  This is function sends up files to the JGCRI community on zenodo.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os
import requests


def send_to_zenodo(access_token = None,
                   delete = False,
                   id = None):
    """Get the sum from a list of values.

    :param access_token:                  Access token to Zenodo Community
    :type access_token:                   str

    :param delete:                  Delete a given id number deposition on Zenodo
    :type delete:                   bool

    :param delete:                  id of Zenodo deposition to edit or delete
    :type delete:                   str

    """

    # Connect to Zenodo
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}

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

    # If delete == TRUE & id != NONE
    if (delete == True) and (id != None):
        r = requests.delete('https://zenodo.org/api/deposit/depositions/' + id,
                            params=params)
        print(f'Deleted object with id#: {id}')
        doi = None

    # Create return dictionary
    return_dict = dict()
    return_dict['id'] = id
    return_dict['doi'] = doi

    return return_dict