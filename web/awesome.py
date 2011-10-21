# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)

import data, logging

#Entering the awesome homepage
@app.route("/")
def home():
    data.init()
    log('Entering the awesome homepage!')
    return render_template('start.html')

#List all projects (sort by project name as standard) and search
@app.route("/list", methods = ['GET'])
def list():
    data.init()
    log('Searching for a project')
    searchStr = request.args.get('search')
    sorting = request.args.get('sort')
    cats = request.args.getlist('categories')
    by_sorting = request.args.get('by_sort')
    technique = request.args.getlist('check_tech')

    if searchStr != None:
        searchStr = searchStr.encode('utf-8')
    if by_sorting == None:
        by_sorting = 'project_name'

    proj_hit = data.retrieve_projects(search = searchStr, search_fields = cats, techniques = technique, sort_order = sorting, sort_by = by_sorting)[1]

    if len(proj_hit) == 0:
        return render_template('list.html', fail = 'No project found')

    return render_template('list.html', proj_hit = data.retrieve_projects(search = searchStr, search_fields = cats, techniques = technique, sort_order = sorting, sort_by = by_sorting)[1])

@app.route("/techniques")
def techniques():
    data.init()
    log('Displaying all techniques')
    return render_template('techniques.html', techniques = data.retrieve_technique_stats()[1])

@app.route("/project/<id>")
def project(id):
    data.init()
    id = id.encode('utf-8')
    log('Displaying project ' + str(id))
    project = data.retrieve_projects(search = str(id), search_fields = ['project_no'])[1]
    if project == []:
        return render_template('no_result.html')
    
    return render_template('project.html', project = data.retrieve_projects(search = str(id), search_fields = ['project_no'])[1])

@app.errorhandler(404)
def not_found(error):
    log('404 error')
    return render_template('page_not_found.html'), 404

def log(logga):
    logging.basicConfig(filename='awesome.log',level=logging.DEBUG)
    logging.debug(logga)


if __name__ == "__main__":
    app.run(debug = True)

