from rest_framework.test import APIClient, APIRequestFactory, URLPatternsTestCase, force_authenticate, APITestCase
from rest_framework import status
from sptApp.responses import colliding_id_response
from sptApp.models import *
from sptApp.responses import *
from sptApp.serializers import *    
from django.test import TestCase
from django.test import Client
from sptApp.apps import SptAppConfig
from django.apps import apps
from sptApp import models
from django.core.exceptions import ImproperlyConfigured
import sptApp
import django
import unittest
from unittest import mock
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spt.settings")
django.setup()
import json
from django.contrib.postgres.fields import JSONField
from datetime import datetime, timedelta
from django.utils import timezone


try:
    from django.db.backends.sqlite3.base import check_sqlite_version
except ImproperlyConfigured:
    # Ignore "SQLite is too old" when running tests on another database.
    pass


# More info about APIClient: https://www.django-rest-framework.org/api-guide/testing/


'''
______________________________________________________________________________________________      Student
 Student: del, get, post, put

    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    join_date = models.DateTimeField(auto_now=True)
______________________________________________________________________________________________
'''


class SptappConfigTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(SptAppConfig.name, 'sptApp')
        self.assertEqual(apps.get_app_config('sptApp').name, 'sptApp')


# Test the CRUDability of the course classes
# To properly test this, each course must have a studenttocourse object with the professor assigned
# All test cases must also pass in an id_token (sometimes referred to as token)
# to properly authenticate and check the user's permissions.

class Test_Course(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')
        Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.all()[0])
        Course.objects.create(
            name="courseName2", course_code="courseCode2", subject_code="subjectCode2",professor=Student.objects.all()[0])
        StudentToCourse.objects.create(student=Student.objects.all()[0],course=Course.objects.all()[0])
        StudentToCourse.objects.create(student=Student.objects.all()[0],course=Course.objects.all()[1])
    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_course1(self):   # Delete existing course
        request = self.client.delete(path='/api/courses/1', format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_course2(self):   # Delete non-existing course
        request = self.client.delete(path='/api/courses/100/', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_course3(self):   # Delete without pk value = error
        request = self.client.delete(path='/api/courses/', format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_course1(self):     # Get All (no pk value)
        request = self.client.get(path='/api/courses/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_course2(self):     # Get existing course
        request = self.client.get(path='/api/courses/1', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_course3(self):     # Get non-existing course = error
        request = self.client.get(path='/api/courses/5',format='json')
        self.assertEqual(404, request.status_code)

    def test_get_course4(self):   # Get course with pk value
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=Student.objects.all()[0])
        stc1 = StudentToCourse.objects.create(student=Student.objects.all()[0],course=course1)
        request = self.client.get(path='/api/courses/' +
                             str(course1.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_course5(self):   # Can't Get course that doesn't exist
        request = self.client.get(path='/api/courses/10000000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_get_course1(self):   #Bad auth should deny access
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "48484")
        request = self.client.get(path='/api/courses/', format='json')
        self.assertEqual(401, request.status_code)
    
    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_course1(self):    # No Data = error
        dp = {}
        request = self.client.post(path='/api/courses/', format='json',data=dp)
        self.assertEqual(400, request.status_code)

    def test_post_course2(self):    # No pk value = add if correct data format
        data_parameters = {
            "name": "Coooool Course Name",
            "course_code": "123454322",
            "subject_code": "989090750",
            "professor": "1",
        }
        request = self.client.post(path='/api/courses/',
                              data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_course3(self):    # Can't POST to existing pk
        dp = {}
        request = self.client.post(path='/api/courses/10000000', format='json',data=dp)
        self.assertEqual(400, request.status_code)

    def test_post_course4(self):    # Bad auth should deny access
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "48484")
        dp = {}
        request = self.client.post(path='/api/courses/', format='json',data=dp)
        self.assertEqual(401, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_course1(self):   # Edit course with and pk with data
        data_parameters = {
            "name": "Dan's Class Now",
            "course_code": "123123",
            "subject_code": "456456",
        }
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=Student.objects.all()[0])
        StudentToCourse.objects.create(student=Student.objects.all()[0],course=course1)
        request = self.client.put(
            path='/api/courses/' + str(course1.pk), data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)


    def test_put_course2(self):   # Edit course with pk and without data = error
        data_parameters = {

                }
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=Student.objects.all()[0])
        StudentToCourse.objects.create(student=Student.objects.all()[0],course=course1)
        request = self.client.put(
            path='/api/courses/' + str(course1.pk), data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)


    def test_put_course3(self):   # Edit course without pk and with data = error
        data_parameters = {
            "name": "Dan's Class Now",
            "course_code": "123123",
            "subject_code": "456456",
        }
        course1 = None
        request = self.client.put(path='/api/courses/',
                             data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_put_course4(self):   # Can't put to non-existent course
        request = self.client.put(path='/api/courses/10000000000000', format='json',data={})
        self.assertEqual(404, request.status_code)

    def test_put_course5(self):   # Bad auth should deny access
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "48484")
        request = self.client.put(path='/api/courses/10000000000000', format='json',data={})
        self.assertEqual(401, request.status_code)



'''
______________________________________________________________________________________________              Student
 Student: del, get, post, put
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    join_date = models.DateTimeField(auto_now=True)
______________________________________________________________________________________________
'''


class Test_Student(APITestCase):

    # Needded for "creating objects in database"
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')
        Student.objects.create(email="first1last1@gmail.com",
                               first_name="first1", last_name="last1")
        Student.objects.create(email="first2last2@gmail.com",
                               first_name="first2", last_name="last2")
        Student.objects.create(email="first3last3@gmail.com",
                               first_name="first3", last_name="last3")

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''
    #Not implemented yet for some reason
    '''
    def test_delete_students1(self):   # Delete existing student

        request = self.client.delete(path='/api/students/1/', format='json',data={"token":"12345"})
        self.assertEqual(200, request.status_code)

    def test_delete_students2(self):   # Delete non-existing student

        request = self.client.delete(path='/api/students/100/', format='json',data={"token":"12345"})
        self.assertEqual(404, request.status_code)

    def test_delete_students3(self):   # Delete without pk value = error

        request = self.client.delete(path='/api/students/', format='json',data={"token":"12345"})
        self.assertEqual(400, request.status_code)
    '''
    '''
    __________________________________________________  Get
    __________________________________________________
    '''
    def test_get_students1(self):   # Get All (no pk value)
        dp = {"id_token":"12345"}
        request = self.client.get(path='/api/students/', format='json',data=dp)
        self.assertEqual(200, request.status_code)

    def test_get_student2(self):   # Get student with pk value
        student1 = Student.objects.create(
            email="first4last4@gmail.com", first_name="first4", last_name="last4")
        request = self.client.get(path='/api/students/' +
                             str(student1.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_students3(self):

        request = self.client.get(path='/api/students/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_student4(self):   # Can't get student with invalid pk

        student1 = Student.objects.create(
            email="first4last4@gmail.com", first_name="first4", last_name="last4")
        request = self.client.get(path='/api/students/' +
                             str(student1.pk+1), format='json')
        self.assertEqual(404, request.status_code)

    def test_get_students5(self): # Bad auth should deny access
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "574839")
        request = self.client.get(path='/api/students/', format='json')
        self.assertEqual(401, request.status_code)

    def test_post_student1(self):    # TODO FIX, Base user creation test. (No current test to ensure google api creation is working
        # Stop including any credentials
        self.client.credentials()

        request = self.client.post(path='/api/students/', format='json', data={"id_token":"54321",})
        self.assertEqual(200, request.status_code)

    def test_post_student2(self):    # TODO Return id_token_error_response if the id_token is bad
        # Stop including any credentials
        self.client.credentials()

        dp = {"id_token": "47294720"}
        request = self.client.post(path='/api/students/', format='json',data=dp)
        self.assertEqual(404, request.status_code)
    '''
    __________________________________________________  Post
    __________________________________________________
    '''
    '''
    __________________________________________________  Put
    __________________________________________________
    '''
    #This section is also not implemented yet for some reason
    '''def test_put_student1(self):   # Can't PUT with no pk

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
            ""
        }
        Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )


        request = self.client.put(
            path='/api/students/', data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_put_student2(self):   # Basic PUT test

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "uniquesnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
            "token":"12345"
        }
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )


        request = self.client.put(path='/api/students/' + str(student.pk), data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    def test_put_student3(self):   # Can't update student with invalid info

        student = Student.objects.create(
            email="unique@virginia.edu",
            first_name="Jon",
            last_name="Snow"
        )

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow",  # Not proper form of email
            "token":"12345",
        }


        request = self.client.put(path='/api/students/' + str(student.pk), data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_put_student4(self):   # Can't PUT to invalid pk

        student = Student.objects.create(
            email="jsno@virginia.edu",
            first_name="Jon",
            last_name="Snow"
        )

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virgini.edu",
            "token":"12345",
        }


        request = self.client.put(
            path='/api/students/1000000000', data=data_parameters, format='json')

        self.assertEqual(404, request.status_code)'''



'''
______________________________________________________________________________________________              Course
 Course: del, get, post, put
    name = models.CharField(max_length=250)
    course_code = models.CharField(max_length=250)
    subject_code = models.CharField(max_length=250)
______________________________________________________________________________________________
'''

class Test_StudentToCourse(APITestCase):

    # Needded for "creating objects in database"
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')

    '''
    __________________________________________________  Post
    __________________________________________________
    '''
    def test_post_student_to_course1(self):  # No Data = error

        request = self.client.post(path='/api/student/course/', format='json')
        self.assertEqual(400, request.status_code)

    # Providing a pk to the url = error
    def test_post_student_to_course2(self):

        request = self.client.post(
            path='/api/student/course/1233333332322/', format='json')
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # POST student to course
    def test_post_student_to_course3(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response


        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s",
        }
        request = self.client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't POST student to course with non-existent course
    def test_post_student_to_course4(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response


        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        DATA_PARAMETERS = {
            "course": str(1000000),
            "student": str(student.pk),
            "semester": "2018-s",
        }
        request = self.client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(404, request.status_code)

    # POST student to course with student in POST data
    def test_post_student_to_course5(self):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }



        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s",
        }
        request = self.client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')

        self.assertEqual(200, request.status_code)

    # Can't POST student to course with (non-existent) student in POST data
    def test_post_student_to_course6(self):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }


        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.all()[0])

        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(1000000000),
            "semester": "2018-s",
        }
        request = self.client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')

        self.assertEqual(404, request.status_code)

    # Can't POST student to course that already exists
    def test_post_student_to_course7(self):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }


        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s",
        }
        request = self.client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')

        self.assertEqual(400, request.status_code)

    def test_post_student_to_course8(self):  # Bad auth should deny access
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "574839")
        request = self.client.post(path='/api/student/course/', format='json')
        self.assertEqual(401, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_student_to_course1(self):   # Get existing student

        student = Student.objects.create(email="user1000@gmail.com")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        request = self.client.get(path='/api/student/course/' +
                             str(studentToCourse.pk), format='json')

        self.assertEqual(200, request.status_code)

    # Can't GET  student to course of non-existent student
    def test_get_student_to_course2(self):

        student = Student.objects.create(email="user1000@gmail.com")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)

        request = self.client.get(
            path='/api/student/course/100000000', format='json',data={"id_token":"12345",})

        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student
    def test_get_student_to_course3(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response


        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = self.client.get(
            path='/api/student/course/', format='json')
        self.assertEqual(200, request.status_code)

    # GET all student to course  for a specific course
    def test_get_student_to_course4(self):

        student = Student.objects.create(email="jsnow@virginia.edu",id_token="54321")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "54321")

        request = self.client.get(
            path='/api/student/course/?courseId=' + str(course.pk), format='json')

        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET whatever courses the student is in
    def test_get_student_to_course6(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response


        student = Student.objects.get(id_token="12345")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = self.client.get(
            path='/api/student/course/', format='json')
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student, generic success on a course object
    def test_get_student_to_course7(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response


        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"],
            id_token="54321",
        )
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "54321")
        request = self.client.get(path='/api/student/course/?courseId='+str(course.pk), format='json')
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student
    def test_get_student_to_course9(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response

        student = Student.objects.create(
            email="jack@gmail.com",
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        professor = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )

        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=Student.objects.get(id_token="12345"))

        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = self.client.get(path='/api/student/course/?courseId=' + str(
            course.pk) + '&view_as=' + str(student.pk), format='json')
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student, but as a different professor
    # Note: The system previously only allowed professors to view their own courses.
    # Now professors can view all courses, even ones they are not professors of
    def test_get_student_to_course99(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response

        student = Student.objects.create(
            email="jack@gmail.com",
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        professor = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )

        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = self.client.get(path='/api/student/course/?courseId='+str(course.pk)+'&view_as='+str(student.pk), format='json')
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student when student to course doesn't exist
    def test_get_student_to_course10(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response

        student = Student.objects.create(
            email="jack@gmail.com",
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        professor = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"],
            is_professor=True,
            id_token="54321",
        )
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "54321")

        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        request = self.client.get(path='/api/student/course/?courseId='+str(course.pk)+'&view_as='+str(student.pk), format='json')
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student when student doesn't exist
    def test_get_student_to_course11(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response

        professor = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"],
            is_professor=True,
        )

        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        request = self.client.get(path='/api/student/course/?courseId='+str(course.pk)+'&view_as='+str(100000000), format='json')
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student when course doesn't exist
    def test_get_student_to_course12(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': data_parameters["email"],
            'email_verified': 'true',
            'at_hash': 'afsdfasfdsa',
            'name': 'Jon Snow',
            'picture': '',
            'given_name': data_parameters["first_name"],
            'family_name': data_parameters["last_name"],
            'locale': 'en',
            'iat': '1551024643',
            'exp': '1551028243',
            'jti': 'asfsd',
            'alg': 'RS256',
            'kid': 'asfasfas',
            'typ': 'JWT'
        }
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_request.return_value = mock_response

        professor = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )

        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        request = self.client.get(path='/api/student/course/?courseId='+str(10000000)+'&view_as='+str(professor.pk), format='json')
        self.assertEqual(404, request.status_code)
    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_student_to_course1(self):   # PUT student to course

        student = Student.objects.create(email="user1000@gmail.com")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course, semester="2018-f")

        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s",
        }

        request = self.client.put(path='/api/student/course/' +
                             str(studentToCourse.pk), data=DATA_PARAMETERS, format='json')

        self.assertEqual(200, request.status_code)

    # Can't PUT student to course with no pk
    def test_put_student_to_course2(self):

        request = self.client.put(path='/api/student/course/', format='json', data={"id_token":"12345"})

        self.assertEqual(400, request.status_code)

    # Can't PUT student to course to non-existent student to course
    def test_put_student_to_course3(self):

        student = Student.objects.create(email="user1000@gmail.com")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)

        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s",
        }

        request = self.client.put(path='/api/student/course/100000000',
                             data=DATA_PARAMETERS, format='json')

        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_student_to_course1(self):   # Delete student to course

        student = Student.objects.create(email="user1000@gmail.com")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        request = self.client.delete(path='/api/student/course/' +
                                str(student.pk) + '?courseId=' + str(course.pk), format='json')

        self.assertEqual(200, request.status_code)

    # Can't Delete student to course with no courseId
    def test_delete_student_to_course2(self):

        student = Student.objects.create(email="user1000@gmail.com")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        request = self.client.delete(path='/api/student/course/' +
                                str(student.pk), format='json')

        self.assertEqual(404, request.status_code)

    # Can't delete non-existent student to course
    def test_delete_student_to_course4(self):

        student = Student.objects.create(email="user1000@gmail.com")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=student)
        request = self.client.delete(path='/api/student/course/' +
                                str(student.pk) + '?courseId=' + str(course.pk), format='json')

        self.assertEqual(404, request.status_code)

    # Can't delete student to course with no pk
    def test_delete_student_to_course5(self):


        request = self.client.delete(path='/api/student/course/', format='json')

        self.assertEqual(400, request.status_code)



class Test_Topics(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        # Student.objects.create(name="name1", course=course1)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_topics1(self):     # Without pk, this will return list of all

        request = self.client.get(path='/api/topics/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_topics2(self):     # Get all topics for a single course
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )


        request = self.client.get(path='/api/topics/?courseId='+str(course.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_get_topics3(self):     # Can't get topics for non-existent classes

        request = self.client.get(
            path='/api/topics/?courseId='+str(10000), format='json')

        self.assertEqual(404, request.status_code)

    def test_get_topics4(self):     # Get a single topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )


        request = self.client.get(path='/api/topics/' +
                             str(topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_get_topics5(self):     # CAn't GET a single topic with a non-existent pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )


        request = self.client.get(path='/api/topics/10000000', format='json')

        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_topic1(self):   # Create multiple topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        data_parameters = {
            "topics": [
                {"pk": "None", "course": str(course.pk), "name": "A"},
                {"pk": "None", "course": str(course.pk), "name": "B"}
            ]
        }


        request = self.client.post(path='/api/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    def test_post_topic2(self):   # Can't POST to already existing PK
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        data_parameters = {
            "topics": [
                {"pk": "None", "course": str(course.pk), "name": "A"},
                {"pk": "None", "course": str(course.pk), "name": "B"}
            ]
        }


        request = self.client.post(path='/api/topics/2',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_post_topic3(self):   # Can't create topic with invalid course pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        data_parameters = {
            "topics": [
                {"pk": "None", "course": -1, "name": "A"},
                {"pk": "None", "course": -1, "name": "B"}
            ]
        }


        request = self.client.post(path='/api/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_post_topic4(self):   # Create multiple topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        data_parameters = {
            "topics": [
                {"pk": "None", "course": str(course.pk), "name": "A"},
                {"pk": "None", "course": str(course.pk), "name": "B"}
            ]
        }


        request = self.client.post(path='/api/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)
    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_topics1(self):     # Update a single topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )

        data_parameters = {
            "course": str(course.pk), "name": "A new",
        }


        request = self.client.put(path='/api/topics/' + str(topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    def test_put_topics2(self):     # Can't PUT a topic with invalid info
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )

        data_parameters = {
            "course": "100000000000",  # Invalid pk for course
            "name": "A new",
        }


        request = self.client.put(path='/api/topics/' + str(topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_put_topics3(self):     # Can't PUT with no pk


        request = self.client.put(path='/api/topics/', format='json')

        self.assertEqual(400, request.status_code)

    def test_put_topics4(self):     # Can't PUT with non-existent pk

        request = self.client.put(path='/api/topics/1000000000000', format='json')

        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    def test_delete_topic1(self):   # DELETE topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="TobeDeleted",
            course=course
        )


        request = self.client.delete(path='/api/topics/' +
                                str(topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_delete_topic2(self):   # Can't DELETE when no pk provided
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="TobeDeleted",
            course=course
        )


        request = self.client.delete(path='/api/topics/', format='json')

        self.assertEqual(400, request.status_code)

    def test_delete_topic3(self):   # Can't DELETE with invalid pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="TobeDeleted",
            course=course
        )


        request = self.client.delete(path='/api/topics/100000000000', format='json')

        self.assertEqual(404, request.status_code)


'''
______________________________________________________________________________________________      Course Grades Upload
 Course grades upload

______________________________________________________________________________________________
'''


class Test_Course_Grades_Upload(APITestCase):

    def setUp(self):
        Student.objects.create(id=0,email="jsnow@virginia.edu",id_token="54321")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')
        course = Course.objects.create(name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        assignment1 = Assignment.objects.create(name="easyassignment1",topic=topic)
        assignment2 = Assignment.objects.create(name="easyassignment2",topic=topic)
        assignment3 = Assignment.objects.create(name="easyassignment3",topic=topic)
        assignment4 = Assignment.objects.create(name="easyassignment4",topic=topic)
        assignment5 = Assignment.objects.create(name="easyassignment5",topic=topic)
        assignment6 = Assignment.objects.create(name="easyassignment6",topic=topic)
        assignment7 = Assignment.objects.create(name="easyassignment7",topic=topic)
        assignment8 = Assignment.objects.create(name="easyassignment8",topic=topic)
        assignment9 = Assignment.objects.create(name="easyassignment9",topic=topic)
        assignment10 = Assignment.objects.create(name="easyassignment10",topic=topic)
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")

    # Should fail due to improper authentication
    def test_course_grades_upload1(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "4829474")
        request = self.client.post(path='/api/courseGradesUpload/0',
                                     data=None)
        self.assertEqual(401, request.status_code)

    # Should fail due to no csv 
    def test_course_grades_upload2(self):
        request = self.client.post(path='/api/courseGradesUpload/0',
                                     data=None)
        self.assertEqual(400, request.status_code)

    # Should fail due to no course pk specified
    def test_course_grades_upload3(self):
        request = self.client.post(path='/api/courseGradesUpload/',
                                     data=None)
        self.assertEqual(404, request.status_code)

    # Should fail authentication for student users
    def test_course_grades_upload4(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "54321")
        request = self.client.post(path='/api/courseGradesUpload/0',
                                    data=None)
        self.assertEqual(403, request.status_code)
    
    # CSV upload for grades should work
    def test_course_grades_upload5(self):
        with open('csv_test/students.csv') as students:
            request = self.client.post(path='/api/courseRosterUpload/0', data={'csv': students})
        with open('csv_test/grades.csv') as grades:
            request = self.client.post(path='/api/courseGradesUpload/0', data={'csv': grades})
        self.assertEqual(200, request.status_code)

'''
______________________________________________________________________________________________      Topic to Topic
 TopicToTopic: del, get, post, put
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
    ancestor_node = models.ForeignKey(Topic,  on_delete=models.CASCADE)
    topic_node = models.ForeignKey(Topic, on_delete=models.CASCADE)
______________________________________________________________________________________________
'''


class Test_Topic_To_Topics(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        pass

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    # Without pk, this will return list of all
    def test_get_topic_to_topic1(self):

        request = self.client.get(path='/api/topic/topics/',
                             data=None, format='json')
        self.assertEqual(200, request.status_code)

    # With pk, this will a specific topic to topic
    def test_get_topic_to_topic2(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )


        request = self.client.get(path='/api/topic/topics/' +
                             str(topic_to_topic.pk), format='json')
        self.assertEqual(200, request.status_code)

    # Will return an empty array because we are using filter
    def test_get_topic_to_topic3(self):     # Can't find non-existent pk

        request = self.client.get(
            path='/api/topic/topics/1000000000', format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_topic_to_topic1(self):   # Create topic to topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = [
            {"course": str(course.pk), "topic_node": str(
                topic1.pk),  "ancestor_node": str(topic2.pk)},
        ]


        request = self.client.post(path='/api/topic/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    # Can't create topic to topic with invalid data
    def test_post_topic_to_topic2(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = [
            {"coursed": str(course.pk), "topic_node": str(
                topic1.pk),  "ancestor_node": str(topic2.pk)},
        ]


        request = self.client.post(path='/api/topic/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    # Can't post topic to topic to pre-existing pk
    def test_post_topic_to_topic3(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = [
            {"coursed": str(course.pk), "topic_node": str(
                topic1.pk),  "ancestor_node": str(topic2.pk)},
        ]


        request = self.client.post(path='/api/topic/topics/1',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_post_topic_to_topic11(self):   # Create topic to topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        # topic_to_topic = TopicToTopic.objects.create(
        #     course=course,
        #     topic_node=topic1,
        #     ancestor_node=topic2
        # )
        data_parameters = [
            {"course": str(course.pk), "topic_node": str(
                topic1.pk),  "ancestor_node": str(topic2.pk)},
        ]


        request = self.client.post(path='/api/topic/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)


    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_topic_to_topic1(self):     # Can't PUT with null pk

        request = self.client.put(path='/api/topic/topics/', format='json')

        self.assertEqual(400, request.status_code)

    def test_put_topic_to_topic2(self):     # Can't PUT to non-existent pk

        request = self.client.put(
            path='/api/topic/topics/100000000000', format='json')

        self.assertEqual(404, request.status_code)

    def test_put_topic_to_topic3(self):   # PUT topic to topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = {"course": str(course.pk), "topic_node": str(
            topic1.pk),  "ancestor_node": str(topic2.pk)}


        request = self.client.put(path='/api/topic/topics/' + str(topic_to_topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    def test_put_topic_to_topic4(self):   # Can't PUT with invalid data
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = {"coursed": str(course.pk), "topic_node": str(
            topic1.pk),  "ancestor_node": str(topic2.pk)}


        request = self.client.put(path='/api/topic/topics/' + str(topic_to_topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    def test_delete_topic_to_topic1(self):   # DELETE topic to topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )

        request = self.client.delete(
            path='/api/topic/topics/' + str(topic_to_topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_delete_topic_to_topic2(self):   # DELETE multiple topic to topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)
        topic3 = Topic.objects.create(name="topic3", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        topic_to_topic2 = TopicToTopic.objects.create(
            course=course,
            topic_node=topic3,
            ancestor_node=topic2
        )
        data_parameters = [str(topic_to_topic.pk), str(topic_to_topic2.pk)]

        request = self.client.delete(path='/api/topic/topics/',
                                data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    # Can't DELETE multiple topic to topics when pk is invalid
    def test_delete_topic_to_topic5(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)
        topic3 = Topic.objects.create(name="topic3", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = [str(topic_to_topic.pk), str(1000000000)]

        request = self.client.delete(path='/api/topic/topics/',
                                data=data_parameters, format='json')

        self.assertEqual(404, request.status_code)

    # Can't DELETE multiple topic to topics when request is empty
    def test_delete_topic_to_topic4(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)
        topic3 = Topic.objects.create(name="topic3", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = []

        request = self.client.delete(path='/api/topic/topics/',
                                data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    # Can't DELETE single topic to topics with no pk
    def test_delete_topic_to_topic3(self):

        request = self.client.delete(path='/api/topic/topics/', format='json')

        self.assertEqual(400, request.status_code)

    # Can't DELETE single topic to topics with invalid pk
    def test_delete_topic_to_topic3(self):

        request = self.client.delete(
            path='/api/topic/topics/100000000000', format='json')

        self.assertEqual(404, request.status_code)


'''
______________________________________________________________________________________________      Student to Topic
 StudentToTopic: del, get, post, put  /api/student/topics/
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
    student = models.ForeignKey(Student,  on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,  on_delete=models.CASCADE)
    grade = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    locked = models.BooleanField()
______________________________________________________________________________________________
'''


class Test_Student_To_Topic(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        pass

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    # Without pk, this will return list of all
    def test_get_student_to_topic1(self):

        request = self.client.get(path='/api/student/topics/',
                             data=None, format='json')
        self.assertEqual(200, request.status_code)

    # Can't get with non-existent student pk
    def test_get_student_to_topic2(self):

        request = self.client.get(
            path='/api/student/topics/1/2000000000', format='json')
        self.assertEqual(404, request.status_code)

    # Can't get with non-existent course pk
    def test_get_student_to_topic3(self):
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")

        request = self.client.get(
            path='/api/student/topics/2000000000/' + str(student.pk), format='json')
        self.assertEqual(404, request.status_code)

    def test_get_student_to_topic4(self):     # GET student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50)

        request = self.client.get(path='/api/student/topics/' +
                             str(course1.pk) + '/' + str(student.pk), format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_student_to_topic1(self):   # Can't POST to null student pk

        request = self.client.post(
            path='/api/student/topics/2000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_post_student_to_topic2(self):   # Can't POST to null student pk

        request = self.client.post(path='/api/student/topics/',
                              data={
                                  "student": str(1000000000000),
                                  "topics": []
                              }, format='json')
        self.assertEqual(404, request.status_code)

    def test_post_student_to_topic3(self):   # POST to student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(name="topic1", course=course1)


        request = self.client.post(path='/api/student/topics/',
                              data={
                                  "student": str(student.pk),
                                  "topics": [
                                      {"topic": str(topic.pk)}
                                  ]
                              }, format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_student_to_topic1(self):     # Can't PUT with null pk

        request = self.client.put(path='/api/student/topics/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_student_to_topic2(self):     # Can't PUT to non-existent pk

        request = self.client.put(
            path='/api/student/topics/?studentToTopicId=100000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_put_student_to_topic3(self):     # PUT student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50)

        DATA_PARAMETERS = {
            "student": str(student.pk),
            "topic": str(topic.pk),
            "grade": 100,
        }


        request = self.client.put(path='/api/student/topics/?studentToTopicId=' +
                             str(student_to_topic.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)


    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    # Can't DELETE student to topic with null pk
    def test_delete_student_to_topic1(self):

        request = self.client.delete(path='/api/student/topics/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't DELETE student to topic with non-existent pk
    def test_delete_student_to_topic2(self):

        request = self.client.delete(
            path='/api/student/topics/?studentToTopicId=100000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_student_to_topic3(self):   # DELETE student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50)

        request = self.client.delete(
            path='/api/student/topics/?studentToTopicId=' + str(student_to_topic.pk), format='json')
        self.assertEqual(200, request.status_code)


class Test_Assignments(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        # Student.objects.create(name="name1", course=course1)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_assignment1(self):     # Without pk, this will return list of all
        request = self.client.get(path='/api/assignments/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_assignment2(self):     # Get all assignments for a single topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        request = self.client.get(path='/api/assignments/?topicId='+str(topic.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_assignment3(self):     # Can't get assignments for non-existent topics
        request = self.client.get(
            path='/api/assignments/?topicId='+str(-1), format='json')
        self.assertEqual(404, request.status_code)

    def test_get_assignment4(self):     # Get a single assignment
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        request = self.client.get(path='/api/topics/' + str(assignment.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_assignment5(self):     # CAn't GET a single assignment with a non-existent pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        request = self.client.get(path='/api/assignments/999999999999999', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_assignment1(self):   # Create one assignment
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )    
        
        data_parameters = {
            "assignments": [
                {"pk": "None", "topic": str(topic.pk), "name": "A"}
            ]
        }

        request = self.client.post(path='/api/assignments/', data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_assignment2(self):   # Can't POST to already existing PK
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        data_parameters = {
            "topics": [
                {"pk": "None", "course": str(course.pk), "name": "A"},
                {"pk": "None", "course": str(course.pk), "name": "B"}
            ]
        }

        request = self.client.post(path='/api/topics/2',
                              data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_post_assignment3(self):   # Can't create assignment with invalid topic pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        data_parameters = {
            "assignments": [
                {"pk": "None", "topic": -1, "name": "A"},
                {"pk": "None", "topic": -1, "name": "B"}
            ]
        }

        request = self.client.post(path='/api/topics/',
                              data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)


    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_assignment1(self):     # Update a single assignment
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        data_parameters = {
            "topic": str(topic.pk), "name": "A new",
        }

        request = self.client.put(path='/api/assignments/' + str(assignment.pk), data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_asignment2(self):     # Can't PUT a topic with invalid info
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        data_parameters = {
            "topic": "100000000000",  # Invalid pk for course
            "name": "A new",
        }

        request = self.client.put(path='/api/topics/' + str(topic.pk),
                             data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_put_assignment3(self):     # Can't PUT with no pk
        request = self.client.put(path='/api/assignments/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_assignment4(self):     # Can't PUT with non-existent pk
        request = self.client.put(path='/api/assignments/1000000000000', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    def test_delete_assignment1(self):   # DELETE assignment
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topicName1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        request = self.client.delete(path='/api/assignments/' + str(assignment.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_assignment2(self):   # Can't DELETE when no pk provided
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topicName1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        request = self.client.delete(path='/api/assignments/', format='json')
        self.assertEqual(400, request.status_code)

    def test_delete_assignment3(self):   # Can't DELETE with invalid pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topicName1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )

        request = self.client.delete(path='/api/assignments/99999999999999', format='json')
        self.assertEqual(404, request.status_code)


class Test_Quizzes(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        # Student.objects.create(name="name1", course=course1)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_quiz1(self):     # Without pk, this will return list of all
        request = self.client.get(path='/api/quizzes/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_quiz2(self):     # Get all quizzes for a single topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment,
        )

        request = self.client.get(path='/api/quizzes/?quizId='+str(quiz.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_quiz3(self):     # Can't get quizzes for non-existent topics
        request = self.client.get(
            path='/api/quizzes/23', format='json')
        self.assertEqual(404, request.status_code)

    def test_get_quiz4(self):     # Get a single quiz
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment,
        )

        request = self.client.get(path='/api/quizzes/' + str(quiz.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_quiz5(self):     # CAn't GET a single quiz with a non-existent pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment,
        )

        request = self.client.get(path='/api/quizzes/999999999999999', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_quiz1(self):   # Create one quiz
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )  
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )  
        
        data_parameters = {
            "quizzes": [{
                        "pk": "None", 
                        "assignment": str(assignment.pk), 
                        "pool": json.dumps(quiz_jason_default()), 
                        "practice_mode": False, 
                        "next_open_date": timezone.now(), 
                        "next_close_date": timezone.now(), 
                        }]
        }

        request = self.client.post(path='/api/quizzes/', data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_quiz2(self):   # Can't POST to already existing PK
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345")
            )
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )  
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )  

        data_parameters = {
            "quizzes": [{
                        "pk": "None", 
                        "assignment": str(assignment.pk), 
                        "pool": json.dumps(quiz_jason_default()), 
                        "practice_mode": False, 
                        "allow_submissions": True, 
                        "next_open_date": timezone.now(), 
                        "next_close_date": timezone.now(), 
                        }]
        }

        request = self.client.post(path='/api/quizzes/2',
                              data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz3(self):   # Can't create quiz with invalid topic pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )  
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )  
        data_parameters = {
            "quizzes": [{
                        "pk": "None", 
                        "assignment": -1, 
                        "pool": json.dumps(quiz_jason_default()), 
                        "practice_mode": False, 
                        "allow_submissions": True, 
                        "next_open_date": timezone.now(), 
                        "next_close_date": timezone.now(), 
                        }]
        }

        request = self.client.post(path='/api/topics/',
                              data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)


    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_quiz1(self):     # Update a single quiz
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment
        )

        data_parameters = {
            "assignment": str(assignment.pk), 
            "next_close_date": datetime.now(),
            "next_open_date": datetime.now(),
        }

        request = self.client.put(path='/api/quizzes/' + str(quiz.pk), data=data_parameters, format='json')
        request_data = request.json()
        print("DATA", request_data)
        self.assertEqual(200, request.status_code)


    def test_put_quiz2(self):     # Can't PUT a quiz with invalid info
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment
        )

        data_parameters = {
            "assignment": "eeeeeeeeeeeee", 
            "allow_submissions": False
        }

        request = self.client.put(path='/api/quizzes/' + str(quiz.pk), data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_put_quiz3(self):     # Can't PUT with no pk
        request = self.client.put(path='/api/quizzes/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_quiz4(self):     # Can't PUT with non-existent pk
        request = self.client.put(path='/api/quizzes/1000000000000', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    def test_delete_quiz1(self):   # DELETE quiz
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment
        )

        request = self.client.delete(path='/api/quizzes/' + str(quiz.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_quiz2(self):   # Can't DELETE when no pk provided
        request = self.client.delete(path='/api/assignments/', format='json')
        self.assertEqual(400, request.status_code)

    def test_delete_quiz3(self):   # Can't DELETE with invalid pk
        request = self.client.delete(path='/api/assignments/99999999999999', format='json')
        self.assertEqual(404, request.status_code)


class Test_QuizQuestions(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        # Student.objects.create(name="name1", course=course1)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_qq1(self):     # Without pk, this will return list of all
        request = self.client.get(path='/api/quiz-questions/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_qq2(self):     # Get all quizzes for a single topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment,
        )
        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type = 0
        )

        request = self.client.get(path='/api/quiz-questions/?quizQuestionId='+str(quiz.pk), format='json')
        self.assertEqual(200, request.status_code)

    #TODO blease make this do what it says
    def test_get_qq3(self):     # Can't get quiz questions for non-existent quizzes
        request = self.client.get(
            path='/api/quiz-questions/23', format='json')
        self.assertEqual(404, request.status_code)

    def test_get_qq4(self):     # Get a single quiz question
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment,
        )
        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type = 0
        )

        request = self.client.get(path='/api/quiz-questions/' + str(quiz_question.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_qq5(self):     # CAn't GET a single quiz question with a non-existent pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment,
        )
        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type = 0
        )

        request = self.client.get(path='/api/quiz-questions/999999999999999', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_qq1(self):   # Create one quiz question
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )  
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        ) 
        quiz = Quiz.objects.create(
            assignment=assignment,
        )
        
        data_parameters = {
            "quiz-questions": [{
                        "pk": "None", 
                        'quiz': str(quiz.pk),
                        'question_type': 0,
                        'answered_correct_count': 0,
                        'answered_total_count': 0,
                        'question_parameters': '[]',
                        }]
        }

        request = self.client.post(path='/api/quiz-questions/', data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_qq2(self):   # Can't create quiz with invalid quiz question pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345")
            )
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )  
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        ) 
        quiz = Quiz.objects.create(
            assignment=assignment,
        )
        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type=0
        )

        data_parameters = {
            "quiz-questions": [{
                        "pk": "None", 
                        'quiz': 999999999999,
                        'question_type': 0,
                        'answered_correct_count': 0,
                        'answered_total_count': 0,
                        'question_parameters': '[]',
                        }]
        }

        request = self.client.post(path='/api/quiz-questions/',
                              data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)


    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_qq1(self):     # Update a single quiz question
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment
        )
        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type=0
        )

        data_parameters = {
            "pk": str(quiz_question.pk), 
            'quiz': str(quiz.pk),
            'question_type': 1,
            'answered_correct_count': 5,
            'answered_total_count': 5,
            'question_parameters': '[]',
        }

        request = self.client.put(path='/api/quiz-questions/' + str(quiz_question.pk), data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)


    def test_put_qq2(self):     # Can't PUT a quiz question with invalid info
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment
        )
        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type=0
        )

        data_parameters = {
            "quiz-questions": [{
                        "pk": "None", 
                        'quiz': "FAULTY DATA",
                        'question_type': "FAULTY DATA",
                        'answered_correct_count': 0,
                        'answered_total_count': 0,
                        'question_parameters': '[]',
                        }]
        }

        request = self.client.put(path='/api/quiz-questions/' + str(quiz_question.pk), data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_put_qq3(self):     # Can't PUT with no pk
        request = self.client.put(path='/api/quiz-questions/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_qq4(self):     # Can't PUT with non-existent pk
        request = self.client.put(path='/api/quiz-questions/1000000000000', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    def test_delete_qq1(self):   # DELETE quiz question
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        quiz = Quiz.objects.create(
            assignment=assignment
        )
        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type=0
        )

        request = self.client.delete(path='/api/quiz-questions/' + str(quiz_question.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_qq2(self):   # Can't DELETE when no pk provided
        request = self.client.delete(path='/api/quiz-questions/', format='json')
        self.assertEqual(400, request.status_code)

    def test_delete_qq3(self):   # Can't DELETE with invalid pk
        request = self.client.delete(path='/api/quiz-questions/99999999999999', format='json')
        self.assertEqual(404, request.status_code)


class Test_Search(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))

        student1 = Student.objects.create(email="test1@virginia.edu")
        student2 = Student.objects.create(email="test2@virginia.edu")
        student3 = Student.objects.create(email="test3@virginia.edu")

        # Student 1 and 2 are in class 1. Student 3 is not.
        StudentToCourse.objects.create(
            student=student1, course=course1)
        StudentToCourse.objects.create(
            student=student2, course=course1)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_search1(self):     # With query = All, this will return list of all students

        request = self.client.get(path='/api/search/?query=All', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_search2(self):     # With query = All, courseId = courseId, this will return list of all students in this class

        request = self.client.get(path='/api/search/?query=All&courseId=1', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_search3(self):     # With query = All, courseId = courseId, invert = 1, this will return list of all students who are not in this class

        request = self.client.get(path='/api/search/?query=All&courseId=1&invert=1', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_search4(self):     # With query = student, returns that student

        request = self.client.get(path='/api/search/?query=test1@virginia.edu', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_search5(self):  # With query = student, but that student does not exist, returns nothing

        request = self.client.get(path='/api/search/?query=test1@virginia.edu', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_search6(self):     # With query = All, courseId = courseId but that course does not exist, this will return nothing

        request = self.client.get(path='/api/search/?query=All&courseId=-1', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_search7(self):     # With query = All, courseId = courseId, page = 2, this will return the second page of all students in this class

        request = self.client.get(path='/api/search/?query=All&courseId=1&page=2', format='json')
        self.assertEqual(200, request.status_code)

    def test_post_search8(self):     # Not implemented

        request = self.client.post(path='/api/search/1', format='json')
        self.assertEqual(404, request.status_code)
    def test_put_search9(self):     # Not implemented

        request = self.client.put(path='/api/search/1', format='json')
        self.assertEqual(404, request.status_code)
    def test_delete_search8(self):     # Not implemented

        request = self.client.delete(path='/api/search/1', format='json')
        self.assertEqual(404, request.status_code)

class Test_Cascading_Grades(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")

        self.professor = Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')
        self.student = Student.objects.create(email="jsnow@virginia.edu",id_token="54321")
        self.course = Course.objects.create(name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=self.professor)
        self.topic = Topic.objects.create(name="topic1",course=self.course)
        self.assignment1 = Assignment.objects.create(name="easyassignment1",topic=self.topic)
        self.assignment2 = Assignment.objects.create(name="easyassignment2",topic=self.topic)

        self.studentToCourse = StudentToCourse.objects.create(student=self.student, course=self.course)
        self.studentToTopic = StudentToTopic.objects.create(student=self.student, topic=self.topic, course=self.course)
        self.studentToAssignment1 = StudentToAssignment.objects.create(student=self.student, assignment=self.assignment1)
        self.studentToAssignment2 = StudentToAssignment.objects.create(student=self.student, assignment=self.assignment2)

    def test_topic_cascade1(self):        
        self.studentToAssignment1.grade = 90
        self.studentToAssignment2.grade = 80
        self.studentToAssignment1.save()
        self.studentToAssignment2.save()

        student_to_topic = StudentToTopic.objects.get(student=self.student,topic=self.topic)

        self.assertEqual(student_to_topic.grade, 85)

    def test_topic_cascade2(self):        
        self.studentToAssignment1.grade = 90
        self.studentToAssignment2.grade = 90
        self.studentToAssignment1.save()
        self.studentToAssignment2.save()

        student_to_topic = StudentToTopic.objects.get(student=self.student,topic=self.topic)

        self.assertEqual(student_to_topic.grade, 90)

    def test_topic_cascade3(self):        
        self.studentToAssignment1.grade = 90
        self.studentToAssignment2.grade = 90
        self.studentToAssignment1.save()
        self.studentToAssignment2.save()

        student_to_topic = StudentToTopic.objects.get(student=self.student,topic=self.topic)

        self.assertEqual(student_to_topic.competency, 2) # 2 is competent
    
    def test_topic_cascade4(self):        
        self.studentToAssignment1.grade = 50
        self.studentToAssignment2.grade = 50
        self.studentToAssignment1.save()
        self.studentToAssignment2.save()

        student_to_topic = StudentToTopic.objects.get(student=self.student,topic=self.topic)

        self.assertEqual(student_to_topic.competency, 1) # 1 is competent
    
    def test_topic_cascade5(self):        
        self.studentToAssignment1.grade = 20
        self.studentToAssignment2.grade = 20
        self.studentToAssignment1.save()
        self.studentToAssignment2.save()

        student_to_topic = StudentToTopic.objects.get(student=self.student,topic=self.topic)

        self.assertEqual(student_to_topic.competency, 0) # 0 is not competent

    def test_grade_cascade1(self):        
        self.studentToAssignment1.grade = 100
        self.studentToAssignment2.grade = 100
        self.studentToAssignment1.save()
        self.studentToAssignment2.save()

        student_to_topic = StudentToTopic.objects.get(student=self.student,topic=self.topic)
        student_to_course = StudentToCourse.objects.get(student=self.student,course=self.course)

        self.assertEqual(student_to_course.grade, 62) # A 62 (D-) is set when a student achieves competency or mastery in one topic (Defined by the defaults in models.py for GradeThresholds)

    def test_grade_cascade2(self):   

        gt = GradeThreshold.objects.get(course=self.course)
        gt.a_plus_mastery = 0
        gt.a_plus_competency = 1
        gt.save()

        self.studentToAssignment1.grade = 50
        self.studentToAssignment2.grade = 50
        self.studentToAssignment1.save()
        self.studentToAssignment2.save()

        student_to_topic = StudentToTopic.objects.get(student=self.student,topic=self.topic)
        student_to_course = StudentToCourse.objects.get(student=self.student,course=self.course)

        self.assertEqual(student_to_course.grade, 100) # A+ is awarded because the threshold for an A+ was set to competency is in at least one topic

class Test_Assignment_Topic_Upload(APITestCase):

    def setUp(self):
        Student.objects.create(id=0,email="jsnow@virginia.edu",id_token="54321")

        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')
        course = Course.objects.create(name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")

    # Should fail due to improper authentication
    def test_assignment_topic_upload1(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "543212")
        request = self.client.post(path='/api/courseAssignmentUpload/0',
                                     data=None)
        self.assertEqual(401, request.status_code)

    # Should fail due to no csv 
    def test_assignment_topic_upload2(self):
        request = self.client.post(path='/api/courseAssignmentUpload/0',
                                     data=None)
        self.assertEqual(400, request.status_code)

    # Should fail due to no course pk specified
    def test_assignment_topic_upload3(self):
        request = self.client.post(path='/api/courseAssignmentUpload/',
                                     data=None)
        self.assertEqual(404, request.status_code)

    # Should fail authentication for student users
    def test_assignment_topic_upload4(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "54321")
        request = self.client.post(path='/api/courseAssignmentUpload/0',
                                    data=None)
        self.assertEqual(403, request.status_code)
    # CSV upload for assignments should work
    def test_assignment_topic_upload5(self):
        with open('csv_test/students.csv') as students:
            request = self.client.post(path='/api/courseRosterUpload/0', data={'csv': students})
        with open('csv_test/assignments.csv') as assignments:
            request = self.client.post(path='/api/courseAssignmentUpload/0', data={'csv': assignments})
        self.assertEqual(200, request.status_code)
    # CSV upload for grades should work
    def test_assignment_topic_upload6(self):
        with open('csv_test/students.csv') as students:
            request = self.client.post(path='/api/courseRosterUpload/0', data={'csv': students})
        with open('csv_test/assignments.csv') as assignments:
            request = self.client.post(path='/api/courseAssignmentUpload/0', data={'csv': assignments})
        with open('csv_test/grades.csv') as grades:
            request = self.client.post(path='/api/courseGradesUpload/0', data={'csv': grades})
        self.assertEqual(200, request.status_code)

'''
Ensure that the serialziers are not exposing the id_token or passwords of students
'''
class Test_Secure_Model_Serializer(APITestCase):

    def test_serialized_fields(self):
        secure_fields = ['password', 'id_token']                                                                     
        serializers = [ClassGraphSerializer(),StudentToCourseSerializer(), CourseSerializer(), StudentToTopicSerializer()]
        for s in serializers:
            for field in secure_fields:
                self.assertEqual(False, field in str(s))


'''
Settings
'''
class Test_Settings(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        student = Student.objects.create(id=1, first_name="Mark", last_name="Floryan", email="mrf8t@virginia.edu",
                               id_token="12345", username="mf", is_professor='t')
        settings = Settings.objects.create(color='red', nickname='Nick', user=student)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_settings1(self):     # Get one settings objects

        request = self.client.get(path='/api/settings/1', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_settings2(self):     # Get nonexistent settings object and return response

        request = self.client.get(path='/api/settings/-1', format='json')  # This returns a valid response even though
        self.assertEqual(200, request.status_code)                         # no settings exist due to the prior team's design

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_settings1(self):     # Create settings objects

        student = Student.objects.get(id_token="12345")
        data = {
            'color' : '#FFFFFF',
            'user' : student.pk
        }
        
        request = self.client.delete(path='/api/settings/1', format='json') # Delete it before creating it
        request = self.client.post(path='/api/settings/', data=data, format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_settings2(self):     # If a student already has a settings object, you cannot create another one for that student

        student = Student.objects.get(id_token="12345")
        data = {
            'color' : '#FFFFFF',
            'user' : student.pk
        }
        
        request = self.client.post(path='/api/settings/', data=data, format='json')
        self.assertEqual(409, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_settings1(self):  # Edit settings objects

        data = {
            'colors': {'hex' : '#FFFFFF'},
            'nickname': 'student'
        }

        request = self.client.put(path='/api/settings/1', data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_settings2(self):  # Edit settings objects that does not exist and return object not found

        self.client.delete(path='/api/settings/1', format='json')

        data = {
            'colors': {'hex' : '#FFFFFF'},
            'nickname': 'student'
        }

        request = self.client.put(path='/api/settings/-1', data=data, format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_settings1(self):  # Edit settings objects

        request = self.client.delete(path='/api/settings/1', format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_settings2(self):  # Edit settings objects

        request = self.client.delete(path='/api/settings/1', format='json')
        request = self.client.delete(path='/api/settings/1', format='json')
        self.assertEqual(404, request.status_code)

'''
Settings
'''
class Test_Resources(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        student = Student.objects.create(id=1, first_name="Mark", last_name="Floryan", email="mrf8t@virginia.edu",
                                         id_token="12345", username="mf", is_professor='t')
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",
            professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course)
        resource = Resources.objects.create(
            link='www.google.com',
            topic=topic,
            name='Quiz Answers')

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_resources1(self):     # Get resources objects

        request = self.client.get(path='/api/resources/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_resources2(self):     # Get one resources object

        request = self.client.get(path='/api/resources/1', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_resources3(self):     # Get nonexistent resources object

        request = self.client.get(path='/api/resources/99999', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_resources1(self):     # Create resources object

        topic = Topic.objects.get(name="topic1")
        data = {
            'link' : 'www.google.com',
            'topic' : topic.pk,
            'name' : 'Quiz Answers'
        }

        request = self.client.post(path='/api/resources/', data=data, format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_resources1(self):  # Edit resources objects

        topic = Topic.objects.get(name="topic1")
        data = {
            'link': 'www.google.com',
            'topic': topic.pk,
            'name': 'Quiz Answers'
        }

        request = self.client.put(path='/api/resources/1', data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_resources2(self):  # Edit resources objects that does not exist and return object not found

        topic = Topic.objects.get(name="topic1")
        data = {
            'link': 'www.google.com',
            'topic': topic.pk,
            'name': 'Quiz Answers'
        }

        request = self.client.put(path='/api/resources/999999', data=data, format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_resources1(self):  # Delete resources objects

        request = self.client.delete(path='/api/resources/1', format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_resources2(self):  # Try to delete nonexistent resources objects

        request = self.client.delete(path='/api/resources/999999', format='json')
        self.assertEqual(404, request.status_code)


class Test_CourseTopicToStudent(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')


        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))

        student1 = Student.objects.create(email="test1@virginia.edu",id_token="54321")
        student2 = Student.objects.create(email="test2@virginia.edu")
        student3 = Student.objects.create(email="test3@virginia.edu")

        # Student 1 and 2 are in class 1. Student 3 is not.
        StudentToCourse.objects.create(
            student=student1, course=course1)
        StudentToCourse.objects.create(
            student=student2, course=course1)
        Topic.objects.create(course=course1,name="hello")

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_coursetopictostudent1(self):     # gets grades for the professor
        request = self.client.get(path='/api/coursetopictostudent/1/1', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_coursetopictostudent2(self):     # Course does not exist

        request = self.client.get(path='/api/coursetopictostudent/10000/1', format='json')
        self.assertEqual(404, request.status_code)

    def test_post_coursetopictostudent1(self):     # Not used, should return bad request

        request = self.client.post(path='/api/coursetopictostudent/1', format='json')
        self.assertEqual(404, request.status_code)
    def test_put_coursetopictostudent1(self):     # Not used, should return bad request

        request = self.client.put(path='/api/coursetopictostudent/1', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_coursetopictostudent1(self):     # Not used, should return bad request

        request = self.client.delete(path='/api/coursetopictostudent/1', format='json')
        self.assertEqual(404, request.status_code)

'''
Settings
'''
class Test_QuizInterface(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
        student = Student.objects.create(id=1, first_name="Mark", last_name="Floryan", email="mrf8t@virginia.edu",
                                         id_token="12345", username="mf", is_professor='t')
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1",professor=Student.objects.get(id_token="12345"))
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )
        assignment = Assignment.objects.create(
            name="assignment1",
            topic=topic
        )
        # The quiz must be open when submitting answers, so set the close date to tomorrow and the open date to yesterday
        tomorrow_datetime = datetime.now() + timedelta(days=1)
        yesterday_datetime = datetime.now() - timedelta(days=1)
        quiz = Quiz.objects.create(
            assignment=assignment,
            next_close_date=tomorrow_datetime,
            next_open_date=yesterday_datetime,
            pool = json.dumps({"parsons": 0, "multiple_choice": 1, "select_all": 1, "free_response": 0})
        )

        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type = 0,
            question_parameters=json.dumps({
                "question": "Which is correct?",
                "choices": [
                    "a",
                    "b",
                    "c",
                    "d"
                ],
                "answer": 2
            })
        )

        quiz_question = QuizQuestion.objects.create(
            quiz=quiz,
            question_type = 2,
            question_parameters=json.dumps({
                "question": "Which are correct?",
                "choices": [
                    "a",
                    "b",
                    "c",
                    "d"
                ],
                "answer": [0,1,2,3]
            })
        )

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_quiz_interface(self):     # Not implemented

        request = self.client.get(path='/api/quiz-interface/1', format='json')
        self.assertEqual(400, request.status_code)


    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_quiz_interface_mc(self):     # Submit multiple choice quiz question
        data = {
        "selection": 0,
        "quizPK": 1,
        "assignmentPK": 1,
        "practice_mode": False,
        }
        request = self.client.post(path='/api/quiz-interface/1', data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_quiz_interface_select_all(self):     # Submit select all quiz question
        data = {
        "all_selections": [0,1],
        "quizPK": 1,
        "assignmentPK": 1,
        "practice_mode": False,
        }
        request = self.client.post(path='/api/quiz-interface/2', data=data, format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_quiz_interface(self):  # Not implemented

        request = self.client.put(path='/api/quiz-interface/1', data={}, format='json')
        self.assertEqual(400, request.status_code)


    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_quiz_interface(self):  # Not implemented

        request = self.client.delete(path='/api/quiz-interface/1', format='json')
        self.assertEqual(400, request.status_code)


class Test_Assignment_Quiz_Upload(APITestCase):

    def setUp(self):
        Student.objects.create(id=0,email="jsnow@virginia.edu",id_token="54321")

        Student.objects.create(id=1,first_name="Mark",last_name="Floryan",email="mrf8t@virginia.edu",id_token="12345",username="mf",is_professor='t')
        course = Course.objects.create(name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        assignment = Assignment.objects.create(name="assignment1",topic=topic)
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "12345")
    
    # Should fail due to improper authentication
    def test_assignment_quiz_upload1(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "543212")
        request = self.client.post(path='/api/assignmentQuizUpload/1',
                                     data=None)
        self.assertEqual(401, request.status_code)

    # Should fail due to no csv 
    def test_assignment_quiz_upload2(self):
        request = self.client.post(path='/api/assignmentQuizUpload/1',
                                     data=None)
        self.assertEqual(400, request.status_code)

    # Should fail due to no course pk specified
    def test_assignment_quiz_upload3(self):
        request = self.client.post(path='/api/assignmentQuizUpload/',
                                     data=None)
        self.assertEqual(404, request.status_code)

    # Should fail authentication for student users
    def test_assignment_quiz_upload4(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "54321")
        request = self.client.post(path='/api/assignmentQuizUpload/1',
                                    data=None)
        self.assertEqual(403, request.status_code)

    # CSV upload for quizzes should work
    def test_assignment_quiz_upload5(self):
        with open('csv_test/quiz.csv') as quiz:
            request = self.client.post(path='/api/assignmentQuizUpload/1', data={'csv': quiz})
        self.assertEqual(200, request.status_code)

    # CSV upload for quizzes should work and have the object created
    def test_assignment_quiz_upload6(self):
        with open('csv_test/quiz.csv') as quiz:
            request = self.client.post(path='/api/assignmentQuizUpload/1', data={'csv': quiz})
        qs = len(QuizQuestion.objects.all())
        self.assertEqual(200, request.status_code)
        with open('csv_test/quiz.csv') as quiz:
            request = self.client.post(path='/api/assignmentQuizUpload/1', data={'csv': quiz})
        self.assertEqual(200, request.status_code)
        quiz_count = len(Quiz.objects.all())
        self.assertEqual(quiz_count, 1)
        self.assertEqual(len(QuizQuestion.objects.all()),qs)

    # CSV upload for quizzes should work and have the object created
    def test_assignment_quiz_upload7(self):
        with open('csv_test/quiz.csv') as quiz:
            request = self.client.post(path='/api/assignmentQuizUpload/1', data={'csv': quiz})
        self.assertEqual(200, request.status_code)
        quiz_question_count = len(QuizQuestion.objects.all())
        self.assertEqual(quiz_question_count, 3)

# Ensure permissions are working properly for student grades
class Test_Student_To_Assignment_Security(APITestCase):

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Authorization: Bearer ' + "54321")
        john = Student.objects.create(id=0,email="jsnow@virginia.edu",id_token="54321")
        connor = Student.objects.create(id=1,email="csnow@virginia.edu",id_token="66666")
        course = Course.objects.create(name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        assignment = Assignment.objects.create(name="assignment1",topic=topic)
        student_to_course = StudentToCourse.objects.create(student=connor,course=course)
        student_to_course2 = StudentToCourse.objects.create(student=john,course=course)
        student_to_topic = StudentToTopic.objects.create(student=connor,topic=topic)
        student_to_topic2 = StudentToTopic.objects.create(student=john,topic=topic)
        studentToAssignment1 = StudentToAssignment.objects.create(student=connor, assignment=assignment, grade=100)
        studentToAssignment2 = StudentToAssignment.objects.create(student=john, assignment=assignment, grade=50)

    # Ensure students cannot view grades of other students
    
    def test_view_other_student_grades(self):
        request_data = self.client.get(path='/api/studenttoassignments/',data=None).json()
        for student_to_assignment in request_data:
            self.assertEqual(student_to_assignment['student'],0) # User john is making this api request, so ensure all grades returned belong to john who has id 0

    # Ensure students cannot create grades
    def test_post_student_grades(self):
        request_data = self.client.post(path='/api/studenttoassignments/',data=None).json()
        self.assertEqual(request_data['detail'],'You do not have permission to perform this action.')

    # Ensure students cannot delete other grades
    def test_delete_student_grades(self):
        request_data = self.client.delete(path='/api/studenttoassignments/').json()
        self.assertEqual(request_data['detail'],'You do not have permission to perform this action.')

    # Ensure students cannot update grades
    def test_update_student_grades(self):
        request_data = self.client.put(path='/api/studenttoassignments/', data=None).json()
        self.assertEqual(request_data['detail'],'You do not have permission to perform this action.')
    