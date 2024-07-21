import os
import imghdr
import config as c
import functions as f
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

recognizer = f.get_recognizer(c.URL, c.FILE_NAME)
project_root = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, c.DOWNLOADS_FOLDER)


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload")


@app.route("/")
def home():
    return "This is an API for gesture recognition!"


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            if not imghdr.what(file):
                return jsonify({"error": "Only image files are allowed!"}), 400

            save_directory = app.config['UPLOAD_FOLDER']
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            filename = secure_filename(file.filename)
            file_path = os.path.join(save_directory, filename)
            file.save(file_path)

            return redirect(url_for('recognize_gesture', filename=filename))
    return render_template('upload.html', form=form)


@app.route('/recognize-gesture')
def recognize_gesture():

    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "No image file provided!"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        gesture_name = f.get_classification_result_from_path(file_path, recognizer)
        return jsonify({"Recognized gesture": gesture_name}), 200
    except Exception as e:
        return jsonify({"error": f"Caught an exception: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)