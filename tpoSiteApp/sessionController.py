# 0 Student id,1 Company Id,2 Member id
def isAuthenticated(request):
	try:
		user_id = request.session['user_id']
		user_type = request.session['user_type']
		user_email = request.session['user_email']
	except:
		return None
	if user_id == None or user_type == None or user_email == None:
		return None
	return (user_id,user_type,user_email)

def authenticate(request,user_id,user_type,user_email):

	request.session['user_id'] = user_id
	request.session['user_type'] = user_type
	request.session['user_email'] = user_email

def getUserType(request):
	return request.session['user_type']

def deAuthenticate(request):
	request.session['user_id'] = None
	request.session['user_type'] = None
	request.session['user_email'] = None




