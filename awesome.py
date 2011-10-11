# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)

import data
data.init()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/list")
def list():
    return render_template('list.html', projects = data.retrieve_projects()[1])

@app.route("/techniques")
def techniques(tech = None):
    return render_template('techniques.html', tech = data.retrieve_techniques()[1])

@app.route("/project/<id>")
def project(id):
    return render_template('project.html', project = data.retrieve_projects(search=str(id), search_fields = ["project_no"])[1])


if __name__ == "__main__":
    app.run(debug = True)

