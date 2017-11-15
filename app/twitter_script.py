import random
import string
import time
import urllib
import hmac
from hashlib import sha1


base_url = 'https://api.twitter.com/1.1/statuses/update.json'
get_nonce = lambda : ''.join(random.choice(string.ascii_letters) for s in xrange(random.randint(10, 20)))
get_timestamp = lambda : str(int(time.time()))

auth_data = {
    'include_entities': 'true',
    'oauth_consumer_key': 'P6jSQmeVPeA7YJK3oI14oz46h',
    'oauth_nonce': get_nonce(),
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': get_timestamp(),
    'oauth_token': '732728148-mneIJp9gAxHpzln28mpPcgIQpB2iVFVoB7vp6wsx',
    'oauth_version': '1.1',
    'status': 'This is a test status'
}
token_secret = 'iomDBUPBrlDkMHflhMVNivbyygobhx7OdeGFPkkg4Sqd3'
consumer_secret = 'Uvaa3T5xuy6qsAJ3YLON5qOM42ACXxhjB9Xyo0COfiVeC3cXwZ'

param_string = '&'.join('%s=%s'%(key, auth_data[key]) for key in sorted(auth_data.keys()))
signature_base_string = 'POST&%s&%s' % (urllib.quote(base_url, safe=''), urllib.quote(param_string, safe=''))
signing_key = '%s&%s' % (urllib.quote(consumer_secret, safe=''), urllib.quote(token_secret, safe=''))
hashed = hmac.new(signing_key, signature_base_string, sha1)
signature = hashed.digest().encode('base64').rstrip('\n')

new_auth_data = dict(
    oauth_consumer_key=auth_data['oauth_consumer_key'],
    oauth_nonce=auth_data['oauth_nonce'],
    oauth_signature=signature,
    oauth_signature_method=auth_data['oauth_signature_method'],
    oauth_timestamp=auth_data['oauth_timestamp'],
    oauth_token=auth_data['oauth_token'],
    oauth_version=auth_data['oauth_version']
)


print DST.replace(', ', '\n')
