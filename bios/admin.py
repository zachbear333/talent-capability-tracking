from distutils.log import error
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import BioInfo, Student
from django import forms
import pandas as pd

# Register your models here.

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES["csv_upload"]
            error_lst = []
            # file_data = pd.read_csv(csv_file)
            df = pd.read_csv(csv_file)
            df = df.fillna('N/A')
            for i, row in df.iterrows():
                # try:
                created = BioInfo.objects.update_or_create(
                    name = row['name'],
                    email = row['email'],
                    position = row['position'],
                    location = row['location'], 
                    skill = row['skill'],
                    technique = row['technique'],
                    application = row['Applications'],
                    ds_skill = row['DS Skills'],
                    program_skill = row['Programming Skills'],
                    tech_stack = row['Techstack'],
                    industry = row['industry'],
                    business_domain = row['business_domain'],
                    university = row['university'],
                    major = row['major'],
                    degree = row['degree'],
                    university2 = row['university2'],
                    major2 = row['major2'],
                    degree2 = row['degree2'],
                    university3 = row['university3'],
                    major3 = row['major3'],
                    degree3 = row['degree3'],
                    intro =  row['intro'],
                )

                    # created_ = Student.objects.update_or_create(
                    #     name = row['name'],
                    #     photo = 'images/logo2.png',
                    #     bio_ppt = 'bio_ppt/Blank_Bio.pdf',
                    # )
                # except:
                #     error_lst.append(row['name'])
                # print(error_lst)
        form = CsvImportForm()
        data = {"form" : form}
        return render(request, 'admin/csv_upload.html', data)
    

admin.site.register(BioInfo, UserAdmin)