from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from html.parser import HTMLParser
import os
# import win32print

PRINTER_NAME = ''

app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['GET'])
def api():
    return jsonify({'message': 'Hello World'})


@app.route('/dotmatrix/print', methods=['POST'])
def api_post_print():
    data = request.form['print_data']
    f = HTMLFilter()
    f.feed(data)
    print(f.text)
    p = win32print.OpenPrinter(PRINTER_NAME)
    job = win32print.StartDocPrinter(p, 1, ("test of raw data", None, "RAW"))
    win32print.StartPagePrinter(p)
    win32print.WritePrinter(p, f.text.encode('utf8'))
    win32print.EndPagePrinter(p)
    return jsonify({'status': 'success', 'data': f.text})


class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
