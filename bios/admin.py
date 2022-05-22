from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import BioInfo, Student
from django import forms

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
            # file_data = pd.read_csv(csv_file)
            # print(file_data)
            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split('\n')
            error_lst = []
            print(len(csv_data))
            for i, x in enumerate(csv_data):
                print(i, x)
                if i == 0 or i == len(csv_data) - 1:
                    continue
                fields = x.split(',')
                try:
                    created = BioInfo.objects.update_or_create(
                        # load existing db from csv file
                        name = fields[0].replace(';', ','),
                        email = fields[1].replace(';', ','),
                        position = fields[2].replace(';', ','),
                        location = fields[3].replace(';', ','), 
                        skill = fields[4].replace(';', ','),
                        technique = fields[5].replace(';', ','),
                        industry = fields[6].replace(';', ','),
                        business_domain = fields[7].replace(';', ','),
                        university = fields[8].replace(';', ','),
                        major = fields[9].replace(';', ','),
                        degree = fields[10].replace(';', ','),
                        university2 = fields[11].replace(';', ','),
                        major2 = fields[12].replace(';', ','),
                        degree2 = fields[13].replace(';', ','),
                        university3 = fields[14].replace(';', ','),
                        major3 = fields[15].replace(';', ','),
                        degree3 = fields[16].replace(';', ','),
                        intro =  fields[17].replace(';', ','),
                        # first run
                        # name = fields[3],
                        # email = fields[1],
                        # position = fields[2].replace(';', ','),
                        # location = 'Columbia, MD (HQ)',
                        # industry = 'N/A',
                        # skill = 'N/A',
                        # technique = 'N/A',
                        # degree = 'N/A',
                        # university = 'N/A',
                        # major = 'N/A',
                        # degree2 = 'N/A',
                        # university2 = 'N/A',
                        # major2 = 'N/A',
                        # degree3 = 'N/A',
                        # university3 = 'N/A',
                        # major3 = 'N/A',
                        # intro = 'N/A',
                        # business_domain = 'N/A',
                    )

                    created_ = Student.objects.update_or_create(
                        name = fields[3],
                        photo = 'images/logo2.png',
                        bio_ppt = 'bio_ppt/Blank_Bio.pdf',
                    )
                except:
                    error_lst.append(i)
        print(error_lst)
        form = CsvImportForm()
        data = {"form" : form}
        return render(request, 'admin/csv_upload.html', data)
    

admin.site.register(BioInfo, UserAdmin)