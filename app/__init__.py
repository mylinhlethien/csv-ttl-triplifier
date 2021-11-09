from flask import Flask, render_template, request, redirect, url_for
import os
import sys


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def homepage():
        return render_template("homepage.html")

    # @app.route("/uploads/<filename>")
    # def uploaded_file(filename):
    #    filename_processed = 'processed' + '-' + filename
    #    return send_from_directory("downloads", filename, as_attachment=True, attachment_filename=filename_processed)

    @app.route('/convertFile', methods=['POST'])
    def convertFile():
        if request.method == 'POST':
            uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join("test", uploaded_file.filename))
        # return redirect(url_for('uploaded_file', filename=filename))

        result = request.form
        print(result, file=sys.stderr)

        return "<p>SUCCESS</p>"

    return app
