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

            for i, x in enumerate(csv_data):
                if i == 0:
                    continue
                fields = x.split(',')
                created = BioInfo.objects.update_or_create(
                    name = fields[1].replace(';', ','),
                    email = fields[2].replace(';', ','),
                    position = fields[3].replace(';', ','),
                    location = fields[4].replace(';', ','),
                    industry = fields[5].replace(';', ','),
                    skill = fields[8].replace(';', ','),
                    technique = fields[9].replace(';', ','),
                    client = fields[10].replace(';', ','),
                    intro = fields[11],
                )

        form = CsvImportForm()
        data = {"form" : form}
        return render(request, 'admin/csv_upload.html', data)
    

admin.site.register(BioInfo, UserAdmin)