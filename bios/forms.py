from logging import PlaceHolder
from django import forms
from django.forms import BoundField, ModelForm
from .models import BioInfo, Student


LOCATION_CHOICES = [
    ('Columbia, MD (HQ)', 'Columbia, MD (HQ)'),
    ('New York, NY', 'New York, NY'),
    ('Denver, CO', 'Denver, CO'),
    ('India', 'India'),
    ('Remote', 'Remote')
]

SKILL_CHOICES = [
    ('Predictive Modeling', 'Predictive Modeling'),
    ('Machine Learning', "Machine Learning"),
    ('Deep Learning', "Deep Learning"),
    ('Natural Language Processing', 'Natural Language Processing'), 
    ('Recommendation System', "Recommendation System"),
    ('LTV', 'LTV'),
    ('Optimization', 'Optimization'),
    ('Markov Chain', 'Markov Chain'),
    ('Measurement', 'Measurement'),
    ('AB Testing', 'AB Testing'), 
    ('Business Intelligence', 'Business Intelligence'),
    ('Campaign Design / Execution', 'Campaign Design / Execution'), 
    ('Cloud Services', 'Cloud Services'),
    ('Customer Segmentation and Insights', 'Customer Segmentation and Insights'),
    ('Data Governence', 'Data Governence'),
    ('Data Visualization', 'Data Visualization'),
    ('Data Wrangling', 'Data Wrangling'),
    ('Data / Network Security', 'Data / Network Security'),
    ('Deployment', 'Deployment'),
    ('Digital Analytics', 'Digital Analytics'),
    ('Personalization', 'Personalization'),
    ('SEO', 'SEO'),
    ('Simulation', 'Simulation'),
    ('Time Series Analysis', 'Time Series Analysis'),
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
    ('Python', 'Python'),
    ('SQL', "SQL"),
    ('Spark', "Spark"),
    ('GCP', 'GCP'), 
    ('AWS', "AWS"),
    ('Databricks', 'Databricks'),
    ('R', 'R'),
    ('Snowflakes', 'Snowflakes'),
    ('Java', 'Java'),
    ('C/C++', 'C/C++')
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

LEVEL_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

class CreateNewProfile(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    email = forms.CharField(label="Email", max_length=200)
    # position = forms.CharField(label="Position", max_length=100)
    position = forms.CharField(label="Position", widget=forms.Select(choices=POSITION_CHOICES))
    location = forms.CharField(label="Location", widget=forms.Select(choices=LOCATION_CHOICES))
    skill = forms.MultipleChoiceField(required=False, label="Areas of Expertise", choices=SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'onclick':'test();',}))
    technique = forms.MultipleChoiceField(required=False, label="Techniques", choices=TECHNICUQE_CHOICES, widget=forms.CheckboxSelectMultiple)
    industry = forms.MultipleChoiceField(required=False, label="Industry Experiences", choices=INDUSTRIES_CHOICES, widget=forms.CheckboxSelectMultiple)
    # client = forms.MultipleChoiceField(label="Blend Client", choices=CLIENT_CHOICES, widget=forms.CheckboxSelectMultiple)
    client = forms.CharField(required=False, label="Client", max_length=400,
                                widget=forms.TextInput(attrs={'placeholder':'Seperate Clients by Comma.',
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    intro = forms.CharField(required=False, label="Intro", widget=forms.Textarea(attrs={
                                                                'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;'}))

class EditProfile(forms.Form):
    location = forms.CharField(label="Location", widget=forms.Select(choices=LOCATION_CHOICES))
    skill = forms.MultipleChoiceField(required=False, label="Areas of Expertise", choices=SKILL_CHOICES, widget=forms.CheckboxSelectMultiple)
    technique = forms.MultipleChoiceField(required=False, label="Techniques", choices=TECHNICUQE_CHOICES, widget=forms.CheckboxSelectMultiple)
    industry = forms.MultipleChoiceField(required=False, label="Industry Experiences", choices=INDUSTRIES_CHOICES, widget=forms.CheckboxSelectMultiple)
    client = forms.CharField(required=False, label="Client", max_length=400,
                                widget=forms.TextInput(attrs={'placeholder':'Seperate Clients by Comma.',
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    intro = forms.CharField(required=False, label="Intro", widget=forms.Textarea(attrs={
                                                                'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;'}))


class testform(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    skill = forms.MultipleChoiceField(required=False, label="Areas of Expertise", choices=SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
        'class':'skill-test',
        'onchange':'test(event);',
        }))
    level = forms.CharField(label="level", widget=forms.RadioSelect(choices=LEVEL_CHOICES, attrs={"id":'hidden'}))



class FileUpload(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
