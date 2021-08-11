"""send_to_zenodo  This is function sends up files to the JGCRI community on zenodo.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os
import requests


def send_to_zenodo(access_token):
    """Get the sum from a list of values.

    :param access_token:                  Access token to Zenodo Community
    :type access_token:                   str

    :return:                              int

    """

    # Connect to Zenodo
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}

    r = requests.post('https://zenodo.org/api/deposit/depositions',
                      params=params,
                      json={},
                      headers=headers)

    r.status_code

    return(r.status_code)