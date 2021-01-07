import csv
from datetime import datetime
from html import escape
import logging
from os import environ, makedirs

from flask import Flask, request, redirect

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    )

makedirs('data', exist_ok=True)

app = Flask(__name__)


def represent_event(raw_data):
    """Given a raw object from the frontend, generate an HTML representation.

    Takes care of escaping, naming the fields and handling empty ones.
    """
    name = escape(raw_data.get('name', '-'))
    family_name = escape(raw_data.get('family name', '-'))
    company = escape(raw_data.get('company', '-'))
    signature = escape(raw_data.get('signature', ''))

    return f'''
        <p>Name: {name}</p>
        <p>Family name: {family_name}</p>
        <p>Company: {company}</p>

        <img src="{signature}" />
    ''', [name, family_name, company]


def register_event(event_type, event_data):
    report_snippet, row = represent_event(event_data)
    current_ts = datetime.now().strftime("%Y%d%m_%H%M%S")
    human_ts = datetime.now().strftime("%Y-%d-%m %H:%M:%S")
    with open(f'data/{current_ts}_{event_type}.html', 'w') as f:
        f.write(f'''
        <!doctype html>
        <html lang="en">
        <head><title>{event_type.capitalize()} log</title></head>
        <body>
        {event_type.capitalize()} at {human_ts}
        {report_snippet}
        </body>
        </html>
        ''')
    with open('data/events.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([event_type, human_ts] + row)
    return redirect('/static/index.html')


@app.route('/log_entry', methods=['POST'])
def log_entry():
    register_event('entry', request.get_json())
    return redirect('/static/index.html')


@app.route('/log_exit', methods=['POST'])
def log_exit():
    register_event('exit', request.get_json())
    return redirect('/static/index.html')


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
    app.run(host='0.0.0.0', port=port)
