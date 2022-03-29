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

SKILL_RUBRIC = {
    "1" : "Unfamiliar",
    "2" : "Novice",
    "3" : "Proficient",
    "4" : "Advanced",
    "5" : "Expert"
}

EXPERIENCE_RUBRIC = {
    "1" : "<1 YOE",
    "2" : "1-3 YOE",
    "3" : "4-5 YOE",
    "4" : "5-10 YOE",
    "5" : ">10 YOE" 
}

REVERSE_RUBRIC = {
    "Unfamiliar" : "1",
    "Novice" : "2",
    "Proficient" : "3",
    "Advanced" : "4",
    "Expert" : "5",
    "<1YOE" : "1",
    "1-3YOE" : "2",
    "4-5YOE" : "3",
    "5-10YOE" : "4",
    ">10YOE" : "5"  
}

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
        form = request.POST
        n = form.get('name')
        e = form.get('email')
        p = form.get('position')
        l = form.get('location')

        s = form.getlist('skill')
        if not s:
            s = ['N/A']
        for i in range(len(s)):
            level = s[i].split(' ')[-1]
            for j in range(len(s[i])):
                if s[i][j].isdigit():
                    flag = j
                    break
            print("{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level]))
            s[i] = "{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level])

        tech = form.getlist('technique')
        if not tech:
            tech = ['N/A']
        for i in range(len(tech)):
            level = tech[i].split(' ')[-1]
            for j in range(len(tech[i])):
                if tech[i][j].isdigit():
                    flag = j
                    break
            print("{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level]))
            tech[i] = "{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level])

        i = form.getlist('industry')
        if not i:
            i = ['N/A']
        for i_ in range(len(i)):
            level = i[i_].split(' ')[-1]
            for j in range(len(i[i_])):
                if i[i_][j].isdigit():
                    flag = j
                    break
            print("{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level]))
            i[i_] = "{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level])


        c = form.get('client')
        if not c:
            c = 'N/A'
        intro = form.get('intro')
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
    print(person.skill)
    # initial skills
    skills = person.skill.split(',')
    skill_init = []
    preselect_dict = {}
    for s in skills:
        # print(' '.join(s.strip().split(" ")[:-1]))
        # skill_init.append(' '.join(s.strip().split(" ")[:-1]))
        for i in range(len(s)):
            if s[i].isdigit() or s[i] == '(':
                flag = i
                break
        # print(flag)
        if flag != 0:
            skill_init.append(s[:flag-1].strip())
        # else:
        #     skill_init.append(' '.join(s.strip().split(" ")[:-1]))
        print("SKILL ****>", skill_init)
        # preselect_dict[' '.join(s.strip().split(" ")[:-1])] = s.strip().split(" ")[-1]
        preselect_dict[s[:flag-1]] = ''.join(s.strip().split(" ")[-1])
    print(skill_init)
    # initial industries
    industries = person.industry.split(',')
    industry_init = []
    for ins in industries:
        for i in range(len(ins)):
            if ins[i].isdigit() or ins[i] == '(':
                flag = i
                break
        if flag != 0:
            industry_init.append(ins[:flag-1].strip())
        print("INDUSTRY ****>", industry_init)
        # industry_init.append(' '.join(ins.strip().split(" ")[:-2]))
        # preselect_dict[' '.join(ins.strip().split(" ")[:-2])] = ' '.join(ins.strip().split(" ")[-2:])
        preselect_dict[ins[:flag-1]] = ''.join(ins.strip().split(" ")[-2:])
    print(industry_init)

    # initial techniques
    techniques = person.technique.split(',')
    tech_init = []
    for tech in techniques:
        for i in range(len(tech)):
            if tech[i].isdigit() or tech[i] == '(':
                flag = i
                break
        if flag != 0:
            tech_init.append(tech[:flag-1].strip())
        print("TECH ****>", tech_init)
        # tech_init.append(' '.join(tech.strip().split(" ")[:-1]))
        # preselect_dict[' '.join(tech.strip().split(" ")[:-1])] = tech.strip().split(" ")[-1]
        preselect_dict[tech[:flag-1]] = ''.join(tech.strip().split(" ")[-1])
    print(tech_init)
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
            s = ['N/A']
        for i in range(len(s)):
            level = s[i].split(' ')[-1]
            for j in range(len(s[i])):
                if s[i][j].isdigit():
                    flag = j
                    break
            # print(flag, s[i], s[i][:flag])
            # print("ahahahahhahah {} ({})".format(' '.join(s[i].split(' ')[:j-1]), SKILL_RUBRIC[level]))
            print("{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level]))
            s[i] = "{} ({})".format(s[i][:flag-1], SKILL_RUBRIC[level])

        tech = form.getlist('technique')
        if not tech:
            tech = ['N/A']
        for i in range(len(tech)):
            level = tech[i].split(' ')[-1]
            for j in range(len(tech[i])):
                if tech[i][j].isdigit():
                    flag = j
                    break
            print("{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level]))
            tech[i] = "{} ({})".format(tech[i][:flag-1], SKILL_RUBRIC[level])

        i = form.getlist('industry')
        if not i:
            i = ['N/A']
        for i_ in range(len(i)):
            level = i[i_].split(' ')[-1]
            for j in range(len(i[i_])):
                if i[i_][j].isdigit():
                    flag = j
                    break
            print("{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level]))
            i[i_] = "{} ({})".format(i[i_][:flag-1], EXPERIENCE_RUBRIC[level])


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
                "industry" : ', '.join(i), 
                "client" : c, 
                "intro" : intro
            }
        )
        t.save()
        # form = EditProfile(request.POST)
        # if form.is_valid():
        #     l = form.cleaned_data['location']
        #     s = form.cleaned_data['skill']
        #     if not s:
        #         s = ['N/A']
        #     tech = form.cleaned_data['technique']
        #     if not tech:
        #         tech = ['N/A']
        #     i = form.cleaned_data['industry']
        #     if not i:
        #         i = ['N/A']
        #     c = form.cleaned_data['client']
        #     if not c:
        #         c = 'N/A'
        #     intro = form.cleaned_data['intro']
        #     if not intro:
        #         intro = 'N/A'
            
        #     t, _ = BioInfo.objects.update_or_create(
        #         name = name,
        #         defaults={
        #             "location" : l, 
        #             "skill" : ', '.join(s),
        #             "technique" : ', '.join(tech), 
        #             "industry" : ', '.join(i), 
        #             "client" : c, 
        #             "intro" : intro
        #         }
        #     )
        #     t.save()
        
        
        return HttpResponseRedirect("/")      
    else:
        form = EditProfile(initial={'skill' : skill_init,
                                    'industry' : industry_init,
                                    'technique' : tech_init, 
                                    'client' : person.client,
                                    'intro' : person.intro})
        return render(request, "bios/edit.html", {"form":form,
                                                  "person":person,
                                                  "preselect":preselect_dict})

def error_404(request, exception):
        data = {}
        return render(request,'certman/404.html', data)
        
