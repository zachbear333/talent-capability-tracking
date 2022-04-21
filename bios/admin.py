from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import BioInfo
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
            print(len(csv_data))
            for i, x in enumerate(csv_data):
                if i == 0 or i == len(csv_data) - 1:
                    continue
                fields = x.split(',')
                # print(i, fields[4], fields[1])
                created = BioInfo.objects.update_or_create(
                    name = fields[3],
                    email = fields[1],
                    position = fields[2].replace(';', ','),
                    location = 'Columbia, MD (HQ)',
                    industry = 'N/A',
                    skill = 'N/A',
                    technique = 'N/A',
                    client = 'N/A',
                    university = 'N/A',
                    major = 'N/A',
                    intro = 'N/A',
                    business_domain = 'N/A',
                )

        form = CsvImportForm()
        data = {"form" : form}
        return render(request, 'admin/csv_upload.html', data)
    

admin.site.register(BioInfo, UserAdmin)