"""Dev server for the dashboard: serves the static files on http://0.0.0.0:3000 with caching off."""

import os

try:
    from flask import Flask, send_from_directory
except ImportError:
    print("Flask isn't installed. Run `pip3 install -r requirements.txt` and try again.")
    exit(1)

static_file_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable cache


@app.route('/', methods=['GET'])
def serve_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file(path):
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
