# -*- coding: cp1252 -*-
import csv

projects = []
unicode_projects = []
list_techniques = []

############################ INIT()######################################
def init():
    #READ IN THE CSV FILE
    global projects
    global unicode_projects
    projects = csv.DictReader(open("data.csv"))   
    unicode_projects = []

    #REDO THE VALUES TO UNICODE AND ADD THEM TO THE LIST UNICODE_PROJECTS
    for dicts in projects:
        temp_dict = {} 
        for value in dicts:
            #IF PROJECT_NO IS A DIGIT, KEEP IT AS AN DIGIT (AKA NOT UNICODE)
            if value.find("project_no") != -1 and dicts[value].isdigit():
                temp_dict[unicode(value, "utf-8")] = int(dicts[value])
            #IF VALUE IN DICT IS ANYTHING ELSE BUT A DIGIT, ENCODE TO UNICODE
            else:
                temp_dict[unicode(value, "utf-8")] = unicode(dicts[value], "utf-8")
        #ADD THE DICTIONARIES TO THE LIST UNICODE_PROJECTS
        unicode_projects.append(temp_dict)
    
    #REDO TECHNIQUES_USED TO A COMMA-SEPARATED LIST
    for dicts in unicode_projects:
        temp = dicts['techniques_used'].split(',')
        list_techniques = temp
        for i in temp:
            if i not in list_techniques and len(i) > 0:
                list_techniques.append(i)
            temp2 = dicts['techniques_used']
            if len(temp2) < 1:
                list_techniques.remove(temp2)
        list_techniques.sort()
        dicts['techniques_used'] = list_techniques
        errcode = 0

    return unicode_projects


############################### PROJECT_COUNT() ##############################
def project_count():   

#CHECK IF UNICODE_PROJECTS IS EMPTY OR NOT
    if len(unicode_projects) == 0:
        errcode = 1
        return (errcode, len(unicode_projects))
    else:
        errcode = 0
        return (errcode, len(unicode_projects))

############################## LOOKUP_PROJECT(ID) ###########################
def lookup_project(id):

#CHECK IF UNICODE_PROJECTS IS EMPTY OR NOT
    if len(unicode_projects) == 0:
        errcode = 1
        return errcode, None
#IF ID IS BIGGER THAN THE AMOUNT OF PROJECTS, RETURN AN ERROR
    elif id > len(unicode_projects):
        errcode = 2
        return errcode, None
#RETURN THE PROJECT
    else:
        for dicts in unicode_projects:
            if dicts['project_no'] == int(id):
                errcode = 0
                return errcode, dicts

############################# RETRIEVE_TECHNIQUES() ##########################
def retrieve_techniques():
#MAKE A LIST WHERE ALL THE TECHNIQUES WILL GO
    dict_tec_lista = []

    for dicts in unicode_projects:
        temp = dicts['techniques_used']
#FIND ALL UNIQUE TECHNIQUES AND ADD THEM TO DICT_TEC_LISTA
        for i in temp:
            if i not in dict_tec_lista and len(i) > 0:
                dict_tec_lista.append(i)
    dict_tec_lista.sort()
    errcode = 0
    return errcode, dict_tec_lista

############################# RETRIEVE_PROJECTS ################################
def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
#MAKE A LIST WHERE THE SEARCHRESULTS WILL GO
    return_lista = []

#GET ALL PROJECTS IN UNICODE_PROJECTS   
    for proj in unicode_projects:
        add = False

#CHECK IF THE USER WROTE SOMETHING IN SEARCH OR SEARCH_FIELDS    
        if search or search_fields:
            for field in search_fields:
                data = proj[field]
                if isinstance(data, int):
                    data = str(data)

                if data.lower().find(unicode(search, 'utf-8').lower()) != -1:
                    add = True
        else:
            add = True

#CHECK IF THE USER WROTE IN TECHNIQUES_USED
        if add and techniques:
            for tech in techniques:
                if not tech in proj['techniques_used']:
                    add = False

        if add:
            return_lista.append(proj)

#CHECK HOW THE USER WANT TO SORT
    return_lista.sort(key=lambda val: val[sort_by])

#DESC OR ASC    
    if sort_order == 'desc':
        return_lista.reverse()

    errcode = 0
    return errcode, return_lista

##################################### RETRIEVE_TECHNIQUE_STATS() ###################
def retrieve_technique_stats():
#A LOT OF BEAUTIFUL VARIABLES
    temp_dict = {}
    proj_dict = {}
    asd_dict = {}
    dsa_list = []

#CHECK WHICH TECHNIQUES THAT WERE USED  
    for tech in retrieve_techniques()[1]:
        x = 0
        temp_list = []
        temp_dict = {'name': str(tech)}

#CHECK HOW MANY TIMES THAT TECHNIQUE WAS USED     
        for dicts in unicode_projects:
            if tech in dicts['techniques_used']:
                x += 1
                asd_dict['id'] = dicts['project_no']
                asd_dict['name'] = dicts['project_name']
                temp_list.append(asd_dict)
                asd_dict = {}
        temp_dict['count'] = x

#SORT BY THE PROJECTS NAME
        temp_list = sorted(temp_list, key=lambda asd_dict: asd_dict['name'])

        temp_dict['projects'] = temp_list
        dsa_list.append(temp_dict)
    errcode = 0
    return errcode, dsa_list
        
    


