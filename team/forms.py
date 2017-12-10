from django import forms
from tpoSiteApp.choices import *

forms.DateInput.input_type="date"
forms.DateTimeInput.input_type="datetime-local" 
class SlotDefine(forms.Form):
	result_date = forms.DateField(label = "Result Date",widget = forms.TextInput(attrs ={'class' : 'datepicker'}))
	slot_number = forms.ChoiceField(label = "Slot No.:",choices = slot_types)
	slot_limit = forms.IntegerField(label = "Slot limit:")


class Notification(forms.Form):

	allowed_students = forms.ChoiceField(choices = user_types[0:2],label = "Notication for:")
	content = forms.CharField(widget = forms.Textarea , label = "content")


class Service(forms.Form):
	name = forms.CharField(label = 'Name:')
	description = forms.CharField(widget = forms.Textarea,label = "Description:")
	service_date = forms.DateField(label = "Date:")
	service_time = forms.TimeField(label = "Time:")
	payment = forms.IntegerField(label = "Cost:")


class willForm(forms.Form):
	company_id = forms.IntegerField(label = "company_id")
	course = forms.ChoiceField(label = 'Course',choices = courses)
	typ = forms.CharField(label = 'Type')
	exam_date = forms.DateField(label = "Exam Date")
	branch_issue_date = forms.DateField(label = "Branch Issue Date")
	willingness_deadline = forms.DateField(label = "WillingNess Deadline")
	result_date = forms.DateField(label = "Result Date")
	slt_number = forms.ChoiceField(label = "Slot No.",choices = [(0,0),(1,1),(2,2),(3,3)])

class MemberSignUpForm(forms.Form):
	email = forms.EmailField(label = 'Email  ')
	password = forms.CharField(label = 'Password',widget = forms.PasswordInput())
	name = forms.CharField(label = "Name")
	mobile = forms.CharField(label = 'Mobile No.')
	department = forms.ChoiceField(label = 'Department',choices = depts,required = False)
	designation = forms.CharField(label = 'Designation')