# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)

import data
data.init()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/search", methods = ['GET'])
def search():
    sokning = request.args.get('search')
    sorting = request.args.get('sort')
    cats = request.args.get('categories')
    technique = request.args.get('technique')
    by_sorting = request.args.get('by_sorting')
    projects = data.retrieve_projects()[1]
    if sokning != None:
        sokning = sokning.encode('ascii')
        sorting = sorting.encode('ascii')
        cats = cats.encode('ascii')
        technique = technique.encode('ascii')
        by_sorting = by_sorting.encode('ascii')
        if technique == 'Choose a technique':
            technique = None
        return render_template('search.html', proj_hit = data.retrieve_projects(search = sokning, search_fields = [cats], techniques = technique, sort_order = sorting, sort_by = by_sorting)[1])
    else:
        return render_template('search.html', projects = data.retrieve_projects()[1])

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

