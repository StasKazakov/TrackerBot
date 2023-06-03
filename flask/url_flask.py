import datetime

from flask import Flask, request, redirect
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

from waitress import serve


def add_utm_params(url, utm_source, utm_medium, utm_campaign, country):
    parsed_url = urlparse(url)
    query_params = parsed_url.query
    f = [utm_source, utm_medium, utm_campaign, country]
    params = dict(p.split('=') for p in query_params.split('&')) if query_params else {}

    params['utm_source'] = utm_source
    params['utm_medium'] = utm_medium
    params['utm_campaign'] = utm_campaign
    params['country'] = country
    params['datetime'] = datetime.datetime.now().strftime('%H:%M:%S-%d/%m/%Y')

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



redirect_url = add_utm_params('https://t.me/botfatherdev', 'Telegram', 'adv', 'new service',
                                  'Spain')


app = Flask(__name__)

@app.route('/', methods=['GET'])
def utm_tracker():
    g = ['utm_source', 'utm_medium', 'utm_campaign', 'country', 'datetime']
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    params_list = [f"{i}: {query_params.get(i, [''])[0]}" for i in g]
    print(*params_list, sep='\n')
    return redirect(redirect_url)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)




