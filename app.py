from flask import Flask

app = Flask(__name__)

UPLOADED_IMAGES_DEST = 'uploads/images'
app.config['UPLOADED_IMAGES_DEST'] = UPLOADED_IMAGES_DEST
app.config['SECRET_KEY'] = 'thisisasecret'

app.config['MAX_CONTEXT_LENGTH'] = 30 * 1024 * 1024
