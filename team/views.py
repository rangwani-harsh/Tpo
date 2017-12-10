# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import unicode_literals
from tpoSiteApp.sessionController import isAuthenticated,authenticate,getUserType
from django.shortcuts import render

from django.contrib import messages
from django.db import connection
from django.utils.timezone import localtime,now
from .forms import Notification,SlotDefine,Service,willForm 
from django.http import  HttpResponseRedirect
from django.urls import reverse
import time
from tpoSiteApp.forms import StudentSignUpForm,CompanySignUpForm,MemberSignUpForm 
from tpoSiteApp.views import getCompanyName,getNotifications
from company.views import getMemberEmailName,getCompanyDetail
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
def generateNotification(request):
	error = ""
	error = ""
	if request.method == "POST":
		form = Notification(request.POST)
		user = isAuthenticated(request)
		if form.is_valid() and user and user[1] == 2:
			form_data = form.cleaned_data
			user_id = user[0]
			user_type = user[1]
			try:
				cursor = connection.cursor()
				print """INSERT INTO Notification VALUES ({},'{}',{},'{}',{}); """.format(user_id,now().strftime('%Y-%m-%d %H:%M:%S'),1,form_data['content'],form_data['allowed_students']) 
				cursor.execute("""INSERT INTO Notification VALUES ('{}','{}','{}','{}','{}');""".format(user_id,now().strftime('%Y-%m-%d %H:%M:%S'),1,form_data['content'],form_data['allowed_students']))	
				connection.close()
				
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")
			
			
		else:
			if user[1] != 2:
				messages.error(request,"Please login is a teammeber")
				return HttpResponseRedirect(reverse('Login'))

			messages.error(request,"Please fill the  form correctly")


	
	form = Notification()
	notificationList = getNotifications(request)
	return render(request,'createNotification.html',{'form':form,'notifications':notificationList})







def generateService(request):
	error = ""
	error = ""
	if request.method == "POST":
		form = Service(request.POST)
		user = isAuthenticated(request)
		if form.is_valid() and user and user[1] == 2:
			form_data = form.cleaned_data
			user_id = user[0]
			user_type = user[1]
			try:
				cursor = connection.cursor()
				print """INSERT INTO Service(service_name,service_date,service_time,payment,responsible_id,description) VALUES ('{}','{}','{}','{}','{}','{}');""".format(form_data['name'],form_data['service_date'],form_data['service_time'],form_data['payment'],int(user_id),form_data['description']) 
				cursor.execute("""INSERT INTO Service(service_name,service_date,service_time,payment,responsible_id,description) VALUES ('{}','{}','{}','{}','{}','{}');""".format(form_data['name'],form_data['service_date'],form_data['service_time'],form_data['payment'],int(user_id),form_data['description']) )	
				connection.close()
				
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")

			return HttpResponseRedirect(reverse('generateService'))
			
			
		else:
			if user[1] != 2:
				messages.error(request,"Please login is a teammeber")
				return HttpResponseRedirect(reverse('Login'))

			service_id = request.POST['service_key']
			cursor = connection.cursor()
			print "UPDATE Service set responsible_id = NULL where service_id = {} ;".format(service_id)
			cursor.execute("UPDATE Service set responsible_id = NULL where service_id = {} ;".format(service_id))
			connection.close()

			messages.success(request,"The service has been successfully completed")



	user = isAuthenticated(request)
	if user and user[1] == 2:
		data = []
		cursor = connection.cursor()
		cursor.execute("SELECT * from Service;")
		data = cursor.fetchall()
		cursor.close()
		my_service_list = []
		other_service =[]
		print "Data",data
		for row in data:
			details = {}
			details['service_id'] = row[0]
			details['service_name'] = row[1]
			details['service_date'] = row[2]
			details['service_time'] = row[3]
			details['payment'] = row[4]
			if not row[5] :
				details['responsible_id'] = "Completed"
			else:
				details['responsible_id'] = getMemberEmailName(row[5])[0]
			if row[5] == user[0]:
				my_service_list.append(details)
			else:
				other_service.append(details)
			print row[5]
			

		form = Service()
		print other_service
		print my_service_list
		return render(request,'generateService.html',{'form':form,'my_service':my_service_list,'other_service':other_service})
	else:
		return HttpResponseRedirect(reverse('Login'))




def getStudentName(student_id):
	"""Returns a string of Name of the student with particular id"""
	name = ""
	data = ""
	if student_id:
		try:
			cursor = connection.cursor()
			print "SELECT name FROM Student where student_id = {};".format(student_id)
			cursor.execute("SELECT name FROM Student where student_id = {};".format(student_id))
			data = cursor.fetchone()
			connection.close()

		except Exception as e:
			print "Exception",e
			#messages.error(request,"Error loading from database")
		if data:
			name = data
	return name

def willingnessAdmin(request):
	error = ""
	form = None
	if request.method == "POST":
		print request.POST
		form = willForm(request.POST)
		user_cred = isAuthenticated(request)
		if user_cred and int(user_cred[1]) == 2 and form.is_valid():
			#print "Hello"
			form_data = form.cleaned_data
			
			member_id = user_cred[0]
			try:
				cursor = connection.cursor()
				cursor.execute("""UPDATE  Willingness set branch_issue_date  = '{}' ,result_date = '{}',willingness_deadline = '{}',exam_date = '{}', slt_number = {} where company_id = {} AND course = '{}' AND type = '{}' ;""".format(form_data['branch_issue_date'],form_data['result_date'],form_data['willingness_deadline'],form_data['exam_date'],form_data['slt_number'],form_data['company_id'],form_data['course'],form_data['typ']))

				
				cursor.close()

			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")

		else:
			if request.POST.has_key('company_id'):
				company_id = request.POST['company_id']
				course = request.POST['course']
				typ = request.POST['type']
				print company_id,course,typ
				form = willForm(initial = {'company_id':company_id,'course':course,'typ':typ})
			
			#return render(request,"willingnessAdmin.html",{'form':form})


	user_cred = isAuthenticated(request)
	if user_cred and int(user_cred[1]) == 2:
		user_id = user_cred[0]
		unverifiedList = []
		verifiedList = []
		#messages.error(request,"Error inserting into database")
		try:
			cursor = connection.cursor()
			cursor.execute("""SELECT * from Willingness ; """)
			data = cursor.fetchall()
			cursor.close()

		except Exception as e:
			print e
			messages.error(request,"Error inserting into database")
		object_list = []
		for row in data:
			details = {}
			details['company_id'] = row[0]
			details['company_name'] = getCompanyName(row[0])[0]
			details['course'] = row[1]
			details['type'] = row[2]
			details['gpa'] = row[3]
			details['willingness_deadline'] = row[6]
			details['exam_date'] = row[4]
			details['branch_issue_date'] = row[5]
			details['result_date'] = row[7]
			details['slt_number'] = row[8]
			object_list.append(details)


		return render(request,"willingnessAdmin.html",{'form':form,'object_list':object_list,"title" : "Willingness"})
	
	return HttpResponseRedirect(reverse('Login'))


def verifyWillingness(request):
	error = ""
	if request.method == "POST":
		user_cred = isAuthenticated(request)
		if user_cred and int(user_cred[1]) == 2:
			company_id = request.POST['company_key']
			student_id = request.POST['student_key']
			member_id = user_cred[0]
			try:
				cursor = connection.cursor()
				cursor.execute("""UPDATE  Files set member_id  = {} where (company_id = {} and student_id = {}); """.format(member_id,company_id,student_id))

				
				cursor.close()

			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")

	user_cred = isAuthenticated(request)
	if user_cred and int(user_cred[1]) == 2:
		user_id = user_cred[0]
		unverifiedList = []
		verifiedList = []
		#messages.error(request,"Error inserting into database")
		try:
			cursor = connection.cursor()
			cursor.execute("""SELECT * from Files ; """)
			data = cursor.fetchall()
			cursor.close()

		except Exception as e:
			print e
			messages.error(request,"Error inserting into database")
		
		for row in data:
			details = {}
			details['company_id'] = row[0]
			details['course'] = row[1]
			details['type'] = row[2]
			
			details['student_id'] = row[3]
			details['preference'] = row[5]
			details['student_name'] = getStudentName(row[3])[0]
			details['company_name'] = getCompanyName(row[0])[0]
			if row[4]:

				details['verified'] = getMemberEmailName(row[4])
				details['verified'] = " Id:".join(details['verified']) 
				verifiedList.append(details)
			else:
				unverifiedList.append(details)



		return render(request,'verifywillingness.html',{'unverifiedList':unverifiedList,'verifiedList':verifiedList})
	
	return HttpResponseRedirect(reverse('Login'))



def verifyAcademicDetail(request):
	print "Hello"
	
	if request.method == "POST":
		user_cred = isAuthenticated(request)

		if user_cred and user_cred[1] == 2:
			member_id = user_cred[0]
			action = request.POST['action']
			student_id = request.POST['student_key']
			semester = request.POST['semester_key']
			if action == "yes":
				cursor = connection.cursor()
				cursor.execute("UPDATE AcademicDetail SET verified_by = {} where student_id = {} and semester = {};".format(member_id,student_id,semester))
				connection.close()
			else:
				cursor = connection.cursor()
				cursor.execute("DELETE from AcademicDetail WHERE student_id = {} and semester = {};".format(student_id,semester))
				connection.close()
			messages.success(request,"Operation is successfull.")


		else:

			return HttpResponseRedirect(reverse('Login'))
		

		
	
	#Fetch the previous data of user
	user_cred = isAuthenticated(request)
	if user_cred:
		student_id = user_cred[0]
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT semester,roll_no,department,course,summer_cgpa,sem_cgpa,backlogs,verified_by,student_id FROM AcademicDetail ;")
			data = cursor.fetchall()
			cursor.close()
		except Exception as e:
			data = []
			print e
			messages.debug(request,"Error in database fetch" + str(e))
			messages.error(request,"An error occured please try later")
		

		unverifiedList = []
		verifiedList = []
		roll_no = ""
		department = ""
		course = ""
		print data
		for rows in data:
			data = {}
			data['student_id'] = rows[8]
			data['semester'] = rows[0]
			data['summer_cgpa'] = rows[4]
			data['sem_cgpa'] = rows[5]
			data['backlogs'] = rows[6]
			data['roll_no'] = rows[1]
			data['department'] = rows[2]
			data['course'] = rows[3]
			print rows[7]
			if rows[7]:
				data['verified_by'] = getMemberEmailName(rows[7])[0]
				verifiedList.append(data)

			else:
				unverifiedList.append(data) 
		#print object_list
		return render(request,'showAcademicDetails.html',{'verified_list':verifiedList,'unverified_list':unverifiedList})


def viewStudents(request):
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
				return render(request,"logged_in.html")
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")
			
		

		else:
			student_id = request.POST['key']
			cursor = connection.cursor()
			print "DELETE from Student where student_id ={};".format(student_id)
			cursor.execute("DELETE from Student where student_id ={};".format(student_id))
			connection.close()

	user = isAuthenticated(request)
	if user and user[1] == 2 :
		#Proceed if user is member
		form = StudentSignUpForm()
		cursor = connection.cursor()
		cursor.execute("SELECT * from Student;")
		data = cursor.fetchall()
		connection.close()
		table_head = []
		object_list = []
		table_head = ['Name','Email','DOB','category','gender','address','fathers_name','mothers_name']
		for rows in data:
			object_list.append(rows[:-2])
		return render(request,'genericAdmin.html',{'form':form,'table_head':table_head,'object_list':object_list,'title':"Student View"})

	return HttpResponseRedirect(reverse('Login'))


def companyView(request):
	error = ""
	error = ""
	if request.method == "POST":
		form = CompanySignUpForm(request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			try:
				cursor = connection.cursor()
				cursor.execute("SELECT password FROM Company WHERE email = '{}';".format(form_data['email']))
				data = cursor.fetchone()
				if data is not None:
					messages.error(request,"You are already registered.")
				cursor.execute("""INSERT INTO Company(name,email,password,ppt_date,interview_date,package_take_home,package_ctc,jd) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}'); """.format(form_data['name'],form_data['email'],form_data['password'],form_data['ppt_date'],form_data['interview_date'],form_data['package_take_home'],form_data['package_ctc'],form_data['jd']) )

				
					
				connection.close()
				#return render(request,"logged_in.html")
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")
			
			
		else:
			company_id = request.POST['key']
			cursor = connection.cursor()
			print "DELETE from Company where company_id ={};".format(company_id)
			cursor.execute("DELETE from Company where company_id ={};".format(company_id))
			connection.close()

	user = isAuthenticated(request)
	if user:
		form = CompanySignUpForm()
		cursor = connection.cursor()
		cursor.execute("SELECT company_id from Company;")
		data = cursor.fetchall()
		connection.close()
		company_list = []
		print data
		for cid in data:
			company_list.append(getCompanyDetail(cid[0]))



		

    
		print company_list
		
		return render(request,'companies.html',{'form':form,'company_list':company_list})

	else:
		return HttpResponseRedirect(reverse('Login'))



def viewMembers(request):
	if request.method == "POST":
		form = MemberSignUpForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			name = form.cleaned_data.get('name')
			mobile = form.cleaned_data.get('mobile')
			department = form.cleaned_data.get('department')
			designation = form.cleaned_data.get('designation')
			#roll_no = form.cleaned_data.get('roll_no')
			#department = form.cleaned_data.get('department')
			#course = form.cleaned_data.get('course')
			#DOB = form.cleaned_data.get('DOB')
			#category = form.cleaned_data.get('category')
			#gender = form.cleaned_data.get('gender')
			#address = form.cleaned_data.get('address')
			try:
				cursor = connection.cursor()
				cursor.execute("SELECT password FROM Team WHERE EMAIL = '"+email+"';")
				data = cursor.fetchone()
				if data is not None:
					messages.error(request,"You are already registered.")
				cursor.execute("INSERT INTO Team(name,email,password,mobile,department,designation) VALUES ('"+name+"','"+email+"','"+make_password(password)+"','"+mobile+"','"+department+"','"+designation+"');" )
				
					
				connection.close()
				messages.success(request,"Operation successfull")
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")
			
		

		else:
			member_id = request.POST['key']
			cursor = connection.cursor()
			print "DELETE from Team where member_id ={};".format(member_id)
			cursor.execute("DELETE from Team where member_id ={};".format(member_id))
			connection.close()

	user = isAuthenticated(request)
	if True:
		#Proceed if user is member
		form = MemberSignUpForm()
		cursor = connection.cursor()
		cursor.execute("SELECT * from Team;")
		data = cursor.fetchall()
		connection.close()
		table_head = []
		object_list = []
		table_head = ['Name','Designation','Department','Email','Mobile']
		for rows in data:
			object_list.append(rows[:-1])
		return render(request,'genericAdmin.html',{'form':form,'table_head':table_head,'object_list':object_list,'title':"Team View"})

	return HttpResponseRedirect(reverse('Login'))







def slotDefine(request):
	if request.method == "POST":
		form = SlotDefine(request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			try:
				cursor = connection.cursor()
				cursor.execute("DELETE From  Slot  where result_date = '{}' and slt_number  = {} ;".format(form_data['result_date'],form_data['slot_number']))
				data = cursor.fetchone()
				if data is not None:
					messages.error(request,"The user is already registered .Please delate the entry.")

				else:
					#print "INSERT INTO Team(name,designation,department,email,mobile,password) VALUES ('{}','{}','{}','{}','{}','{}'');".format(form_data['name'],form_data['designation'],form_data['department'],form_data['email'],form_data['mobile'],form_data['password'])
					cursor.execute("INSERT INTO Slot(result_date,slt_number,limi) VALUES ('{}','{}','{}'');".format(form_data['result_date'],form_data['slot_number'],form_data['slot_limit']))

				connection.close()
			except Exception as e:
				print e
				messages.error(request,"Invalid input.")
	user = isAuthenticated(request)
	if user:
		form = SlotDefine()
		cursor = connection.cursor()
		cursor.execute("SELECT * from Slot;")
		data = cursor.fetchall()
		connection.close()
		table_head = ['Result Date','Slot','Limit on Companies']
		slot_list = []
		for rows in data:
			slot_list.append(rows)

		return render(request,'genericAdmin.html',{'form':form,'table_head':table_head,'object_list':slot_list,'title':"Slot Admin",'flag':True})		


	return HttpResponseRedirect(reverse('Login'))


def adminView(request):

	return render(request,"adminview.html")
	


