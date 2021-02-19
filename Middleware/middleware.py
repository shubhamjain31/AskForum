import pytz

from django.utils.timezone import activate

class TimezoneMiddleware(object):
	
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_request(self, request):
		activate(pytz.timezone('Asia/Kolkata'))