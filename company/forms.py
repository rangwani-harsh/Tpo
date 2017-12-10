from django import forms
from tpoSiteApp.choices import *
forms.DateInput.input_type="date"
#forms.DateTimeInput.input_type="datetime-local" 
class CompanySignUpForm(forms.Form):
	email = forms.EmailField(label = 'Email')
	password = forms.CharField(label = 'Password',widget = forms.PasswordInput())
	name = forms.CharField(label = "Company Name")
	ppt_date = forms.DateField(label = 'PPT Date')
	interview_date = forms.DateField(label = 'Interview Date')
	package_take_home = forms.IntegerField(label = 'Take Home Package',min_value = 0)
	package_ctc = forms.IntegerField(label = 'CTC Package',min_value = 0)
	jd = forms.CharField(widget = forms.Textarea)


class createWillingnessForm(forms.Form):
	course = forms.ChoiceField(label = 'Course',choices = courses )
	typ = forms.CharField(label = 'Type')
	gpa = forms.FloatField(label = "GPA Req.",max_value = 10.0,min_value = 0.0)
	
