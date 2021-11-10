from flask import Flask, render_template, request, redirect, url_for
import os
#import sys
from serializer import processCSV, serializeToTurtle


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def homepage():
        return render_template("homepage.html")

    @app.route('/convertFile', methods=['POST'])
    def convertFile():
        # save file into the "test" folder
        if request.method == 'POST':
            uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join("test", uploaded_file.filename))

        # parameters
        result = request.form
        delimiter = result.getlist('separator')[0]
        dataLine = result.getlist('first_line')[0]
        # set titleLine to 0 if no titleLine
        if len(result.getlist('title_line')) == 0:
            titleLine = 0
        else:
            titleLine = int(result.getlist('title_line')[0])
        # set withTitles to True or False
        if len(result.getlist('withTitles')) == 0:
            withTitles = False
        else:
            withTitles = result.getlist('withTitles')[0]

        #print(withTitles, delimiter, titleLine, dataLine)

        # Manage file paths
        filename, file_extension = os.path.splitext(
            os.path.join("test", uploaded_file.filename))
        path = os.path.join("test", uploaded_file.filename)
        # print(path)
        turtlepath = filename + ".ttl"
        # print(turtlepath)

        # call the functions from serializer.py
        title, values = processCSV(path, withTitles=withTitles,
                                   delimiter=delimiter, titleLine=titleLine, dataLine=int(dataLine))

        serializeToTurtle(turtlepath, values,
                          elementTitlePredicateName=title)

        return "<p>SUCCESS! You will find the output file in the folder \"test\"</p>"

    return app
