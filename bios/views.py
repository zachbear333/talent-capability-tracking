# show http requests, and the things showing up on the website

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


register = template.Library()
@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)
    
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
    ('Unit Testing (QA)', 'Unit Testing (QA)'),
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
    ('Tensorflow', 'Tensorflow')
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

def test(request):
    if request.method == "POST":
        temp = request.POST
        print(temp.get("skill"))
        return HttpResponseRedirect("/upload_img/")
    else:    
        form = testform()
    # return render(request, "bios/create.html", {"form" : form})
    return render(request, 'bios/test.html', {"form" : form})


def index(response, name):
    item = BioInfo.objects.get(name=name)
    # area of expertise table
    skill_tmp = item.skill
    skill_dict = {}
    for s in skill_tmp.split(','):
        if '(' in s:
            idx = s.index('(')
            skill_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s[idx+1:-1].strip()]
        else:
            skill_dict[s] = "1"
    skill_dict = sorted(skill_dict.items(), key=lambda x:x[1], reverse=True)
    skill_dict = {k:SKILL_RUBRIC_MAIN[v] for k, v in skill_dict}

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

    # technique skill table
    tech_tmp = item.technique
    tech_dict = {}
    for s in tech_tmp.split(','):
        if '(' in s:
            idx = s.index('(')
            tech_dict[s[:idx-1].strip()] = REVERSE_RUBRIC[s[idx+1:-1].strip()]
        else:
            tech_dict[s] = "1"
    tech_dict = sorted(tech_dict.items(), key=lambda x:x[1], reverse=True)
    tech_dict = {k:SKILL_RUBRIC_MAIN[v] for k, v in tech_dict}

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

    return render(response, 'bios/bio-info.html', {"people":item,
                                                   "skill":skill_dict,
                                                   "industry":industry_dict,
                                                   "technique":tech_dict,
                                                   "domain":domain_dict,
                                                   })

def distinct_features():
    skill_res, industry_res, tech_res, domain_res = [], [], [], []
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

        # deal with technology
        for domain in domain_lst:
            domain = domain.strip()
            if domain in domain_res or not domain or domain == "N/A" or "N/A" in domain:
                continue
            if "(" in domain:
                if ' '.join(domain.split(' ')[:-1]) not in domain_res:
                    domain_res.append(' '.join(domain.split(' ')[:-1]))
            else:
                domain_res.append(domain)

    return sorted(skill_res), sorted(industry_res), sorted(tech_res), sorted(domain_res)

def home(request):
    # single selection
    position_query = request.GET.get('position-dropdown')
    location_query = request.GET.get('location-dropdown')
    # multi selection
    skill_query = request.GET.getlist('skill-dropdown')
    skill_level_query = request.GET.get('skill-level-dropdown') # number
    industry_query = request.GET.getlist('industry-dropdown')
    industry_level_query = request.GET.get('industry-level-dropdown') # number
    tech_query = request.GET.getlist('tech-dropdown')
    tech_level_query = request.GET.get('tech-level-dropdown') # number
    domain_query = request.GET.getlist('domain-dropdown')
    domain_level_query = request.GET.get('domain-level-dropdown') # number

    print(skill_query, industry_query, tech_query, domain_query)
    print(skill_level_query, industry_level_query, tech_level_query, domain_level_query)
    
    # search bar
    search_query = request.GET.get('search-input')
    # distinct options in filter
    people = BioInfo.objects.all()
    position_dist = BioInfo.objects.values('position').distinct()
    location_dist = BioInfo.objects.values('location').distinct()
    skill_dist, industry_dist, tech_dist, domain_dist = distinct_features()

    if position_query:
        people = people.filter(position=position_query)
    if location_query:
        people = people.filter(location=location_query)

    if skill_query != ['']:
        for i in skill_query:
            people = people.filter(skill__contains=i)
            if skill_level_query:
                for person in people:
                    tmp_skill = person.skill
                    for t in tmp_skill.split(','):
                        if ")" in t[-1]:
                            t = t.strip()
                            if i in t:
                                if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < skill_level_query:
                                    print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], skill_level_query)
                                    print(person.name, "excluded")
                                    people = people.exclude(id=person.id)
                        elif ")" not in t[-1] and skill_level_query == 1:
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

    if tech_query != ['']:
        for i in tech_query:
            people = people.filter(technique__contains=i)
            if tech_level_query:
                for person in people:
                    tmp_tech = person.technique
                    for t in tmp_tech.split(','):
                        if ")" in t[-1]:
                            t = t.strip()
                            if i in t:
                                if REVERSE_RUBRIC[t.split(' ')[-1][1:-1]] < tech_level_query:
                                    print(REVERSE_RUBRIC[t.split(' ')[-1][1:-1]], tech_level_query)
                                    print(person.name, "excluded")
                                    people = people.exclude(id=person.id)
                        elif ")" not in t[-1] and tech_level_query == 1:
                            continue
                        else:
                            people = people.exclude(id=person.id)

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
        search_sections = search_query.split(' ')
        search_list = [None] * len(search_sections)
        # first search word
        people = people.filter(name__contains=search_sections[0]) | \
                        people.filter(skill__contains=search_sections[0]) | \
                        people.filter(technique__contains=search_sections[0]) | \
                        people.filter(industry__contains=search_sections[0]) | \
                        people.filter(position__contains=search_sections[0])
        search_list[0] = people 
        if len(search_sections) > 1:
            for i in range(1, len(search_sections)):
                search_list[i] = people.filter(name__contains=search_sections[i]) | \
                                    people.filter(skill__contains=search_sections[i]) | \
                                    people.filter(technique__contains=search_sections[i]) | \
                                    people.filter(industry__contains=search_sections[i]) | \
                                    people.filter(position__contains=search_sections[i])

                people = search_list[i] & search_list[i - 1]            
            

    return render(request, 'bios/home.html', {"people_number": people,
                                              "position_distinct": position_dist,
                                              "location_distinct": location_dist,
                                              "skill_distinct": skill_dist,
                                              "industry_distinct": industry_dist,
                                              "tech_distinct": tech_dist,
                                              "domain_distinct": domain_dist,
                                              "skill_query": skill_query,
                                              "industry_query": industry_query,
                                              "technique_query": tech_query,
                                              "domain_query": domain_query,
                                              "skill_level": skill_level_query,
                                              "tech_level": tech_level_query,
                                              "industry_level": industry_level_query,
                                              "domain_level": domain_level_query,
                                              })

def create(request):
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

        c = form.get('client')
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
                "client" : c, 
                "intro" : intro,
                "business_domain" : ', '.join(d),
            }
        )
        t.save()
        return HttpResponseRedirect("/")
    else:    
        form = CreateNewProfile()
    return render(request, "bios/create.html", {"form" : form})

def upload_img(request):
    if request.method == "POST":
        print(os.listdir('bios/static/media/images'))
        form = request.FILES

        # if 'photo' in form and form['photo'].name.split('.')[-1] != 'jpeg':
        #     messages.error(request, 'The wrong format detected! Use this link to convert your profile image https://cloudconvert.com/jpeg-converter') 


        existed_file = Student.objects.filter(name="{}_{}".format(request.user.first_name,request.user.last_name))
        print(existed_file)
        print('photo' in request.FILES, 'bio_ppt' in request.FILES)

        if not existed_file:
            print("Creating new object!!!")
            file, _ = Student.objects.update_or_create(
                name = "{}_{}".format(request.user.first_name,request.user.last_name),
                defaults = {
                    "photo" : request.FILES['photo'] if 'photo' in request.FILES else None,
                    "bio_ppt" : request.FILES['bio_ppt'] if 'bio_ppt' in request.FILES else None, 
                }
            )
            file.save()
        else:
            existed_file = Student.objects.get(name="{}_{}".format(request.user.first_name,request.user.last_name))
            print("Updating existed object!!!", os.listdir('bios/static/media/images'))
            if 'photo' in request.FILES:
                existed_file.photo.delete()
            if 'bio_ppt' in request.FILES:
                existed_file.bio_ppt.delete()
            # existed_file.delete()
            print(os.listdir('bios/static/media/images'))
            # if existed_file.photo:
            #     print("hell yes")
            #     existed_file.photo.delete()
            #     print(os.listdir('bios/static/media/images'))
            #     # print("{}_{}.jpeg".format(request.user.first_name,request.user.last_name) in os.listdir('bios/static/media/images'))
            #     if os.path.exists('bios/static/media/images/{}_{}.jpeg'.format(request.user.first_name,request.user.last_name)):
            #         os.remove("bios/static/media/images/{}_{}.jpeg".format(request.user.first_name,request.user.last_name))
            #         print("PHOTO REMOVED!!!")
            if os.path.exists('bios/static/media/images/{}_{}.jpeg'.format(request.user.first_name,request.user.last_name)) and "photo" in request.FILES:
                os.remove("bios/static/media/images/{}_{}.jpeg".format(request.user.first_name,request.user.last_name))
                print("PHOTO REMOVED!!!")

            # if existed_file.bio_ppt:
            #     print("hell no")
            #     existed_file.bio_ppt.delete()
            #     print(os.listdir('bios/static/media/bio_ppt'))
            #     # print("{}_{}.pdf".format(request.user.first_name,request.user.last_name) in os.listdir('bios/static/media/bio_ppt'))
            #     if os.path.exists('bios/static/media/bio_ppt/{}_{}.pdf'.format(request.user.first_name,request.user.last_name)):
            #         os.remove("bios/static/media/bio_ppt/{}_{}.pdf".format(request.user.first_name,request.user.last_name))
            #         print("BIO PPT REMOVED!!!")
            if os.path.exists('bios/static/media/bio_ppt/{}_{}.pdf'.format(request.user.first_name,request.user.last_name)) and "bio_ppt" in request.FILES:
                os.remove("bios/static/media/bio_ppt/{}_{}.pdf".format(request.user.first_name,request.user.last_name))
                print("BIO PPT REMOVED!!!")
            
            
            # rename the file
            for filename, file in form.items():
                print('======================')
                print(filename, request.FILES[filename].name)
                if request.FILES[filename].name.split('.')[-1] == 'jpeg':
                    request.FILES[filename].name = "{}_{}.jpeg".format(request.user.first_name,request.user.last_name)
                else:
                    request.FILES[filename].name = "{}_{}.pdf".format(request.user.first_name,request.user.last_name)
                print(filename, request.FILES[filename].name)

            # print(request.FILES['photo'].name)
            file, _ = Student.objects.update_or_create(
                name = "{}_{}".format(request.user.first_name,request.user.last_name),
                defaults = {
                    "photo" : request.FILES['photo'] if 'photo' in request.FILES else None,
                    "bio_ppt" : request.FILES['bio_ppt'] if 'bio_ppt' in request.FILES else None, 
                }
            )
            file.save()
        return HttpResponseRedirect("/{}".format(request.user.first_name+'_'+request.user.last_name))
    else:
        form = FileUpload()
        return render(request, "bios/upload.html", {"form" : form})
        
    
    
    # try:
    #     if request.method == "POST":
    #         print(request.user.last_name, request.user.first_name)
    #         form = FileUpload(request.POST, request.FILES)
    #         form.name = "{}_{}".format(request.user.first_name, request.user.last_name)
    #         print(form.is_valid())
    #         if form.is_valid():
    #             form.save()
    #         return HttpResponseRedirect("/")
    #     else:
    #         form = FileUpload()
    #         return render(request, "bios/upload.html", {"form" : form})
    # except:
    #     raise("CHECK YOUR FILE FORMAT!!")

def edit(request, name):
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
    print(skill_init)

    # initial industries
    industries = person.industry.split(',')
    industry_init = []
    for ins in industries:
        if 'N/A' in ins:
            continue
        flag = 0
        for i in range(len(ins)):
            if ins[i].isdigit() or ins[i] == '(':
                flag = i
                break
        if flag != 0:
            industry_init.append(ins[:flag-1].strip())
            print("INDUSTRY ****>", industry_init)
            preselect_dict['id_industry_{}'.format(tmp2.index(ins[:flag-1].strip()))] = ''.join(ins.strip().split(" ")[-2:])
    print(industry_init)

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
    print(tech_init)

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
        print(domain_init)

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
            level = i[i_].split(' ')[-1]
            if level.isdigit():
                for j in range(len(i[i_])):
                    if i[i_][j].isdigit():
                        flag = j
                        break
                print("{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level]))
                i[i_] = "{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level])
            else:
                i[i_] = "{} ({})".format(i[i_], EXPERIENCE_RUBRIC['1'])
    
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

        uni = form.get('university')
        if not uni:
            uni = ' '

        major = form.get('major')
        if not major:
            major = ' '

        c = form.get('client')
        if not c:
            c = 'N/A'
        intro = form.get('intro')
        if not intro:
            intro = 'N/A'
        t, _ = BioInfo.objects.update_or_create(
            name = name,
            defaults={
                "location" : l, 
                "skill" : ', '.join(s),
                "technique" : ', '.join(tech), 
                "university": uni,
                "major": major,
                "industry" : ', '.join(i), 
                "client" : c, 
                "intro" : intro,
                "business_domain" : ', '.join(d)
            }
        )
        t.save()
        
        return HttpResponseRedirect("/{}".format(name))      
    else:
        form = EditProfile(initial={'skill' : skill_init,
                                    'industry' : industry_init,
                                    'technique' : tech_init, 
                                    'client' : person.client,
                                    'intro' : person.intro,
                                    'domain':domain_init,
                                    'university':person.university,
                                    'major': person.major,
                                    })
        return render(request, "bios/edit.html", {"form":form,
                                                  "person":person,
                                                  "preselect":preselect_dict})

def error_404(request, exception):
        data = {}
        return render(request,'certman/404.html', data)

def dashboard(request):
    return render(request, 'bios/dashboard.html')
        
