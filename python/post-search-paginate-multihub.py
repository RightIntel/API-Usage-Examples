""" Request posts from multiple hubs at the same time using the pagination 
    feature; usage: `python3 post-search-paginate-multihub.py` 
    
    Getting posts from multiple hubs at the same time requires the following steps:
    1. Get bearer token using Basic Auth and an email address of someone who is 
	an account manager on the account.
    2. Hit GET /api/v2/posts/search and send `mine` in the Hubs header"""
    

import requests as r # `pip install requests`
from requests.auth import HTTPBasicAuth

# credentials
API_USER = '[ enter user here ]'
API_PASSWORD = '[ enter password here ]'
BEARER_TOKEN = ''

# API params
LIMIT = 100

def api_query_success(response, msg):
    """ Function to verify that API query was successful """
    if response.status_code != 200:
        print('{0}. Server responded with status {1}.'
                    .format(msg, response.status_code))

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
        return True


def get_bearer_token():
    """ Request a bearer token for future API calls (querying multiple hubs at 
        the same time is not possible without a bearer token) """
    global BEARER_TOKEN
    print('Getting bearer token...')

    if len(BEARER_TOKEN) > 0:
        print('Found cached bearer token')
        return BEARER_TOKEN

    response = r.post(
        'https://sharpr.com/api/v2/auth/bearer',
        params={'email': '[email address of an account manager user]'},
        # this handles the base64encoding for you
        auth=HTTPBasicAuth(API_USER, API_PASSWORD)
    )

    success = api_query_success(response, 'Error creating bearer token')
    if success:
        try:
            print('Successfully retrieved bearer token')
            result = response.json()
            BEARER_TOKEN = result['token']

            return BEARER_TOKEN

        except ValueError as e:
            # If we are here, then response.json() is empty. That means there
            ## are no records that match our query.
            print('Unable to get bearer token')
    else:
        return False


def crunch_data(record):
    # do something with this post...
    # record details available as `record['id']`
    pass


def get_posts(url):
    """ Query the API to get all current posts from any hub the user has access
        to. Uses pagination to continue querying until all posts are retrieved. """
    bearer_token = get_bearer_token()

    print('Getting batch of posts from {0}...'.format(url))
    response = r.get(
        url,
        # `order_by` param is required to get the API-Next-Page header
        params={'order_by': 'created', 'limit': LIMIT},
        # Using Bearer authorization here, allows us to use the Hubs
        ## header. This means we will get results from all hubs the 
        ## user is a part of.
        headers={'Authorization': 'Bearer {0}'.format(bearer_token),
                    'Hubs': 'mine'}
    )

    success = api_query_success(response, 'Error fetching posts from {0}'.format(url))

    if success:
        try:
            result_count = len(response.json())
            print('API returned {0} records.'.format(result_count))
            for record in response.json():
                crunch_data(record)

            # once we've saved all records from previous call, we can get the
            ## next set of records. The value of the API-Next-Page header is a
            ## URL that we can use to make the next call.
	
            # NOTE: uncomment the if/else below to get all posts in all the hubs
            ## the user is a part of:
            #if 'API-Next-Page' in response.headers and result_count == LIMIT:
            #    get_posts(response.headers['API-Next-Page'])
            #else:
                # if we don't have that header or if the API returned fewer
                ## results than we asked for, then we're done.
            #    print('No more records available for this search.')
        except ValueError as e:
            # If we are here, then response.json() is empty. That means there
            ## are no records that match our query.
            print('No records returned from {0}.'.format(url))
    else:
        return False

if __name__ == '__main__':
    get_posts('https://sharpr.com/api/v2/posts/search')
