import datetime

from urllib.parse import urlparse, urlencode, urlunparse


'''-----------------CLASS VERSION-----------------'''
class UTMTracker:
    def init(self, user_id):
        self.user_id = user_id

    def add_utm_params(self):
        parsed_url = urlparse('http://tracklink.tech')
        query_params = parsed_url.query
        params = {
            'user_id': self.user_id,
        }

        # Build the updated URL with UTM parameters
        updated_query_params = urlencode(params)
        updated_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            updated_query_params,
            parsed_url.fragment
        ))
        print(updated_url)
        return updated_url