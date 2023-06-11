import logging
from urllib.parse import urlparse, parse_qs

from quart import request, redirect, Quart

from db import get_link
from tools.db import Database

app = Quart(__name__)

@app.route('/', methods=['GET'])
async def handle_request():

    parsed_url = urlparse(request.url)
    query_params = parse_qs(parsed_url.query)
    link_id = query_params.get('link_id', 0)
    '''ТУТ ПОДКЛЮЧЕНИЕ К БД ЧТОБЫ ВЫТАЩИТЬ МЕТОДОМ КЛАССА 
    БД ССЫЛКУ НА КОТОРУЮ НУЖНО ПЕРЕНАПРАВИТЬ ФЛАСК'''
    orig_link = Database.get_user_link(link_id)
    logging.info(link_id)
    g = get_link(link_id)
    logging.info(g)
    return redirect(g)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)