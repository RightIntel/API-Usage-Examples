""" send GET requests to /posts/search on Sharpr's API using the pagination
    feature; usage `python3 posts-search-paginate.py` """

import requests as r # `pip install requests`
from requests.auth import HTTPBasicAuth

# credentials
API_USER = '[enter user name here ]'
API_PASSWORD = '[ enter password here ]'

# API params
LIMIT = 100

def crunch_data(record):
    # do something with this post...
    # record details available as `record['id']`
    pass

def get_posts(url):
    response = r.get(
        url,
        # `order_by` param is required to get the API-Next-Page header
        params={'order_by': 'created', 'limit': LIMIT},
        # this handles the base64encoding for you
        auth=HTTPBasicAuth(API_USER, API_PASSWORD)
    )

    # check response code to make sure request was successful
    if response.status_code != 200:
        print('Error fetching posts from {0}. Server responded with status {1}.'
                    .format(url, response.status_code))
        
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

            # once we've saved all records from previous call, we can get the
            ## next set of records. The value of the API-Next-Page header is a
            ## URL that we can use to make the next call.
            if 'API-Next-Page' in response.headers and result_count == LIMIT:
                get_posts(response.headers['API-Next-Page'])
            else:
                # if we don't have that header or if the API returned fewer
                ## results than we asked for, then we're done.
                print('No more records available for this search.')
        except ValueError as e:
            # If we are here, then response.json() is empty. That means there
            ## are no records that match our query.
            print('No records returned from {0}.'.format(url))


if __name__ == '__main__':
    get_posts('https://sharpr.com/api/v2/posts/search')
