import logging
from urllib.parse import urlparse, parse_qs

from quart import request, redirect, Quart


app = Quart(name)

@app.route('/', methods=['GET'])
async def handle_request():
    parsed_url = urlparse(request.url)
    query_params = parse_qs(parsed_url.query)
    params_list = {i: query_params.get(i, [''])[0] for i in g}
    logging.info(params_list)
    return redirect(params_list['link'])