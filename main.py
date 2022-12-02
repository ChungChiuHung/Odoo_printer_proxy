from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
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
    # p = win32print.OpenPrinter(PRINTER_NAME)
    # job = win32print.StartDocPrinter(p, 1, ("test of raw data", None, "RAW"))
    # win32print.StartPagePrinter(p)
    # win32print.WritePrinter(p, data.encode())
    # win32print.EndPagePrinter(p)
    return jsonify({'status': 'success', 'data': data})


'''
***something need to be done here, for translate html source code to printer data***
soup = BeautifulSoup(html_input , "html.parser")
for elem in soup.find_all(["a", "p", "div", "h3", "br"]):
            elem.replace_with(elem.text + "\n\n")
'''

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
