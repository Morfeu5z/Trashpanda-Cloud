import logging
import sys

import static.scripts.EnvironmentVariable
from flask import Flask, render_template, redirect, request, jsonify, render_template_string, make_response

app = Flask(__name__)

@app.route('/')
def index():
    zmienna = "zmienna"
    return render_template('index.html', zmienna=zmienna)

@app.route('/userCheck', methods=['POST'])
def userCheck():
    # print('Check userID...')
    id = request.form['uid']
    # print(id)
    if id:
        inDB = 'true'
        return jsonify({'res' : inDB})

    return jsonify({'error' : 'Missing data!'})

@app.route('/info')
def info():
    return render_template('info_pages/info.html')

@app.route('/about')
def about():
    return render_template('info_pages/about.html')
    # return redirect("https://www.asciipr0n.com/pr0n/morepr0n/pr0n03.txt", code=302)
    # hackerman... jo-jo-jo

@app.route('/contact')
def kontakt():
    return render_template('info_pages/contact.html')

@app.route('/mytrashbox')
def mytrashbox():
    return render_template('trashbox.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('info_pages/404.html')
    # return redirect("https://www.asciipr0n.com/pr0n/morepr0n/pr0n04.txt", code=302)

@app.route('/loadingTrashbox', methods=['POST'])
def loadingTrashbox():
    googleID = request.form['gid']
    print('GoogleID from ajax: '+googleID)
    return jsonify({
        'load' : render_template('include/trashbox.html', gid=googleID)
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
