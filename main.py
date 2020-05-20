import os
from concurrent.futures import ThreadPoolExecutor
from flask import flash, render_template, request, redirect, abort,send_file,Flask
from werkzeug.utils import secure_filename
import speech_recognition as sr
#from app import app

app = Flask(__name__)

UPLOADED_IMAGES_DEST = 'file'
app.config['UPLOADED_IMAGES_DEST'] = UPLOADED_IMAGES_DEST
app.config['SECRET_KEY'] = 'thisisasecret'

app.config['MAX_CONTEXT_LENGTH'] = 30 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['wav'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('original.html')

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))
        text = "File uploaded Successfully....."
    else:
        text = "Your file was not a Audio file or not audio.wav"
    return render_template('predict.html', prediction = text)


    #pool = ThreadPoolExecutor(max_workers=1)
    #os.remove(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))
    #flash('File(s) successfully uploaded')
    #pool.shutdown(wait=True)



@app.route('/view_file', methods=['GET','POST'])
def view_file():
    file_name = 'file/audio.wav'
    speech = sr.AudioFile(file_name)
    recog = sr.Recognizer()
    with speech as filename:
        recog.adjust_for_ambient_noise(filename)
        audio = recog.record(filename)
        try:
            text = recog.recognize_google(audio)
            text = ("{}".format(text))
        except:
             text = ("Sorry could not recognize your voice")
    return render_template('view.html', prediction = text)


#@app.route('/download_file', methods=['GET','POST'])
#def download_file():
    #p = 'uploads/images/audio.wav'
    #return send_file(p, as_attachment=True)
    #text = 'File downloaded'
    #return render_template('download.html', prediction = text)



@app.route('/delete_file', methods=['GET','POST'])
def delete_file():
    file = 'audio.wav'
    location = "file"
    path = os.path.join(location, file)
    try:
        os.remove(os.path.join(app.config['UPLOADED_IMAGES_DEST'], file))
        #os.remove(path)
        #for root, dirs, files in os.walk('uploads/images'):
            #for file in files:
                #os.remove(os.path.join(root))
        text = "File removed successfully"
    except OSError as error:
        text = error,"File path can not be removed"
    return render_template('delete.html', prediction = text)


if __name__ == '__main__':
    app.run(debug=True)
