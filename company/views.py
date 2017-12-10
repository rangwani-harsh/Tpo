# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tpoSiteApp.sessionController import isAuthenticated,authenticate,getUserType
from django.shortcuts import render
from forms import CompanySignUpForm,createWillingnessForm
from django.contrib import messages
from django.db import connection
from django.http import  HttpResponseRedirect
from django.urls import reverse
from tpoSiteApp.views import getNotifications
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
def companySignUp(request):
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
				cursor.execute("""INSERT INTO Company(name,email,password,ppt_date,interview_date,package_take_home,package_ctc,jd) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}'); """.format(form_data['name'],form_data['email'],make_password(form_data['password']),form_data['ppt_date'],form_data['interview_date'],form_data['package_take_home'],form_data['package_ctc'],form_data['jd']) )

				
					
				connection.close()
				messages.success(request,"User Successfully Registered.Login to continue")
				return HttpResponseRedirect(reverse('indexPage'))
			except Exception as e:
				print e
				messages.error(request,"Error inserting into database")
			
			
		else:
			messages.error(request,"Please fill the signup form correctly")


	else:
		form = CompanySignUpForm()
		return render(request,'companySignup.html',{'form':form})


	return render(request,'companySignup.html',{'form':form})

def companyDashboard(request):

	return render(request,'companyDashboard.html')

def transactionStatus(request):
	#Get the status of transaction after it has completed
	return True

def companyDashboard(request,service_num = -1):
	form = None
	print service_num
	if request.method == "POST":
		form = createWillingnessForm(request.POST)
		user_cred = isAuthenticated(request)
		if  user_cred and form.is_valid(): 
			data_form = form.cleaned_data
			company_id = user_cred[0]
		try:
			cursor = connection.cursor()
			cursor.execute("INSERT INTO Willingness(company_id,course,type,gpa) values ({},'{}','{}','{}');".format(company_id,data_form['course'],data_form['typ'],data_form['gpa']))
			cursor.close()
			messages.success(request,'Operation Completed Successfull.Refresh to view changes.')
		except Exception as e:
				print e
				messages.debug(request,"Error in database store" + str(e))
				messages.error(request,"An error occured please try later")
	
	else:
		#Fetch the previous data of user
		form = createWillingnessForm()
		user_cred = isAuthenticated(request)
		print "user_cred",user_cred[1]
		if user_cred and int(user_cred[1]) == 1:
			company_id = user_cred[0]
			try:
				cursor = connection.cursor()
				cursor.execute("SELECT * FROM Service WHERE company_id IS NULL OR company_id = '{}';".format(company_id))
				data = cursor.fetchall()
				cursor.close()
			except Exception as e:
				data = []
				print e
				messages.debug(request,"Error in database fetch" + str(e))
				messages.error(request,"An error occured please try later")
			

			free_service_list =[]
			purchased_service_list = []
			
			print "Service",data
			cgpa = 0

			for rows in data:
				data = {}
				data['service_id'] = rows[0]
				data['service_name'] = rows[1]
				data['service_date'] = rows[2]
				data['service_time'] = rows[3]
				data['payment'] = rows[4]
				data['description'] = rows[6]
				if rows[7]:
					purchased_service_list.append(data)
				elif  rows[5]:
					name,email = getMemberEmailName(int(rows[5]))
					data['name'] = name
					data['email'] = email
					free_service_list.append(data)
					
		 
				
			#List of companies for which the user is eligible
			#lis = getCompanies(request,student_id,course,department,cgpa)
			notifs = getNotifications(request)
			companyDetail = getCompanyDetail(company_id)
			selected_service = {}
			if service_num and int(service_num) > 0 :
				print "Service_num",service_num
				service_id = -1
				if int(user_cred[1]) == 1:
					service_id  = int(service_num)
				print "Service id",service_id
				try:
					cursor = connection.cursor()
					print "SELECT * FROM Service WHERE service_id = {};".format(service_id)
					cursor.execute("SELECT * FROM Service WHERE service_id = {};".format(service_id))
					rows = cursor.fetchone()
					cursor.close()
				except Exception as e:
					data = []
					print e
					messages.debug(request,"Error in database fetch" + str(e))
					messages.error(request,"An error occured please try later")

				
				if rows:
					selected_service['service_id'] = rows[0]
					selected_service['service_name'] = rows[1]
					selected_service['service_date'] = rows[2]
					selected_service['service_time'] = rows[3]
					selected_service['payment'] = rows[4]
					selected_service['description'] = rows[6]
					if not rows[7]:
						pass
					else:
						print "Name",name,email
						name,email = getMemberEmailName(int(rows[5]))
						print "Name",name,email
						data['name'] = name
						data['email'] = email
						pass

			
			return render(request,'companyDashboard.html',{'form':form,'company':companyDetail,'notifications':notifs,'services':free_service_list,'purchased_services':purchased_service_list,'service':selected_service})
		else:
			return HttpResponseRedirect(reverse('Login'))

	return render(request,'companyDashboard.html',{'form':form})

	return render(request,"companyDashboard.html")


def getCompanyDetail(company_id):
	detail = {}
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM Company WHERE company_id = '{}';".format(company_id))
		data = cursor.fetchone()
		cursor.close()
	except Exception as e:
		data = []
		print e
		messages.debug(request,"Error in database fetch" + str(e))
		messages.error(request,"An error occured please try later")

	print data
	if data:
		detail['company_id'] = data[0]
		detail['company_name'] = data[1]
		detail['email'] = data[2]
		detail['ppt_date'] = data[3]
		detail['interview_date'] = data[5]
		detail['package_take_home'] = data[6]
		detail['package_ctc'] = data[7]
		detail['jd'] = data[8]

	return detail


def getMemberEmailName(member_id):
	cursor = connection.cursor()
	cursor.execute("SELECT name,email FROM Team WHERE member_id = {};".format(member_id))
	name = cursor.fetchone()
	cursor.close()	
	print "name",name
	if name is not None:
		return (name[0],name[1])
	return (member_id,'')


def adminView(request):

	return render(request,"adminview.html")
