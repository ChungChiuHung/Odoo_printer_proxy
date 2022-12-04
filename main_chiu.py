from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from html.parser import HTMLParser
from codecs import encode
from codecs import decode
import win32con
import win32ui
import os
import win32print


# PRINTER_NAME = 'EPSON LQ-690C ESC/P2'
# convert the dc into a "printer dc"
# get default printer
PRINTER_NAME = win32print.GetDefaultPrinter()

app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['GET'])
def api():
    return jsonify({'message': 'Hello World'})


@app.route('/dotmatrix/print', methods=['POST'])
def api_post_print():
    data = request.form['print_data']
    print(data)
    f = HTMLFilter()
    f.feed(data)
    print(f.text)

    # create a dc (Device Context) object (actually a PyCDC)
    dc = win32ui.CreateDC()

    # leave out the printername to get the default printer automatically
    dc.CreatePrinterDC(PRINTER_NAME)

    # you need to set the map mode mainly so you know how
    # # to scale your output. I do everything in points, so setting
    # the map mode as "twips" works for me.
    dc.SetMapMode(win32con.MM_TWIPS)  # 1440 per inch

    # here's that scaling I mentioned:
    scale_factor = 20  # i.e. 20 twips to the point

    # start the document. the description variable is a string
    # which will appear in the print queue to identify the job.
    dc.StartDoc('Win32print test')

    # to draw anything (other than text) you need a pen.
    # the variables are pen style, pen width and pen color.
    pen = win32ui.CreatePen(0, int(scale_factor), 0)

    # SelectObject is used to apply a pen or font object to a dc.
    dc.SelectObject(pen)

    # how about a font? Lucida Console 10 point.
    # I'm unsure how to tell if this failed.
    font = win32ui.CreateFont({
        "name": "Lucida Console",
        "height": int(scale_factor * 10),
        "weight": 400,
    })

    # again with the SelectObject call.
    dc.SelectObject(font)

    # okay, now let's print something.
    # TextOut takes x, y, and text values.
    # the map mode determines whether y increases in an
    # upward or downward direction; in MM_TWIPS mode, it
    # advances up, so negative numbers are required to
    # go down the page. If anyone knows why this is a
    # "good idea" please email me; as far as I'm concerned
    # it's garbage.
    y = 1
    for lineStr in f.text.splitlines():
        print(lineStr)
        dc.TextOut(scale_factor * 72,
                   -1 * scale_factor * y * 10,
                   lineStr)
        y += 1

    # for completeness, I'll draw a line.
    # from x = 1", y = 1"
    # dc.MoveTo((scale_factor * 72, scale_factor * -72))
    # to x = 6", y = 3"
    # dc.LineTo((scale_factor * 6 * 72, scale_factor * 3 * -72))

    # must not forget to tell Windows we're done.
    dc.EndDoc()
    return jsonify({'status': 'success', 'data': f.text})


class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
