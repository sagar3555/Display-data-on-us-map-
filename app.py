import os
import numpy  as np
import  pandas as pd
from flask import Flask, flash, request, redirect, url_for ,render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'E:\\fulfil.io assignment\\uploads'   ## Change it as per your File system 
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            csv = pd.read_csv(file, header=0, delimiter=",")
            csv["Order Amount"] = csv["Order Amount"].map(lambda x: np.float64(x.replace("$", "")))
            df1 = csv.groupby("State")["Order Amount"].agg({"Order Amount": ['mean', 'max', 'min','sum']})


            data = []
            for index, row in df1.iterrows():
                print (row[3])
                temp_data = {"state":index , "mean":round(row[0],0),"max":round(row[1],0),"min":round(row[2],0),"sum":round(row[3],0)}
                data.append(temp_data)
            return (render_template('index.html' ,data=data))
    return """<!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """



if __name__ == "__main__":
    app.run( host = "10.102.112.150", port=80,threaded = True)  ## Make sure you enter correct ip address 
