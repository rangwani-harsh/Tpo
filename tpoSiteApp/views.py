# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import LoginForm,StudentSignUpForm,CompanySignUpForm,MemberSignUpForm,AcademicDetailForm,ChangePassForm
from .sessionController import isAuthenticated,authenticate,getUserType,deAuthenticate
from django.shortcuts import render
from django.contrib import messages
from django.db import connection
from django.utils.timezone import localtime,now
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

def Login(request):
	error = ""
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user_type = form.cleaned_data.get('user')
			cursor = connection.cursor()
			print type(user_type)
			if user_type == '0':
			
				cursor.execute("SELECT student_id,password FROM Student WHERE email = '"+email+"';")
			elif user_type == '1':
				
				cursor.execute("SELECT company_id,password FROM Company WHERE email = '"+email+"';")
			elif user_type == '2':
				cursor.execute("SELECT member_id,password FROM Team WHERE email = '"+email+"';")
			data = cursor.fetchone()
			connection.close()
			
			if data is not None:
				passw =  data[1]
				
				if check_password(password,passw):

					authenticate(request,data[0],int(user_type),email)
					return HttpResponseRedirect(reverse('indexPage'))
				else:
					messages.error(request,"The login credentials are incorrect")
			else:
				messages.error(request,"No such user is registered in the database")

			#return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))




	else:
		form = LoginForm()
		return render(request,'login.html',{'form':form})


	return render(request,'login.html',{'form':form})



def ChangePass(request):
	error = ""
	if request.method == "POST":
		form = ChangePassForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user_type = form.cleaned_data.get('user')
			new_password = form.cleaned_data.get('new_password')
			confirm_password = form.cleaned_data.get('confirm_password')

			cursor = connection.cursor()
			print type(user_type)
			if user_type == '0':
			
				cursor.execute("SELECT student_id,password FROM Student WHERE email = '"+email+"';")
			elif user_type == '1':
				
				cursor.execute("SELECT company_id,password FROM Company WHERE email = '"+email+"';")
			elif user_type == '2':
				cursor.execute("SELECT member_id,password FROM Team WHERE email = '"+email+"';")
			data = cursor.fetchone()
			connection.close()
			print data
			if data is not None:
				passw =  data[1]
				#if True:
				if check_password(password,passw):

					authenticate(request,data[0],int(user_type),email)
					cursor = connection.cursor()
					if user_type == '0':
						if new_password == confirm_password :
							cursor.execute("UPDATE   Student set password = '{}' WHERE email = '{}';".format(make_password(new_password),email))
						else:
							messages.error(request,"Passwords don't match")
					elif user_type == '1':
				
						if new_password == confirm_password :
							cursor.execute("UPDATE   Company set password = '{}' WHERE email = '{}';".format(make_password(new_password),email))
						else:
							messages.error(request,"Passwords don't match")
					elif user_type == '2':
						if new_password == confirm_password :
							cursor.execute("UPDATE   Team set password = '{}' WHERE email = '{}';".format(make_password(new_password),email))
						else:
							messages.error(request,"Passwords don't match")

					messages.success(request,"Password changed Successfully.")
					return HttpResponseRedirect(reverse('indexPage'))
				else:
					messages.error(request,"The login credentials are incorrect")
					ChangePass(request)
			else:
				messages.error(request,"No such user is registered in the database")

			#return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))




	else:
		form = ChangePassForm()
		return render(request,'changepass.html',{'form':form})

# Create your views here.

def companyLogin(request):
	error = ""
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			cursor = connection.cursor()
			cursor.execute("SELECT password FROM Company WHERE EMAIL = '"+email+"';")
			data = cursor.fetchone()
			connection.close()
			print data
			if data is not None:
				passw =  data[0]
				if passw == password:
					pass
				else:
					messages.error(request,"The login credentials are incorrect")
			else:
				messages.error(request,"No such user is registered in the database")






	else:
		form = LoginForm()
		return render(request,'login.html',{'form':form})


	return render(request,'login.html',{'form':form})



def studentSignUp(request):
	error = ""
	error = ""
	if request.method == "POST":
		form = StudentSignUpForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			name = form.cleaned_data.get('name')
			fathers_name = form.cleaned_data.get('fathers_name')
			mothers_name = form.cleaned_data.get('mothers_name')
			#roll_no = form.cleaned_data.get('roll_no')
			#department = form.cleaned_data.get('department')
			#course = form.cleaned_data.get('course')
			DOB = form.cleaned_data.get('DOB')
			category = form.cleaned_data.get('category')
			gender = form.cleaned_data.get('gender')
			address = form.cleaned_data.get('address')
			try:
				cursor = connection.cursor()
				cursor.execute("SELECT password FROM Student WHERE EMAIL = '"+email+"';")
				data = cursor.fetchone()
				if data is not None:
					messages.error(request,"You are already registered.")
				cursor.execute("INSERT INTO Student(name,email,password,father_name,mother_name,DOB,category,gender,address) VALUES ('"+name+"','"+email+"','"+make_password(password)+"','"+fathers_name+"','"+mothers_name+"','"+str(DOB)+"','"+category+"','"+gender+"','"+address+"');" )
				
					
				connection.close()
				return HttpResponseRedirect(reverse('indexPage'))
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")
			
		else:
			messages.error(request,"Please fill the signup form correctly")







	else:
		form = StudentSignUpForm()
		return render(request,'studentsignup.html',{'form':form})


	return render(request,'studentsignup.html',{'form':form})


def studentAcademicDetail(request):
	print "Hello"
	form = AcademicDetailForm()
	if request.method == "POST":
		print "POST"
		form = AcademicDetailForm(request.POST)
		user_cred = isAuthenticated(request)
		if form.is_valid() and user_cred:
			data_form = form.cleaned_data
			student_id = user_cred[0]
			try:
				cursor = connection.cursor()
				cursor.execute("DELETE FROM AcademicDetail WHERE (student_id = "+str(student_id)+") AND (semester = "+str(data_form['semester'])+");")
				cursor.execute("INSERT INTO AcademicDetail(student_id,semester,roll_no,department,course,summer_cgpa,sem_cgpa,backlogs) VALUES ("+str(student_id)+","+str(data_form['semester'])+",'"+str(data_form['roll_no'])+"','"+data_form['department']+"','"+data_form['course']+"',"+str(data_form['summer_cgpa']) +","+str(data_form['sem_cgpa'])+","+str(data_form['backlogs']) +");")
				cursor.close()
				messages.success(request,'Operation Completed Successfull.Refresh to view changes.')
			except Exception as e:
					print e
					messages.debug(request,"Error in database store" + str(e))
					messages.error(request,"An error occured please try later")
		

		
	else:
		#Fetch the previous data of user
		user_cred = isAuthenticated(request)
		if user_cred:
			student_id = user_cred[0]
			try:
				cursor = connection.cursor()
				cursor.execute("SELECT semester,roll_no,department,course,summer_cgpa,sem_cgpa,backlogs FROM AcademicDetail WHERE student_id = "+str(student_id)+";")
				data = cursor.fetchall()
				cursor.close()
			except Exception as e:
				data = []
				print e
				messages.debug(request,"Error in database fetch" + str(e))
				messages.error(request,"An error occured please try later")
			

			object_list =[]
			roll_no = ""
			department = ""
			course = ""
			for rows in data:
				data = {}
				data['semester'] = rows[0]
				data['summer_cgpa'] = rows[4]
				data['sem_cgpa'] = rows[5]
				data['backlogs'] = rows[6]
				roll_no = rows[1]
				department = rows[2]
				course = rows[3]
				object_list.append(data)
			print object_list
			return render(request,'showAcademicDetails.html',{'form':form,'roll_no':roll_no,'department':department,'course':course,'objects':object_list})


	return render(request,'showAcademicDetails.html',{'form':form})

def studentDashboard(request):
	form = AcademicDetailForm()
	if request.method == "POST":
		form = AcademicDetailForm(request.POST)
		user_cred = isAuthenticated(request)
		if form.is_valid() and user_cred:
			data_form = form.cleaned_data
			student_id = user_cred[0]
			try:
				cursor = connection.cursor()
				cursor.execute("DELETE FROM AcademicDetail WHERE (student_id = "+str(student_id)+") AND (semester = "+str(data_form['semester'])+");")
				cursor.execute("INSERT INTO AcademicDetail(student_id,semester,roll_no,department,course,summer_cgpa,sem_cgpa,backlogs) VALUES ("+str(student_id)+","+str(data_form['semester'])+",'"+str(data_form['roll_no'])+"','"+data_form['department']+"','"+data_form['course']+"',"+str(data_form['summer_cgpa']) +","+str(data_form['sem_cgpa'])+","+str(data_form['backlogs']) +");")
				cursor.close()
				messages.success(request,'Operation Completed Successfull.Refresh to view changes.')
			except Exception as e:
					print e
					messages.debug(request,"Error in database store" + str(e))
					messages.error(request,"An error occured please try later")
		else:
			print "Filling Willingness"
			company_id = str(request.POST['company_key'])
			course = str(request.POST['company_course'])
			company_type = str(request.POST['company_type'])
			preference = str(request.POST['preference'])
			#try:
			cursor = connection.cursor()
			print "DELETE FROM Files where company_id = {} AND student_id = {}".format(company_id,str(user_cred[0]))
			cursor.execute("DELETE FROM Files where company_id = {} AND student_id = {}".format(company_id,str(user_cred[0])))
			cursor.execute("INSERT INTO Files values({},'{}','{}',{},NULL,{});".format(company_id,course,company_type,str(user_cred[0]),preference))
			cursor.close()
			messages.success(request,'Operation Completed Successfull.Refresh to view changes. The preference was set to'+preference+".")
			"""except Exception as e:
					print e
					messages.debug(request,"Error in database store" + str(e))
					messages.error(request,"An error occured please try later")			
			"""

	#Fetch the previous data of user
	user_cred = isAuthenticated(request)
	if user_cred:
		student_id = user_cred[0]
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT semester,roll_no,department,course,summer_cgpa,sem_cgpa,backlogs,verified_by FROM AcademicDetail WHERE student_id = "+str(student_id)+";")
			data = cursor.fetchall()
			cursor.close()
		except Exception as e:
			data = []
			print e
			messages.debug(request,"Error in database fetch" + str(e))
			messages.error(request,"An error occured please try later")
		

		object_list =[]
		roll_no = ""
		department = ""
		course = ""
		cgpa = 0
		for rows in data:
			data = {}
			data['semester'] = rows[0]
			data['summer_cgpa'] = rows[4]
			data['sem_cgpa'] = rows[5]
			data['backlogs'] = rows[6]
			cgpa = rows[5]
			roll_no = rows[1]
			department = rows[2]
			course = rows[3]
			print "Row 7",rows[7]
			if rows[7]:
				data['verified_by'] = getMemberEmailName(rows[7])[0]
			object_list.append(data)
		#List of companies for which the user is eligible
		lis = []
		if isAcademicDetailVerified(student_id):
			lis = getCompanies(request,student_id,course,department,cgpa)
		notifs = getNotifications(request)
		return render(request,'studentDashboard.html',{'form':form,'roll_no':roll_no,'department':department,'course':course,'objects':object_list,'companies':lis,'notifications':notifs,'name':getUserName(request)})


	return render(request,'studentDashboard.html',{'form':form})

	return render(request,"studentDashboard.html")


def isAcademicDetailVerified(student_id):
	data = []
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT student_id,verified_by from AcademicDetail where student_id = {};".format(student_id))
		data = cursor.fetchall()
		connection.close()
	except Exception as e:
		print e
		pass
	print "Data",data
	for rows in data:
		if  not rows[1]:
			return False
	if len(data)<=0:
		return False
	return True



def getCompanies(request,student_id,course,department,cgpa):
	companies = []
	#try:
	cursor = connection.cursor()
	print localtime(now()).date()
	cursor.execute("SELECT * FROM Willingness WHERE gpa<={} and course = '{}' and willingness_deadline <= '{}'".format(cgpa,course,str(now().date())))
	companies = cursor.fetchall()
	cursor.close()
	"""except Exception as e:
		print e
		messages.error(request,"Error inserting into database")
	"""

	#Organizing companies into a list of dictionaries
	company_list =[]
	print companies
	for cpny in companies:
		cp  = {}
		cp['company_id'] = cpny[0]
		cp['company'] = getCompanyName(cpny[0])[0]
		cp['course'] = cpny[1]
		cp['type'] = cpny[2]
		cp['gpa_req'] = cpny[3]
		cp['branch_issue_date'] = cpny[4]
		cp['willingness_deadline'] = cpny[5]
		cp['result_date'] = cpny[6]
		cp['slt_number'] = cpny[7]
		company_list.append(cp)


	return company_list





def getCompanyName(company_id):
	cursor = connection.cursor()
	cursor.execute("SELECT name FROM Company WHERE company_id = {};".format(company_id))
	company_name = cursor.fetchone()
	cursor.close()	
	if company_name is not None:
		return company_name
	return company_id
def getUserName(request):
	name = ""
	user = isAuthenticated(request)
	if user:
		user_type = int(user[1])
		ids =  user[0]
		print "user_type",user_type
		if user_type == 0:
			print "hello1"
			cursor = connection.cursor()
			cursor.execute("SELECT name FROM Student WHERE student_id = {}".format(ids))
			name = cursor.fetchone()
			cursor.close()	
		elif user_type == 1:
			print "hello2"
			cursor = connection.cursor()
			cursor.execute("SELECT name FROM Company WHERE company_id = {}".format(ids))
			name = cursor.fetchone()
			cursor.close()
		elif user_type == 2:
			print "hello3"
			cursor = connection.cursor()
			cursor.execute("SELECT name FROM Team WHERE member_id = {}".format(ids))
			name = cursor.fetchone()
			cursor.close()
	else:
		messages.error(request,"Please authenticate first")

	return name[0]
def getNotifications(request):
	user = isAuthenticated(request)
	notificationList = []
	if user:
		user_type = int(user[1])

		if user_type ==0 or user_type == 2:
			
			try:
				cursor = connection.cursor()
				print localtime(now()).date()
				cursor.execute("SELECT * FROM Notification WHERE allowed = 0 ORDER by time_stamp desc;")
				notifs = cursor.fetchall()
				cursor.close()
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")

			for n in notifs:
				attributes = {}
				attributes['content'] = n[3]
				attributes['name'] = getUserName(request)
				attributes['date'] = n[1].date()
				attributes['time'] = n[1].time()
				attributes['views'] = n[2]
				notificationList.append(attributes)
		if user_type == 1 or user_type == 2:
			try:
				cursor = connection.cursor()
				print localtime(now()).date()
				cursor.execute("SELECT * FROM Notification WHERE allowed = 1 ORDER by time_stamp desc ;")
				notifs = cursor.fetchall()
				cursor.close()
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")

			for n in notifs:
				attributes = {}
				attributes['content'] = n[3]
				attributes['name'] = getUserName(request)
				attributes['date'] = str(n[1]).split()[0]
				attributes['time'] = str(n[1]).split()[1]
				attributes['views'] = n[2]
				attributes['allowed_students'] = n[4]
				notificationList.append(attributes)
	#messages.error(request,str(notificationList))

	return notificationList


def indexPage(request):
	return render(request,"home.html")

def policies(request):
	return render(request,"policies.html")

def logOut(request):
	deAuthenticate(request)
	messages.success(request,"You have been logged out Successfully")
	return render(request,"home.html")

def about(request):
	return render(request,"about.html")


def getMemberEmailName(member_id):
	cursor = connection.cursor()
	cursor.execute("SELECT name,email FROM Team WHERE member_id = {};".format(member_id))
	name = cursor.fetchone()
	cursor.close()	
	print "name",name
	if name is not None:
		return (name[0],name[1])
	return (member_id,'')
