# show http requests, and the things showing up on the website
# from math import dist
# import pandas as pd
from requests import request
import seaborn as sns
from ast import If
from email.policy import default
from operator import itemgetter
from re import search
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import BioInfo, Student
from .forms import CreateNewProfile, EditProfile, FileUpload, testform
# from django.views import View
from django.core.files.storage import FileSystemStorage
# from io import BytesIO
from django.template.loader import get_template
from django import template
import os
from django.contrib import messages
import csv
from datetime import datetime
from django.core.exceptions import PermissionDenied
import collections

SUB_CATEGORY = {
    'Process': ['Automation & Job Scheduling', 'Process efficiency', 'Version Controlling',
            'Project Management', 'Space Management'],
    'NLP': ['Spatical Statistics', 'LSTM', 'CNN', 'Autoencoder', 'Transformer', 'BERT', 'TF-IDF',
            'Word Embedding', 'Sentiment Analysis', 'Latent Dirichlet Allocation', 'Topic Modelling',
            'Named Entity Recognition']
}
LOCATION_CHOICES = [
    ('Columbia, MD (HQ)', 'Columbia, MD (HQ)'),
    ('New York, NY', 'New York, NY'),
    ('Denver, CO', 'Denver, CO'),
    ('India', 'India'),
    ('Remote', 'Remote')
]

DOMAIN_CHOICES = [
        ('Sales & Marketing', 'Sales & Marketing'),
        ('Supply Chain', 'Supply Chain'),
        ('Pricing', 'Pricing'),
        ('Product', 'Product'),
        ('Finance', 'Finance'),
        ('IoT', 'IoT'),
        ('HR', 'HR'),
        ('Real Estate', 'Real Estate'),
        ('Manufacturing', 'Manufacturing'),
        ('Customer Experience', 'Customer Experience'),
]

SKILL_CHOICES = [
    # Data Engineering
    ('Data Governence', 'Data Governence'),
    ('Data Wrangling', 'Data Wrangling'),
    ('Data / Network Security', 'Data / Network Security'),
    # BI
    ('Data Visualization', 'Data Visualization'),
    ('Business Intelligence', 'Business Intelligence'),
    ('Application Architecture', 'Application Architecture'),
    # Process Infrastructure
    ('Automation & Job Scheduling', 'Automation & Job Scheduling'),
    ('Process efficiency', 'Process efficiency'),
    ('Version Controlling', 'Version Controlling'),
    ('Project Management', 'Project Management'),
    ('Space Management', 'Space Management'),
    # Analytics Application
    ('Campaign Design/Execution', 'Campaign Design/Execution'),
    ('Operation', 'Operation'),
    ('Personalization', 'Personalization'),
    ('Customer Segmentation and Insights', 'Customer Segmentation and Insights'),
    ('LTV', 'LTV'),
    ('Unit Testing / QA', 'Unit Testing / QA'),
    ('Digital Analytics', 'Digital Analytics'),
    ('Factor Analysis', 'Factor Analysis'),
    ('Insight Generation', 'Insight Generation'),
    ('Outlier Detection Algorithms', 'Outlier Detection Algorithms'),
    ('Experimental Design', 'Experimental Design'),
    ('MMM', 'MMM'),
    ('MTA', 'MTA'),
    ('Optimization', 'Optimization'),
    ('Simulation', 'Simulation'),
    ('Search Engine Optimization', 'Search Engine Optimization'),
    # Statistics / ML
    ('A/B Testing', 'A/B Testing'),
    ('Ada Boost', 'Ada Boost'),
    ('Bayesian Modelling', 'Bayesian Modelling'),
    ('Causal Inference', 'Causal Inference'),
    ('Clustering Models', 'Clustering Models'),
    ('Decision Trees', 'Decision Trees'),
    ('KNN', 'KNN'),
    ('Random Forest', 'Random Forest'),
    ('XGBoost', 'XGBoost'),
    ('Survival analysis', 'Survival analysis'),
    ('Time Series Analysis', 'Time Series Analysis'),
    ('Discriminant Analysis', 'Discriminant Analysis'),
    ('SVM', 'SVM'),
    ('PCA', 'PCA'),
    ('Logistic Regression', 'Logistic Regression'),
    ('Linear Regression', 'Linear Regression'),
    ('Multi-levels Stacking', 'Multi-levels Stacking'),
    ('Spatial Statistics', 'Spatial Statistics'),
    # Deep Learning / NLP
    ('LSTM', 'LSTM'),
    ('CNN', 'CNN'),
    ('Autoencoder', 'Autoencoder'),
    ('Transformer', 'Transformer'),
    ('BERT', 'BERT'),
    ('TF-IDF', 'TF-IDF'),
    ('Word Embedding', 'Word Embedding'),
    ('Sentiment analysis', 'Sentiment analysis'),
    ('Latent Dirichlet Allocation', 'Latent Dirichlet Allocation'),
    ('Topic Modelling', 'Topic Modelling'),
    ('Named Entity Recognition', 'Named Entity Recognition'),
]


INDUSTRIES_CHOICES = [
    ('Retail', 'Retail'),
    ('Grocery', "Grocery"),
    ('Financial Services', "Financial Services"),
    ('Transportation', 'Transportation'), 
    ('Healthcare', "Healthcare"),
    ('B2B', 'B2B'),
    ('Construction', 'Construction'),
    ('Manufacturing', 'Manufacturing'),
    ('Utilities', 'Utilities'),
    ('Insurance', 'Insurance'),
    ('Communication Services', 'Communication Services'),
    ('E Commerce', 'E Commerce'),
    ('Educational Services', 'Educational Services'),
    ('Energy', 'Energy'),
    ('Hospitality', 'Hospitality'),
    ('Information Technology', 'Information Technology'),
    ('Life Sciences', 'Life Sciences'),
    ('Real Estate', 'Real Estate'),
    ('Technology', 'Technology'),
]

CLIENT_CHOICES = [
    ('AARP', 'AARP'),
    ('Acorns', "Acorns"),
    ('CVS', "CVS"),
    ('Grammarly', 'Grammarly'), 
    ('HGV', "HGV"),
    ('Marriott MTA', 'Marriott MTA'),
    ('Sunovion', 'Sunovion'),
    ('Visa', 'Visa'),
    ('Walmart', 'Walmart')
]

TECHNICUQE_CHOICES = [
    # CLOUD COMPUTING SERVICES
    ('AWS', 'AWS'),
    ('Azure', 'Azure'),
    ('GCP', 'GCP'),
    ('Snowflake', 'Snowflake'),
    ('Databricks', 'Databricks'),
    # PROGRAMMING LANGUAGE
    ('Python', 'Python'),
    ('R', 'R'),
    ('C/C++', 'C/C++'),
    ('Java', 'Java'),
    ('SAS', 'SAS'),
    ('SCALA', 'SCALA'),
    ('MATLAB', 'MATLAB'),
    # DATA VISUALIZATION
    ('Tableau', 'Tableau'),
    ('Power BI', 'Power BI'),
    ('Dashboard Design', 'Dashboard Design'),
    ('Plotly', 'Plotly'),
    ('Streamlit', 'Streamlit'),
    # DATABASE
    ('SQL', "SQL"),
    ('MySQL', 'MySQL'),
    ('MongoDB', 'MongoDB'),
    ('Adobe Analytics', 'Adobe Analytics'),
    # Other
    ('Django', 'Django'),
    ('Docker', 'Docker'),
    ('Linux', 'Linux'),
    ('Git', 'Git'),
    ('PyTorch', 'PyTorch'),
    ('Tensorflow', 'Tensorflow'),
    ('Keras', 'Keras'),
]

POSITION_CHOICES = [
    ('Associate Data Scientist/Intern', 'Associate Data Scientist/Intern'),
    ('Associate Data Scientist, All-Star', 'Associate Data Scientist, All-Star'),
    ('Lead Data Scientist', 'Lead Data Scientist'),
    ('Senior Manager, Data Science', 'Senior Manager, Data Science'),
    ('Director, Data Science', 'Director, Data Science'),
    ('Senior Data Scientist', 'Senior Data Scientist'),
    ('Data Scientist', 'Associate Director, Data Science'),
    ('Manager, Data Science', 'Manager, Data Science '),
    ('Senior Director, Data Science', 'Senior Director, Data Science'),
    ('Marketing Scientist, All-Star', 'Marketing Scientist, All-Star'),
    ('Senior Marketing Scientist', 'Senior Marketing Scientist'),
    ('Associate Marketing Scientist, All-Star', 'Associate Marketing Scientist, All-Star'),
    ('VP, Data Science', 'VP, Data Science'),
    ('SVP, Data Science', 'SVP, Data Science')
]

SKILL_RUBRIC = {
    "1" : "Unfamiliar",
    "2" : "Novice",
    "3" : "Proficient",
    "4" : "Advanced",
    "5" : "Expert"
}

SKILL_RUBRIC_MAIN = {
    "1" : "1 - Unfamiliar",
    "2" : "2 - Novice",
    "3" : "3 - Proficient",
    "4" : "4 - Advanced",
    "5" : "5 - Expert"
}

EXPERIENCE_RUBRIC = {
    "1" : "<1 YOE",
    "2" : "1-3 YOE",
    "3" : "4-5 YOE",
    "4" : "5-10 YOE",
    "5" : ">10 YOE" 
}

EXPERIENCE_RUBRIC_MAIN = {
    "1" : "<1 Year",
    "2" : "1-3 Year",
    "3" : "4-5 Year",
    "4" : "5-10 Year",
    "5" : ">10 Year" 
}

ADJUST_EXP = {
    "<1YOE" : "<1 Year",
    "1-3YOE" : "1-3 Year",
    "4-5YOE" : "4-5 Year",
    "5-10YOE" : "5-10 Year",
    ">10YOE" : ">10 Year"    
}

REVERSE_RUBRIC = {
    "Unfamiliar" : "1",
    "Novice" : "2",
    "Proficient" : "3",
    "Advanced" : "4",
    "Expert" : "5",
    "<1" : "1",
    "1-3" : "2",
    "4-5" : "3",
    "5-10" : "4",
    ">10" : "5",
    "<1YOE" : "1",
    "1-3YOE" : "2",
    "4-5YOE" : "3",
    "5-10YOE" : "4",
    ">10YOE" : "5"    
}

DOMAIN_MODIFICATION = {
    "Unfamiliar" : "<1 Year",
    "Novice" : "1-3 Year",
    "Proficient" : "4-5 Year",
    "Advanced" : "5-10 Year",
    "Expert" : ">10 Year",
}

tmp1 = []
for a, _ in SKILL_CHOICES:
    tmp1.append(a)

tmp2 = []
for a, _ in INDUSTRIES_CHOICES:
    tmp2.append(a)

tmp3 = []
for a, _ in TECHNICUQE_CHOICES:
    tmp3.append(a)

tmp4 = []
for a, _ in DOMAIN_CHOICES:
    tmp4.append(a)

def export(response):
    if response.user.first_name != 'Zach':
        raise PermissionDenied("Custom message")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tct{}.csv"'.format(datetime.now().strftime("%Y%m%d"))

    writer = csv.writer(response)
    writer.writerow(['name','email', 'position', 'location', 'skill', 'technique', 
                        'industry', 'business_domain', 'university', 'major', 'degree',
                        'university2', 'major2', 'degree2', 'university3', 'major3', 'degree3',
                        'intro', 'date_modified'])

    users = BioInfo.objects.all().values_list('name','email', 'position', 'location', 'skill', 'technique', 
                                            'industry', 'business_domain', 'university', 'major', 'degree',
                                            'university2', 'major2', 'degree2', 'university3', 'major3', 'degree3',
                                            'intro', 'date_modified')
    for user in users:
        writer.writerow(user)

    return response

def sub_cate_search(people, cate_name):
    result = []
    if cate_name not in SUB_CATEGORY:
        return result
    for person in people:
        for val in SUB_CATEGORY[cate_name]:
            if val in person.skill:
                result.append(person)
                break
    return result

def test(request):
    people = BioInfo.objects.all()
    sub_cate = {"Process":['Automation & Job Scheduling', 'Process efficiency', 'Version Controlling',
                           'Project Management', 'Space Management']}
    sub_cate = ['Automation & Job Scheduling', 'Process efficiency', 'Version Controlling',
            'Project Management', 'Space Management']
    result = []
    for person in people:
        for cate in sub_cate:
            if cate in person.skill:
                result.append(person)
                break
    print(len(result))
    return render(request, 'bios/test.html', {"result":result})


def index(response, name):
    # print(response.user.first_name)
    # user in our database
    user_db = []
    for person in BioInfo.objects.all():
        if person.email not in user_db:
            user_db.append(person.email)
    # in_db
    # name_str = response.user.first_name.replace(' ', '_') + '_' + response.user.last_name.replace(' ', '_')
    email_str = str(response.user)
    in_db = 1 if email_str.lower() in user_db else 0
    item = BioInfo.objects.get(name=name)
    try:
        item_file = Student.objects.get(name=name)
    except:
        item_file = None

    # application table
    app_tmp = item.application
    app_dict = {}
    for s in app_tmp.split(','):
        if '(' in s:
            idx = s.rfind('(')
            print(s, idx, s[:idx-1].strip())
            app_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s.strip()[idx+1:-1]]
        else:
            app_dict[s] = "1"
    app_dict = sorted(app_dict.items(), key=lambda x:x[1], reverse=True)
    app_dict = {k:SKILL_RUBRIC_MAIN[v] for k, v in app_dict}

    # ds_skill table
    skill_tmp = item.ds_skill
    skill_dict = {}
    for s in skill_tmp.split(','):
        if '(' in s:
            idx = s.rfind('(')
            skill_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s.strip()[idx+1:-1]]
        else:
            skill_dict[s] = "1"
    skill_dict = sorted(skill_dict.items(), key=lambda x:x[1], reverse=True)
    skill_dict = {k:SKILL_RUBRIC_MAIN[v] for k, v in skill_dict}

    
    # program_skill table
    prog_skill_tmp = item.program_skill
    prog_skill_dict = {}
    for s in prog_skill_tmp.split(','):
        if '(' in s:
            idx = s.rfind('(')
            prog_skill_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s.strip()[idx+1:-1]]
        else:
            prog_skill_dict[s] = "1"
    prog_skill_dict = sorted(prog_skill_dict.items(), key=lambda x:x[1], reverse=True)
    prog_skill_dict = {k:SKILL_RUBRIC_MAIN[v] for k, v in prog_skill_dict}

    # techstack table
    techstack_tmp = item.tech_stack
    techstack_dict = {}
    for s in techstack_tmp.split(','):
        if '(' in s:
            idx = s.rfind('(')
            techstack_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s.strip()[idx+1:-1]]
        else:
            techstack_dict[s] = "1"
    techstack_dict = sorted(techstack_dict.items(), key=lambda x:x[1], reverse=True)
    techstack_dict = {k:SKILL_RUBRIC_MAIN[v] for k, v in techstack_dict}

    # industry experience table
    industry_tmp = item.industry
    industry_dict = {}
    for s in industry_tmp.split(','):
        if '(' in s:
            idx = s.index('(')
            industry_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s.split(' ')[-2][1:]]
        else:
            industry_dict[s] = "1"
    industry_dict = sorted(industry_dict.items(), key=lambda x:x[1], reverse=True)
    industry_dict = {k:EXPERIENCE_RUBRIC_MAIN[v] for k, v in industry_dict}

    # domain skill table
    domain_tmp = item.business_domain
    domain_dict = {}
    if domain_tmp:
        for s in domain_tmp.split(','):
            if '(' in s:
                idx = s.index('(')
                # print(s[idx+1:-1].strip())
                domain_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s[idx+1:-1].strip()]
            else:
                domain_dict[s] = "1"
        domain_dict = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
        domain_dict = {k:EXPERIENCE_RUBRIC_MAIN[v] for k, v in domain_dict}

    # if link existed
    tmp_file_name = "{}.pdf".format(item.name)
    if tmp_file_name in os.listdir('bios/static/media/bio_ppt') or tmp_file_name.replace('(','').replace(')', '') in os.listdir('bios/static/media/bio_ppt'):
        bio_obj = 1
    else:
        bio_obj = 0
    
    # preprocess the user name
    user_first_name = response.user.first_name.replace(' ', '_')
    user_last_name = response.user.last_name.replace(' ', '_')
    return render(response, 'bios/bio-info.html', {"people":item,
                                                   "skill":skill_dict,
                                                   "application": app_dict,
                                                   "program_skill":prog_skill_dict,
                                                   "techstack":techstack_dict,
                                                   "industry":industry_dict,
                                                   "domain":domain_dict,
                                                   "file":item_file,
                                                   "bio_obj": bio_obj,
                                                   'in_db': in_db,
                                                   'user_first': user_first_name,
                                                   'user_last': user_last_name,
                                                   })
def distinct_skill():
    application, ds_skill, program_skill, techstack = [], [], [], []
    for person in BioInfo.objects.all():
        app_lst = person.application.split(',')
        for apps in app_lst:
            apps = apps.strip()
            if apps in application or not apps or apps == 'N/A' or 'N/A' in apps:
                continue
            if "(" in apps:
                if ' '.join(apps.split(' ')[:-1]) not in application:
                    application.append(' '.join(apps.split(' ')[:-1]))
            else:
                application.append(apps)

        ds_lst = person.ds_skill.split(',')
        for ds in ds_lst:
            ds = ds.strip()
            if ds in ds_skill or not ds or ds == 'N/A' or 'N/A' in ds:
                continue
            if "(" in ds:
                if ' '.join(ds.split(' ')[:-1]) not in ds_skill:
                    ds_skill.append(' '.join(ds.split(' ')[:-1]))
            else:
                ds_skill.append(ds)

        prog_lst = person.program_skill.split(',')
        for prog in prog_lst:
            prog = prog.strip()
            if prog in program_skill or not prog or prog == 'N/A' or 'N/A' in prog:
                continue
            if "(" in prog:
                if ' '.join(prog.split(' ')[:-1]) not in program_skill:
                    program_skill.append(' '.join(prog.split(' ')[:-1]))
            else:
                program_skill.append(prog)

        tech_lst = person.tech_stack.split(',')
        for tech in tech_lst:
            tech = tech.strip()
            if tech in techstack or not tech or tech == 'N/A' or 'N/A' in tech:
                continue
            if "(" in tech:
                if ' '.join(tech.split(' ')[:-1]) not in techstack:
                    techstack.append(' '.join(tech.split(' ')[:-1]))
            else:
                techstack.append(tech)
    return application, ds_skill, program_skill, techstack

def distinct_features():
    skill_res, industry_res, tech_res, domain_res= [], [], [], []
    university_res, major_res, degree_res = [], [], []
    people_all = BioInfo.objects.all()
    # loop thru all the people
    for person in people_all:
        skill_lst = person.skill.split(',')
        industry_lst = person.industry.split(',')
        tech_lst = person.technique.split(',')
        if person.business_domain:
            domain_lst = person.business_domain.split(',')
        else:
            domain_lst = []
        university_lst = person.university.split(';')
        university_lst2 = person.university2.split(';')
        university_lst3 = person.university3.split(';')
        major_lst = person.major.split(',')
        major_lst2 = person.major2.split(',')
        major_lst3 = person.major3.split(',')
        # deal with skill
        for skill in skill_lst:
            skill = skill.strip()
            if skill in skill_res or not skill or skill == 'N/A' or 'N/A' in skill:
                continue
            if "(" in skill:
                if ' '.join(skill.split(' ')[:-1]) not in skill_res:
                    skill_res.append(' '.join(skill.split(' ')[:-1]))
            else:
                skill_res.append(skill)

        # deal with industry
        for industry in industry_lst:
            industry = industry.strip()
            if industry in industry_res or not industry or industry == 'N/A' or 'N/A' in industry: 
                continue
            if "(" in industry:
                if ' '.join(industry.split(' ')[:-2]) not in industry_res:
                    industry_res.append(' '.join(industry.split(' ')[:-2]))
            else:
                industry_res.append(industry)
        
        # deal with technology
        for tech in tech_lst:
            tech = tech.strip()
            if tech in tech_res or not tech or tech == "N/A" or "N/A" in tech:
                continue
            if "(" in tech:
                if ' '.join(tech.split(' ')[:-1]) not in tech_res:
                    tech_res.append(' '.join(tech.split(' ')[:-1]))
            else:
                tech_res.append(tech)

        # deal with business domain
        for domain in domain_lst:
            domain = domain.strip()
            if domain in domain_res or not domain or domain == "N/A" or "N/A" in domain:
                continue
            if "(" in domain:
                if ' '.join(domain.split(' ')[:-1]) not in domain_res:
                    domain_res.append(' '.join(domain.split(' ')[:-1]))
            else:
                domain_res.append(domain)

        # deal with university
        for uni in university_lst:
            uni = uni.strip()
            if uni in university_res or not uni or uni == "N/A" or "N/A" in uni:
                continue
            uni_section = uni.split(',')
            if uni_section[0] not in university_res:
                university_res.append(uni_section[0])

        # deal with university
        for uni in university_lst2:
            uni = uni.strip()
            if uni in university_res or not uni or uni == "N/A" or "N/A" in uni:
                continue
            uni_section = uni.split(',')
            if uni_section[0] not in university_res:
                university_res.append(uni_section[0])

        for uni in university_lst3:
            uni = uni.strip()
            if uni in university_res or not uni or uni == "N/A" or "N/A" in uni:
                continue
            uni_section = uni.split(',')
            if uni_section[0] not in university_res:
                university_res.append(uni_section[0])
        
        # deal with major
        for major in major_lst:
            major = major.strip()
            if major in major_res or not major or major == "N/A" or "N/A" in major:
                continue
            major_res.append(major)
            
        for major in major_lst2:
            major = major.strip()
            if major in major_res or not major or major == "N/A" or "N/A" in major:
                continue
            major_res.append(major)
        
        for major in major_lst3:
            major = major.strip()
            if major in major_res or not major or major == "N/A" or "N/A" in major:
                continue
            major_res.append(major)

    return sorted(skill_res), sorted(industry_res), sorted(tech_res), sorted(domain_res), sorted(university_res), sorted(major_res)

def home(request):
    # user in our database
    user_db = []
    for person in BioInfo.objects.all():
        if person.email not in user_db:
            user_db.append(person.email)
    # in_db
    # name_str = request.user.first_name.replace(' ', '_') + '_' + request.user.last_name.replace(' ', '_')
    email_str = str(request.user)
    in_db = 1 if email_str.lower() in user_db else 0
    print(request.user, in_db)
    print(user_db)

    # single selection
    position_query = request.GET.get('position-dropdown')
    location_query = request.GET.get('location-dropdown')
    # multi selection
    # skill_query = request.GET.getlist('skill-dropdown')
    # skill_level_query = request.GET.get('skill-level-dropdown') # number
    industry_query = request.GET.getlist('industry-dropdown')
    industry_level_query = request.GET.get('industry-level-dropdown') # number
    tech_query = request.GET.getlist('tech-dropdown')
    tech_level_query = request.GET.get('tech-level-dropdown') # number
    domain_query = request.GET.getlist('domain-dropdown')
    domain_level_query = request.GET.get('domain-level-dropdown') # number
    # education background
    university_query = request.GET.get('university-dropdown')
    major_query = request.GET.get('major-dropdown')
    degree_query = request.GET.get('degree-dropdown')
    print("degree here", degree_query)
    # search bar
    search_query = request.GET.get('search-input')
    # distinct options in filter
    people = BioInfo.objects.all()
    position_dist = BioInfo.objects.values('position').distinct()
    location_dist = BioInfo.objects.values('location').distinct()
    skill_dist, industry_dist, tech_dist, domain_dist, university_dist, major_dist = distinct_features()
    ###########################
    #### new category here ####
    ###########################
    application, ds_skill, program_skill, techstack = distinct_skill()
    app_query = request.GET.get('app-dropdown')
    app_level_query = request.GET.get('app-level-dropdown') # number
    ds_query = request.GET.get('ds-dropdown')
    ds_level_query = request.GET.get('ds-level-dropdown') # number
    program_query = request.GET.get('program-dropdown')
    program_level_query = request.GET.get('program-level-dropdown') # number
    techstack_query = request.GET.get('techstack-dropdown')
    techstack_level_query = request.GET.get('techstack-level-dropdown') # number
    
    # university_dist = list(set().union(university_dist, university_dist2, university_dist3))
    if position_query:
        people = people.filter(position=position_query)
    if location_query:
        people = people.filter(location=location_query)
    if university_query:
        people = people.filter(university=university_query) | \
                        people.filter(university2=university_query) | \
                        people.filter(university3=university_query) 
    if major_query:
        people = people.filter(major=major_query) | \
                    people.filter(major2=major_query) | \
                    people.filter(major3=major_query) 
    if degree_query:
        people = people.filter(degree=degree_query)

    if app_query and app_query != '':
        # for i in app_query:
        people = people.filter(application__contains=app_query)
        print("check here: ", len(people))
        if app_level_query:
            for person in people:
                tmp_skill = person.application
                for t in tmp_skill.split(','):
                    if not app_query in t:
                        continue
                    t = t.strip()
                    if ")" == t[-1]:
                        # t = t.strip()
                        print(t.split(' ')[-1])
                        if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < app_level_query:
                            print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], app_level_query)
                            print(person.name, "excluded")
                            people = people.exclude(id=person.id)
                    elif ")" not in t[-1] and app_level_query == 1:
                        continue
                    else:
                        people = people.exclude(id=person.id)

    if ds_query and ds_query != '':
        # for i in app_query:
        people = people.filter(ds_skill__contains=ds_query)
        print("check here: ", len(people))
        if ds_level_query:
            for person in people:
                tmp_skill = person.ds_skill
                for t in tmp_skill.split(','):
                    if not ds_query in t:
                        continue
                    t = t.strip()
                    if ")" == t[-1]:
                        # t = t.strip()
                        print(t.split(' ')[-1])
                        if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < ds_level_query:
                            print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], ds_level_query)
                            print(person.name, "excluded")
                            people = people.exclude(id=person.id)
                    elif ")" not in t[-1] and ds_level_query == 1:
                        continue
                    else:
                        people = people.exclude(id=person.id)
    
    if program_query and program_query != '':
        # for i in app_query:
        people = people.filter(program_skill__contains=program_query)
        if program_level_query:
            for person in people:
                tmp_skill = person.program_skill
                for t in tmp_skill.split(','):
                    if not program_query in t:
                        continue
                    t = t.strip()
                    if ")" == t[-1]:
                        # t = t.strip()
                        print(t.split(' ')[-1])
                        if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < program_level_query:
                            print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], program_level_query)
                            print(person.name, "excluded")
                            people = people.exclude(id=person.id)
                    elif ")" not in t[-1] and program_level_query == 1:
                        continue
                    else:
                        people = people.exclude(id=person.id)
    
    if techstack_query and techstack_query != '':
        # for i in app_query:
        people = people.filter(tech_stack__contains=techstack_query)
        if techstack_level_query:
            for person in people:
                tmp_skill = person.tech_stack
                for t in tmp_skill.split(','):
                    if not techstack_query in t:
                        continue
                    t = t.strip()
                    if ")" == t[-1]:
                        # t = t.strip()
                        print(t.split(' ')[-1])
                        if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < techstack_level_query:
                            print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], techstack_level_query)
                            print(person.name, "excluded")
                            people = people.exclude(id=person.id)
                    elif ")" not in t[-1] and techstack_level_query == 1:
                        continue
                    else:
                        people = people.exclude(id=person.id)

    if industry_query != ['']:
        for i in industry_query:
            people = people.filter(industry__contains=i)
            if industry_level_query:
                for person in people:
                    tmp_industry = person.industry
                    for t in tmp_industry.split(','):
                        if ")" in t[-1]:
                            t = t.strip()  
                            if i in t:
                                if REVERSE_RUBRIC[''.join(t.split(' ')[-2:])[1:-1]] < industry_level_query:
                                    print(REVERSE_RUBRIC[''.join(t.split(' ')[-2:])[1:-1]], industry_level_query)
                                    print(person.name, "excluded")
                                    people = people.exclude(id=person.id)
                        elif ")" not in t[-1] and industry_level_query == 1:
                            continue
                        else:
                            people = people.exclude(id=person.id)

    # if tech_query != ['']:
    #     for i in tech_query:
    #         people = people.filter(technique__contains=i)
    #         if tech_level_query:
    #             for person in people:
    #                 tmp_tech = person.technique
    #                 for t in tmp_tech.split(','):
    #                     if ")" in t[-1]:
    #                         t = t.strip()
    #                         if i in t:
    #                             if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < tech_level_query:
    #                                 print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], tech_level_query)
    #                                 print(person.name, "excluded")
    #                                 people = people.exclude(id=person.id)
    #                     elif ")" not in t[-1] and tech_level_query == 1:
    #                         continue
    #                     else:
    #                         people = people.exclude(id=person.id)

    if domain_query != ['']:
        for i in domain_query:
            people = people.filter(business_domain__contains=i)
            if domain_level_query:
                for person in people:
                    tmp_domain = person.business_domain
                    for t in tmp_domain.split(','):
                        if ")" in t[-1]:
                            t = t.strip()
                            if i in t:
                                if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < domain_level_query:
                                    print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], domain_level_query)
                                    print(person.name, "excluded")
                                    people = people.exclude(id=person.id)
                        elif ")" not in t[-1] and domain_level_query == 1:
                            continue                        
                        else:
                            people = people.exclude(id=person.id)

    if search_query:
        search_sections = search_query.split(',')
        search_list = [None] * len(search_sections)
        # subcategory search
        additional_peope = sub_cate_search(people, search_query)
        # print('addition_people', len(additional_peope), additional_peope)

        # first search word
        people = people.filter(nickname__contains=search_sections[0]) | \
                        people.filter(name__contains=search_sections[0]) | \
                        people.filter(skill__contains=search_sections[0]) | \
                        people.filter(technique__contains=search_sections[0]) | \
                        people.filter(industry__contains=search_sections[0]) | \
                        people.filter(position__contains=search_sections[0]) | \
                        people.filter(business_domain__contains=search_sections[0])
        search_list[0] = people 
        if len(search_sections) > 1:
            for i in range(1, len(search_sections)):
                search_list[i] = people.filter(nickname__contains=search_sections[i]) | \
                                    people.filter(name__contains=search_sections[i]) | \
                                    people.filter(skill__contains=search_sections[i]) | \
                                    people.filter(technique__contains=search_sections[i]) | \
                                    people.filter(industry__contains=search_sections[i]) | \
                                    people.filter(position__contains=search_sections[i]) | \
                                    people.filter(business_domain__contains=search_sections[i])

                people = search_list[i] & search_list[i - 1]    
        # print('people', len(people), people, len(list(people) + additional_peope))
        people = list(set(list(people) + additional_peope))
            
    return render(request, 'bios/home.html', {"people_number": people,
                                            "position_distinct": position_dist,
                                            "location_distinct": location_dist,
                                            "industry_distinct": industry_dist,
                                            # "tech_distinct": tech_dist,
                                            "domain_distinct": domain_dist,
                                            "university_distinct": university_dist,
                                            "major_distinct": major_dist,
                                            "industry_query": industry_query,
                                            # "technique_query": tech_query,
                                            "domain_query": domain_query,
                                            # "tech_level": tech_level_query,
                                            "industry_level": industry_level_query,
                                            "domain_level": domain_level_query,
                                            'university_query': university_query,
                                            'major_query': major_query,
                                            'degree_query':degree_query,
                                            'search_query':search_query,
                                            'in_db': in_db,
                                            "request_len": len(request.GET),
                                            "app_distinct":application,
                                            "app_query":app_query,
                                            "app_level": app_level_query,
                                            "ds_distinct":ds_skill,
                                            "ds_query":ds_query,
                                            "ds_level": ds_level_query,
                                            "program_distinct":program_skill,
                                            "program_query":program_query,
                                            "program_level": program_level_query,
                                            "techstack_distinct":techstack,
                                            "techstack_query":techstack_query,
                                            "techstack_level": techstack_level_query,
                                            })

def create(request):
    # user in our database
    user_db = []
    for person in BioInfo.objects.all():
        if person.name not in user_db:
            user_db.append(person.name)
    # in_db
    # name_str = request.user.first_name.replace(' ', '_') + '_' + request.user.last_name.replace(' ', '_')
    email_str = str(request.user)
    in_db = 1 if email_str.lower() in user_db else 0
    if request.method == "POST":
        form = request.POST
        n = form.get('name')
        e = form.get('email')
        p = form.get('position')
        l = form.get('location')

        s = form.getlist('skill')
        if not s:
            s = ['N/A']
        else:
            for i in range(len(s)):
                level = s[i].split(' ')[-1]
                flag = 0
                for j in range(len(s[i])):
                    if s[i][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level]))
                s[i] = "{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level])

        tech = form.getlist('technique')
        if not tech:
            tech = ['N/A']
        else:
            for i in range(len(tech)):
                level = tech[i].split(' ')[-1]
                flag = 0
                for j in range(len(tech[i])):
                    if tech[i][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level]))
                tech[i] = "{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level])

        i = form.getlist('industry')
        if not i:
            i = ['N/A']
        else:
            for i_ in range(len(i)):
                level = i[i_].split(' ')[-1]
                flag = 0
                for j in range(len(i[i_])):
                    if i[i_][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level]))
                i[i_] = "{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level])

        u = form.get('university')
        if not u:
            u = 'N/A'

        m = form.get('major')
        if not m:
            m = 'N/A'

        c = form.get('degree')
        if not c:
            c = 'N/A'
        intro = form.get('intro')
        if not intro:
            intro = 'N/A'

        d = form.getlist('domain')
        if not d:
            d = ['N/A']
        else:
            for k in range(len(d)):
                level = d[k].split(' ')[-1]
                flag = 0
                for j in range(len(d[k])):
                    if d[k][j].isdigit():
                        flag = j
                        break
                # print("{} ({})".format(d[k][:flag-1], SKILL_RUBRIC[level]))
                d[k] = "{} ({})".format(d[k][:flag-1], SKILL_RUBRIC[level])
        t, _ = BioInfo.objects.update_or_create(
            name = n,
            defaults={
                "email" : e, 
                "position" : p, 
                "location" : l, 
                "skill" : ', '.join(s),
                "technique" : ', '.join(tech), 
                "industry" : ', '.join(i), 
                "university" : u,
                "major" : m,
                "degree" : c, 
                "university2" : u,
                "major2" : m,
                "degree2" : c,
                "university3" : u,
                "major3" : m,
                "degree3" : c,
                "intro" : intro,
                "business_domain" : ', '.join(d),
            }
        )

        stu, _ = Student.objects.update_or_create(
            name = n,
            defaults={
                'photo': 'images/logo2.png',
                'bio_ppt': 'bio_ppt/Blank_Bio.pdf',
            }
        )

        t.save()
        return HttpResponseRedirect("/")
    else:    
        form = CreateNewProfile()
    return render(request, "bios/create.html", {"form" : form,
                                                "in_db": in_db,})

def upload_img(request):
    # user in our database
    user_db = []
    for person in BioInfo.objects.all():
        if person.name not in user_db:
            user_db.append(person.name)
    # in_db
    # name_str = request.user.first_name.replace(' ', '_') + '_' + request.user.last_name.replace(' ', '_')
    email_str = str(request.user)
    in_db = 1 if email_str.lower() in user_db else 0
    if request.method == "POST":
        print(os.listdir('bios/static/media/images'))
        form = request.FILES

        existed_file = Student.objects.filter(name="{}_{}".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')))
        # print(existed_file['photo'].url)
        print('photo' in request.FILES, 'bio_ppt' in request.FILES)

        if not existed_file:
            print("Creating new object!!!")
            # remove the existing file that already has the name
            print("{}_{}.pdf".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')), os.listdir('bios/static/media/bio_ppt'))
            if 'bio_ppt' in request.FILES and "{}_{}.pdf".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')) in os.listdir('bios/static/media/bio_ppt'):
                print("check check bio!")
                os.remove("bios/static/media/bio_ppt/{}_{}.pdf".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')))
                print(os.listdir('bios/static/media/bio_ppt'))
            print("==========================")
            print("{}_{}.pdf".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')), os.listdir('bios/static/media/images'))
            if 'photo' in request.FILES and "{}_{}.{}".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_'), request.FILES['photo'].name.split('.')[-1]) in os.listdir('bios/static/media/images'):
                print("check check photo!")
                os.remove("bios/static/media/images/{}_{}.{}".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_'), request.FILES['photo'].name.split('.')[-1]))
                print(os.listdir('bios/static/media/images'))

            file, _ = Student.objects.update_or_create(
                name = "{}_{}".format(request.user.first_name,request.user.last_name),
                defaults = {
                    "photo" : request.FILES['photo'] if 'photo' in request.FILES else 'images/logo2.png',
                    "bio_ppt" : request.FILES['bio_ppt'] if 'bio_ppt' in request.FILES else 'bio_ppt/Blank_Bio.pdf', 
                }
            )
            file.save()
        else:
            existed_file = Student.objects.get(name="{}_{}".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')))
            print("Updating existed object!!!", os.listdir('bios/static/media/images'))
            print("Updating existed object!!!", os.listdir('bios/static/media/bio_ppt'))
            if 'photo' in request.FILES and existed_file.photo != 'images/logo2.png':
                print('checkpoint 1')
                print(os.listdir('bios/static/media/images'), existed_file.photo)
                existed_file.photo.delete()
            if 'bio_ppt' in request.FILES and existed_file.bio_ppt != 'bio_ppt/Blank_Bio.pdf':
                print('checkpoint 2')
                print(os.listdir('bios/static/media/bio_ppt'), existed_file.bio_ppt)
                existed_file.bio_ppt.delete()

            if os.path.exists('bios/static/media/images/{}_{}.jpeg'.format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_'))) and "photo" in request.FILES:
                os.remove("bios/static/media/images/{}_{}.jpeg".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')))
                print("PHOTO REMOVED!!!")
                print(os.listdir('bios/static/media/images'), existed_file.photo)

            if os.path.exists('bios/static/media/bio_ppt/{}_{}.pdf'.format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_'))) and "bio_ppt" in request.FILES:
                os.remove("bios/static/media/bio_ppt/{}_{}.pdf".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')))
                print("BIO PPT REMOVED!!!")
                print(os.listdir('bios/static/media/bio_ppt'), existed_file.bio_ppt)       
            
            # rename the file
            for filename, file in form.items():
                print('======================')
                print(filename, request.FILES[filename].name)
                if request.FILES[filename].name.split('.')[-1] in ['jpeg', 'jpg', 'png', 'JPG', 'JPEG', 'PNG']:
                    request.FILES[filename].name = "{}_{}.{}".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_'), request.FILES[filename].name.split('.')[-1])
                else:
                    request.FILES[filename].name = "{}_{}.pdf".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_'))
                print(filename, request.FILES[filename].name)
            print('after rename file')
            print(os.listdir('bios/static/media/images'), existed_file.photo)
            print(os.listdir('bios/static/media/bio_ppt'), existed_file.bio_ppt)
            # print(request.FILES["bio_ppt"])
            file, _ = Student.objects.update_or_create(
                name = "{}_{}".format(request.user.first_name.replace(' ', '_'),request.user.last_name.replace(' ', '_')),
                defaults = {
                    "photo" : request.FILES['photo'] if 'photo' in request.FILES else existed_file.photo,
                    "bio_ppt" : request.FILES['bio_ppt'] if 'bio_ppt' in request.FILES else existed_file.bio_ppt, 
                }
            )
            # if file.bio_ppt == "static/media/bio_ppt/Cheng_Yu_Jacob_Li.pdf":
            #     os.rename("static/media/bio_ppt/Cheng_Yu_Jacob_Li.pdf", "static/media/bio_ppt/Cheng_Yu_(Jacob)_Li.pdf")
            file.save()
        return HttpResponseRedirect("/{}".format(request.user.first_name.replace(' ', '_')+'_'+request.user.last_name.replace(' ', '_')))

    else:
        form = FileUpload()
        return render(request, "bios/upload.html", {"form" : form,
                                                    'in_db': in_db})

def edit(request, name):
    if name != request.user.first_name.replace(" ", "_") + '_' + request.user.last_name.replace(' ', '_'):
        raise PermissionDenied('You are not allowed')
    
    # user in our database
    user_db = []
    for person in BioInfo.objects.all():
        if person.name not in user_db:
            user_db.append(person.name)
    # in_db
    # name_str = request.user.first_name.replace(' ', '_') + '_' + request.user.last_name.replace(' ', '_')
    email_str = str(request.user)
    in_db = 1 if email_str.lower() in user_db else 0

    person = BioInfo.objects.get(name=name)

    # initial skills
    skills = person.skill.split(',')
    skill_init = []
    preselect_dict = {}
    for s in skills:
        if 'N/A' in s:
            continue
        flag = 0
        for i in range(len(s)):
            if s[i].isdigit() or s[i] == '(':
                flag = i
                break
        # print(flag)
        if flag != 0:
            skill_init.append(s[:flag-1].strip())
            print("SKILL ****>", skill_init)
            preselect_dict['id_skill_{}'.format(tmp1.index(s[:flag-1].strip()))] = ''.join(s.strip().split(" ")[-1])
        if flag == 0:
            print(s[:flag-1].strip())
    print("skill initial", skill_init)

    # initial industries
    industries = person.industry.split(',')
    industry_init = []
    for ins in industries:
        if 'N/A' in ins:
            continue
        flag = 0
        for i in range(len(ins)):
            if ins[i] == "2" and ins[i-1] == "B" and ins[i+1] == "B":
                print('warning here')
                continue   
            if ins[i].isdigit() or ins[i] == '(':
                flag = i
                break
        if flag != 0:
            industry_init.append(ins[:flag-1].strip())
            print("INDUSTRY ****>", industry_init)
            preselect_dict['id_industry_{}'.format(tmp2.index(ins[:flag-1].strip()))] = ''.join(ins.strip().split(" ")[-2:])
    print("industry initial", industry_init)

    # initial techniques
    techniques = person.technique.split(',')
    tech_init = []
    for tech in techniques:
        if 'N/A' in tech:
            continue
        flag = 0
        for i in range(len(tech)):
            if tech[i].isdigit() or tech[i] == '(':
                flag = i
                break
        if flag != 0:
            tech_init.append(tech[:flag-1].strip())
        if tech_init:
            print("TECH ****>", tech_init)
            preselect_dict['id_technique_{}'.format(tmp3.index(tech[:flag-1].strip()))] = ''.join(tech.strip().split(" ")[-1])
    print('technique skill initial', tech_init)

    # initial domain
    domain_init = []
    if person.business_domain:
        domain = person.business_domain.split(',')    
        for dom in domain:
            if 'N/A' in dom:
                continue
            flag = 0
            for i in range(len(dom)):
                if dom[i].isdigit() or dom[i] == '(':
                    flag = i
                    break
            if flag != 0:
                domain_init.append(dom[:flag-1].strip())
            if domain_init:
                print("DOMAIN ****>", domain_init)
                preselect_dict['id_domain_{}'.format(tmp4.index(dom[:flag-1].strip()))] = ''.join(dom.strip().split(" ")[-1])
    print('domain initial', domain_init)

    location_init = ''
    if person.location and person.location != 'N/A':
        location_init = person.location

    print(preselect_dict)
    print("====================")
    for k, v in preselect_dict.items():
        # print(k, v)
        preselect_dict[k] = REVERSE_RUBRIC[v[1:-1]]
    print(preselect_dict)

    if request.method == "POST":
        form = request.POST

        l = form.get('location')

        s = form.getlist('skill')
        if not s:
            s = ['N/A 1']
        for i in range(len(s)):
            level = s[i].split(' ')[-1]
            if level.isdigit():
                for j in range(len(s[i])):
                    if s[i][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level]))
                s[i] = "{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level])
            else:
                s[i] = "{} ({})".format(s[i], SKILL_RUBRIC['1'])


        tech = form.getlist('technique')
        if not tech:
            tech = ['N/A 1']
        for i in range(len(tech)):
            level = tech[i].split(' ')[-1]
            if level.isdigit():
                for j in range(len(tech[i])):
                    if tech[i][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level]))
                tech[i] = "{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level])
            else:
                tech[i] = "{} ({})".format(tech[i], SKILL_RUBRIC['1'])

        i = form.getlist('industry')
        if not i:
            i = ['N/A 1']
        for i_ in range(len(i)):
            # print(i[i_])
            level = i[i_].split(' ')[-1]
            if level.isdigit():
                for j in range(len(i[i_])):
                    if i[i_][j] == "2" and i[i_][j-1] == 'B' and i[i_][j+1] == 'B':
                        print("B2B special", i[i_])
                        continue
                    if i[i_][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level]))
                i[i_] = "{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level])
            else:
                i[i_] = "{} ({})".format(i[i_], EXPERIENCE_RUBRIC['1'])
        print(i)
    
        d = form.getlist('domain')
        if not d:
            d = ['N/A 1']
        for k in range(len(d)):
            level = d[k].split(' ')[-1]
            if level.isdigit():
                for j in range(len(d[k])):
                    if d[k][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(d[k][:flag-1], SKILL_RUBRIC[level]))
                d[k] = "{} ({})".format(d[k][:flag-1], SKILL_RUBRIC[level])
            else:
                d[k] = "{} ({})".format(d[k], SKILL_RUBRIC['1'])

        uni_1 = form.get('university')
        major_1 = form.get('major')
        degree_1 = form.get('degree')
        if not uni_1 or not major_1 or not degree_1:
            uni_1, major_1, degree_1 = 'N/A', 'N/A', 'N/A'

        uni_2 = form.get('university_2')
        major_2 = form.get('major_2')
        degree_2 = form.get('degree_2')
        if not uni_2 or not major_2 or not degree_2:
            uni_2, major_2, degree_2 = 'N/A', 'N/A', 'N/A'

        uni_3 = form.get('university_3')
        major_3 = form.get('major_3')
        degree_3 = form.get('degree_3')
        if not uni_3 or not major_3 or not degree_3:
            uni_3, major_3, degree_3 = 'N/A', 'N/A', 'N/A'

        nickname = form.get('nickname')
        if not nickname:
            nickname = ' '

        intro = form.get('intro')
        if not intro:
            intro = 'N/A'
        t, _ = BioInfo.objects.update_or_create(
            name = name,
            defaults={
                "location" : l, 
                "skill" : ', '.join(s),
                "technique" : ', '.join(tech), 
                "university": uni_1,
                "major": major_1,
                "industry" : ', '.join(i), 
                "degree" : degree_1, 
                "intro" : intro,
                "business_domain" : ', '.join(d),
                "university2": uni_2,
                "major2": major_2,
                "degree2": degree_2,
                "university3": uni_3,
                "major3": major_3,
                "degree3": degree_3,  
                "nickname":nickname, 
            }
        )
        t.save()
        
        return HttpResponseRedirect("/{}".format(name))      
    else:
        u1 = person.university if person.university != 'N/A' else ''
        u2 = person.university2 if person.university2 != 'N/A' else ''
        u3 = person.university3 if person.university3 != 'N/A' else ''
        m1 = person.major if person.major != 'N/A' else ''
        m2 = person.major2 if person.major2 != 'N/A' else ''
        m3 = person.major3 if person.major3 != 'N/A' else ''
        d1 = person.degree if person.degree != 'N/A' else ''
        d2 = person.degree2 if person.degree2 != 'N/A' else ''
        d3 = person.degree3 if person.degree3 != 'N/A' else ''
        intro = person.intro if person.intro != 'N/A' else ''
        nickname = person.nickname if person.nickname != ' ' else person.name.replace('_', ' ')
        form = EditProfile(initial={'location' : location_init,
                                    'skill' : skill_init,
                                    'industry' : industry_init,
                                    'technique' : tech_init, 
                                    'degree' : person.degree,
                                    'intro' : intro,
                                    'domain':domain_init,
                                    'university':u1,
                                    'major': m1,
                                    'degree': d1,
                                    'university_2':u2,
                                    'major_2': m2,
                                    'degree_2': d2,
                                    'university_3':u3,
                                    'major_3': m3,
                                    'degree_3': d3,
                                    'nickname':nickname,
                                    })
        return render(request, "bios/edit.html", {"form":form,
                                                  "person":person,
                                                  "preselect":preselect_dict,
                                                  'in_db':in_db,})

def dashboard(request):
    people = BioInfo.objects.all()
    location_dist = list(BioInfo.objects.values('location').distinct())
    location_distinct = []
    for x in location_dist:
        location_distinct.append(x['location'])
    # user in our database
    user_db = []
    for person in BioInfo.objects.all():
        if person.name not in user_db:
            user_db.append(person.name)
    # in_db
    # name_str = request.user.first_name.replace(' ', '_') + '_' + request.user.last_name.replace(' ', '_')
    email_str = str(request.user)
    in_db = 1 if email_str.lower() in user_db else 0

    # sorted(skill_res), sorted(industry_res), sorted(tech_res), sorted(domain_res), 
    # sorted(university_res), sorted(major_res)
    feature_lst = distinct_features()

    ###############################################
    ## filter people out ##
    ###############################################
    skill_query = request.GET.getlist('skill-dropdown')
    industry_query = request.GET.getlist('industry-dropdown')
    location_query = request.GET.get('location-dropdown')
    degree_query = request.GET.get('degree-dropdown')
    filter_count = 0
    if skill_query and skill_query != ['']:
        people = people.filter(skill__contains=skill_query[0])| \
                    people.filter(technique__contains=skill_query[0])
        filter_count += 1
    if industry_query and industry_query != ['']:
        people = people.filter(industry__contains=industry_query[0]) | \
                    people.filter(business_domain__contains=industry_query[0])
        filter_count += 1
    # print(len(people), people, filter_count)
    if location_query:
        people = people.filter(location__contains=location_query)
    if degree_query:
        print('check check here', degree_query)
        people = people.filter(degree__contains=degree_query)

    ###############################################
    ## generate the data passed to visualization ##
    ###############################################
    if filter_count == 2:
        res_freq = collections.defaultdict(list)

        if skill_query and skill_query != ['']:
            for item in people:
                ### find the skill level ###
                # area of expertise
                skills = item.skill.split(',')
                for skill in skills:
                    if skill_query[0] in skill:
                        skill_lvl = skill.split(' ')[-1][1:-1]
                # technique skill
                techs = item.technique.split(',')
                for tech in techs:
                    if skill_query[0] in tech:
                        skill_lvl = tech.split(' ')[-1][1:-1]

                ### find the industry level ###
                # industry experience
                industries = item.industry.split(',')
                if industries == ['N/A']:
                    continue
                for industry in industries:
                    exp = ''.join(industry.split(' ')[-2:])[1:-1]
                    if industry_query[0] and industry_query[0] in industry:   
                        industry_lvl = ADJUST_EXP[exp]
                # business domain
                domains = item.business_domain.split(',')
                if domains == ['N/A']:
                    continue
                for domain in domains:
                    exp = DOMAIN_MODIFICATION[domain.split(' ')[-1][1:-1]]
                    if industry_query[0] and industry_query[0] in domain:
                        industry_lvl = exp
                        # res_freq[exp] = res_freq.get(exp, 0) + 1

                res_freq[skill_lvl].append(industry_lvl)

        data = [[0 for _ in range(5)] for _ in range(5)]
        for i, sk_opt in enumerate(SKILL_RUBRIC.values()):
            if sk_opt not in res_freq:
                continue
            this_lvl = res_freq[sk_opt]
            lvl_freq = collections.Counter(this_lvl)
            for j, ins_opt in enumerate(EXPERIENCE_RUBRIC.values()):
                data[i][j] = lvl_freq.get(ADJUST_EXP[ins_opt.replace(' ', '')], 0)
        plot_name = skill_query[0] + " by " + industry_query[0]

    else:
        res_freq = {}
        if skill_query and skill_query != ['']:
            for item in people:
                ### for 'area of expertise' 
                skills = item.skill.split(',')
                for skill in skills:
                    if skill_query[0] in skill:
                        res_freq[skill.split(' ')[-1][1:-1]] = res_freq.get(skill.split(' ')[-1][1:-1], 0) + 1               
                ### for 'technique skill'
                techs = item.technique.split(',')
                for tech in techs:
                    if skill_query[0] in tech:
                        res_freq[tech.split(' ')[-1][1:-1]] = res_freq.get(tech.split(' ')[-1][1:-1], 0) + 1
            plot_name = skill_query[0]
            ### put the result in the correct order 
            tmp_res = {}
            for val in SKILL_RUBRIC.values():
                if val in res_freq:   
                    tmp_res[val] = res_freq[val]
            res_freq = tmp_res

        elif industry_query and industry_query != ['']:
            for item in people:
                ### for 'industry experience'
                industries = item.industry.split(',')
                if industries == ['N/A']:
                    continue
                for industry in industries:
                    exp = ''.join(industry.split(' ')[-2:])[1:-1]
                    if industry_query[0] in industry:
                        res_freq[ADJUST_EXP[exp]] = res_freq.get(ADJUST_EXP[exp], 0) + 1
                ### for 'business domain'
                domains = item.business_domain.split(',')
                if domains == ['N/A']:
                    continue
                for domain in domains:
                    print("test123", DOMAIN_MODIFICATION[domain.split(' ')[-1][1:-1]])
                    exp = DOMAIN_MODIFICATION[domain.split(' ')[-1][1:-1]]
                    if industry_query[0] in domain:
                        res_freq[exp] = res_freq.get(exp, 0) + 1

            plot_name = industry_query[0]
            print(res_freq)
            tmp_res = {}
            for val in EXPERIENCE_RUBRIC_MAIN.values():  
                if val in res_freq:  
                    tmp_res[val] = res_freq[val]
            res_freq = tmp_res
        # default page (bar chart by position)
        else:
            for person in people:
                res_freq[person.location] = res_freq.get(person.location, 0) + 1
            plot_name = 'Work Location'

        data = res_freq.values()
    a = str(sns.color_palette("Set2").as_hex())

    return render(request, 'bios/dashboard.html', {'labels':list(res_freq.keys()),
                                                   'single_data':list(res_freq.values()),
                                                   'data':data,
                                                   'sns_color':a,
                                                   'skill_distinct':feature_lst[0],
                                                   'skill_query':skill_query,
                                                   'industry_distinct':feature_lst[1],
                                                   'industry_query':industry_query,
                                                   'tech_distinct':feature_lst[2],
                                                   'domain_distinct':feature_lst[3],
                                                   'filter_count': filter_count,
                                                   'in_db': in_db,
                                                   'plot_name':plot_name,
                                                   'location_distinct':location_distinct,
                                                   'location_query':location_query,
                                                   'degree_query':degree_query,
                                                   "filter_count":filter_count,
                                                   })
