from django import forms
from .choices import *
forms.DateInput.input_type="date"
forms.DateTimeInput.input_type="datetime-local" 
class LoginForm(forms.Form):
	email = forms.EmailField(label = 'Enter your email id')
	password = forms.CharField(label = "Password",widget = forms.PasswordInput())
	user = forms.ChoiceField(label = "User Type",choices = user_types)

class ChangePassForm(forms.Form):
	email = forms.EmailField(label = 'Enter your email id')
	password = forms.CharField(label = "Password",widget = forms.PasswordInput())
	new_password = forms.CharField(label = "New Password",widget = forms.PasswordInput())
	confirm_password = forms.CharField(label = "Retype New Password",widget = forms.PasswordInput())
	user = forms.ChoiceField(label = "User Type",choices = user_types)


class StudentSignUpForm(forms.Form):

	email = forms.EmailField(label = 'Email')
	password = forms.CharField(label = "Password",widget = forms.PasswordInput())
	name = forms.CharField(label = 'Full Name')
	fathers_name = forms.CharField(label = "Father's name")
	mothers_name = forms.CharField(label = "Mother's name")
	
	#roll_no = forms.CharField(label = 'Roll No.')
	#department = forms.ChoiceField(label = 'Department',choices = depts)
	#course = forms.ChoiceField(label = 'Course',choices = courses )
	DOB = forms.DateField(label = 'DateOfBirth')
	category = forms.CharField(label = 'Category')
	gender = forms.CharField(label = 'Gender')
	address = forms.CharField(widget = forms.Textarea)


class CompanySignUpForm(forms.Form):
	name = forms.CharField(label = 'Company Name')
	email = forms.EmailField(label = 'Email')
	password = forms.CharField(label = 'Password',widget = forms.PasswordInput())
	ppt_date = forms.DateField(label = 'PPT Date')
	interview_date = forms.DateField(label = 'Interview Date')
	package_take_home = forms.IntegerField(label = 'Take Home Package')
	package_ctc = forms.IntegerField(label = 'CTC Package')
	jd = forms.CharField(widget = forms.Textarea)


class MemberSignUpForm(forms.Form):
	email = forms.EmailField(label = 'Email  ')
	password = forms.CharField(label = 'Password',widget = forms.PasswordInput())
	name = forms.CharField(label = "Name")
	mobile = forms.CharField(label = 'Mobile No.')
	department = forms.ChoiceField(label = 'Department',choices = depts,required = False)
	designation = forms.CharField(label = 'Designation')

class AcademicDetailForm(forms.Form):
	semester = forms.IntegerField(max_value = 10,label = "Semester")
	roll_no = forms.CharField(label = 'Roll No.')
	department = forms.ChoiceField(label = 'Department',choices = depts)
	course = forms.ChoiceField(label = 'Course',choices = courses )
	summer_cgpa = forms.FloatField(label = 'Summer CGPA',required = False,min_value = 0.0,max_value = 10.0)
	sem_cgpa = forms.FloatField(label = 'Semester CGPA',min_value = 0.0,max_value = 10.0)
	backlogs = forms.IntegerField(label = "Backlogs",min_value = 0)



class ForumPost(forms.Form):
	title = forms.CharField(max_length = 30,label = 'Title Of the Post')
	content = forms.CharField(widget = forms.Textarea)


class SlotDefine(forms.Form):
	result_date = forms.DateField(widget = forms.TextInput(attrs ={'class' : 'datepicker'}))
	slot_limit = forms.IntegerField()


class Notification(forms.Form):

	allowed_students = forms.MultipleChoiceField(choices = user_types)
	content = forms.CharField(widget = forms.TextInput() , label = "content")













