# Access logger

This is a small self-contained tool to register accesses (entry and exit).

## Usage
You need Python 3.6 or later.

Use:

     python3 -m venv .venv
     .venv/bin/python3 -m pip install -r requirements.txt
     .venv/bin/gunicorn -w 4 -b '0.0.0.0:4242' access_logger:app

Then visit http://{your IP}:4242/static/index.html

The data for eache entry/exit is stored in an HTML file, and also as a row in a CSV.

## License
This is MIT licensed. It uses Bulma for the CSS and Fabric.js to collect the signature.
