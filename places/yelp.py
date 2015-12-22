# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import sys
import urllib
import urllib2
import os
import oauth2
import pdb


DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Campbell, CA'
SEARCH_LIMIT = 8
SEARCH_PATH = '/v2/search'
BUSINESS_PATH = '/v2/business/'


def request(path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    # OAuth credential placeholders that must be filled in by users.
    CONSUMER_KEY = os.environ.get('YELP_CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('YELP_CONSUMER_SECRET')
    TOKEN = os.environ.get('YELP_TOKEN')
    TOKEN_SECRET = os.environ.get('YELP_TOKEN_SECRET')

    host = 'api.yelp.com'
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print('Querying {0} with params {1}...'.format(url, url_params),
          file=sys.stderr)
    print('URL: {}'.format(signed_url))

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    if "error" in response:
        print(response['error'], file=sys.stderr)

    return response


def search(term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(SEARCH_PATH, url_params=url_params)


def get_yelp_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    business = request(business_path)
    # print('-------', file=sys.stderr)
    # print(business, file=sys.stderr)
    return dict(name=business['name'], url=business['url'])


def get_yelp_matches(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.

    Returns:
        list of dicts with keys of: name, id and cuisine
    """
    # print('term={}'.format(term), file=sys.stderr)
    # print('location={}'.format(location), file=sys.stderr)
    response = search(term, location)
    # response contains ['region', 'total', 'businesses']

    try:
        businesses = response.get('businesses')
    except Exception as e:
        print('------ Got an exception in getting businesses from yelp', file=sys.stderr)
        print(e, file=sys.stderr)

    # ['is_claimed', 'rating', 'mobile_url', 'rating_img_url', 'review_count',
    # 'name', 'rating_img_url_small', 'url', 'is_closed', 'phone', 'snippet_text',
    # 'image_url', 'categories', 'display_phone', 'rating_img_url_large', 'id',
    # 'snippet_image_url', u'location']

    if not businesses:
        return

    matches = []
    for bus in businesses:
        item = dict(name=bus['name'], id=bus['id'])
        try:
            item['location'] = bus['location']['address'][0]
        except:
            item['location'] = ''

        try:
            item['cuisine'] = ','.join([x[0] for x in bus['categories']])
        except:
            item['cuisine'] = ''

        matches.append(item)

    print(matches, file=sys.stderr)
    return matches
