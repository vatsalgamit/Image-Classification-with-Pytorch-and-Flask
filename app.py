from flask import Flask, request, jsonify, render_template
from torch_utils import transform_image,get_prediction
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

MY_FOLDER = os.path.join('static', 'uploads')
UPLOAD_FOLDER = MY_FOLDER

ALLOWED_EXTENTIONS = {'png','jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS

@app.route('/',methods = ['GET','POS'])
def index():
    return render_template('index.html')

@app.route('/predict',methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        if file is None or file.filename == "":
            return jsonify({'error':'no-file'})
        if not allowed_file(file.filename):
            return jsonify({'error':"format not supported"})
        
        try:
            file.seek(0)
            image_bytes  = file.read()
            tensor = transform_image(image_bytes)
            prediction = get_prediction(tensor)
            data = {'prediction':prediction.item()}
            return render_template("index.html", prediction = data['prediction'],file_path = file_path)
        except:
            return jsonify({'error':'error during prediction'})


if __name__ == '__main__':
    app.debug = True
    app.run()