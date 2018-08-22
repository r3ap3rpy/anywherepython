import requests
import json

class AnywherePythonError(Exception):
	''' Class for custom error codes! '''
	pass

class AnywherePython(object):
	__domain = 'https://www.pythonanywhere.com'
	__owndomain = '.pythonanywhere.com'
	__consoles = None
	def __init__(self, **kwargs):
		self.__username = kwargs['username']
		self.__apikey = kwargs['apikey']
		self.__headers = {'Authorization': f"Token {kwargs['apikey']}"}
		self.__owndomain = kwargs['username'] + self.__owndomain

		Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/consoles/"),headers=self.__headers)
		if Response.status_code != 200:
			raise AnywherePythonError('The specified API Key is INVALID!')


	def __str__(self):
		return f"{self.__class__.__name__}(username = {self.__username}, apikey = {self.__apikey})"

	def __format__(self):
		return f"{self.__class__.__name__}(username = {self.__username}, apikey = {self.__apikey})"

	def __repr__(self):
		return f"{self.__class__.__name__}(username = {self.__username}, apikey = {self.__apikey})"

	def __unicode__(self):
		return f"{self.__class__.__name__}(username = {self.__username}, apikey = {self.__apikey})"

	@property
	def consoles(self):
		return self.get_consoles()

	def get_consoles(self):
		Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/consoles/"),headers=self.__headers)
		if len(json.loads(Response.text)) > 0:
			self.__consoles = json.loads(Response.text)
			return self.__consoles
		else:
			raise AnywherePythonError('You have no consoles running!')
		
	def get_console(self, id):
		try:
			int(id)
		except:
			raise AnywherePythonError('The console id must be an integer!')

		if not self.__consoles:
			self.get_consoles()

		if id in [_['id'] for _ in self.__consoles]:
			Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/consoles/{id}"),headers=self.__headers)
			if Response.status_code == 200:
				if json.loads(Response.text).get('detail'):
					raise AnywherePythonError('The specified console is not running anymore!')
				else:
					return json.loads(Response.text)
		else:
			raise AnywherePythonError('The specified id is not in the valid console id-s: {}'.format(','.join([str(_['id']) for _ in self.__consoles])))

	def get_console_output(self, id):
		try:
			int(id)
		except:
			raise AnywherePythonError('The console id must be an integer!')

		if not self.__consoles:
			self.get_consoles()

		if id in [_['id'] for _ in self.__consoles]:
			Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/consoles/{id}/get_latest_output/"),headers=self.__headers)
			if Response.status_code == 200:
				if json.loads(Response.text).get('detail'):
					raise AnywherePythonError('The specified console is not running anymore!')
				else:
					return json.loads(Response.text)
		else:
			raise AnywherePythonError('The specified id is not in the valid console id-s: {}'.format(','.join([str(_['id']) for _ in self.__consoles])))

	def send_console_input(self, id, tobesent):
		try:
			int(id)
		except:
			raise AnywherePythonError('The console id must be an integer!')

		try:
			str(tobesent)
		except:
			raise AnywherePythonError('The what you send must be a string!')

		if not self.__consoles:
			self.get_consoles()

		if id in [_['id'] for _ in self.__consoles]:
			Response = requests.post(url = (self.__domain + f"/api/v0/user/{self.__username}/consoles/{id}/send_input/"),data = {'input':tobesent+'\n'},headers=self.__headers)
			if Response.status_code == 200:
				if json.loads(Response.text).get('status') != 'OK':
					raise AnywherePythonError('An error happend when processing the sent command!')
				else:
					return json.loads(Response.text)
		else:
			raise AnywherePythonError('The specified id is not in the valid console id-s: {}'.format(','.join([str(_['id']) for _ in self.__consoles])))

	def kill_console(self, id):
		try:
			int(id)
		except:
			raise AnywherePythonError('The console id must be an integer!')

		if not self.__consoles:
			self.get_consoles()

		if id in [_['id'] for _ in self.__consoles]:
			Response = requests.delete(url = (self.__domain + f"/api/v0/user/{self.__username}/consoles/{id}/"),headers=self.__headers)
			if Response.status_code == 404:
				return 'Successfully killed the console with ID: {}'.format(id)
			else:
				raise AnywherePythonError('Could not kill the console, the error was: {}'.format(Response.status_code))
		else:
			raise AnywherePythonError('The specified id is not in the valid console id-s: {}'.format(','.join([str(_['id']) for _ in self.__consoles])))

	def get_shared_consoles(self):
		Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/consoles/shared_with_you/"),headers=self.__headers)
		if Response.status_code == 200:
			if Response.text == '[]':
				raise AnywherePythonError('Noone has shared a console with you!') from None
			else:
				return json.loads(Response.text)

	def get_webapps(self):
		Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/webapps/{self.__owndomain}/"),headers=self.__headers)
		if len(json.loads(Response.text)) > 0:
			return json.loads(Response.text)
		else:
			raise AnywherePythonError('You have no webapps!')

	def reload_webapps(self):
		Response = requests.post(url = (self.__domain + f"/api/v0/user/{self.__username}/webapps/{self.__owndomain}/reload/"),headers=self.__headers)
		if json.loads(Response.text)['status'] == 'OK':
			return 'Successfully reloaded the webapp!'
		else:
			raise AnywherePythonError('Could not reload webapp, maybe a configuration error!')

	def get_webapps_static(self):
		#/api/v0/user/{username}/webapps/{domain_name}/static_files/
		Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/webapps/{self.__owndomain}/static_files/"),headers=self.__headers)
		if len(json.loads(Response.text)) > 0:
			return json.loads(Response.text)
		else:
			raise AnywherePythonError('There are no static files for your webapp!')

	def get_scheduled_task(self):
		#/api/v0/user/{username}/schedule/
		Response = requests.get(url = (self.__domain + f"/api/v0/user/{self.__username}/schedule/"),headers=self.__headers)
		if len(json.loads(Response.text)) > 0:
			return json.loads(Response.text)
		else:
			raise AnywherePythonError('There are no scheduled tasks!')




