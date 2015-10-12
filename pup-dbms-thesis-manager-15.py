import webapp2
import jinja2
import os
import urllib
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
import json
import csv


JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)


#For DB- Login and Registration System
class User(ndb.Model):
	email = ndb.StringProperty(indexed=True)
	first_name = ndb.StringProperty(indexed=True)
	last_name = ndb.StringProperty(indexed=True)
	phone_number = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

#HOME PAGE
class HomePage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('HomePage.html')
		self.response.write(template.render())

#REGISTRATION PAGE
#Front
class RegistrationPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('RegistrationPage.html')
		self.response.write(template.render())
	
	def post(self):
		user = User()
		user.email = self.request.get('email')
		user.first_name = self.request.get('first_name')
		user.last_name = self.request.get('last_name')
		user.phone_number = self.request.get('phone_number')
		user.put()
		self.redirect('/RegistrationUP')

	# def get(self):
 #        loggedin_user = users.get_current_user()
 #        if loggedin_user:
 #            user_key = ndb.Key('User',loggedin_user.user_id())
 #            user = user_key.get()
 #            if user:
 #                self.redirect('/RegistrationUP')
 #            else:
 #                if loggedin_user:
 #                    template = JINJA_ENVIRONMENT.get_template('RegistrationPage.html')
 #                    logout_url = users.create_logout_url('/Login')
 #                    template_value = {
 #                        'logout_url' : logout_url
 #                    }
 #                    self.response.write(template.render(template_value))
                    
 #                else:
 #                    login_url = users.create_login_url('/Registration')
 #                    self.redirect(login_url)
 #        else:
 #            self.redirect('/Login')

 #    def post(self):
 #        loggedin_user = users.get_current_user()
 #        user =  User(id=loggedin_user.user_id(), email=loggedin_user.email(), first_name=self.request.get('first_name'), last_name=self.request.get('last_name'), phone_number=self.request.get('phone_number'))
 #        user.put()
 #        self.redirect('/MainPage')

#Back
class RegistrationCompPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('RegistrationCompPage.html')
		self.response.write(template.render())

#LOGIN PAGE
class LoginPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		template_values = {
			'login_url': users.create_login_url(self.request.uri)
		}

		# if user:
		# 	self.redirect('/Registration')
		# else:
		# 	template = JINJA_ENVIRONMENT.get_template('MainPage.html')
		# 	self.response.write(template.render(template_values))


		if user:
			logout_url = users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('MainPage.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

#MAIN PAGE
#Body
class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('MainPage.html')
		self.response.write(template.render())

	# def get(self):
 #        user = users.get_current_user()
 #        url = users.create_logout_url(self.request.uri)

 #        template_value = {
 #            'user' : user,
 #            'url' : url,
 #        }
 #        if user:
 #            template = JINJA_ENVIRONMENT.get_template('MainPage.html')
 #            self.response.write(template.render(template_value))
 #        else:
 #            self.redirect('/Login')

#For DB- CRUD
#THESIS
class Thesis(ndb.Model):
	author_id = ndb.StringProperty(indexed=True)
	title = ndb.StringProperty(indexed=True)
	adviser = ndb.StringProperty(indexed=True)
	abstract = ndb.TextProperty()
	university = ndb.StringProperty(indexed=True)
	college = ndb.StringProperty(indexed=True)
	department = ndb.StringProperty(indexed=True)
	member1 = ndb.StringProperty(indexed=True)
	member2 = ndb.StringProperty(indexed=True)
	member3 = ndb.StringProperty(indexed=True)
	member4 = ndb.StringProperty(indexed=True)
	member5 = ndb.StringProperty(indexed=True)
	yearlist = ndb.StringProperty(indexed=True)
	section = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

#THESIS PAGE
#Front
class ThesisPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if user:
			logout_url = users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('ThesisPage.html')
			self.response.write(template.render(template_values))
	
	def post(self):
		thesis = Thesis()
		thesis.author_id = self.request.get('author_id')
		thesis.title = self.request.get('title')
		thesis.adviser = self.request.get('adviser')
		thesis.abstract = self.request.get('abstract')
		thesis.university = self.request.get('university')
		thesis.college = self.request.get('college')
		thesis.department = self.request.get('department')
		thesis.member1 = self.request.get('member1')
		thesis.member2 = self.request.get('member2')
		thesis.member3 = self.request.get('member3')
		thesis.member4 = self.request.get('member4')
		thesis.member5 = self.request.get('member5')
		thesis.yearlist = self.request.get('yearlist')
		thesis.section = self.request.get('section')
		thesis.put()
		
		self.redirect('/thesis/create/done')
#Back
class ThesisCompPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('ThesisCompPage.html')
		self.response.write(template.render())
#Body
class ThesisListPage(webapp2.RequestHandler):
	def get(self):
		thesis = Thesis.query().order(-Thesis.date).fetch()
		logging.info(thesis)
		template_data = {
			'thesis_list':thesis
		}
		template = JINJA_ENVIRONMENT.get_template('ThesisListPage.html')
		self.response.write(template.render(template_data))
#Sub-body
class ThesisInfoPage(webapp2.RequestHandler):
	def get(self,thesis_id):
		thesis = Thesis.get_by_id(int(thesis_id))
		template_data = {
		'thesis_list': thesis
		}
		template = JINJA_ENVIRONMENT.get_template('ThesisInfoPage.html')
		self.response.write(template.render(template_data))


#FACULTY
class Faculty(ndb.Model):
	title = ndb.StringProperty(indexed=True)
	first_name = ndb.StringProperty(indexed=True)
	last_name = ndb.StringProperty(indexed=True)
	email = ndb.StringProperty(indexed=True)
	phone_number = ndb.StringProperty(indexed=True)
	birthdate = ndb.StringProperty(indexed=True)
	picture = ndb.StringProperty(indexed=True)
	department_key = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)
#FACULTY PAGE
#Front
class FacultyPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if user:
			logout_url = users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('FacultyPage.html')
			self.response.write(template.render(template_values))
	
	def post(self):
		faculty = Faculty()
		faculty.title = self.request.get('title')
		faculty.first_name = self.request.get('first_name')
		faculty.last_name = self.request.get('last_name')
		faculty.email = self.request.get('email')
		faculty.phone_number = self.request.get('phone_number')
		faculty.birthdate = self.request.get('birthdate')
		faculty.picture = self.request.get('picture')
		faculty.put()
		
		self.redirect('/faculty/create/done')
#Back
class FacultyCompPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('FacultyCompPage.html')
		self.response.write(template.render())
#Body
class FacultyListPage(webapp2.RequestHandler):
	def get(self):
		faculty = Faculty.query().order(-Faculty.date).fetch()
		logging.info(faculty)
		template_data = {
			'faculty_list':faculty
		}
		template = JINJA_ENVIRONMENT.get_template('FacultyListPage.html')
		self.response.write(template.render(template_data))
#Sub-body
class FacultyInfoPage(webapp2.RequestHandler):
	def get(self,faculty_id):
		faculty = Faculty.get_by_id(int(faculty_id))
		template_data = {
		'faculty_list': faculty
		}
		template = JINJA_ENVIRONMENT.get_template('FacultyInfoPage.html')
		self.response.write(template.render(template_data))


#STUDENT
class Student(ndb.Model):
	first_name = ndb.StringProperty(indexed=True)
	last_name = ndb.StringProperty(indexed=True)
	email = ndb.StringProperty(indexed=True)
	phone_number = ndb.StringProperty(indexed=True)
	student_number = ndb.StringProperty(indexed=True)
	birthdate = ndb.StringProperty(indexed=True)
	picture = ndb.StringProperty(indexed=True)
	year_graduated = ndb.StringProperty(indexed=True)
	department_key = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)	
#STUDENT PAGE
#Front
class StudentPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if user:
			logout_url = users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('StudentPage.html')
			self.response.write(template.render(template_values))
	
	def post(self):
		student = Student()
		student.first_name = self.request.get('first_name')
		student.last_name = self.request.get('last_name')
		student.email = self.request.get('email')
		student.phone_number = self.request.get('phone_number')
		student.student_number = self.request.get('student_number')
		student.birthdate = self.request.get('birthdate')
		student.picture = self.request.get('picture')
		student.year_graduated = self.request.get('year_graduated')
		student.put()
		
		self.redirect('/student/create/done')
#Back
class StudentCompPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('StudentCompPage.html')
		self.response.write(template.render())
#Body
class StudentListPage(webapp2.RequestHandler):
	def get(self):
		students = Student.query().order(-Student.date).fetch()
		logging.info(students)
		template_data = {
			'student_list':students
		}
		template = JINJA_ENVIRONMENT.get_template('StudentListPage.html')
		self.response.write(template.render(template_data))
#Sub-body
class StudentInfoPage(webapp2.RequestHandler):
	def get(self,student_id):
		students = Student.get_by_id(int(student_id))
		template_data = {
		'student_list': students
		}
		template = JINJA_ENVIRONMENT.get_template('StudentInfoPage.html')
		self.response.write(template.render(template_data))


#UNIVERSITY
class University(ndb.Model):
	name = ndb.StringProperty(indexed=True)
	address = ndb.StringProperty(indexed=True)
	initial = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)
#UNIVERSITY PAGE
#Front
class UniversityPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if user:
			logout_url = users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('UniversityPage.html')
			self.response.write(template.render(template_values))
	
	def post(self):
		university = University()
		university.name = self.request.get('name')
		university.address = self.request.get('address')
		university.initial = self.request.get('initial')
		university.put()
		self.redirect('/university/create/done')
#Back
class UniversityCompPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('UniversityCompPage.html')
		self.response.write(template.render())
#Body
class UniversityListPage(webapp2.RequestHandler):
	def get(self):
		university = University.query().order(-University.date).fetch()
		logging.info(university)
		template_data = {
			'university_list':university
		}
		template = JINJA_ENVIRONMENT.get_template('UniversityListPage.html')
		self.response.write(template.render(template_data))
#Sub-body
class UniversityInfoPage(webapp2.RequestHandler):
	def get(self,university_id):
		university = University.get_by_id(int(university_id))
		template_data = {
		'university_list': university
		}
		template = JINJA_ENVIRONMENT.get_template('UniversityInfoPage.html')
		self.response.write(template.render(template_data))


#COLLEGE
class College(ndb.Model):
	university_key = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=True)
	departments = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)
#COLLEGE PAGE
#Front
class CollegePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if user:
			logout_url = users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('CollegePage.html')
			self.response.write(template.render(template_values))

	def post(self):
		college = College()
		college.name = self.request.get('name')
		college.departments = self.request.get('departments')
		college.put()

		self.redirect('/college/create/done')
#Back
class CollegeCompPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('CollegeCompPage.html')
		self.response.write(template.render())
#Body
class CollegeListPage(webapp2.RequestHandler):
	def get(self):
		college = College.query().order(-College.date).fetch()
		logging.info(college)
		template_data = {
			'college_list':college
		}
		template = JINJA_ENVIRONMENT.get_template('CollegeListPage.html')
		self.response.write(template.render(template_data))
#Sub-body
class CollegeInfoPage(webapp2.RequestHandler):
	def get(self,college_id):
		college = College.get_by_id(int(college_id))
		template_data = {
		'college_list': college
		}
		template = JINJA_ENVIRONMENT.get_template('CollegeInfoPage.html')
		self.response.write(template.render(template_data))


#DEPARTMENT
class Department(ndb.Model):
	college_key = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=True)
	chairperson = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)	
#DEPARTMENT PAGE
#Front
class DepartmentPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if user:
			logout_url = users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('DepartmentPage.html')
			self.response.write(template.render(template_values))
	def post(self):
		department = Department()
		department.name = self.request.get('name')
		department.chairperson = self.request.get('chairperson')
		department.put()

		self.redirect('/department/create/done')
#Back
class DepartmentCompPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('DepartmentCompPage.html')
		self.response.write(template.render())
#Body
class DepartmentListPage(webapp2.RequestHandler):
	def get(self):
		department = Department.query().order(-Department.date).fetch()
		logging.info(department)
		template_data = {
			'department_list':department
		}
		template = JINJA_ENVIRONMENT.get_template('DepartmentListPage.html')
		self.response.write(template.render(template_data))
#Sub-body
class DepartmentInfoPage(webapp2.RequestHandler):
	def get(self,department_id):
		department = Department.get_by_id(int(department_id))
		template_data = {
		'department_list':department
		}
		template = JINJA_ENVIRONMENT.get_template('DepartmentInfoPage.html')
		self.response.write(template.render(template_data))


#DataStore
 f=csv.reader(open('thesis_list.csv','r'),skipinitialspace=True)
 for row in f:
 	thesis = Thesis()
 	thesis.university = row[0]
 	thesis.college = row[1]
 	thesis.department = row[2]
 	thesis.yearlist = row[3]
 	thesis.title = row[4]
 	thesis.abstract = row[5]
 	thesis.section = row[6]
 	thesis.adviser = row[7]
 	thesis.member1 = row[8]
 	thesis.member2 = row[9]
 	thesis.member3 = row[10]
 	thesis.member4 = row[11]
 	thesis.member5 = row[12]
 	thesis.put()

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/Registration', RegistrationPage),
	('/RegistrationUP', RegistrationCompPage),
	('/Login', LoginPage),
	('/MainPage', MainPage),
	('/thesis/create', ThesisPage),	##
	('/thesis/create/done', ThesisCompPage),
	('/thesis/list/all', ThesisListPage), ##Filter ALL Thesis
	('/thesis/(.*)', ThesisInfoPage),
	('/faculty/create', FacultyPage), ##
	('/faculty/create/done', FacultyCompPage),
	('/faculty/list', FacultyListPage), ##
	('/faculty/(.*)', FacultyInfoPage), ##
	('/student/create', StudentPage), ##
	('/student/create/done', StudentCompPage),
	('/student/list', StudentListPage), ##
	('/student/(.*)', StudentInfoPage), ##
	('/university/create', UniversityPage), ##
	('/university/create/done', UniversityCompPage),
	('/university/list', UniversityListPage), ##
	('/university/(.*)', UniversityInfoPage), ##
	('/college/create', CollegePage), ##
	('/college/create/done', CollegeCompPage),
	('/college/list', CollegeListPage), ##
	('/college/(.*)', CollegeInfoPage), ##
	('/department/create', DepartmentPage), ##
	('/department/create/done', DepartmentCompPage),
	('/department/list', DepartmentListPage),
	('/department/(.*)', DepartmentInfoPage),
], debug = True)
