from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils  import secure_filename
import os
from tensorflow.keras.models import load_model



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'

rslt = -1
file = ""

@app.route('/')
def index():    
    return render_template('index.html')


@app.route('/result',methods=['POST']) 
def result():
    global rslt,file
    if request.method=='POST':
        print('pd1')
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        pt = os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
        
        file = filename

        
        rslt = calc(pt)
        
        return render_template('result.html',res=rslt,filep=file)
    else:
        return "else"


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def calc(pth):
    
    mod = load_model('model/Roadss_model.h5')
    X = cv2.imread(pth,cv2.IMREAD_COLOR)
    X = cv2.resize(X,(256,256))

    X = np.array(X)
    X = np.expand_dims(X, axis=0)

    y_pred = np.round(model.predict(X))

    return y_pred[0][0]