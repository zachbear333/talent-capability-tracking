# show http requests, and the things showing up on the website

from ast import If
from operator import itemgetter
from re import search
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import BioInfo
from .forms import CreateNewProfile, EditProfile, FileUpload, testform
# from django.views import View
from django.core.files.storage import FileSystemStorage
# from io import BytesIO
from django.template.loader import get_template
# from xhtml2pdf import pisa

# Create your views here.
# def pdf_view(request):
#     fs = FileSystemStorage()
#     filename = ''
#     if fs.exists(filename):
#         with fs.open(filename) as pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="mypdf.pdf"' #user will be prompted display the PDF in the browser
#             return response
#     else:
#         return HttpResponseNotFound('The requested pdf was not found in our server.')



def test(request):
    if request.method == "POST":
        form = testform(request.POST)
        if form.is_valid():
            print('yse')
        # return HttpResponseRedirect("/%i" %t.id)
        return HttpResponseRedirect("/upload_img/")
    else:    
        form = testform()
    # return render(request, "bios/create.html", {"form" : form})
    return render(request, 'bios/test.html', {"form" : form})


def index(response, name):
    item = BioInfo.objects.get(name=name)
    # item = dict(item.__dict__.items())
    return render(response, 'bios/bio-info.html', {"people":item})

def distinct_features():
    skill_res, industry_res, tech_res = [], [], []
    people_all = BioInfo.objects.all()
    for person in people_all:
        skill_lst = person.skill.split(',')
        industry_lst = person.industry.split(',')
        tech_lst = person.technique.split(',')
        # deal with skill
        for skill in skill_lst:
            skill = skill.strip()
            if skill in skill_res or not skill:
                continue
            skill_res.append(skill)

        # deal with industry
        for industry in industry_lst:
            industry = industry.strip()
            if industry in industry_res or not industry:
                continue
            industry_res.append(industry)
        
        # deal with technology
        for tech in tech_lst:
            tech = tech.strip()
            if tech in tech_res or not tech:
                continue
            tech_res.append(tech)

    return skill_res, industry_res, tech_res



def home(request):
    
    position_query = request.GET.get('position-dropdown')
    location_query = request.GET.get('location-dropdown')
    skill_query = request.GET.getlist('skill-dropdown')
    industry_query = request.GET.getlist('industry-dropdown')
    tech_query = request.GET.getlist('tech-dropdown')
    search_query = request.GET.get('search-input')

    people = BioInfo.objects.all()
    position_dist = BioInfo.objects.values('position').distinct()
    location_dist = BioInfo.objects.values('location').distinct()
    # skill_dist = BioInfo.objects.values('skill').distinct()
    # industry_dist = BioInfo.objects.values('industry').distinct()
    skill_dist, industry_dist, tech_dist = distinct_features()

    if position_query:
        people = people.filter(position=position_query)
    if location_query:
        people = people.filter(location=location_query)

    if skill_query:
        for i in skill_query:
            people = people.filter(skill__contains=i)
    if industry_query:
        for i in industry_query:
            people = people.filter(industry__contains=i)
    if tech_query:
        for i in tech_query:
            people = people.filter(technique__contains=i)

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
                                              })   

def create(request):
    if request.method == "POST":
        form = CreateNewProfile(request.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            e = form.cleaned_data['email']
            p = form.cleaned_data['position']
            l = form.cleaned_data['location']
            s = form.cleaned_data['skill']
            if not s:
                s = ['N/A']
            tech = form.cleaned_data['technique']
            if not tech:
                tech = ['N/A']
            i = form.cleaned_data['industry']
            if not i:
                i = ['N/A']
            c = form.cleaned_data['client']
            if not c:
                c = 'N/A'
            intro = form.cleaned_data['intro']
            if not intro:
                intro = 'N/A'
            
            t, _ = BioInfo.objects.update_or_create(
                name = n,
                defaults={
                    "email" : e, 
                    "position" : p, 
                    "location" : l, 
                    "skill" : ', '.join(s),
                    "technique" : ', '.join(tech), 
                    "industry" : ', '.join(i), 
                    "client" : c, 
                    "intro" : intro
                }
            )
            t.save()
        # return HttpResponseRedirect("/%i" %t.id)
        return HttpResponseRedirect("/upload_img/")
    else:    
        form = CreateNewProfile()
    return render(request, "bios/create.html", {"form" : form})

def upload_img(request):
    try:
        if request.method == "POST":
            form = FileUpload(request.POST, request.FILES)
            # print(request.FILES[0].name)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect("/")
        else:
            form = FileUpload()
            return render(request, "bios/upload.html", {"form" : form})
    except:
        raise("CHECK YOUR FILE FORMAT!!")

def edit(request, name):
    person = BioInfo.objects.get(name=name)
    skills = person.skill.split(',')
    industries = person.industry.split(',')
    techniques = person.technique.split(',')
    # pre-select skills
    for i in range(len(skills)):
        skills[i] = skills[i].strip()
    # pre-select industry
    for i in range(len(industries)):
        industries[i] = industries[i].strip()
    # pre-select technique
    for i in range(len(techniques)):
        techniques[i] = techniques[i].strip()   
    if request.method == "POST":
        form = EditProfile(request.POST)
        if form.is_valid():
            # print(form.is_valid())
            # n = form.cleaned_data['name']
            # e = form.cleaned_data['email']
            # p = form.cleaned_data['position']
            l = form.cleaned_data['location']
            s = form.cleaned_data['skill']
            if not s:
                s = ['N/A']
            tech = form.cleaned_data['technique']
            if not tech:
                tech = ['N/A']
            i = form.cleaned_data['industry']
            if not i:
                i = ['N/A']
            c = form.cleaned_data['client']
            if not c:
                c = 'N/A'
            intro = form.cleaned_data['intro']
            if not intro:
                intro = 'N/A'
            
            t, _ = BioInfo.objects.update_or_create(
                name = name,
                defaults={
                    "location" : l, 
                    "skill" : ', '.join(s),
                    "technique" : ', '.join(tech), 
                    "industry" : ', '.join(i), 
                    "client" : c, 
                    "intro" : intro
                }
            )
            t.save()
        return HttpResponseRedirect("/")      
    else:
        form = EditProfile(initial={'skill' : skills,
                                    'industry' : industries,
                                    'technique' : techniques, 
                                    'client' : person.client,
                                    'intro' : person.intro})
        # print(person.skill.split(','))
        return render(request, "bios/edit.html", {"form":form,
                                                  "person":person})

def error_404(request, exception):
        data = {}
        return render(request,'certman/404.html', data)
        
