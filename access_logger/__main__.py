import logging
from os import environ

from flask import Flask

logger = logging.getLogger(__name__)

app = Flask(__name__)


if __name__ == "__main__":
    port = int(environ.get('PORT', 4242))
    logger.warning(f'Starting the server at port {port}')
    logger.warning(
        '\n-------\n'
        'It seems you are using flask directly, but cool kids now use a '
        'WSGI server. Try something like:\n\n '
        "  gunicorn -w 4 -b '0.0.0.0:4242' access_logger:app"
        '\n-------  \n'
    )
    app.run(port=port)
