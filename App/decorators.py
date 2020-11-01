from django.http import HttpResponseRedirect

def is_logged_In(view_func):
	def wrapper(request,*args,**kwargs):
		if request.session.has_key('user'):
			return view_func(request,*args,**kwargs)
		else:
			return HttpResponseRedirect('/login')
	return wrapper