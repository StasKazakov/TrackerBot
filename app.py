import logging
from urllib.parse import urlparse, parse_qs

from quart import request, redirect, Quart
from run import db
import betterlogging as bl


logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)


app = Quart(__name__)


@app.route('/', methods=['GET'])
async def handle_request():
    parsed_url = urlparse(request.url)
    query_params = parse_qs(parsed_url.query)
    link_id = query_params.get('link_id', [0])[0]
    if link_id == 0:
        return "<h1>Please stand by. All Jedi are busy.</h1><h1><p>Our contacts for support: </p></h1>" \
               "<h1>@adskiyponchik_ua, @CBoY_XD, @dankondankon, @staskazakovcom</h1>"

    try:
        with app.logger:
            app.logger.info(link_id)
            orig_link = await db.get_user_link(link_id)
            app.logger.info(orig_link)

        return redirect(orig_link)
    except KeyError:
        return "Invalid link_id", 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return "An error occurred", 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)