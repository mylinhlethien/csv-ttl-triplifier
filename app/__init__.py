from flask import Flask, render_template, request, flash, redirect, url_for
import os
#import sys
from serializer import processCSV, serializeToTurtle
import pandas as pd


def create_app():
    app = Flask(__name__)
    app.secret_key = 'thisisasecretforthesession'

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

        # Parameters
        result = request.form
        delimiter = result.getlist('separator')[0]
        # set titleLine to None if no titleLine
        if len(result.getlist('title_line')) == 0:
            titleLine = None  # None
        else:
            titleLine = int(result.getlist('title_line')[0])
        # set withTitles to True or False
        if len(result.getlist('withTitles')) == 0:
            withTitles = False
        else:
            withTitles = result.getlist('withTitles')[0]  # True
        # set dataLine to None if no firstLine
        if len(result.getlist('first_line')) == 0:
            dataLine = None  # None
        else:
            dataLine = int(result.getlist('first_line')[0])

        # set lasrLine to None if = 0
        if len(result.getlist('last_line')) == 0:
            lastLine = None  # None
        else:
            lastLine = int(result.getlist('last_line')[0])

        print(withTitles, delimiter, titleLine, dataLine, lastLine)

        # Manage file paths
        filename, file_extension = os.path.splitext(
            os.path.join("test", uploaded_file.filename))
        path = os.path.join("test", uploaded_file.filename)
        # print(path)
        turtlepath = filename + ".ttl"
        # print(turtlepath)

        # call the functions from serializer.py
        try:
            title, values = processCSV(
                path, withTitles=withTitles, delimiter=delimiter, titleLine=titleLine, dataLine=dataLine)

            serializeToTurtle(turtlepath, values,
                              elementTitlePredicateName=title)
        except:
            flash("Please double check your parameters.")
            return redirect("/")

        # to read csv file named "samplee"
        csv = pd.read_csv(path, delimiter=delimiter)

        # convert to String
        csvString = csv.to_string()

        # convert .ttl file to string
        with open(turtlepath, 'r') as file:
            turtleData = file.read()

        # redirection to second page to display results
        return render_template("results.html", csvString=csvString, turtleData=turtleData, path=path, turtlepath=turtlepath)

    return app
