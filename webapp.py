from flask import Flask, request, render_template
from splits import calc
app = Flask(__name__)

def calc_splits(tcxfile, split):
    return calc(tcxfile, float(split))

@app.route('/', methods=['POST', 'GET'])
def splits():

    if request.method == 'POST':
        tcxfile = request.files['tcxfile']
        split = request.form['split']
        splits = calc_splits(tcxfile, split)
        return render_template('splits.html', splits=splits)
    else:
        return render_template('splits.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
