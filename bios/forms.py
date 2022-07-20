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

### APPLICATION CHOICE
APPLICATION_SUBCATEGORY = {
    'Analytics Application' : ['Demand Forcasting', 'Fraud detection', 'Image processing', 'Insight Generation',
                                'Inventory/Space Management', 'LTV', 'Personalization', 'Pricing optimization',
                                'Product Assortment', 'Recommender System', 'Supplier chain'],
    'Digital Analystics' : ['Adobe Analytics', 'Digital Analytics', 'Google Analytics', 'Search Engine Optimization - SEO',
                            'Web development'],
    'Sales and Marketing' : ['Campaign Management', 'Customer AcqusitioN', 'Customer retention', 'Customer Segmentation',
                            'Marketing Mix Modeling - MMM', 'Market Structure Analysis - MSA', 'Multi-touch attribution - MTA'] 
}                 
APPLICATION_CHOICES = []
for sub_cate in APPLICATION_SUBCATEGORY:
    for choices in APPLICATION_SUBCATEGORY[sub_cate]:
        APPLICATION_CHOICES.append((choices, choices))

### DS SKILL CHOICE
DSSKILL_SUBCATEGORY = {
    'NLP' : ['Feature Creation', 'Sentiment Analysis', 'Text Reasoning', 'Text Summarization', 'Topic Modeling'],
    'Optimization' : ['Graph Analytics', 'Optimization', 'Simulation'],
    'Statistics/ML' : ['A/B Test', 'Bayesian Modelling', 'Causal Inference', 'Clustering', 'Deep Learning',
                       'Experimental Design', 'Regression & Classification', 'Reinforcement Learning',
                       'Spatial Statistics', 'Survival analysis', 'Time Series']
}
DS_SKILL_CHOICES = []
for sub_cate in DSSKILL_SUBCATEGORY:
    for choices in DSSKILL_SUBCATEGORY[sub_cate]:
        DS_SKILL_CHOICES.append((choices, choices))

### PROGRAMMING SKILL CHOICE
PROGRAM_SKILL_SUBCATEGORY = {
    'Optimization Programming' : ['Cplex', 'Gurobi'],
    'Parallel Programming' : ['OpenCL', 'CUDA'],
    'Programming Language' : ['C/C++/C#/.NET', 'Java', 'Matlab', 'PySpark', 'Python', 'R',
                              'SAS', 'Scala', 'Spark', 'SQL', 'Tensorflow/Pytorch', 'HTML', 'Javascript'],
    # 'Web Programming' : ['HTML', 'Javascript'] 
}
PROGRAM_SKILL_CHOICES = []
for sub_cate in PROGRAM_SKILL_SUBCATEGORY:
    for choices in PROGRAM_SKILL_SUBCATEGORY[sub_cate]:
        PROGRAM_SKILL_CHOICES.append((choices, choices))

### TECHSTACK CHOICE
TECHSTACK_SUBCATEGORY = {
    'BI' : ['Dash', 'Dashboard Design', 'Data Visualization', 'PowerBI', 'Qlik', 'R Shiny', 'Streamlit', 'Tableau'],
    'Operation' : ['Airflow', 'Automation & Job Scheduling', 'Deployment', 'MLOps', 'Process Management'],
    'Cloud Computing Service' : ['AWS', 'Azure', 'Databricks', 'GCP', 'Snowflakes'],
    'Data' : ['3rd Party Data', 'Database Design'],
    'Collabration' : ['GIT', 'Jira', 'Project Management', 'GitHub']
}
TECHSTACK_CHOICES = []
for sub_cate in TECHSTACK_SUBCATEGORY:
    for choices in TECHSTACK_SUBCATEGORY[sub_cate]:
        TECHSTACK_CHOICES.append((choices, choices))

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

DEGREE_CHOICE = [
    ('B.A.', 'B.A.'),
    ('B.S.', 'B.S.'),
    ('M.S.', 'M.S.'),
    ('PhD', 'PhD'),
    ('Other', 'Other'),
]

class CreateNewProfile(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    nickname = forms.CharField(label="Nickname", max_length=200)
    email = forms.CharField(label="Email", max_length=200)
    # position = forms.CharField(label="Position", max_length=100)
    position = forms.CharField(label="Position", widget=forms.Select(choices=POSITION_CHOICES))
    location = forms.CharField(label="Location", widget=forms.Select(choices=LOCATION_CHOICES))
    domain = forms.MultipleChoiceField(required=False, label="Business Domain", choices=DOMAIN_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'domain-test',
    'onchange':'checkbox(event);',
    }))

    #skill = forms.MultipleChoiceField(required=False, label="Areas of Expertise", choices=SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'onchange':'test(event);',}))
    skill = forms.MultipleChoiceField(required=False, label="Areas of Expertise", choices=SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'skill-test',
    'onchange':'checkbox(event);',
    }))
    technique = forms.MultipleChoiceField(required=False, label="Techniques", choices=TECHNICUQE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'tech-test',
    'onchange':'checkbox(event);',    
    }))
    industry = forms.MultipleChoiceField(required=False, label="Industry Experiences", choices=INDUSTRIES_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'checkbox(event);',      
    }))
    university = forms.CharField(required=False, label="University", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    major = forms.CharField(required=False, label="Major", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))

    # client = forms.MultipleChoiceField(label="Blend Client", choices=CLIENT_CHOICES, widget=forms.CheckboxSelectMultiple)
    degree = forms.CharField(required=False, label="Degree", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    intro = forms.CharField(required=False, label="Intro", widget=forms.Textarea(attrs={
                                                                'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:100px;'}))

class EditProfile(forms.Form):
    location = forms.CharField(label="Location", widget=forms.Select(choices=LOCATION_CHOICES))
    domain = forms.CharField(label="Business Domain", widget=forms.Select(choices=DOMAIN_CHOICES))
    application = forms.MultipleChoiceField(required=False, label="Application", choices=APPLICATION_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'test(event);',      
    }))
    ds_skill = forms.MultipleChoiceField(required=False, label="DS Skill", choices=DS_SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'test(event);',      
    }))
    program_skill = forms.MultipleChoiceField(required=False, label="Programming Skill", choices=PROGRAM_SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'test(event);',      
    }))
    tech_stack = forms.MultipleChoiceField(required=False, label="Techstack", choices=TECHSTACK_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'test(event);',      
    }))
    skill = forms.MultipleChoiceField(required=False, label="Areas of Expertise", choices=SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'test(event);',      
    }))
    technique = forms.MultipleChoiceField(required=False, label="Techniques", choices=TECHNICUQE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'test(event);',  
    }))
    industry = forms.MultipleChoiceField(required=False, label="Industry Experiences", choices=INDUSTRIES_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'industry-test',
    'onchange':'test(event);',  
    }))
    domain = forms.MultipleChoiceField(required=False, label="Business Domain", choices=DOMAIN_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
    'class':'domain-test',
    'onchange':'test(event);',  
    }))
    university = forms.CharField(required=False, label="University", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    major = forms.CharField(required=False, label="Major", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    degree = forms.CharField(required=False, label="Degree", widget=forms.Select(choices=DEGREE_CHOICE))
    
    
    university_2 = forms.CharField(required=False, label="University2", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    major_2 = forms.CharField(required=False, label="Major2", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))

    # client = forms.MultipleChoiceField(label="Blend Client", choices=CLIENT_CHOICES, widget=forms.CheckboxSelectMultiple)
    degree_2 = forms.CharField(required=False, label="Degree", widget=forms.Select(choices=DEGREE_CHOICE)) 

    university_3 = forms.CharField(required=False, label="University3", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    major_3 = forms.CharField(required=False, label="Major3", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))

    # client = forms.MultipleChoiceField(label="Blend Client", choices=CLIENT_CHOICES, widget=forms.CheckboxSelectMultiple)
    degree_3 = forms.CharField(required=False, label="Degree", widget=forms.Select(choices=DEGREE_CHOICE))
    
    nickname = forms.CharField(required=False, label="Major2", max_length=400,
                                widget=forms.TextInput(attrs={
                                                             'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:25px;'}))
    
    intro = forms.CharField(required=False, label="Intro", widget=forms.Textarea(attrs={
                                                                'style' : 'width:100%;border: 1px solid grey; border-radius: 5px;height:100px;'}))


class testform(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    skill = forms.MultipleChoiceField(required=False, label="Areas of Expertise", choices=SKILL_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
        'class':'skill form-check-input',
        'onchange':'test(event);',
        }))



class FileUpload(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
