""" send basic GET request to /posts/search to return the 25 most-recent results; 
        usage `python3 posts-search.py` """

import requests as r # `pip install requests`
from requests.auth import HTTPBasicAuth

# credentials
API_USER = '[ enter api user here ]'
API_PASSWORD = '[ enter api password here ]'

# API params
LIMIT = 40

def crunch_data(record):
    # do something with this post...
    # record details available as `record['id']`
    pass
    
def get_posts(url):
    response = r.get(
        url,
        # add any params here
        params={'limit': LIMIT},
        # this handles the base64encoding for you
        auth=HTTPBasicAuth(API_USER, API_PASSWORD)
    )

    # check response code to make sure request was successful
    if response.status_code != 200:
        print('Error fetching posts from {0}. Server responded with status {1}.'
                    .format(full_url, response.status_code))
        
        # See https://sharpr.com/developers/rest/overview/request for details
        ## on the API-Response-Errors header.
        print('Error details: {0}'
                    .format(response.headers['API-Response-Errors']))

        if 'API-Response-Notices' in response.headers:
            # See https://sharpr.com/developers/rest/overview/request for details
            ## on the API-Response-Notices header.
            print('Error response notices: {0}'
                    .format(response.headers['API-Response-Notices']))

        return False
    else:
        try:
            result_count = len(response.json())
            print('API returned {0} records.'.format(result_count))
            for record in response.json():
                crunch_data(record)
        except ValueError as e:
            # If we are here, then response.json() is empty. That means there
            ## are no records that match our query.
            print('No records returned from {0}.'.format(url))


if __name__ == '__main__':
    get_posts('https://sharpr.com/api/v2/posts/search')