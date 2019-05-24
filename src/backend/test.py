from rest_framework.test import APIClient, APIRequestFactory, URLPatternsTestCase, force_authenticate, APITestCase
from rest_framework import status
from rest_framework.test import APITestCase
from sptApp.responses import colliding_id_response
from sptApp.models import *
from sptApp.responses import *
from django.test import TestCase
from django.test import Client
from sptApp.apps import SptappConfig
from django.apps import apps
from sptApp import models
from sptApp import views
from django.core.exceptions import ImproperlyConfigured
import sptApp
import django
import unittest
from unittest import mock
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spt.settings")
django.setup()
import json

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
        self.assertEqual(SptappConfig.name, 'sptApp')
        self.assertEqual(apps.get_app_config('sptApp').name, 'sptApp')


class Test_Quiz(TestCase):  # pragma: no cover

    # Needded for "creating objects in database"
    def setUp(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        topic2 = Topic.objects.create(name="topic2", course=course1)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        quiz_questions = []
        quiz_question_answers = []

        for i in range(5):
            question = QuizQuestion(
                text="question_${i}",
                question_type=0,
                quiz=quiz,
                total_points=1,
                index=i
            )

            answers = []
            for i in range(3):
                answer = QuizQuestionAnswer(
                    text="yabba-dabba-doo-${i}",
                    question=question,
                    weight=1,
                    correct=(i % 3 == 0),
                    index=i
                )
                answers.append(answer)

            quiz_questions.append(question)
            quiz_question_answers.append(answers)

        # Student to quiz set up

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_quiz1(self):  # No Data = error
        client = APIClient()
        request = client.post(path='/api/quiz/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz2(self):  # Providing a pk to the url = error
        client = APIClient()
        request = client.post(path='/api/quiz/1233333332322/', format='json')
        self.assertEqual(400, request.status_code)

    # def test_post_quiz2(self):   # Create student
    #     client = APIClient()
    #     student = Student.objects.create(email="first1last1@gmail.com", first_name="first1", last_name="last1")
    #     course1 = Course.objects.create(name="courseName1",course_code="courseCode1",subject_code="subjectCode1")
    #     topic = Topic.objects.create(name="topic1", course=course1)

    #     data = {
    #       "topic_id": 1,
    #       "answers": [
    #         { },

    #       ]
    #     }
    #     request = client.post(path='/api/student/quiz/1', data=data, format='json')
    #     self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_quiz1(self):   # Get existing student
        client = APIClient()
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        request = client.get(path='/api/quiz/' +
                             str(temp_topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_get_quiz2(self):   # Get non-existing student
        client = APIClient()
        request = client.get(path='/api/quiz/12343342322222', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_quiz1(self):   # Delete existing student
        client = APIClient()
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        request = client.delete(
            path='/api/quiz/' + str(quiz.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_quiz2(self):   # Delete without pk value = error
        client = APIClient()
        request = client.delete(path='/api/quiz/', format='json')
        self.assertEqual(400, request.status_code)

    def test_delete_quiz3(self):   # Delete with invalid pk value = error
        client = APIClient()
        request = client.delete(path='/api/quiz/12222222', format='json')
        self.assertEqual(404, request.status_code)


class Test_StudentToCourse(TestCase):

    # Needded for "creating objects in database"
    def setUp(self):
        pass

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_student_to_course1(self):  # No Data = error
        client = APIClient()
        request = client.post(path='/api/student/course/', format='json')
        self.assertEqual(400, request.status_code)

    # Providing a pk to the url = error
    def test_post_student_to_course2(self):
        client = APIClient()
        request = client.post(
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s",
            "id_token": "fdasasd"
        }
        request = client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
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

        client = APIClient()
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        DATA_PARAMETERS = {
            "course": str(1000000),
            "student": str(student.pk),
            "semester": "2018-s",
            "id_token": "fdasasd"
        }
        request = client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")

        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s"
        }
        request = client.post(path='/api/student/course/',
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")

        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(1000000000),
            "semester": "2018-s"
        }
        request = client.post(path='/api/student/course/',
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s"
        }
        request = client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')

        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't POST student to course when google errors out
    def test_post_student_to_course8(self, mock_request):
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s",
            "id_token": "fdasasd"
        }
        request = client.post(path='/api/student/course/',
                              data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)
    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_student_to_course1(self):   # Get existing student
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        request = client.get(path='/api/student/course/' +
                             str(studentToCourse.pk), format='json')

        self.assertEqual(200, request.status_code)

    # Can't GET  student to course of non-existent student
    def test_get_student_to_course2(self):
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")

        request = client.get(
            path='/api/student/course/100000000', format='json')

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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(
            path='/api/student/course/?id_token=fdasasd', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    # GET all student to course  for a specific course
    def test_get_student_to_course4(self):
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(
            path='/api/student/course/?courseId=' + str(course.pk), format='json')

        self.assertEqual(200, request.status_code)

    # Can't GET all student to course for a specific (non-existent) course
    def test_get_student_to_course5(self):
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(
            path='/api/student/course/?courseId=100000000', format='json')

        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't GET student to course when google errors
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(
            path='/api/student/course/?id_token=fdasasd', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(path='/api/student/course/?courseId=' +
                             str(course.pk) + '&id_token=fdasasd', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't GET if google errors student
    def test_get_student_to_course8(self, mock_request):
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

        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(path='/api/student/course/?courseId=' +
                             str(course.pk) + '&id_token=fdasasd', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

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
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(path='/api/student/course/?courseId=' + str(
            course.pk) + '&id_token=fdasasd&view_as=' + str(student.pk), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student
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
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=student)

        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        request = client.get(path='/api/student/course/?courseId=' + str(
            course.pk) + '&id_token=fdasasd&view_as=' + str(student.pk), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student
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
            last_name=data_parameters["last_name"]
        )
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        request = client.get(path='/api/student/course/?courseId=' + str(
            course.pk) + '&id_token=fdasasd&view_as=' + str(student.pk), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student
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
            last_name=data_parameters["last_name"]
        )
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        request = client.get(path='/api/student/course/?courseId=' + str(
            course.pk) + '&id_token=fdasasd&view_as=' + str(1000000), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # GET student to course for student
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
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)

        request = client.get(path='/api/student/course/?courseId=' + str(
            10000000) + '&id_token=fdasasd&view_as=' + str(1000000), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_student_to_course1(self):   # PUT student to course
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course, semester="2018-f")

        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s"
        }

        request = client.put(path='/api/student/course/' +
                             str(studentToCourse.pk), data=DATA_PARAMETERS, format='json')

        self.assertEqual(200, request.status_code)

    # Can't PUT student to course with no pk
    def test_put_student_to_course2(self):
        client = APIClient()
        request = client.put(path='/api/student/course/', format='json')

        self.assertEqual(400, request.status_code)

    # Can't PUT student to course to non-existent student to course
    def test_put_student_to_course3(self):
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")

        DATA_PARAMETERS = {
            "course": str(course.pk),
            "student": str(student.pk),
            "semester": "2018-s"
        }

        request = client.put(path='/api/student/course/100000000',
                             data=DATA_PARAMETERS, format='json')

        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_student_to_course1(self):   # Delete student to course
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        request = client.delete(path='/api/student/course/' +
                                str(studentToCourse.pk) + '?courseId=' + str(course.pk), format='json')

        self.assertEqual(200, request.status_code)

    # Can't Delete student to course with no courseId
    def test_delete_student_to_course2(self):
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        request = client.delete(path='/api/student/course/' +
                                str(studentToCourse.pk), format='json')

        self.assertEqual(404, request.status_code)

    # Can't Delete student to course with non-existent student
    def test_delete_student_to_course3(self):
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")

        request = client.delete(
            path='/api/student/course/10000000000?courseId=' + str(course.pk), format='json')

        self.assertEqual(404, request.status_code)

    # Can't delete non-existent student to course
    def test_delete_student_to_course4(self):
        client = APIClient()
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")

        request = client.delete(path='/api/student/course/' +
                                str(student.pk) + '?courseId=' + str(course.pk), format='json')

        self.assertEqual(404, request.status_code)

    # Can't delete student to course with no pk
    def test_delete_student_to_course5(self):
        client = APIClient()

        request = client.delete(path='/api/student/course/', format='json')

        self.assertEqual(400, request.status_code)


'''
______________________________________________________________________________________________              Course
 Course: del, get, post, put
    name = models.CharField(max_length=250)
    course_code = models.CharField(max_length=250)
    subject_code = models.CharField(max_length=250)
______________________________________________________________________________________________
'''


class Test_Course(TestCase):

    def setUp(self):
        Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        Course.objects.create(
            name="courseName2", course_code="courseCode2", subject_code="subjectCode2")

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_course1(self):   # Delete existing course
        client = APIClient()
        request = client.delete(path='/api/courses/1/', format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_course2(self):   # Delete non-existing course
        client = APIClient()
        request = client.delete(path='/api/courses/100/', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_course3(self):   # Delete without pk value = error
        client = APIClient()
        request = client.delete(path='/api/courses/', format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_course1(self):     # Get All (no pk value)
        client = APIClient()
        request = client.get(path='/api/courses/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_course2(self):     # Get existing course
        client = APIClient()
        request = client.get(path='/api/courses/', data=None, format='json')
        # request = client.get(path='/api/courses/1', data=None,format='json')  # Needs to be
        self.assertEqual(200, request.status_code)

    def test_get_course3(self):     # Get non-existing course = error
        client = APIClient()
        request = client.get(path='/api/courses/', data=None, format='json')
        # request = client.get(path='/api/courses/5', data=None,format='json')  # Needs to be
        self.assertEqual(200, request.status_code)

    def test_get_course4(self):   # Get course with pk value
        client = APIClient()
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        request = client.get(path='/api/courses/' +
                             str(course1.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_get_course5(self):   # Can't Get course that doesn't exist
        client = APIClient()
        request = client.get(path='/api/courses/10000000000000', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_course1(self):    # No Data = error
        client = APIClient()
        request = client.post(path='/api/courses/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_course2(self):    # No pk value = add if correct data format
        data_parameters = {
            "name": "Coooool Course Name",
            "course_code": "123454322",
            "subject_code": "989090750",
        }
        client = APIClient()
        request = client.post(path='/api/courses/',
                              data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_course3(self):    # Can't POST to existing pk
        client = APIClient()
        request = client.post(path='/api/courses/10000000', format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_course1(self):   # Edit course with and pk with data
        client = APIClient()
        data_parameters = {
            "name": "Dan's Class Now",
            "course_code": "123123",
            "subject_code": "456456",
        }
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        request = client.put(
            path='/api/courses/' + str(course1.pk), data=data_parameters, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_course2(self):   # Edit course with pk and without data = error
        client = APIClient()
        data_parameters = None
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        request = client.put(
            path='/api/courses/' + str(course1.pk), data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_put_course3(self):   # Edit course without pk and with data = error
        client = APIClient()
        data_parameters = {
            "name": "Dan's Class Now",
            "course_code": "123123",
            "subject_code": "456456",
        }
        course1 = None
        request = client.put(path='/api/courses/',
                             data=data_parameters, format='json')
        self.assertEqual(400, request.status_code)

    def test_put_course4(self):   # Can't put to non-existent course
        client = APIClient()
        request = client.put(path='/api/courses/10000000000000', format='json')
        self.assertEqual(404, request.status_code)




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


class Test_Student(TestCase):

    # Needded for "creating objects in database"
    def setUp(self):
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

    def test_delete_students1(self):   # Delete existing student
        client = APIClient()
        request = client.delete(path='/api/students/1/', format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_students2(self):   # Delete non-existing student
        client = APIClient()
        request = client.delete(path='/api/students/100/', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_students3(self):   # Delete without pk value = error
        client = APIClient()
        request = client.delete(path='/api/students/', format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_students1(self):   # Get All (no pk value)
        client = APIClient()
        request = client.get(path='/api/students/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_student2(self):   # Get student with pk value
        client = APIClient()
        student1 = Student.objects.create(
            email="first4last4@gmail.com", first_name="first4", last_name="last4")
        request = client.get(path='/api/students/' +
                             str(student1.pk), data=None, format=None)
        self.assertEqual(200, request.status_code)

    # Get All (no pk value and id_token for the requester)
    def test_get_students3(self):
        client = APIClient()
        request = client.get(
            path='/api/students/?id_token=sdfasdfsa', format='json')
        self.assertEqual(400, request.status_code)

    def test_get_student4(self):   # Can't get student with invalid pk
        client = APIClient()
        student1 = Student.objects.create(
            email="first4last4@gmail.com", first_name="first4", last_name="last4")
        request = client.get(path='/api/students/' +
                             str(student1.pk+1), data=None, format=None)
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_get_student5(self, mock_request):   # Get student with id_token
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
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
        client = APIClient()
        request = client.get(
            path='/api/students/?id_token=dasfasfa', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "dasfasfa"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't get student with id_token that returns invalid email
    def test_get_student6(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        mock_response = mock.Mock()
        expected_dict = {
            'iss': 'accounts.google.com',
            'sub': 'sadfdsfas',
            'hd': 'virginia.edu',
            'email': "fakeemail@virginia.edu",
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
        client = APIClient()
        request = client.get(
            path='/api/students/?id_token=dasfasfa', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "dasfasfa"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    @mock.patch('sptApp.api_views.requests.post')
    # Signup new student, email already in use
    def test_post_student1(self, mock_request):

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
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
        client = APIClient()
        request = client.post(
            path='/api/students/?id_token=dasfasfa', data=data_parameters, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Signin as student, without signing up first
    def test_post_student2(self, mock_request):

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": False,
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
        client = APIClient()
        request = client.post(
            path='/api/students/?id_token=dasfasfa', data=data_parameters, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_post_student3(self, mock_request):   # Signin as student

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": False,
            "isProfessor": True,
        }
        Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
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
        client = APIClient()
        request = client.post(
            path='/api/students/?id_token=dasfasfa', data=data_parameters, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_post_student4(self, mock_request):   # Successful signup

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
        client = APIClient()
        request = client.post(
            path='/api/students/?id_token=dasfasfa', data=data_parameters, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_post_student5(self, mock_request):   # Can't signup if google errors

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
        client = APIClient()
        request = client.post(
            path='/api/students/?id_token=dasfasfa', data=data_parameters, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    def test_post_student6(self):   # Can't signup if google errors
        client = APIClient()
        request = client.post(
            path='/api/students/1', format='json')
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_post_student7(self, mock_request):   # Successful signup

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        # Student.objects.create(
        #     email=data_parameters["email"],
        #     first_name=data_parameters["first_name"],
        #     last_name=data_parameters["last_name"]
        # )
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
        client = APIClient()
        request = client.post(
            path='/api/students/?id_token=dasfasfa', data=data_parameters, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_student1(self):   # Can't PUT with no pk

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )

        client = APIClient()
        request = client.put(
            path='/api/students/?id_token=dasfasfa', data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_put_student2(self):   # Basic PUT test

        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "uniquesnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )

        client = APIClient()
        request = client.put(path='/api/students/' + str(student.pk) +
                             '?id_token=dasfasfa', data=data_parameters, format='json')

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
        }

        client = APIClient()
        request = client.put(path='/api/students/' + str(student.pk) +
                             '?id_token=dasfasfa', data=data_parameters, format='json')

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
            "email": "jsnow@virgini.edu",  # Not proper form of email
        }

        client = APIClient()
        request = client.put(
            path='/api/students/1000000000?id_token=dasfasfa', data=data_parameters, format='json')

        self.assertEqual(404, request.status_code)


"""         Right Now we got to figure out how to set up a topic first """
'''
______________________________________________________________________________________________      Topics
 Topics: del, get, post, put
    name = models.CharField(max_length=250)
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
______________________________________________________________________________________________
'''


class Test_Topics(TestCase):

    def setUp(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        # Student.objects.create(name="name1", course=course1)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_topics1(self):     # Without pk, this will return list of all
        client = APIClient()
        request = client.get(path='/api/topics/', data=None, format='json')
        self.assertEqual(200, request.status_code)

    def test_get_topics2(self):     # Get all topics for a single course
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )

        client = APIClient()
        request = client.get(path='/api/topics/?courseId=' +
                             str(course.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_get_topics3(self):     # Can't get topics for non-existent classes
        client = APIClient()
        request = client.get(
            path='/api/topics/?courseId=1000000000000', format='json')

        self.assertEqual(404, request.status_code)

    def test_get_topics4(self):     # Get a single topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )

        client = APIClient()
        request = client.get(path='/api/topics/' +
                             str(topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_get_topics5(self):     # CAn't GET a single topic with a non-existent pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )

        client = APIClient()
        request = client.get(path='/api/topics/10000000', format='json')

        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_topic1(self):   # Create multiple topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        data_parameters = [
            {"pk": "None", "course": str(course.pk), "name": "A"},
            {"pk": "None", "course": str(course.pk), "name": "B"}
        ]

        client = APIClient()
        request = client.post(path='/api/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    def test_post_topic2(self):   # Can't POST to already existing PK
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        data_parameters = [
            {"pk": "None", "course": str(course.pk), "name": "A"},
            {"pk": "None", "course": str(course.pk), "name": "B"}
        ]

        client = APIClient()
        request = client.post(path='/api/topics/2',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_post_topic3(self):   # Can't create topic with invalid course pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        data_parameters = [
            {"pk": "None", "course": -1, "name": "A"},
            {"pk": "None", "course": -1, "name": "B"}
        ]

        client = APIClient()
        request = client.post(path='/api/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_post_topic4(self):   # Create multiple topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)
        data_parameters = [
            {"pk": "None", "course": str(course.pk), "name": "A"},
            {"pk": "None", "course": str(course.pk), "name": "B"}
        ]

        client = APIClient()
        request = client.post(path='/api/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)
    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_topics1(self):     # Update a single topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )

        data_parameters = {
            "course": str(course.pk), "name": "A new"
        }

        client = APIClient()
        request = client.put(path='/api/topics/' + str(topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    def test_put_topics2(self):     # Can't PUT a topic with invalid info
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="topic1",
            course=course
        )

        data_parameters = {
            "course": "100000000000",  # Invalid pk for course
            "name": "A new"
        }

        client = APIClient()
        request = client.put(path='/api/topics/' + str(topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_put_topics3(self):     # Can't PUT with no pk

        client = APIClient()
        request = client.put(path='/api/topics/', format='json')

        self.assertEqual(400, request.status_code)

    def test_put_topics4(self):     # Can't PUT with non-existent pk

        client = APIClient()
        request = client.put(path='/api/topics/1000000000000', format='json')

        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    def test_delete_topic1(self):   # DELETE topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="TobeDeleted",
            course=course
        )

        client = APIClient()
        request = client.delete(path='/api/topics/' +
                                str(topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_delete_topic2(self):   # Can't DELETE when no pk provided
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="TobeDeleted",
            course=course
        )

        client = APIClient()
        request = client.delete(path='/api/topics/', format='json')

        self.assertEqual(400, request.status_code)

    def test_delete_topic3(self):   # Can't DELETE with invalid pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(
            name="TobeDeleted",
            course=course
        )

        client = APIClient()
        request = client.delete(path='/api/topics/100000000000', format='json')

        self.assertEqual(404, request.status_code)


'''
______________________________________________________________________________________________      Topic to Topic
 TopicToTopic: del, get, post, put
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
    ancestor_node = models.ForeignKey(Topic,  on_delete=models.CASCADE)
    topic_node = models.ForeignKey(Topic, on_delete=models.CASCADE)
______________________________________________________________________________________________
'''


class Test_Topic_To_Topics(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    # Without pk, this will return list of all
    def test_get_topic_to_topic1(self):
        client = APIClient()
        request = client.get(path='/api/topic/topics/',
                             data=None, format='json')
        self.assertEqual(200, request.status_code)

    # With pk, this will a specific topic to topic
    def test_get_topic_to_topic2(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )

        client = APIClient()
        request = client.get(path='/api/topic/topics/' +
                             str(topic_to_topic.pk), format='json')
        self.assertEqual(200, request.status_code)

    # Will return an empty array because we are using filter
    def test_get_topic_to_topic3(self):     # Can't find non-existent pk
        client = APIClient()
        request = client.get(
            path='/api/topic/topics/1000000000', format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_topic_to_topic1(self):   # Create topic to topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
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

        client = APIClient()
        request = client.post(path='/api/topic/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    # Can't create topic to topic with invalid data
    def test_post_topic_to_topic2(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
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

        client = APIClient()
        request = client.post(path='/api/topic/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    # Can't post topic to topic to pre-existing pk
    def test_post_topic_to_topic3(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
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

        client = APIClient()
        request = client.post(path='/api/topic/topics/1',
                              data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    def test_post_topic_to_topic11(self):   # Create topic to topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
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

        client = APIClient()
        request = client.post(path='/api/topic/topics/',
                              data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)


    '''
    __________________________________________________      Put
    __________________________________________________
    '''

    def test_put_topic_to_topic1(self):     # Can't PUT with null pk
        client = APIClient()
        request = client.put(path='/api/topic/topics/', format='json')

        self.assertEqual(400, request.status_code)

    def test_put_topic_to_topic2(self):     # Can't PUT to non-existent pk
        client = APIClient()
        request = client.put(
            path='/api/topic/topics/100000000000', format='json')

        self.assertEqual(404, request.status_code)

    def test_put_topic_to_topic3(self):   # PUT topic to topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = {"course": str(course.pk), "topic_node": str(
            topic1.pk),  "ancestor_node": str(topic2.pk)}

        client = APIClient()
        request = client.put(path='/api/topic/topics/' + str(topic_to_topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    def test_put_topic_to_topic4(self):   # Can't PUT with invalid data
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = {"coursed": str(course.pk), "topic_node": str(
            topic1.pk),  "ancestor_node": str(topic2.pk)}

        client = APIClient()
        request = client.put(path='/api/topic/topics/' + str(topic_to_topic.pk),
                             data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    def test_delete_topic_to_topic1(self):   # DELETE topic to topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        client = APIClient()
        request = client.delete(
            path='/api/topic/topics/' + str(topic_to_topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_delete_topic_to_topic2(self):   # DELETE multiple topic to topics
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
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
        client = APIClient()
        request = client.delete(path='/api/topic/topics/',
                                data=data_parameters, format='json')

        self.assertEqual(200, request.status_code)

    # Can't DELETE multiple topic to topics when pk is invalid
    def test_delete_topic_to_topic5(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)
        topic3 = Topic.objects.create(name="topic3", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = [str(topic_to_topic.pk), str(1000000000)]
        client = APIClient()
        request = client.delete(path='/api/topic/topics/',
                                data=data_parameters, format='json')

        self.assertEqual(404, request.status_code)

    # Can't DELETE multiple topic to topics when request is empty
    def test_delete_topic_to_topic4(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)
        topic3 = Topic.objects.create(name="topic3", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )
        data_parameters = []
        client = APIClient()
        request = client.delete(path='/api/topic/topics/',
                                data=data_parameters, format='json')

        self.assertEqual(400, request.status_code)

    # Can't DELETE single topic to topics with no pk
    def test_delete_topic_to_topic3(self):
        client = APIClient()
        request = client.delete(path='/api/topic/topics/', format='json')

        self.assertEqual(400, request.status_code)

    # Can't DELETE single topic to topics with invalid pk
    def test_delete_topic_to_topic3(self):
        client = APIClient()
        request = client.delete(
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


class Test_Student_To_Topic(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    # Without pk, this will return list of all
    def test_get_student_to_topic1(self):
        client = APIClient()
        request = client.get(path='/api/student/topics/',
                             data=None, format='json')
        self.assertEqual(200, request.status_code)

    # Can't get with non-existent student pk
    def test_get_student_to_topic2(self):
        client = APIClient()
        request = client.get(
            path='/api/student/topics/1000000000/2000000000', format='json')
        self.assertEqual(404, request.status_code)

    # Can't get with non-existent course pk
    def test_get_student_to_topic3(self):
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        client = APIClient()
        request = client.get(
            path='/api/student/topics/2000000000/' + str(student.pk), format='json')
        self.assertEqual(404, request.status_code)

    def test_get_student_to_topic4(self):     # GET student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)
        client = APIClient()
        request = client.get(path='/api/student/topics/' +
                             str(course1.pk) + '/' + str(student.pk), format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________      Post
    __________________________________________________
    '''

    def test_post_student_to_topic1(self):   # Can't POST to null student pk
        client = APIClient()
        request = client.post(
            path='/api/student/topics/2000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_post_student_to_topic2(self):   # Can't POST to null student pk
        client = APIClient()
        request = client.post(path='/api/student/topics/',
                              data={
                                  "student": str(1000000000000),
                                  "topics": []
                              }, format='json')
        self.assertEqual(404, request.status_code)

    def test_post_student_to_topic3(self):   # POST to student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)

        client = APIClient()
        request = client.post(path='/api/student/topics/',
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
        client = APIClient()
        request = client.put(path='/api/student/topics/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_student_to_topic2(self):     # Can't PUT to non-existent pk
        client = APIClient()
        request = client.put(
            path='/api/student/topics/?studentToTopicId=100000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_put_student_to_topic3(self):     # PUT student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)

        DATA_PARAMETERS = {
            "student": str(student.pk),
            "topic": str(topic.pk),
            "grade": 100,
            "locked": False,
        }

        client = APIClient()
        request = client.put(path='/api/student/topics/?studentToTopicId=' +
                             str(student_to_topic.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't PUT student to topic with invalid serializer
    def test_put_student_to_topic4(self):
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)

        DATA_PARAMETERS = {
            "yolo": False,
        }

        client = APIClient()
        request = client.put(path='/api/student/topics/?studentToTopicId=' +
                             str(student_to_topic.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________      Delete
    __________________________________________________
    '''

    # Can't DELETE student to topic with null pk
    def test_delete_student_to_topic1(self):
        client = APIClient()
        request = client.delete(path='/api/student/topics/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't DELETE student to topic with non-existent pk
    def test_delete_student_to_topic2(self):
        client = APIClient()
        request = client.delete(
            path='/api/student/topics/?studentToTopicId=100000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_student_to_topic3(self):   # DELETE student to topic
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)
        client = APIClient()
        request = client.delete(
            path='/api/student/topics/?studentToTopicId=' + str(student_to_topic.pk), format='json')
        self.assertEqual(200, request.status_code)


'''
______________________________________________________________________________________________      Quiz
  name = models.CharField(max_length=250, default="Quiz")
  topic = models.ForeignKey(
      Topic, related_name='topic', on_delete=models.CASCADE)
______________________________________________________________________________________________
'''


class Test_Quiz(TestCase):

    # Needded for "creating objects in database"
    def setUp(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        topic2 = Topic.objects.create(name="topic2", course=course1)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        quiz_questions = []
        quiz_question_answers = []

        for i in range(5):
            question = QuizQuestion(
                text="question_${i}",
                question_type=0,
                quiz=quiz,
                total_points=1,
                index=i
            )

            answers = []
            for i in range(3):
                answer = QuizQuestionAnswer(
                    text="yabba-dabba-doo-${i}",
                    question=question,
                    weight=1,
                    correct=(i % 3 == 0),
                    index=i
                )
                answers.append(answer)

            quiz_questions.append(question)
            quiz_question_answers.append(answers)

        # Student to quiz set up

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_quiz1(self):  # No Data = error
        client = APIClient()
        request = client.post(path='/api/quiz/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz2(self):  # Providing a pk to the url = error
        client = APIClient()
        request = client.post(path='/api/quiz/1233333332322/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz3(self):   # Create quiz
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        category_2 = Category.objects.create(name="Homework")
        topic_to_cat = TopicToCategory.objects.create(category=category_2, topic=topic, weight=0.5)
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "rewqr",
                    "total_points": 1
                },
            ],
            "name": "qwwer",
            "weight": 0.5
        }
        request = client.post(path='/api/quiz/', data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_quiz4(self):   # Can't POST to quiz with non-existent topic
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        data = {
            "topic": str(1000),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "rewqr",
                    "total_points": 1
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.post(path='/api/quiz/', data=data, format='json')
        self.assertEqual(404, request.status_code)

    def test_post_quiz5(self):   # Can't Create quiz with exceeding 1 weight
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        category_2 = Category.objects.create(name="Homework")
        topic_to_cat = TopicToCategory.objects.create(category=category_2, topic=topic, weight=0.5)
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "rewqr",
                    "total_points": 1
                },
            ],
            "name": "qwwer",
            "weight": 0.7
        }
        request = client.post(path='/api/quiz/', data=data, format='json')
        self.assertEqual(409, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_quiz1(self):  # No Data = error
        client = APIClient()
        request = client.put(path='/api/quiz/', format='json')
        self.assertEqual(404, request.status_code)

    def test_put_quiz2(self):  # Providing a pk to the url = error
        client = APIClient()
        request = client.put(path='/api/quiz/1233333332322/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_quiz3(self):   # PUT Quiz
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(category=category, topic=topic)
        
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "rewqr",
                    "total_points": 1
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.put(path='/api/quiz/' +
                             str(quiz.pk), data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_quiz4(self):   # Can't PUT with non-existent topic
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(category=category, topic=topic)
        
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        data = {
            "topic": str(1000),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "rewqr",
                    "total_points": 1
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.put(path='/api/quiz/' +
                             str(quiz.pk), data=data, format='json')
        self.assertEqual(404, request.status_code)

    def test_put_quiz5(self):   # PUT with removed questions
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(category=category, topic=topic)
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "This is a new question",
                    "total_points": 1,
                },
            ],
            "deletedQuestions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "This question will be deleted",
                    "total_points": 1,
                    "pk": 1
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.put(path='/api/quiz/' +
                             str(quiz.pk), data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_quiz6(self):   # PUT with removed answers
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(category=category, topic=topic)
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "deletedAnswers": [
                        {
                            "correct": True,
                            "index": 0,
                            "pk": 3,
                            "question": 2,
                            "text": "sdfsad"
                        }
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "This is a new question",
                    "total_points": 1,
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.put(path='/api/quiz/' +
                             str(quiz.pk), data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_quiz7(self):   # PUT Quiz
        client = APIClient()
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(category=category, topic=topic)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        student_to_quiz_question = StudentToQuizQuestion.objects.create(
            student_to_quiz=student_to_quiz,
            question=quiz_question,
            student=student,
            answer=quiz_question_answer,
            correct=True
        )
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"pk": str(quiz_question_answer.pk), "correct": True, "text": "werq",
                         "question_type": 0, "total_points": 1, "index": 0},
                        {"text": "qwerwe", "index": 1}
                    ],
                    "pk": str(quiz_question.pk),
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "rewqr",
                    "total_points": 1
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.put(path='/api/quiz/' +
                             str(quiz.pk), data=data, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_quiz9(self):   # PUT with removed questions
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(category=category, topic=topic)
        category_2 = Category.objects.create(name="Homework")
        topic_to_cat = TopicToCategory.objects.create(category=category_2, topic=topic, weight=0.5)
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "This is a new question",
                    "total_points": 1,
                },
            ],
            "deletedQuestions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "This question will be deleted",
                    "total_points": 1,
                    "pk": 1
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.put(path='/api/quiz/' +
                             str(quiz.pk), data=data, format='json')
        self.assertEqual(409, request.status_code)

    def test_put_quiz10(self):   # PUT with removed questions
        client = APIClient()
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        category = Category.objects.create(name="Internal Quiz")
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        data = {
            "topic": str(topic.pk),
            "questions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "This is a new question",
                    "total_points": 1,
                },
            ],
            "deletedQuestions": [
                {
                    "answers": [
                        {"correct": True, "text": "werq", "question_type": 0,
                         "total_points": 1, "index": 0},
                        {"text": "qwerwe", "correct": False, "index": 1}
                    ],
                    "currentAnswer": {"text": "", "correct": False, "index": 2},
                    "index": 0,
                    "question_type": 0,
                    "text": "This question will be deleted",
                    "total_points": 1,
                    "pk": 1
                },
            ],
            "name": "qwwer",
            "weight": 1
        }
        request = client.put(path='/api/quiz/' +
                             str(quiz.pk), data=data, format='json')
        self.assertEqual(200, request.status_code)


    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_quiz1(self):   # Get existing student
        client = APIClient()
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(category=category, topic=temp_topic)
        request = client.get(path='/api/quiz/' +
                             str(temp_topic.pk), format='json')

        self.assertEqual(200, request.status_code)

    def test_get_quiz2(self):   # Get non-existing student
        client = APIClient()
        request = client.get(path='/api/quiz/12343342322222', format='json')
        self.assertEqual(404, request.status_code)

    def test_get_quiz3(self):   # Get all quizzes
        client = APIClient()
        category = Category.objects.create(name="Internal Quiz")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        topic_to_category = TopicToCategory.objects.create(category=category, topic=temp_topic)
        request = client.get(path='/api/quiz/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_quiz4(self):   # Can't get non-existent quiz for topic that exists
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)

        client = APIClient()
        request = client.get(path='/api/quiz/' +
                             str(temp_topic.pk), format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_quiz1(self):   # Delete existing student
        client = APIClient()
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        request = client.delete(
            path='/api/quiz/' + str(quiz.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_quiz2(self):   # Delete without pk value = error
        client = APIClient()
        request = client.delete(path='/api/quiz/', format='json')
        self.assertEqual(400, request.status_code)

    def test_delete_quiz3(self):   # Delete with invalid pk value = error
        client = APIClient()
        request = client.delete(path='/api/quiz/12222222', format='json')
        self.assertEqual(404, request.status_code)


'''
______________________________________________________________________________________________      QuizQuestion
  text = models.CharField(max_length=250)
  question_type = models.IntegerField(choices=QUESTION_TYPES)
  quiz = models.ForeignKey(Quiz, related_name='questions',
                           on_delete=models.CASCADE, null=True, blank=True)
  total_points = models.IntegerField(default=1)
  index = models.IntegerField(default=1)
______________________________________________________________________________________________
'''


class Test_Quiz_Questions(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_quiz_question1(self):  # Can't POST with no data
        client = APIClient()
        request = client.post(path='/api/quiz-question/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz_question2(self):  # Can't POST to pre-existing pk
        client = APIClient()
        request = client.post(path='/api/quiz-question/1', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz_question3(self):  # POST quiz question
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)

        DATA_PARAMETERS = {
            "text": "When do arrays start",
            "question_type": 0,
            "quiz": str(quiz.pk),
            "total_points": 1,
            "index": 0
        }
        client = APIClient()
        request = client.post(path='/api/quiz-question/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't POST quiz question to non-existent quiz
    def test_post_quiz_question4(self):

        DATA_PARAMETERS = {
            "text": "When do arrays start",
            "question_type": 0,
            "quiz": str(1000),
            "total_points": 1,
            "index": 0
        }
        client = APIClient()
        request = client.post(path='/api/quiz-question/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_quiz_question1(self):  # Can't PUT with no pk
        client = APIClient()
        request = client.put(path='/api/quiz-question/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_quiz_question2(self):  # Can't PUT to non-existent pk
        client = APIClient()
        request = client.put(
            path='/api/quiz-question/100000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_put_quiz_question3(self):  # PUT quiz question
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )

        DATA_PARAMETERS = {
            "text": "New question text",
            "question_type": 0,
            "quiz": str(quiz.pk),
            "total_points": 1,
            "index": 0
        }
        client = APIClient()
        request = client.put(path='/api/quiz-question/' +
                             str(quiz_question.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't PUT quiz question with invalid data
    def test_put_quiz_question4(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )

        DATA_PARAMETERS = {
            "text": "New question text",
            "question_type": "lalal",
            "quiz": str(quiz.pk),
            "total_points": 1,
            "index": 0
        }
        client = APIClient()
        request = client.put(path='/api/quiz-question/' +
                             str(quiz_question.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_quiz_question1(self):   # Get all quiz questions
        client = APIClient()
        request = client.get(path='/api/quiz-question/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_quiz_question2(self):   # Get a quiz question
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        client = APIClient()
        request = client.get(path='/api/quiz-question/' +
                             str(quiz_question.pk), format='json')
        self.assertEqual(200, request.status_code)

    # Can't get a quiz question with non-existent pk
    def test_get_quiz_question3(self):
        client = APIClient()
        request = client.get(
            path='/api/quiz-question/10000000000', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    # Can't delete quiz question with no pk
    def test_delete_quiz_question1(self):
        client = APIClient()
        request = client.delete(path='/api/quiz-question/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't delete quiz question with non-existent pk
    def test_delete_quiz_question2(self):
        client = APIClient()
        request = client.delete(
            path='/api/quiz-question/100000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_quiz_question3(self):   # Delete a quiz question
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        client = APIClient()
        request = client.delete(
            path='/api/quiz-question/' + str(quiz_question.pk), format='json')
        self.assertEqual(200, request.status_code)

    # def test_delete_quiz_question4(self):   # Can't Delete a quiz question that's a foreign key
    #     course1 = Course.objects.create(
    #         name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
    #     temp_topic = Topic.objects.create(name="temp_topic", course=course1)
    #     quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
    #     quiz_question = QuizQuestion.objects.create(
    #       text="When do arrays start",
    #       question_type=0,
    #       quiz=quiz,
    #       total_points=1,
    #       index=0
    #     )
    #     quiz_question_answer = QuizQuestionAnswer.objects.create(
    #       text="They start at 0",
    #       question=quiz_question,
    #       weight=1,
    #       correct=True,
    #       index=1
    #     )
    #     client = APIClient()
    #     request = client.delete(path='/api/quiz-question/' + str(quiz_question.pk), format='json')
    #     self.assertEqual(200, request.status_code)


'''
______________________________________________________________________________________________      QuizQuestionAnswer
  text = models.CharField(max_length=250)
  question = models.ForeignKey(
      QuizQuestion, related_name='answers', on_delete=models.CASCADE)
  weight = models.FloatField(
      null=True,
      blank=True,
      default=1,
      validators=[MinValueValidator(0), MaxValueValidator(1)]
  )
  correct = models.BooleanField()
  index = models.IntegerField(default=1)
______________________________________________________________________________________________
'''


class Test_Quiz_Question_Answers(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_quiz_question_answer1(self):  # Can't POST with no data
        client = APIClient()
        request = client.post(path='/api/quiz-question-answer/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz_question_answer2(self):  # Can't POST to pre-existing pk
        client = APIClient()
        request = client.post(
            path='/api/quiz-question-answer/1', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_quiz_question_answer3(self):  # POST quiz question answer
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        DATA_PARAMETERS = {
            "text": "They start at 0",
            "question": str(quiz_question.pk),
            "weight": 1,
            "correct": True,
            "index": 1
        }
        client = APIClient()
        request = client.post(path='/api/quiz-question-answer/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't POST answer to non-existent question
    def test_post_quiz_question_answer4(self):
        DATA_PARAMETERS = {
            "text": "They start at 0",
            "question": str(100000000),
            "weight": 1,
            "correct": True,
            "index": 1
        }
        client = APIClient()
        request = client.post(path='/api/quiz-question-answer/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_quiz_question_answer1(self):  # Can't PUT with no pk
        client = APIClient()
        request = client.put(path='/api/quiz-question-answer/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_quiz_question_answer2(self):  # PUT to quiz question
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        DATA_PARAMETERS = {
            "text": "They start at 0",
            "question": str(quiz_question.pk),
            "weight": 1,
            "correct": True,
            "index": 1
        }
        client = APIClient()
        request = client.put(path='/api/quiz-question-answer/' +
                             str(quiz_question_answer.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't PUT with to non-existent pk
    def test_put_quiz_question_answer3(self):
        client = APIClient()
        request = client.put(
            path='/api/quiz-question-answer/1000000000', format='json')
        self.assertEqual(404, request.status_code)

    # Can't PUT to answer with invalid data
    def test_put_quiz_question_answer4(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        DATA_PARAMETERS = {
            "texffsddt": "They start at 0",
            "question": str(quiz_question.pk),
            "weight": 1,
            "correct": True,
            "index": 1
        }
        client = APIClient()
        request = client.put(path='/api/quiz-question-answer/' +
                             str(quiz_question_answer.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)
    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    # Get all quiz questions answers
    def test_get_quiz_question_answer1(self):
        client = APIClient()
        request = client.get(path='/api/quiz-question-answer/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_quiz_question_answer2(self):   # Can't GET non-existent answer
        client = APIClient()
        request = client.get(
            path='/api/quiz-question-answer/100000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_get_quiz_question_answer3(self):   # GET quiz questions answers
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 0",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        client = APIClient()
        request = client.get(path='/api/quiz-question-answer/' +
                             str(quiz_question_answer.pk), format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_quiz_question_answer1(self):   # Can't delete with no pk
        client = APIClient()
        request = client.delete(
            path='/api/quiz-question-answer/', format='json')
        self.assertEqual(400, request.status_code)

    # DELETE quiz question answer
    def test_delete_quiz_question_answer2(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 0",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        client = APIClient()
        request = client.delete(
            path='/api/quiz-question-answer/' + str(quiz_question_answer.pk), format='json')
        self.assertEqual(200, request.status_code)

    # Can't DELETE quiz question answer with non-existent pk
    def test_delete_quiz_question_answer3(self):
        client = APIClient()
        request = client.delete(
            path='/api/quiz-question-answer/1000000000', format='json')
        self.assertEqual(404, request.status_code)


'''
______________________________________________________________________________________________      Resources
  link = models.CharField(max_length=2000)
  topic = models.ForeignKey(Topic,  on_delete=models.CASCADE)
  name = models.CharField(max_length=2000, blank=True, null=True)
______________________________________________________________________________________________
'''


class Test_Resources(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_resources1(self):  # Can't POST with no data
        client = APIClient()
        request = client.post(path='/api/resources/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_resources2(self):  # Can't POST to non-existent pk
        client = APIClient()
        request = client.post(path='/api/resources/1000000', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_resources3(self):  # POST resources
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic = Topic.objects.create(name="This is topic One", course=course1)
        DATA_PARAMETERS = {
            "link": "https://hello.com",
            "name": "Hello",
            "topic": str(topic.pk)
        }
        client = APIClient()
        request = client.post(path='/api/resources/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_resources1(self):  # Can't PUT with no pk
        client = APIClient()
        request = client.put(path='/api/resources/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_resources2(self):  # PUT resource
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic = Topic.objects.create(name="This is topic One", course=course1)
        resource = Resources.objects.create(
            link="https://hello.com",
            name="Hello",
            topic=topic
        )
        DATA_PARAMETERS = {
            "link": "https://helloworld.com",
            "name": "Hello",
            "topic": str(topic.pk)
        }
        client = APIClient()
        request = client.put(
            path='/api/resources/' + str(resource.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_resources3(self):  # Can't PUT to non-existent pk
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic = Topic.objects.create(name="This is topic One", course=course1)
        DATA_PARAMETERS = {
            "link": "https://helloworld.com",
            "name": "Hello",
            "topic": str(topic.pk)
        }
        client = APIClient()
        request = client.put(path='/api/resources/1000000000',
                             data=DATA_PARAMETERS, format='json')
        self.assertEqual(404, request.status_code)

    def test_put_resources4(self):  # Can't PUT resource with invalid data
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic = Topic.objects.create(name="This is topic One", course=course1)
        resource = Resources.objects.create(
            link="https://hello.com",
            name="Hello",
            topic=topic
        )
        DATA_PARAMETERS = {
            "linfasdk": "https://helloworld.com",  # invalid key
            "name": "Hello",
            "topic": str(topic.pk)
        }
        client = APIClient()
        request = client.put(
            path='/api/resources/' + str(resource.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_resources1(self):   # Get all resources
        client = APIClient()
        request = client.get(path='/api/resources/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_resources2(self):   # Can't Get resource with non-existent pk
        client = APIClient()
        request = client.get(path='/api/resources/100000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_get_resources3(self):  # Get resource
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic = Topic.objects.create(name="This is topic One", course=course1)
        resource = Resources.objects.create(
            link="https://hello.com",
            name="Hello",
            topic=topic
        )
        client = APIClient()
        request = client.get(path='/api/resources/' +
                             str(resource.pk), format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_resources1(self):   # Can't delete resources with no pk
        client = APIClient()
        request = client.delete(path='/api/resources/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't delete resources with non-existent pk
    def test_delete_resources2(self):
        client = APIClient()
        request = client.delete(
            path='/api/resources/10000000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_resources3(self):   # Delete resource
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic = Topic.objects.create(name="This is topic One", course=course1)
        resource = Resources.objects.create(
            link="https://hello.com",
            name="Hello",
            topic=topic
        )
        client = APIClient()
        request = client.delete(
            path='/api/resources/' + str(resource.pk), format='json')
        self.assertEqual(200, request.status_code)


'''
________________________________________________________________________________            User Tests
 *Comment
________________________________________________________________________________
'''


class UserTestCase(TestCase):
    def setUp(self):
        # Students
        Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        Student.objects.create(
            email="fakeemail@testingmemail.com", first_name="Jane", last_name="Doe")

        # Professor
        Student.objects.create(
            email="professor@testingmemail.com", first_name="Professor", last_name="Doe", is_professor=True)

    def test_users_have_correct_fields(self):
        student_one_name = Student.objects.get(
            email="testemail@testingmemail.com")
        student_two_name = Student.objects.get(
            email="fakeemail@testingmemail.com")

        self.assertEqual(student_one_name.get_name(), "John Doe")
        self.assertEqual(student_two_name.get_name(), "Jane Doe")

    def test_user_is_active_after_creation(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")

        self.assertEqual(student_one.is_active, True)

    def test_user_is_not_superuser_after_creation(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")

        self.assertEqual(student_one.is_superuser, False)

    def test_user_is_not_staff_after_creation(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")

        self.assertEqual(student_one.is_staff, False)

    def test_unique_emails(self):
        status = True
        try:
            Student.objects.create(
                email="testemail@testingmemail.com", first_name="Jack", last_name="Doe")
        except Exception:
            status = False
        self.assertEquals(status, False)

    def student_not_professor(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")
        self.assertEqual(student_one.is_professor, False)

    def professor_is_professor(self):
        professor = Student.objects.get(
            email="professor@testingmemail.com")
        self.assertEqual(professor.is_professor, True)


class Test_StudentTopicRelation(TestCase):
    def setUp(self):
        # Create course and topics
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic1 = Topic.objects.create(name="This is topic One", course=course1)

        # Create students
        student_one = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        student_two = Student.objects.create(
            email="fakeemail@testingmemail.com", first_name="Jane", last_name="Doe")

        student_topic_one = StudentToTopic.objects.create(
            course=course1, student=student_one, topic=topic1, grade=50, locked=False)
        student_topic_two = StudentToTopic.objects.create(
            course=course1, student=student_two, topic=topic1, grade=0, locked=True)

    def test_student1_has_correct_grade(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")
        topic = StudentToTopic.objects.get(student=student_one)
        self.assertEqual(topic.grade, 50)

    def test_student1_has_correct_course(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")

        course1 = Course.objects.get(course_code="2150")
        topic = StudentToTopic.objects.get(student=student_one)
        self.assertEqual(topic.course, course1)

    def test_students_not_equal(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")
        student_two = Student.objects.get(
            email="fakeemail@testingmemail.com")

        topic1 = StudentToTopic.objects.get(student=student_one)
        topic2 = StudentToTopic.objects.get(student=student_two)
        self.assertEqual(topic1 == topic2, False)

    def test_students_same_course_equal(self):
        student_one = Student.objects.get(
            email="testemail@testingmemail.com")
        student_two = Student.objects.get(
            email="fakeemail@testingmemail.com")

        topic1 = StudentToTopic.objects.get(student=student_one)
        topic2 = StudentToTopic.objects.get(student=student_two)
        self.assertEqual(topic1.course == topic2.course, True)


# Testing the different str methods of all models and any other internal methods
class Test_ModelFields(TestCase):
    def setUp(self):
        # Create course and topics
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic1 = Topic.objects.create(name="This is topic One", course=course1)

        # Create students
        student_one = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        student_two = Student.objects.create(
            email="fakeemail@testingmemail.com", first_name="Jane", last_name="Doe")
        student_three = Student.objects.create(
            email="testemail2@testingmemail.com")

        student_topic_one = StudentToTopic.objects.create(
            course=course1, student=student_one, topic=topic1, grade=50, locked=False)
        student_topic_two = StudentToTopic.objects.create(
            course=course1, student=student_two, topic=topic1, grade=0, locked=True)

    def test_student_str(self):
        student_one = Student.objects.get(
            email="testemail2@testingmemail.com")
        self.assertEqual(student_one.__str__(), "")

    def test_course_str(self):
        course = Course.objects.get(course_code="2150")
        self.assertEqual(course.__str__(),
                         course.subject_code + " " + course.course_code)

# Basic test for categories


class Test_Categories(TestCase):
    def setUp(self):
        Category.objects.create(name="Quiz")

    def test_category_exists(self):
        cat1 = Category.objects.get(name="Quiz")
        self.assertEqual(cat1.name == "Quiz", True)

    def test_category_cannot_duplicate(self):
        status = False
        try:
            cat1 = Category.objects.create.get(name="Quiz")
        except Exception:
            status = True
        self.assertEqual(status, True)

# Basic tests for Grades


class Test_Grades(TestCase):
    def setUp(self):
        # Create course and topics
        course1 = Course.objects.create(
            name="Test Course", course_code="2150", subject_code="CS")
        topic1 = Topic.objects.create(name="This is topic One", course=course1)

        # Create students
        student_one = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        student_two = Student.objects.create(
            email="fakeemail@testingmemail.com", first_name="Jane", last_name="Doe")
        student_three = Student.objects.create(
            email="testemail2@testingmemail.com")

        # Add student to course
        StudentToCourse.objects.create(
            student=student_one, course=course1, semester="Spring 2019")

        # Assign the students to topics
        student_topic_one = StudentToTopic.objects.create(
            course=course1, student=student_one, topic=topic1, grade=50, locked=False)
        student_topic_two = StudentToTopic.objects.create(
            course=course1, student=student_two, topic=topic1, grade=0, locked=True)

        # Create the Category
        quiz = Category.objects.create(name="Quiz")
        test = Category.objects.create(name="Test")
        hw = Category.objects.create(name="Homework")

        # Create the topic to category
        ttc1 = TopicToCategory.objects.create(
            topic=topic1, category=quiz, weight=0.30)
        ttc2 = TopicToCategory.objects.create(
            topic=topic1, category=test, weight=0.40)
        ttc3 = TopicToCategory.objects.create(
            topic=topic1, category=hw, weight=0.30)

        # Create a grade
        Grade.objects.create(name="Quiz 1", value=89,
                             topic_to_category=ttc1, student=student_one)
        Grade.objects.create(name="Quiz 1", value=90,
                             topic_to_category=ttc1, student=student_two)

        # Set up the quiz
        quiz = Quiz.objects.create(name="quiz1", topic=topic1)
        quiz_questions = []
        quiz_question_answers = []

        for i in range(5):
            question = QuizQuestion(
                text="question_${i}",
                question_type=0,
                quiz=quiz,
                total_points=1,
                index=i
            )

            answers = []
            for i in range(3):
                answer = QuizQuestionAnswer(
                    text="yabba-dabba-doo-${i}",
                    question=question,
                    weight=1,
                    correct=(i % 3 == 0),
                    index=i
                )
                answers.append(answer)

            quiz_questions.append(question)
            quiz_question_answers.append(answers)
        # Create a student to quiz
        StudentToQuiz.objects.create(quiz=quiz, student=student_one, grade=90)

    def test_topic_to_cat_has_right_weight(self):
        topic_to_cat_1 = TopicToCategory.objects.get(topic=1, category="Quiz")
        self.assertEqual(topic_to_cat_1.weight == 0.30, True)

    def test_grade_has_right_value(self):
        grade = Grade.objects.get(name="Quiz 1", student=1)
        self.assertEqual(grade.value == 89, True)

    def test_correct_grade_on_student(self):
        grade_1 = Grade.objects.get(name="Quiz 1", student=1)
        grade_2 = Grade.objects.get(name="Quiz 1", student=2)
        self.assertEqual(grade_1.value == grade_2.value, False)

    def test_weight_cannot_exceed_1(self):
        status = False
        try:
            topic_to_cat = TopicToCategory.objects.create(
                topic=1, category="Test", weight=0.40)
        except Exception:
            status = True
        self.assertEqual(status, True)

    def test_right_cat_associated_to_topic(self):
        # Topic 1 should be associated to category quiz
        topic_to_cat_1 = TopicToCategory.objects.get(topic=1, category="Quiz")
        self.assertEqual(topic_to_cat_1.category.name ==
                         "Quiz" and topic_to_cat_1.topic.name == "This is topic One", True)

    def test_quiz_associated_to_topic(self):
        # A quiz should now be associated to a topic
        # update the grades for the student in class 1
        client = APIClient()
        request = client.get(path='/api/class_grades/1/1/', format='json')
        self.assertEqual(200, request.status_code)

    def test_quiz_associated_to_topic_value(self):
        # A quiz should now be associated to a topic
        # update the grades for the student in class 1
        client = APIClient()
        request = client.get(path='/api/class_grades/1/1/', format='json')

        # Get the student
        student = Student.objects.get(email="testemail@testingmemail.com")
        # Get the topic for that student
        student_to_topic = StudentToTopic.objects.get(student=student)
        # bc python is funny
        self.assertEqual(student_to_topic.grade, 26.849999999999998)


'''
______________________________________________________________________________________________      Categories
  link = models.CharField(max_length=2000)
  topic = models.ForeignKey(Topic,  on_delete=models.CASCADE)
  name = models.CharField(max_length=2000, blank=True, null=True)
______________________________________________________________________________________________
url(r'^api/categories/(?P<pk>[A-z]+)', category_list, name='category-detail'),
url(r'^api/categories', category_list, name='category-list'),
'''


class Test_Categories(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_categories1(self):  # Can't POST with no data
        client = APIClient()
        request = client.post(path='/api/categories/', format='json')
        self.assertEqual(400, request.status_code)

    def test_post_categories2(self):  # POST category
        DATA_PARAMETERS = {
            "name": "test_category"
        }
        client = APIClient()
        request = client.post(path='/api/categories/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't POST category to already existing pk
    def test_post_categories3(self):
        DATA_PARAMETERS = {
            "name": "test_category"
        }
        client = APIClient()
        request = client.post(path='/api/categories/quiz',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_categories1(self):  # Can't PUT with no pk
        client = APIClient()
        request = client.put(path='/api/categories/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_categories2(self):  # Can't PUT to non-existent category
        client = APIClient()
        request = client.put(
            path='/api/categories/nonexistentcategory', format='json')
        self.assertEqual(404, request.status_code)

    def test_put_categories3(self):  # PUT category
        category = Category.objects.create(name='popquiz')

        DATA_PARAMETERS = {
            "name": "updatedpopquiz"
        }

        client = APIClient()
        request = client.put(path='/api/categories/' +
                             str(category.name), data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_categories4(self):  # Can't PUT category with invalid data
        category = Category.objects.create(name='popquiz')

        DATA_PARAMETERS = {
            "newname": "updatedpopquiz"
        }

        client = APIClient()
        request = client.put(path='/api/categories/' +
                             str(category.name), data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_categories1(self):   # Get all categories
        client = APIClient()
        request = client.get(path='/api/categories/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_categories2(self):   # Get specific category
        category = Category.objects.create(name='popquiz')
        client = APIClient()
        request = client.get(path='/api/categories/' +
                             str(category.name), format='json')
        self.assertEqual(200, request.status_code)

    # Can't get specific category that doesn't exist
    def test_get_categories3(self):
        client = APIClient()
        request = client.get(
            path='/api/categories/fakecategory', format='json')
        self.assertEqual(404, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_categories1(self):   # Can't delete resources with no pk
        client = APIClient()
        request = client.delete(path='/api/categories/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't delete resources that doesn't exist
    def test_delete_categories2(self):
        client = APIClient()
        request = client.delete(
            path='/api/categories/fakecategory', format='json')
        self.assertEqual(404, request.status_code)

    # Can't delete resources that doesn't exist
    def test_delete_categories3(self):
        category = Category.objects.create(name='popquiz')
        client = APIClient()
        request = client.delete(
            path='/api/categories/' + str(category.name), format='json')
        self.assertEqual(200, request.status_code)


'''
______________________________________________________________________________________________      StudentToQuiz
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  grade = models.FloatField(
      default=0,
      validators=[MinValueValidator(0), MaxValueValidator(100)]
  )
______________________________________________________________________________________________
url(r'^api/student/quiz/(?P<pk>[0-9]+)', student_to_quiz_list, name='student-to-quiz-detail'),
url(r'^api/student/quiz/', student_to_quiz_list, name='student-to-quiz-list'),
'''


class Test_StudentToQuiz(TestCase):

    def setUp(self):
        pass

    ''' Not implemented
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_put_student_to_quiz1(self):   # Tests non-implemented put method
        client = APIClient()
        request = client.put(
            path='/api/student/quiz/', format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    @mock.patch('sptApp.api_views.requests.post')
    # Get specific student_to_quiz
    def test_post_student_to_quiz1(self, mock_request):
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=100)

        # student_to_quiz = StudentToQuiz.objects.create(quiz=quiz, student=student, grade=100)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
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

        DATA_PARAMETERS = {
            "answers": [{"question_id": str(quiz_question.pk), "answer_id": str(quiz_question_answer.pk)}],
            "id_token": "fdasasd",
            "topic_id": str(topic.pk),
            "weight": 1
        }
        client = APIClient()
        request = client.post(
            path='/api/student/quiz/' + str(quiz.pk), data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    def test_post_student_to_quiz2(self):   # Can't POST to null pk
        client = APIClient()
        request = client.post(
            path='/api/student/quiz/', format='json')
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't specific student_to_quiz if google errors
    def test_post_student_to_quiz3(self, mock_request):
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        # student_to_quiz = StudentToQuiz.objects.create(quiz=quiz, student=student, grade=100)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
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

        DATA_PARAMETERS = {
            "answers": [{"question_id": str(quiz_question.pk), "answer_id": str(quiz_question_answer.pk)}],
            "id_token": "fdasasd",
            "topic_id": str(topic.pk),
            "weight": 1
        }
        client = APIClient()
        request = client.post(
            path='/api/student/quiz/' + str(quiz.pk), data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't specific student_to_quiz if google errors
    def test_post_student_to_quiz4(self, mock_request):
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=100)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        student_to_quiz_question = StudentToQuizQuestion.objects.create(
            student_to_quiz=student_to_quiz,
            question=quiz_question,
            student=student,
            answer=quiz_question_answer,
            correct=True
        )
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

        DATA_PARAMETERS = {
            "answers": [{"question_id": str(quiz_question.pk), "answer_id": str(quiz_question_answer.pk)}],
            "id_token": "fdasasd",
            "topic_id": str(topic.pk),
            "weight": 1
        }
        client = APIClient()
        request = client.post(
            path='/api/student/quiz/' + str(quiz.pk), data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Update specific student_to_quiz with already created grade
    def test_post_student_to_quiz5(self, mock_request):
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        category = Category.objects.create(name="Internal Quiz")
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=100)

        # student_to_quiz = StudentToQuiz.objects.create(quiz=quiz, student=student, grade=100)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        grade = Grade.objects.create(
            topic_to_category=topic_to_category,
            student=student,
            value=100,
            name="Quiz grade"
        )
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

        DATA_PARAMETERS = {
            "answers": [{"question_id": str(quiz_question.pk), "answer_id": str(quiz_question_answer.pk)}],
            "id_token": "fdasasd",
            "topic_id": str(topic.pk),
            "weight": 1
        }
        client = APIClient()
        request = client.post(
            path='/api/student/quiz/' + str(quiz.pk), data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)
    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    @mock.patch('sptApp.api_views.requests.post')
    # Get specific student_to_quiz
    def test_get_student_to_quiz1(self, mock_request):
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)

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

        client = APIClient()
        request = client.get(
            path='/api/student/quiz/' + str(topic.pk) + '', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't get student_to_quiz for non-existnent quiz
    def test_get_student_to_quiz2(self, mock_request):
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)

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

        client = APIClient()
        request = client.get(
            path='/api/student/quiz/' + str(topic.pk) + '', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't get student_to_quiz for non-existnent student_to_quiz
    def test_get_student_to_quiz3(self, mock_request):
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
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)

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

        client = APIClient()
        request = client.get(
            path='/api/student/quiz/' + str(topic.pk) + '', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    def test_get_student_to_quiz4(self):   # Get all student_to_quiz
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
        category = Category.objects.create(name="Internal Quiz")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        topic_to_category = TopicToCategory.objects.create(topic=topic, category=category)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)

        client = APIClient()
        request = client.get(path='/api/student/quiz/', format='json')

        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # CN'T Get specific student_to_quiz if google errors
    def test_get_student_to_quiz1(self, mock_request):
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
        category = Category.objects.create(name="Internal Quiz")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        topic_to_category = TopicToCategory.objects.create(topic=topic, category=category)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)

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

        client = APIClient()
        request = client.get(
            path='/api/student/quiz/' + str(topic.pk) + '', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Get specific student_to_quiz
    def test_get_student_to_quiz5(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        professor = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )

        student = Student.objects.create(
            email="fake@gmail.com",
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        category = Category.objects.create(name="Internal Quiz")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=professor)
        topic = Topic.objects.create(name="topic1", course=course)

        topic_to_category = TopicToCategory.objects.create(topic=topic, category=category)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)

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

        client = APIClient()
        request = client.get(
            path='/api/student/quiz/' + str(topic.pk) + '?view_as=' + str(student.pk), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Get specific student_to_quiz
    def test_get_student_to_quiz6(self, mock_request):
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }
        professor = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )

        student = Student.objects.create(
            email="fake@gmail.com",
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1", professor=student)
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)

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

        client = APIClient()
        request = client.get(
            path='/api/student/quiz/' + str(topic.pk) + '?view_as=' + str(student.pk), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': None
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    # Can't delete student_to_quiz with no pk
    def test_delete_student_to_quiz1(self):
        client = APIClient()
        request = client.delete(path='/api/student/quiz/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't delete student_to_quiz with invalid pk
    def test_delete_student_to_quiz2(self):
        client = APIClient()
        request = client.delete(
            path='/api/student/quiz/100000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_student_to_quiz3(self):   # Delete student_to_quiz
        student = Student.objects.create(
            email="first4last4@gmail.com", first_name="first4", last_name="last4")

        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        quiz = Quiz.objects.create(name="quiz1", topic=topic)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student, grade=100)
        client = APIClient()
        request = client.delete(
            path='/api/student/quiz/' + str(student_to_quiz.pk), format='json')
        self.assertEqual(200, request.status_code)


'''
______________________________________________________________________________________________      Settings
  color = models.CharField(max_length=250)
  nickname = models.CharField(max_length=250, null=True, blank=True)
  user = models.ForeignKey(Student, on_delete=models.CASCADE)
______________________________________________________________________________________________
url(r'^api/settings/(?P<pk>[0-9]+)', settings_list),
url(r'^api/settings/', settings_list),

'''


class Test_Settings(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    @mock.patch('sptApp.api_views.requests.post')
    def test_put_settings1(self, mock_request):   # Post specific settings
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
        settings = Settings.objects.create(
            color="#000000",
            nickname="Jon",
            user=student
        )

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

        DATA_PARAMETERS = {
            "colors": {"hsl": {"h": 248.29787234042553, "s": 1, "l": 0.8156862745098039, "a": 1}, "hex": "#AEA1FF", "hex8": "#AEA1FFFF"},
            "nickname": "stuff",
            "token": "fdasasd"
        }
        client = APIClient()
        request = client.put(
            path='/api/settings/' + str(student.pk), data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_put_settings2(self, mock_request):   # Post specific settings
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

        DATA_PARAMETERS = {
            "colors": {"hsl": {"h": 248.29787234042553, "s": 1, "l": 0.8156862745098039, "a": 1}, "hex": "#AEA1FF", "hex8": "#AEA1FFFF"},
            "nickname": "stuff",
            "token": "fdasasd"
        }
        client = APIClient()
        request = client.put(
            path='/api/settings/' + str(student.pk), data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't PUT specific settings if google errors
    def test_put_settings3(self, mock_request):
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
        settings = Settings.objects.create(
            color="#000000",
            nickname="Jon",
            user=student
        )

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

        DATA_PARAMETERS = {
            "colors": {"hsl": {"h": 248.29787234042553, "s": 1, "l": 0.8156862745098039, "a": 1}, "hex": "#AEA1FF", "hex8": "#AEA1FFFF"},
            "nickname": "stuff",
            "token": "fdasasd"
        }
        client = APIClient()
        request = client.put(
            path='/api/settings/' + str(student.pk), data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    @mock.patch('sptApp.api_views.requests.post')
    def test_post_settings1(self, mock_request):   # Post specific settings
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

        DATA_PARAMETERS = {
            "colors": {"hsl": {"h": 248.29787234042553, "s": 1, "l": 0.8156862745098039, "a": 1}, "hex": "#AEA1FF", "hex8": "#AEA1FFFF"},
            "nickname": "stuff",
            "token": "fdasasd"
        }
        client = APIClient()
        request = client.post(
            path='/api/settings/?id_token=fdasasd', data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    def test_post_settings2(self):   # Can't POST to already created settings
        client = APIClient()
        request = client.post(path='/api/settings/1', format='json')

        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't POST settings to a student that already has them
    def test_post_settings3(self, mock_request):
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
        settings = Settings.objects.create(
            color="#000000",
            nickname="Jon",
            user=student
        )
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

        DATA_PARAMETERS = {
            "colors": {"hsl": {"h": 248.29787234042553, "s": 1, "l": 0.8156862745098039, "a": 1}, "hex": "#AEA1FF", "hex8": "#AEA1FFFF"},
            "nickname": "stuff",
            "token": "fdasasd"
        }
        client = APIClient()
        request = client.post(
            path='/api/settings/', data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't Post specific settings if google errors
    def test_post_settings4(self, mock_request):
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

        DATA_PARAMETERS = {
            "colors": {"hsl": {"h": 248.29787234042553, "s": 1, "l": 0.8156862745098039, "a": 1}, "hex": "#AEA1FF", "hex8": "#AEA1FFFF"},
            "nickname": "stuff",
            "token": "fdasasd"
        }
        client = APIClient()
        request = client.post(
            path='/api/settings/?id_token=fdasasd', data=DATA_PARAMETERS, format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)
    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    # This should fail because you must specify the id_token for a user
    def test_get_settings1(self):   # Get all settings
        client = APIClient()
        request = client.get(path='/api/settings/', format='json')

        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_get_settings2(self, mock_request):   # Get specific settings
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
        settings = Settings.objects.create(
            color="#000000",
            nickname="Jon",
            user=student
        )
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
        client = APIClient()
        request = client.get(
            path='/api/settings/' + str(student.pk) + '?id_token=fdasasd', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't Get specific settings that doesn't exist
    def test_get_settings3(self, mock_request):
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
        client = APIClient()
        request = client.get(
            path='/api/settings/' + str(student.pk) + '?id_token=fdasasd', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    # Can't Get specific settings if google errors
    def test_get_settings4(self, mock_request):
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
        settings = Settings.objects.create(
            color="#000000",
            nickname="Jon",
            user=student
        )
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
        client = APIClient()
        request = client.get(
            path='/api/settings/' + str(student.pk) + '?id_token=fdasasd', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)
    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_settings1(self):   # Can't delete student_to_quiz with no pk
        client = APIClient()
        request = client.delete(path='/api/settings/', format='json')
        self.assertEqual(400, request.status_code)

    def test_delete_settings2(self):   # delete settings
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
        settings = Settings.objects.create(
            color="#000000",
            nickname="Jon",
            user=student
        )
        client = APIClient()
        request = client.delete(
            path='/api/settings/' + str(student.pk), format='json')
        self.assertEqual(200, request.status_code)

    def test_delete_settings3(self):   # can't delete non-existent settings
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
        client = APIClient()
        request = client.delete(
            path='/api/settings/' + str(student.pk), format='json')
        self.assertEqual(404, request.status_code)


'''
______________________________________________________________________________________________      TopicToCategory
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  weight = models.FloatField(
      null=True,
      blank=True,
      default=1,
      validators=[MinValueValidator(0), MaxValueValidator(1)]
  )
______________________________________________________________________________________________
# Topic to Category
url(r'^api/topic/category/(?P<topic_pk>[0-9]+)/(?P<category_pk>[A-z]+)', topic_to_category_list),
url(r'^api/topic/category/(?P<topic_pk>[0-9]+)/', topic_to_category_list),
url(r'^api/topic/category', topic_to_category_list),

'''


class Test_TopicToCategory(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    # Can't put topic_to_category to null topic_pk
    def test_put_topic_to_category1(self):
        client = APIClient()
        request = client.put(path='/api/topic/category/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't put topic_to_category to with non-existent topic
    def test_put_topic_to_category2(self):
        client = APIClient()
        request = client.put(
            path='/api/topic/category/10000000/', format='json')
        self.assertEqual(404, request.status_code)

    # Can't put to non-existent topic_to_category
    def test_put_topic_to_category3(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)

        client = APIClient()
        request = client.put(path='/api/topic/category/' +
                             str(topic.pk) + '/', format='json')
        self.assertEqual(404, request.status_code)

    def test_put_topic_to_category4(self):   # Put topic_to_category
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category_furst = TopicToCategory.objects.create(
            topic=topic, category=category, weight=0.4)

        DATA_PARAMETERS = {
            "topic": str(topic.pk),
            "weight": 0.5,
            "category": str(category.pk)
        }

        client = APIClient()
        request = client.put(path='/api/topic/category/' +
                             str(topic.pk) + '/', data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't Put topic_to_category with invalid serializer
    def test_put_topic_to_category5(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category_furst = TopicToCategory.objects.create(
            topic=topic, category=category, weight=0.4)

        DATA_PARAMETERS = {
            "topic": str(topic.pk),
            "weight": 0.5,
            "categoryeeeeeee": str(category.pk)
        }

        client = APIClient()
        request = client.put(path='/api/topic/category/' +
                             str(topic.pk) + '/', data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_topic_to_category1(self):   # Post specific topic_to_category
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')

        DATA_PARAMETERS = {
            "topic": str(topic.pk),
            "weight": 1,
            "category": str(category.pk)
        }

        client = APIClient()
        request = client.post(path='/api/topic/category/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    # Can't Post specific topic_to_category to non-null pk
    def test_post_topic_to_category2(self):
        client = APIClient()
        request = client.post(path='/api/topic/category/1/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't Post specific topic_to_category with invalid serializer
    def test_post_topic_to_category3(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')

        DATA_PARAMETERS = {
            "topic": str(topic.pk),
            "weight": 1,
            "categoryeeeeee": str(category.pk)
        }

        client = APIClient()
        request = client.post(path='/api/topic/category/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    # Can't Post specific topic_to_category with weight > 1
    def test_post_topic_to_category4(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')

        DATA_PARAMETERS = {
            "topic": str(topic.pk),
            "weight": 2,
            "category": str(category.pk)
        }

        client = APIClient()
        request = client.post(path='/api/topic/category/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(409, request.status_code)

    # Can't Post specific topic_to_category with weight > 1
    def test_post_topic_to_category5(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category_furst = TopicToCategory.objects.create(
            topic=topic, category=category, weight=0.4)

        DATA_PARAMETERS = {
            "topic": str(topic.pk),
            "weight": 0.6,
            "category": str(category.pk)
        }

        client = APIClient()
        request = client.post(path='/api/topic/category/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_topic_to_category1(self):   # Get all topic_to_category
        client = APIClient()
        request = client.get(path='/api/topic/category/', format='json')
        self.assertEqual(200, request.status_code)

    # Can't Get topic_to_category for non-existent topic
    def test_get_topic_to_category2(self):
        client = APIClient()
        request = client.get(
            path='/api/topic/category/1000000/', format='json')
        self.assertEqual(404, request.status_code)

    # Can't Get topic_to_category for non-existent topic
    def test_get_topic_to_category3(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)

        client = APIClient()
        request = client.get(path='/api/topic/category/' +
                             str(topic.pk) + '/', format='json')
        self.assertEqual(200, request.status_code)

    # Can't Get topic_to_category for non-existent topic
    def test_get_topic_to_category4(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')

        client = APIClient()
        request = client.get(path='/api/topic/category/' + str(topic.pk) +
                             '/' + str(category.name) + '/', format='json')
        self.assertEqual(404, request.status_code)

    # Can't Get topic_to_category for non-existent topic
    def test_get_topic_to_category5(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)

        client = APIClient()
        request = client.get(path='/api/topic/category/' + str(topic.pk) +
                             '/' + str(category.name) + '/', format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    # Can't delete topic_to_category with no topic_pk
    def test_delete_topic_to_category1(self):
        client = APIClient()
        request = client.delete(path='/api/topic/category/', format='json')
        self.assertEqual(400, request.status_code)

    # Can't delete non-existent topic_to_category
    def test_delete_topic_to_category2(self):
        client = APIClient()
        request = client.delete(
            path='/api/topic/category/1000000000/', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_topic_to_category3(self):   # Delete topic_to_category
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')

        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        client = APIClient()
        request = client.delete(
            path='/api/topic/category/' + str(topic_to_category.pk) + '/', format='json')
        self.assertEqual(200, request.status_code)


'''
______________________________________________________________________________________________      Grade
  name = models.CharField(max_length=250)
  value = models.FloatField(default=0, validators=[
                          MinValueValidator(0), MaxValueValidator(100)])
  topic_to_category = models.ForeignKey(
      TopicToCategory, related_name='grades', on_delete=models.CASCADE)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
______________________________________________________________________________________________
url(r'^api/grades/(?P<student_pk>[0-9]+)/(?P<topic_pk>[0-9]+)/(?P<category_pk>[A-z]+)',
    grade_list, name='grade-detail'),
url(r'^api/grades/(?P<student_pk>[0-9]+)/(?P<topic_pk>[0-9]+)',
    grade_list, name='grade-detail'),
url(r'^api/grades/(?P<student_pk>[0-9]+)',
    grade_list, name='grade-detail'),
url(r'^api/grades',
    grade_list, name='grade-list'),

'''


class Test_Grade(TestCase):

    def setUp(self):
        pass

    '''
    __________________________________________________  Put
    __________________________________________________
    '''

    def test_put_grade1(self):   # PUT grade
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        grade = Grade.objects.create(
            name="dfadsfa",
            value=100,
            topic_to_category=topic_to_category,
            student=student
        )

        DATA_PARAMETERS = {
            "name": "dfadsfa",
            "value": 80,
            "topic_to_category": str(topic_to_category.pk),
            "student": str(student.pk)
        }

        client = APIClient()
        request = client.put(path='/api/grades/?gradeId=' +
                             str(grade.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    def test_put_grade2(self):   # Can't put grade to null topic_pk
        client = APIClient()
        request = client.put(path='/api/grades/', format='json')
        self.assertEqual(400, request.status_code)

    def test_put_grade3(self):   # Can't put grade to non-existent pk
        client = APIClient()
        request = client.put(
            path='/api/grades/?gradeId=1000000000', format='json')
        self.assertEqual(404, request.status_code)

    def test_put_grade4(self):   # Can't putgrade with invalid serializer
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        grade = Grade.objects.create(
            name="dfadsfa",
            value=100,
            topic_to_category=topic_to_category,
            student=student
        )

        DATA_PARAMETERS = {
            "nameeeeeeeeeee": "dfadsfa",
            "value": 80,
            "topic_to_category": str(topic_to_category.pk),
            "student": str(student.pk)
        }

        client = APIClient()
        request = client.put(path='/api/grades/?gradeId=' +
                             str(grade.pk), data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Post
    __________________________________________________
    '''

    def test_post_grade1(self):   # POST grade
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        DATA_PARAMETERS = {
            "name": "dfadsfa",
            "value": 80,
            "topic_to_category": str(topic_to_category.pk),
            "student": str(student.pk)
        }

        client = APIClient()
        request = client.post(path='/api/grades/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(200, request.status_code)

    def test_post_grade2(self):   # Can't POST grade to non-null pk
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        DATA_PARAMETERS = {
            "name": "dfadsfa",
            "value": 80,
            "topic_to_category": str(topic_to_category.pk),
            "student": str(student.pk)
        }

        client = APIClient()
        request = client.post(path='/api/grades/2',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    def test_post_grade3(self):   # Can't POST grade with invalid serializer
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        DATA_PARAMETERS = {
            "nameeee": "dfadsfa",
            "value": 80,
            "topic_to_category": str(topic_to_category.pk),
            "student": str(student.pk)
        }

        client = APIClient()
        request = client.post(path='/api/grades/',
                              data=DATA_PARAMETERS, format='json')
        self.assertEqual(400, request.status_code)

    '''
    __________________________________________________  Get
    __________________________________________________
    '''

    def test_get_grade1(self):   # Get grade for student/topic/category
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        grade = Grade.objects.create(
            name="dfadsfa",
            value=100,
            topic_to_category=topic_to_category,
            student=student
        )

        client = APIClient()
        request = client.get(path='/api/grades/' + str(student.pk) + '/' +
                             str(topic.pk) + '/' + str(category.pk) + '/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_grade2(self):   # Get grade for student/topic/category that doesnt exist
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        client = APIClient()
        request = client.get(path='/api/grades/' + str(student.pk) + '/' +
                             str(topic.pk) + '/' + str(category.pk) + '/', format='json')
        self.assertEqual(404, request.status_code)

    def test_get_grade3(self):   # Get grades for student/topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        client = APIClient()
        request = client.get(path='/api/grades/' + str(student.pk) +
                             '/' + str(topic.pk) + '/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_grade4(self):   # Get grades for student
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        client = APIClient()
        request = client.get(path='/api/grades/' +
                             str(student.pk) + '/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_grade5(self):   # Get grades
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        client = APIClient()
        request = client.get(path='/api/grades/', format='json')
        self.assertEqual(200, request.status_code)

    def test_get_grade6(self):   # Get grades for student/topic
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        client = APIClient()
        request = client.get(path='/api/grades/' + str(student.pk) + '/' +
                             str(topic.pk) + '/?view_as=' + str(student.pk), format='json')
        self.assertEqual(200, request.status_code)

    '''
    __________________________________________________  Delete
    __________________________________________________
    '''

    def test_delete_grade1(self):   # Can't delete grade with no pk
        client = APIClient()
        request = client.delete(path='/api/grades/', format='json')
        self.assertEqual(400, request.status_code)

    def test_delete_grade2(self):   # Can't delete grade with non-existent pk
        client = APIClient()
        request = client.delete(
            path='/api/grades/?gradeId=1000', format='json')
        self.assertEqual(404, request.status_code)

    def test_delete_grade3(self):   # delete grade
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)
        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=1)
        student = Student.objects.create(
            email="first1last1@gmail.com", first_name="first1", last_name="last1")

        grade = Grade.objects.create(
            name="dfadsfa",
            value=100,
            topic_to_category=topic_to_category,
            student=student
        )

        client = APIClient()
        request = client.delete(
            path='/api/grades/?gradeId=' + str(grade.pk), format='json')
        self.assertEqual(200, request.status_code)


class Test_Views(TestCase):
    def test_update_class_grades1(self):  # Can't run if course doesn't exist
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")

        request = views.update_class_grades(None, 100000, student.pk)
        self.assertEqual(404, request.status_code)

    def test_update_class_grades2(self):  # Can't run if student doesn't exist
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")

        request = views.update_class_grades(None, course1.pk, 10000)
        self.assertEqual(404, request.status_code)

    def test_update_class_grades3(self):
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)

        category = Category.objects.create(name='popquiz')
        # topic_to_category = TopicToCategory.objects.create(topic=topic, category=category, weight=0.4)

        request = views.update_class_grades(None, course1.pk, student.pk)
        self.assertEqual(200, request.status_code)

    def test_update_class_grades4(self):  # Can't run if student doesn't exist
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)

        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=0.4)
        grade = Grade.objects.create(
            name="dfadsfa",
            value=100,
            topic_to_category=topic_to_category,
            student=student
        )
        request = views.update_class_grades(None, course1.pk, student.pk)
        self.assertEqual(200, request.status_code)

    def test_update_class_grades5(self):  # Can't run if student doesn't exist
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)

        category = Category.objects.create(name='popquiz')
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=0.4)
        grade = Grade.objects.create(
            name="dfadsfa",
            value=100,
            topic_to_category=topic_to_category,
            student=student
        )
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        request = views.update_class_grades(None, course1.pk, student.pk)
        self.assertEqual(200, request.status_code)

    def test_update_class_grades6(self):  # Testing weighted average
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        topic2 = Topic.objects.create(name="topic2", course=course1)
        topic_to_topic = TopicToTopic.objects.create(
            course=course1, topic_node=topic, ancestor_node=topic2, weight=0.50)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)

        student_to_topic2 = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic2, grade=50, locked=False)

        category = Category.objects.create(name='popquiz')
        # Topic 1
        topic_to_category = TopicToCategory.objects.create(
            topic=topic, category=category, weight=0.4)
        # Topic 2
        topic_to_category2 = TopicToCategory.objects.create(
            topic=topic2, category=category, weight=0.4)
        grade = Grade.objects.create(
            name="dfadsfa",
            value=100,
            topic_to_category=topic_to_category,
            student=student
        )
        grade = Grade.objects.create(
            name="dfadsfa",
            value=60,
            topic_to_category=topic_to_category2,
            student=student
        )
        quiz = Quiz.objects.create(name="temp_quiz", topic=topic)
        request = views.update_class_grades(None, course1.pk, student.pk)
        self.assertEqual(200, request.status_code)

    # Can't run if student doesn't exist
    def test_get_class_and_topic_students1(self):
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student, topic=topic, grade=50, locked=False)

        request = views.get_class_and_topic_students(
            None, course1.pk, topic.pk)
        self.assertEqual(200, request.status_code)


class Test_Models(TestCase):
    def test_ExternalSite(self):
        externalSite = ExternalSite.objects.create(name="External Site", base_url= 'http://baseurl.com'   )
        self.assertEqual(externalSite.name + ' (' + externalSite.base_url + ')', externalSite.__str__() )


    def test_ExternalSiteToCourse(self):
        externalSite = ExternalSite.objects.create(name="External Site", base_url= 'http://baseurl.com/')
        professor = Student.objects.create(email="danielalanseymour@gmail.com", first_name="Dan", last_name="Seymour", 
            username="professorDan", is_professor=True,  id_token="123abc" )
        course = Course.objects.create(name= 'Course' , course_code= 'CS', subject_code= '123', professor= professor )

        externalSiteToCourse = ExternalSiteToCourse.objects.create(course= course, external_site= externalSite, 
            url_ending= '1?APIKEY=123123')

        expected = course.course_code + " " + course.subject_code + " (" + externalSite.name + externalSiteToCourse.url_ending + ")"
        self.assertEqual(expected, externalSiteToCourse.__str__() )


        
    def test_ExternalSiteToGrade(self):
        externalSite = ExternalSite.objects.create(name="External Site", base_url= 'http://baseurl.com')
        professor = Student.objects.create(email="danielalanseymour@gmail.com", first_name="Dan", last_name="Seymour", 
            username="professorDan", is_professor=True,  id_token="123abc" )
        student = Student.objects.create(email="das5fa@virginia.edu", first_name="Dan", last_name="Seymour",  
            username="studentDan", is_professor=False, id_token="abc123")
        course = Course.objects.create(name= 'Course' , course_code= 'CS', subject_code= '123', professor= professor )
        topic= Topic.objects.create(name= 'Topic' , course= course )
        category = Category.objects.create(name= 'External Site') 
        topicToCategory = TopicToCategory.objects.create(topic= topic, category= category)
        grade = Grade.objects.create(name='Grade Name', topic_to_category= topicToCategory,student= student)
        
        externalSiteToCourse = ExternalSiteToCourse.objects.create(course= course, external_site= externalSite, 
            url_ending= '1?APIKEY=123123')
        externalSiteToGrade = ExternalSiteToGrade.objects.create(external_site_to_course=externalSiteToCourse, grade=grade, 
            link='http://exampleurl.com/12?APIKEY=12312')
        expected = "Grade: " + str(grade.value) + " (" + str(externalSiteToGrade.link) + ')'

        self.assertEqual(expected, externalSiteToGrade.__str__() )

    def test_student_save(self):
        student = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=None, student=student, topic=topic, grade=50, locked=False)

        self.assertEqual(StudentToTopic.save(student_to_topic), None)

    def test_student(self):
        student = Student.objects.create(email="user1000@gmail.com")
        self.assertEqual(student.email, student.get_short_name())
        self.assertEqual(student.email, student.natural_key())
        self.assertEqual(student.get_id(), None)

    def test_object_is_foreign_key_response(self):
        response = object_is_foreign_key_response()

        self.assertEqual(409, response.status_code)

    def test_successful_get_externalSite(self):
        response = successful_get_externalSite()

        self.assertEqual(200, response.status_code)

    def test_already_found_response(self):
        response = already_found_response()

        self.assertEqual(200, response.status_code)

    def test_studenttocourse(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        student = Student.objects.create(email="user1000@gmail.com")
        studentToCourse = StudentToCourse.objects.create(
            student=student, course=course)

        self.assertEqual(student.__str__() + " is taking " +
                         course.__str__(), studentToCourse.__str__())

    def test_topic_name(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic = Topic.objects.create(name="topic1", course=course)

        self.assertEqual(topic.name, topic.__str__())

    def test_topictocategory(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        quiz = Category.objects.create(name="Quiz")
        ttc1 = TopicToCategory.objects.create(
            topic=topic1, category=quiz, weight=0.30)

        self.assertEqual(quiz.__str__() + " is related to topic " +
                         topic1.__str__() + " with a weight of " + str(0.30), ttc1.__str__())

    def test_grade(self):
        quiz = Category.objects.create(name="Quiz")
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        student_one = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        ttc1 = TopicToCategory.objects.create(
            topic=topic1, category=quiz, weight=0.30)
        grade = Grade.objects.create(name="Quiz 1", value=89,
                                     topic_to_category=ttc1, student=student_one)
        self.assertEqual(student_one.__str__() + " got a " + str(grade.value) +
                         " on " + grade.name + " in " + ttc1.category.__str__(), grade.__str__())

    def test_studenttotopic(self):
        student_one = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course1)
        student_to_topic = StudentToTopic.objects.create(
            course=course1, student=student_one, topic=topic1, grade=50, locked=False)

        self.assertEqual(student_one.__str__() + " is in " +
                         topic1.__str__(), student_to_topic.__str__())
        course1 = None
        student_to_topic.save()

    def test_quiz(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        category = Category.objects.create(name="Quiz")

        topic1 = Topic.objects.create(name="topic1", course=course1)
        quiz = Quiz.objects.create(name="quiz1", topic=topic1)
        self.assertEqual("Quiz for " + topic1.__str__(), quiz.__str__())

    def test_quizquestion(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        self.assertEqual("Quiz id: " + str(quiz_question.quiz.pk) +
                         ", question: " + quiz_question.text, quiz_question.__str__())

    def test_quizquestionanswer(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        temp_topic = Topic.objects.create(name="temp_topic", course=course1)
        quiz = Quiz.objects.create(name="temp_quiz", topic=temp_topic)
        quiz_question = QuizQuestion.objects.create(
            text="When do arrays start",
            question_type=0,
            quiz=quiz,
            total_points=1,
            index=0
        )
        quiz_question_answer = QuizQuestionAnswer.objects.create(
            text="They start at 1",
            question=quiz_question,
            weight=1,
            correct=True,
            index=1
        )
        self.assertEqual("Question id: " + str(quiz_question_answer.pk) +
                         " answer: " + quiz_question_answer.text, quiz_question_answer.__str__())

    def test_studenttoquiz(self):
        course1 = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course1)
        quiz = Quiz.objects.create(name="quiz1", topic=topic1)
        student_one = Student.objects.create(
            email="testemail@testingmemail.com", first_name="John", last_name="Doe")
        # ttc1 = TopicToCategory.objects.create(
        #    topic=topic1, category=quiz, weight=0.30)
        # grade = Grade.objects.create(name="Quiz 1", value=89,
        #                     topic_to_category=ttc1, student=student_one)
        student_to_quiz = StudentToQuiz.objects.create(
            quiz=quiz, student=student_one, grade=90)
        self.assertEqual("Student took quiz for " +
                         quiz.__str__(), student_to_quiz.__str__())
        self.assertEqual(None, student_to_quiz.generate_score())

    def test_settings(self):
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
        settings = Settings.objects.create(
            color="#000000",
            nickname="Jon",
            user=student
        )
        self.assertEqual("Settings for " +
                         settings.user.__str__(), settings.__str__())

    def test_topictotopic(self):
        course = Course.objects.create(
            name="courseName1", course_code="courseCode1", subject_code="subjectCode1")
        topic1 = Topic.objects.create(name="topic1", course=course)
        topic2 = Topic.objects.create(name="topic2", course=course)

        topic_to_topic = TopicToTopic.objects.create(
            course=course,
            topic_node=topic1,
            ancestor_node=topic2
        )

        self.assertEqual(topic_to_topic.ancestor_node.__str__(
        ) + " -> " + topic_to_topic.topic_node.__str__(), topic_to_topic.__str__())

    def test_externalsiteslist(self):
        yo = ExternalSitesList.objects.create(
            website_name="Site 1", website_nickname="Site 1", is_website_used=False)
        self.assertEqual(yo.website_name +
                         ' (' + yo.website_nickname + ')', yo.__str__())
        self.assertEqual(yo.set_website_used(False), None)

    def test_ExternalQuizStatic(self):
        to = ExternalQuizStatic.objects.create(quizName="Quiz 1", quizScore=0, question1="Question 1", question1answer1="Answer 1",
                                               question1answer2="Answer 2", question1answer3="Answer 3", question1answer4="Answer 4", correctIndex1=1, isCorrectAnswer1=False)
        self.assertEqual(to.quizName, to.__str__())
        self.assertEqual(to.isCorrectAnswer1, to.getIsCorrect())
        self.assertEqual(to.quizScore, to.getQuizScore())
        self.assertEqual("{\"quizName\": \"" + str(to.quizName) +
                         "\", \"quizScore\": " + str(to.quizScore) + "}", str(to.getModel()))


class Test_Search(TestCase):

    @mock.patch('sptApp.api_views.requests.post')
    def test_search1(self, mock_request):   # Search specific students
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

        client = APIClient()
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        request = client.get(
            path='/api/search/?id_token=fdasasd&query=' + str(student.first_name), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_search2(self, mock_request):   # Can't search if google errors
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

        client = APIClient()
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        request = client.get(
            path='/api/search/?id_token=fdasasd&query=' + str(student.first_name), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_search3(self, mock_request):   # Search all students
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

        client = APIClient()
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        request = client.get(
            path='/api/search/?id_token=fdasasd&query=All', format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(200, request.status_code)

    def test_search4(self):   # Can't search with pk
        data_parameters = {
            "first_name": "Jon",
            "last_name": "Snow",
            "email": "jsnow@virginia.edu",
            "isCreate": True,
            "isProfessor": True,
        }

        client = APIClient()
        student = Student.objects.create(
            email=data_parameters["email"],
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        request = client.get(
            path='/api/search/safdsa?id_token=fdasasd&query=All', format='json')

        self.assertEqual(400, request.status_code)

    @mock.patch('sptApp.api_views.requests.post')
    def test_search5(self, mock_request):   # Can't search if you dont have an email
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

        client = APIClient()
        student = Student.objects.create(
            email="fakeemail@virginia.edu",
            first_name=data_parameters["first_name"],
            last_name=data_parameters["last_name"]
        )
        request = client.get(
            path='/api/search/?id_token=fdasasd&query=' + str(student.first_name), format='json')
        mock_request.assert_called_once_with(
            params={
                'id_token': "fdasasd"
            },
            url="https://www.googleapis.com/oauth2/v3/tokeninfo"
        )
        self.assertEqual(404, request.status_code)

    def test_search_post1(self):
        client = APIClient()
        request = client.post(
            path='/api/search/?id_token=fdasasd&query=afsasd', format='json')
        self.assertEqual(404, request.status_code)

    def test_search_put1(self):
        client = APIClient()
        request = client.put(
            path='/api/search/?id_token=fdasasd&query=afsasd', format='json')
        self.assertEqual(404, request.status_code)

    def test_search_delete1(self):
        client = APIClient()
        request = client.delete(
            path='/api/search/?id_token=fdasasd&query=afsasd', format='json')
        self.assertEqual(404, request.status_code)



'''
______________________________________________________________________________________________              External Import Grades
 ExternalImportGrades
______________________________________________________________________________________________
'''
 
class Test_ExternalImportGrades(TestCase):

    '''
    __________________________________________________  Delete (Not A Feature)
    __________________________________________________
    '''

    def test_delete_externalImportGrades(self): 
        client = APIClient()

        professor = Student.objects.create(email="danielalanseymour@gmail.com", first_name="Dan", last_name="Seymour",  
            username="professorDan", is_professor=True,  id_token="123abc")
        bad_professor = Student.objects.create(email="daniel.a.seymour.cs@gmail.com", first_name="Dan", last_name="Seymour",  
            username="badProfessor", is_professor=True,  id_token="321cba")
        student = Student.objects.create(email="das5fa@virginia.edu", first_name="Dan", last_name="Seymour",  
            username="studentDan", is_professor=False, id_token="abc123")

        course = Course.objects.create(name= 'Course' , course_code= 'CS', subject_code= '123', professor= professor )
        topic= Topic.objects.create(name= 'Topic' , course= course )
        category = Category.objects.create(name= 'External Site') 
        topicToCategory = TopicToCategory.objects.create(topic= topic, category= category)
        grade = Grade.objects.create(name='Grade Name', topic_to_category= topicToCategory,student= student)
        externalSite = ExternalSite.objects.create(name="Site 1", base_url = 'http://example1.com')
        externalSiteToCourse = ExternalSiteToCourse.objects.create(course= course, external_site= externalSite, 
            url_ending= '1?APIKEY=123123')
        externalSiteToGrade = ExternalSiteToGrade.objects.create(external_site_to_course=externalSiteToCourse, grade=grade, 
            link='http://exampleurl.com/12?APIKEY=12312')


        # Tests ()
        request = client.delete(path='/api/external_import_grades/',format='json')
        self.assertEqual(406, request.status_code, "No professor_id => Fail")
        self.assertEqual('Missing ID', request.data['result'], "No professor_id => Fail") 

        request = client.delete(path='/api/external_import_grades/?id=123',format='json')
        self.assertEqual(406, request.status_code, "No externalSiteToCourse pk => Fail")
        self.assertEqual('Missing ExternalSiteToCourse pk', request.data['result'], "No externalSiteToCourse pk => Fail") 

        request = client.delete(path='/api/external_import_grades/1?id=44444',format='json')
        self.assertEqual(406, request.status_code, "Bad professor_id => Fail")
        self.assertEqual('Invalide ID', request.data['result'], "Bad professor_id => Fail") 

        request = client.delete(path='/api/external_import_grades/1?id=' + str(student.id_token),format='json')
        self.assertEqual(406, request.status_code, "student_ID => Fail")
        self.assertEqual('Student ID passed in', request.data['result'], "student_ID => Fail") 

        request = client.delete(path='/api/external_import_grades/313121?id=' + str(professor.id_token),format='json')
        self.assertEqual(406, request.status_code, "Bad externalSiteToCourse pk => Fail")
        self.assertEqual('ExternalSiteToCourse does not exist', request.data['result'], "Bad externalSiteToCourse pk => Fail") 

        request = client.delete(path='/api/external_import_grades/313121?id=' + str(bad_professor.id_token),format='json')
        self.assertEqual(406, request.status_code, "Bad externalSiteToCourse pk => Fail")
        self.assertEqual('ExternalSiteToCourse does not exist', request.data['result'], "Bad externalSiteToCourse pk => Fail") 


        # Tests ()        
        before_num_ExternalSiteToCourse = len(ExternalSiteToCourse.objects.all())
        before_num_ExternalSiteToGrade = len(ExternalSiteToGrade.objects.all())
        before_num_Grade = len(Grade.objects.all())
        self.assertEqual(1, before_num_ExternalSiteToCourse, "Number of ExternalSiteToCourse Before") 
        self.assertEqual(1, before_num_ExternalSiteToGrade, "Number of ExternalSiteToGrade Before")
        self.assertEqual(1, before_num_Grade, "Number of Grade Before")
        

        
        request = client.delete(path='/api/external_import_grades/' + str(externalSiteToCourse.pk) + '?id=' + str(professor.id_token),format='json')
        self.assertEqual(200, request.status_code, "Successful Delete")
        self.assertEqual('Successfully Deleted', request.data['result'], "Successful Delete") 


        # Tests ()
        after_num_ExternalSiteToCourse = len(ExternalSiteToCourse.objects.all())
        after_num_ExternalSiteToGrade = len(ExternalSiteToGrade.objects.all())
        after_num_Grade = len(Grade.objects.all())
        self.assertEqual(0, after_num_ExternalSiteToCourse, "Number of ExternalSiteToCourse After") 
        self.assertEqual(0, after_num_ExternalSiteToGrade, "Number of ExternalSiteToGrade After")

        self.assertEqual(0, after_num_Grade, "Number of Grade After")
        
    
    '''
    __________________________________________________  Get
    __________________________________________________
    '''
    def test_get_externalImportGrades(self): 
        client = APIClient()
        
        professor = Student.objects.create(email="danielalanseymour@gmail.com", first_name="Dan", last_name="Seymour",  
            username="professorDan", is_professor=True,  id_token="123abc")
        student = Student.objects.create(email="das5fa@virginia.edu", first_name="Dan", last_name="Seymour",  
            username="studentDan", is_professor=False, id_token="abc123")
        course = Course.objects.create(name= 'Course' , course_code= 'CS', subject_code= '123', professor= professor )
        topic= Topic.objects.create(name= 'Topic' , course= course )
        category = Category.objects.create(name= 'External Site') 
        topicToCategory = TopicToCategory.objects.create(topic= topic, category= category)
        grade = Grade.objects.create(name='Grade Name', topic_to_category= topicToCategory,student= student)
        externalSite = ExternalSite.objects.create(name="Site 1", base_url = 'http://testserver/')
        externalSiteToCourse = ExternalSiteToCourse.objects.create(course= course, external_site= externalSite, 
            url_ending= '1?APIKEY=123123')
        externalSiteToGrade = ExternalSiteToGrade.objects.create(external_site_to_course=externalSiteToCourse, grade=grade, 
            link='http://exampleurl.com/12?APIKEY=12312')

        bad_professor = Student.objects.create(email="badbad@gmail.com", first_name="Dan", last_name="Seymour",  
            username="badProfessor", is_professor=True,  id_token="321cba")
        bad_course = Course.objects.create(name= 'Bad Course' , course_code= 'CS', subject_code= '4444', professor= bad_professor)
        bad_externalSitesToCourse= ExternalSiteToCourse.objects.create(course= bad_course, external_site= externalSite, 
            url_ending= '1?APIKEY=123')


        # Tests ()
        request = client.get(path='/api/external_import_grades/',format='json')
        self.assertEqual(406, request.status_code, "No professor_id => Fail")
        self.assertEqual('Missing ID', request.data['result'], "No professor_id => Fail") 

        request = client.get(path='/api/external_import_grades/?id=123',format='json')
        self.assertEqual(406, request.status_code, "No course pk => Fail")
        self.assertEqual('Missing course pk', request.data['result'], "No course pk => Fail") 

        request = client.get(path='/api/external_import_grades/?id=4444&course_pk=4444',format='json')
        self.assertEqual(406, request.status_code, "Invalide ID => Fail")
        self.assertEqual('Invalide ID', request.data['result'], "Invalide ID => Fail") 

        request = client.get(path='/api/external_import_grades/?id=' + str(student.id_token) + '&course_pk=4444',format='json')
        self.assertEqual(406, request.status_code, "Student ID => Fail")
        self.assertEqual('Student ID passed in', request.data['result'], "Student ID => Fail") 

        request = client.get(path='/api/external_import_grades/?id=' + str(professor.id_token) + '&course_pk=4444',
            format='json')
        self.assertEqual(406, request.status_code, "Invalid course pk => Fail")
        self.assertEqual('Invalid course pk', request.data['result'], "Invalid course pk => Fail") 

        request = client.get(path='/api/external_import_grades/?id=' + str(professor.id_token) + '&course_pk=' + str(bad_course.pk),
            format='json')
        self.assertEqual(406, request.status_code, "Bad course pk => Fail")
        self.assertEqual('Invalid course pk', request.data['result'], "Bad course pk => Fail") 

        request = client.get(path='/api/external_import_grades/4443?id=' + str(professor.id_token) + '&course_pk=' + str(course.pk),
            format='json')
        self.assertEqual(406, request.status_code, "No studentToCourse objects => Fail")
        self.assertEqual('No students in course', request.data['result'], "No studentToCourse objects => Fail") 




        studentToCourse = StudentToCourse.objects.create(student= student, course= course, semester= 'Spring-2019')





        # Tests ()
        request = client.get(path='/api/external_import_grades/4443?id=' + str(professor.id_token) + '&course_pk=' + str(course.pk),
            format='json')
        self.assertEqual(406, request.status_code, "Invalid ExternalSiteToCourse pk => Fail")
        self.assertEqual('Invalid ExternalSiteToCourse pk', request.data['result'], "Invalid ExternalSiteToCourse pk => Fail") 

        request = client.get(path='/api/external_import_grades/' + str(bad_externalSitesToCourse.pk) + '?id=' + str(professor.id_token) + '&course_pk=' + str(course.pk),
            format='json')
        self.assertEqual(406, request.status_code, "Bad ExternalSiteToCourse pk => Fail")
        self.assertEqual('Invalid ExternalSiteToCourse pk', request.data['result'], "Bad ExternalSiteToCourse pk => Fail") 

        

        print('\n\nLUKE HERE IS THE PROBLEM \n\n')
        # TODO GO to the bottom of ExternalImportGradesViewSet's get (line 2453)
        request = client.get('http://testserver/api/external_import_grades/' + str(externalSiteToCourse.pk) + '?id=' + str(professor.id_token) + '&course_pk=' + str(course.pk))
        self.assertEqual(200, request.status_code, "Bad ExternalSiteToCourse pk => Fail")

    

    '''
    __________________________________________________  Post (Not A Feature)
    __________________________________________________
    '''
    
    def test_post_externalImportGrades(self): 
        client = APIClient()

        professor = Student.objects.create(email="danielalanseymour@gmail.com", first_name="Dan", last_name="Seymour",  
            username="professorDan", is_professor=True,  id_token="123abc")
        student = Student.objects.create(email="das5fa@virginia.edu", first_name="Dan", last_name="Seymour",  
            username="studentDan", is_professor=False, id_token="abc123")
        course = Course.objects.create(name= 'Course' , course_code= 'CS', subject_code= '123', professor= professor )
        topic= Topic.objects.create(name= 'Topic' , course= course )
        category = Category.objects.create(name= 'External Site') 
        topicToCategory = TopicToCategory.objects.create(topic= topic, category= category)
        grade = Grade.objects.create(name='Grade Name', topic_to_category= topicToCategory,student= student)
        externalSite = ExternalSite.objects.create(name="Site 1", base_url = 'http://testserver/')
        
        bad_professor = Student.objects.create(email="badbad@gmail.com", first_name="Dan", last_name="Seymour",  
            username="badProfessor", is_professor=True,  id_token="321cba")
        bad_course = Course.objects.create(name= 'Bad' , course_code= 'CS', subject_code= '4444', professor= bad_professor )
        bad_externalSiteToCourse= ExternalSiteToCourse.objects.create(course= course, external_site= externalSite, url_ending='123123')
        
        param_missing_professorID = {'course_pk': 2222, 'externalSite_pk': 3333, 'url_ending': 4444}
        param_missing_coursePK = {'professor_id': 1111, 'externalSite_pk': 3333, 'url_ending': 4444}
        param_missing_externalSitePk = {'professor_id': 1111, 'course_pk': 2222, 'url_ending': 4444}
        param_missing_urlEnding = {'professor_id': 1111, 'course_pk': 2222, 'externalSite_pk': 3333}

        param_invalid_professorID = {'professor_id': 1111, 'course_pk': 2222, 'externalSite_pk': 3333, 'url_ending': 4444 }
        param_bad_studentID = {'professor_id': student.id_token, 'course_pk': 2222, 'externalSite_pk': 3333, 'url_ending': 4444 }
        param_invalid_coursePK = {'professor_id': professor.id_token, 'course_pk': 2222, 'externalSite_pk': 3333, 'url_ending': 4444 }
        param_bad_coursePK = {'professor_id': professor.id_token, 'course_pk': bad_course.pk, 'externalSite_pk': 3333,'url_ending': 4444 }
        param_bad_externalSitePK = {'professor_id': professor.id_token, 'course_pk': course.pk, 'externalSite_pk': 3333, 'url_ending': 4444 }
        param_bad_url_ending = {'professor_id': professor.id_token, 'course_pk': course.pk, 
            'externalSite_pk': externalSite.pk, 'url_ending': bad_externalSiteToCourse.url_ending }


        # Tests ()
        request = client.post(path='/api/external_import_grades/1',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('PK should not be passed', request.data['result'], "PK => Fail") 

        request = client.post(path='/api/external_import_grades/', data= param_missing_professorID,format='json')
        self.assertEqual(406, request.status_code, "Missing professor_id => Fail")
        self.assertEqual('Missing professor_id', request.data['result'], "Missing professor_id => Fail") 

        request = client.post(path='/api/external_import_grades/', data= param_missing_coursePK,format='json')
        self.assertEqual(406, request.status_code, "Missing course_pk => Fail")
        self.assertEqual('Missing course_pk', request.data['result'], "Missing course_pk => Fail") 

        request = client.post(path='/api/external_import_grades/', data= param_missing_externalSitePk,format='json')
        self.assertEqual(406, request.status_code, "Missing externalSite_pk => Fail")
        self.assertEqual('Missing externalSite_pk', request.data['result'], "Missing externalSite_pk => Fail") 

        request = client.post(path='/api/external_import_grades/', data= param_missing_urlEnding,format='json')
        self.assertEqual(406, request.status_code, "Missing url_ending => Fail")
        self.assertEqual('Missing url_ending', request.data['result'], "Missing url_ending => Fail") 

        request = client.post(path='/api/external_import_grades/', data= param_invalid_professorID,format='json')
        self.assertEqual(406, request.status_code, "Invalide ID => Fail")
        self.assertEqual('Invalide ID', request.data['result'], "Invalide ID => Fail") 

        request = client.post(path='/api/external_import_grades/', data= param_bad_studentID,format='json')
        self.assertEqual(406, request.status_code, "Student ID => Fail")
        self.assertEqual('Student ID passed in', request.data['result'], "Student ID => Fail") 

        request = client.post(path='/api/external_import_grades/', data= param_bad_coursePK,format='json')
        self.assertEqual(406, request.status_code, "Invalid course pk => Fail")
        self.assertEqual('Invalid course pk', request.data['result'], "Invalid course pk => Fail")

        request = client.post(path='/api/external_import_grades/', data= param_invalid_coursePK,format='json')
        self.assertEqual(406, request.status_code, "Invalid course pk => Fail")
        self.assertEqual('Invalid course pk', request.data['result'], "Invalid course pk => Fail")

        request = client.post(path='/api/external_import_grades/', data= param_bad_externalSitePK,format='json')
        self.assertEqual(406, request.status_code, "Invalid ExternalSite pk => Fail")
        self.assertEqual('Invalid ExternalSite pk', request.data['result'], "Invalid ExternalSite pk => Fail")

        request = client.post(path='/api/external_import_grades/', data= param_bad_url_ending, format='json')
        self.assertEqual(406, request.status_code, "ExternalSiteToCourse already exists => Fail")
        self.assertEqual('ExternalSiteToCourse already exists', request.data['result'], "ExternalSiteToCourse already exists => Fail")




        # TODO Test create_import_grades 
        param_good = {'professor_id': professor.id_token, 'course_pk': course.pk, 'externalSite_pk': externalSite.pk, 'url_ending': '1?APIKey=1231' }

        request = client.post('http://testserver/api/external_import_grades/', data= param_good,format='json' )
        self.assertEqual(200, request.status_code, "Bad ExternalSiteToCourse pk => Fail")
    


    
    '''
    __________________________________________________  Put (Not A Feature)
    __________________________________________________
    '''

    def test_put_externalImportGrades(self): 
        client = APIClient()
        request = client.put(path='/api/external_import_grades/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.put(path='/api/external_import_grades/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 


















'''
______________________________________________________________________________________________              External Sites
 External Site: The list of websites that can be used for external interaction (API's)
______________________________________________________________________________________________
'''
 
class Test_ExternalSite(TestCase):

    '''
    __________________________________________________  Delete (Not A Feature)
    __________________________________________________
    '''

    def test_delete_externalSite(self): 
        client = APIClient()
        request = client.delete(path='/api/external_sites/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.delete(path='/api/external_sites/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    '''
    __________________________________________________  Get
    __________________________________________________
    '''
    def test_get_externalSite(self):
        client = APIClient()

        professor = Student.objects.create(email="danielalanseymour@gmail.com", first_name="Dan", last_name="Seymour",  
            username="professorDan", is_professor=True,  id_token="123abc")
        student = Student.objects.create(email="das5fa@virginia.edu", first_name="Dan", last_name="Seymour",  
            username="studentDan", is_professor=False, id_token="abc123")


        # Test
        request = client.get(path='/api/external_sites/120',format='json')
        self.assertEqual(406, request.status_code, "No professor_id => Error" )
        self.assertEqual('Missing ID', request.data['result'], "No professor_id => Error") 

        request = client.get(path='/api/external_sites/120?id=111111111111' ,format='json')
        self.assertEqual(406, request.status_code, "Invalid ID => Error" )
        self.assertEqual('Invalide ID', request.data['result'], "Invalid ID => Error") 

        request = client.get(path='/api/external_sites/120?id=' + str(student.id_token) ,format='json')
        self.assertEqual(406, request.status_code, "Student ID => Error" )
        self.assertEqual('Student ID passed in', request.data['result'], "Student ID => Error") 

        request = client.get(path='/api/external_sites/?id=' + str(professor.id_token) ,format='json')
        self.assertEqual(200, request.status_code, "Get all external sites when none" )
        self.assertEqual([], request.data['result'], "Get all external sites when none") 

        request = client.get(path='/api/external_sites/1?id=' + str(professor.id_token) ,format='json')
        self.assertEqual(406, request.status_code, "Invalid externalSite pk => Error" )
        self.assertEqual('Invalid externalSite pk', request.data['result'], "Invalid externalSite pk => Error") 


        
        external_site_1 = ExternalSite.objects.create(name="Site 1", base_url = 'http://example1.com')
        external_site_2 = ExternalSite.objects.create(name="Site 2", base_url = 'http://example2.com')
        


        # Tests
        expected = "[OrderedDict([('pk', 1), ('name', 'Site 1'), ('base_url', 'http://example1.com')]), OrderedDict([('pk', 2), ('name', 'Site 2'), ('base_url', 'http://example2.com')])]"
        request = client.get(path='/api/external_sites/?id=' + str(professor.id_token) ,format='json')
        self.assertEqual(200, request.status_code, "Get all external sites" )
        self.assertEqual(expected, str(request.data['result']), "Get all external sites") 
        
        expected = {'pk': 1, 'name': 'Site 1', 'base_url': 'http://example1.com'}
        request = client.get(path='/api/external_sites/' + str(external_site_1.pk) + '?id=' + str(professor.id_token) ,format='json')
        self.assertEqual(200, request.status_code, "Get individual external site" )
        self.assertEqual(expected, request.data['result'], "Get all external sites") 

    

    '''
    __________________________________________________  Post (Not A Feature)
    __________________________________________________
    '''
    
    def test_post_externalSite(self):   
        client = APIClient()
        request = client.post(path='/api/external_sites/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.post(path='/api/external_sites/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    
    '''
    __________________________________________________  Put (Not A Feature)
    __________________________________________________
    '''

    def test_put_externalSite(self): 
        client = APIClient()
        request = client.put(path='/api/external_sites/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.put(path='/api/external_sites/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 







'''
______________________________________________________________________________________________          ExternalImportGrades (Test)
ExternalImportGradesTest
______________________________________________________________________________________________
'''
 
class Test_ExternalImportGradesTest(TestCase):

    '''
    __________________________________________________  Delete (Not A Feature)
    __________________________________________________
    '''

    def test_delete_externalImportGradesTest(self): 
        client = APIClient()
        request = client.delete(path='/api/external_import_grades_test/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.delete(path='/api/external_import_grades_test/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    '''
    __________________________________________________  Get
    __________________________________________________
    '''
    def test_get_externalImportGradesTest(self):
        client = APIClient()
        
        expected_grades_good = {'exams': [{'topic_name': 'Arrays','grade_name': 'External Site Grade','students': [
            {'email': 'das5fa@virginia.edu','grade_value': 90},{'email': 'ceb4aq@virginia.edu','grade_value': 101},
            {'email': 'abs4cr@virginia.edu','grade_value': -1},{'email': 'smm2zr@virginia.edu','grade_value': 100},
            {'email': 'lsm5fm@virginia.edu','grade_value': 0}]}]}
        expected_grades_missing_exams = {} 
        expected_grades_missing_topicName = {'exams': [{'grade_name': 'External Site Grade','students': [
            {'email': 'das5fa@virginia.edu','grade_value': 90},{'email': 'ceb4aq@virginia.edu','grade_value': 101},
            {'email': 'abs4cr@virginia.edu','grade_value': -1},{'email': 'smm2zr@virginia.edu','grade_value': 100},
            {'email': 'lsm5fm@virginia.edu','grade_value': 0}]}]}
        expected_grades_missing_gradeName = {'exams': [{'topic_name': 'Arrays','students': [
            {'email': 'das5fa@virginia.edu','grade_value': 90},{'email': 'ceb4aq@virginia.edu','grade_value': 101},
            {'email': 'abs4cr@virginia.edu','grade_value': -1},{'email': 'smm2zr@virginia.edu','grade_value': 100},
            {'email': 'lsm5fm@virginia.edu','grade_value': 0}]}]}
        expected_grades_missing_students = {'exams': [{'topic_name': 'Arrays','grade_name': 'External Site Grade',}]}
        expected_grades_missing_email = {'exams': [{'topic_name': 'Arrays','grade_name': 'External Site Grade','students': [
            {'grade_value': 90},{'grade_value': 101},{'grade_value': -1},{'grade_value': 100},{'grade_value': 0}]}]}
        expected_grades_missing_gradeValue = {'exams': [{'topic_name': 'Arrays','grade_name': 'External Site Grade',
            'students': [{'email': 'das5fa@virginia.edu'},{'email': 'ceb4aq@virginia.edu'},
            {'email': 'abs4cr@virginia.edu'},{'email': 'smm2zr@virginia.edu'},{'email': 'lsm5fm@virginia.edu'}]}]}




        # Tests
        request = client.get(path='/api/external_import_grades_test/',format='json')
        self.assertEqual(400, request.status_code, "No PK => Fail")
        
        request = client.get(path='/api/external_import_grades_test/1',format='json')
        self.assertEqual(200, request.status_code, "grades_good")
        self.assertEqual(expected_grades_good, json.loads(request.content.decode("utf-8")), "grades_good") 

        request = client.get(path='/api/external_import_grades_test/2',format='json')
        self.assertEqual(200, request.status_code, "grades_missing_exams")
        self.assertEqual(expected_grades_missing_exams, json.loads(request.content.decode("utf-8")), "grades_missing_exams") 

        request = client.get(path='/api/external_import_grades_test/3',format='json')
        self.assertEqual(200, request.status_code, "grades_missing_topicName")
        self.assertEqual(expected_grades_missing_topicName, json.loads(request.content.decode("utf-8")), "grades_missing_topicName") 

        request = client.get(path='/api/external_import_grades_test/4',format='json')
        self.assertEqual(200, request.status_code, "grades_missing_gradeName")
        self.assertEqual(expected_grades_missing_gradeName, json.loads(request.content.decode("utf-8")), "grades_missing_gradeName") 
        
        request = client.get(path='/api/external_import_grades_test/5',format='json')
        self.assertEqual(200, request.status_code, "grades_missing_students")
        self.assertEqual(expected_grades_missing_students, json.loads(request.content.decode("utf-8")), "grades_missing_students") 
        
        request = client.get(path='/api/external_import_grades_test/6',format='json')
        self.assertEqual(200, request.status_code, "grades_missing_email")
        self.assertEqual(expected_grades_missing_email, json.loads(request.content.decode("utf-8")), "grades_missing_email") 

        request = client.get(path='/api/external_import_grades_test/7',format='json')
        self.assertEqual(200, request.status_code, "expected_grades_missing_gradeValue")
        self.assertEqual(expected_grades_missing_gradeValue, json.loads(request.content.decode("utf-8")), "expected_grades_missing_gradeValue") 
        

        request = client.get(path='/api/external_import_grades_test/80',format='json')
        self.assertEqual(400, request.status_code, "No JSON => Fail")
        
        
        
        
    

    '''
    __________________________________________________  Post (Not A Feature)
    __________________________________________________
    '''
    
    def test_post_externalImportGradesTest(self):   
        client = APIClient()
        request = client.post(path='/api/external_import_grades_test/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.post(path='/api/external_import_grades_test/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    
    '''
    __________________________________________________  Put (Not A Feature)
    __________________________________________________
    '''

    def test_put_externalImportGradesTest(self): 
        client = APIClient()
        request = client.put(path='/api/external_import_grades_test/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.put(path='/api/external_import_grades_test/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 


'''
______________________________________________________________________________________________              ExternalSite To Course
 ExternalSite To Course
______________________________________________________________________________________________
'''
 
class Test_ExternalSiteToCourse(TestCase):

    '''
    __________________________________________________  Delete (Not A Feature)
    __________________________________________________
    '''

    def test_delete_externalSiteToCourse(self): 
        client = APIClient()
        request = client.delete(path='/api/external_sites_to_course/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.delete(path='/api/external_sites_to_course/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    '''
    __________________________________________________  Get
    __________________________________________________
    '''
    def test_get_externalSiteToCourse(self):
        client = APIClient()

        professor = Student.objects.create(email="danielalanseymour@gmail.com", first_name="Dan", last_name="Seymour", 
            username="professorDan", is_professor=True,  id_token="123abc" )
        student = Student.objects.create(email="das5fa@virginia.edu", first_name="Dan", last_name="Seymour",  
            username="studentDan", is_professor=False, id_token="abc123")
        course = Course.objects.create(name= 'Course' , course_code= 'CS', subject_code= '123', professor= professor )
        externalSite = ExternalSite.objects.create(name="Site 1", base_url = 'http://example1.com')

        # Tests
        request = client.get(path='/api/external_sites_to_course/1',format='json')
        self.assertEqual(406, request.status_code, "No professor_id => Fail")
        self.assertEqual('Missing ID', request.data['result'], "No professor_id => Fail") 
        
        request = client.get(path='/api/external_sites_to_course/1?id=BADBAD',format='json')
        self.assertEqual(406, request.status_code, "Invalide ID => Fail")
        self.assertEqual('Invalide ID', request.data['result'], "Invalide ID => Fail") 
        
        request = client.get(path='/api/external_sites_to_course/1?id=' + str(student.id_token),format='json')
        self.assertEqual(406, request.status_code, "Student ID passed in => Fail")
        self.assertEqual('Student ID passed in', request.data['result'], "Student ID passed in => Fail") 

        request = client.get(path='/api/external_sites_to_course/1213?id=' + str(professor.id_token),format='json')
        self.assertEqual(406, request.status_code, "Invalid Course PK => Fail")
        self.assertEqual('Course not found', request.data['result'], "Invalid Course PK => Fail") 

        request = client.get(path='/api/external_sites_to_course/' + str(course.pk) + '?id=' + str(professor.id_token),format='json')
        self.assertEqual(200, request.status_code, "No ExternalSiteToCourse")
        self.assertEqual([], request.data['result'], "No ExternalSiteToCourse") 




        externalSiteToCourse1 = ExternalSiteToCourse.objects.create(course= course, external_site=  externalSite,
            url_ending = '12?APIKEY=123')

        
        # Tests 
        
        request = client.get(path='/api/external_sites_to_course/' + str(course.pk) + '?id=' + str(professor.id_token),format='json')
        self.assertEqual(200, request.status_code, "One ExternalSiteCourse object for course")
        #expected = "{'pk': 1, 'course': OrderedDict([('id', 1), ('name', 'Course'), ('course_code', 'CS'), ('subject_code', '123'), ('professor', OrderedDict([('id', 1), ('password', ''), ('last_login', None), ('is_superuser', False), ('is_staff', False), ('is_active', True), ('date_joined', '2019-04-14T13:02:33.882144Z'), ('first_name', 'Dan'), ('last_name', 'Seymour'), ('email', 'danielalanseymour@gmail.com'), ('join_date', '2019-04-14T13:02:33.882956Z'), ('id_token', '123abc'), ('is_professor', True), ('username', 'professorDan'), ('groups', []), ('user_permissions', [])]))]), 'external_site': OrderedDict([('id', 1), ('name', 'Site 1'), ('base_url', 'http://example1.com')]), 'url_ending': '12?APIKEY=123'}"
        #self.assertEqual(expected, str(request.data['result']), "One ExternalSiteCourse object for course") 

        
        
        externalSiteToCourse2 = ExternalSiteToCourse.objects.create(course= course, external_site=  externalSite,
            url_ending = '12?APIKEY=124')


        # Tests 
        request = client.get(path='/api/external_sites_to_course/' + str(course.pk) + '?id=' + str(professor.id_token),format='json')
        self.assertEqual(200, request.status_code, "Multiple ExternalSiteCourse objects for course")
        #expected = "[OrderedDict([('pk', 1), ('course', 1), ('external_site', 1), ('url_ending', '12?APIKEY=123')]), OrderedDict([('pk', 2), ('course', 1), ('external_site', 1), ('url_ending', '12?APIKEY=124')])]"
        #self.assertEqual(expected, str(request.data['result']), "Multiple ExternalSiteCourse objects for course") 



    

    '''
    __________________________________________________  Post (Not A Feature)
    __________________________________________________
    '''
    
    def test_post_externalSiteToCourse(self):
        client = APIClient()
        request = client.post(path='/api/external_sites_to_course/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.post(path='/api/external_sites_to_course/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    
    '''
    __________________________________________________  Put (Not A Feature)
    __________________________________________________
    '''

    def test_put_externalSiteToCourse(self):
        client = APIClient()
        request = client.put(path='/api/external_sites_to_course/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.put(path='/api/external_sites_to_course/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 


















'''
______________________________________________________________________________________________              ExternalSite To Grade
 ExternalSite To Grade
______________________________________________________________________________________________
'''
 
class Test_ExternalSiteToGrade(TestCase):

    '''
    __________________________________________________  Delete (Not A Feature)
    __________________________________________________
    '''

    def test_delete_externalSiteToGrade(self): 
        client = APIClient()
        request = client.delete(path='/api/external_sites_to_grade/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.delete(path='/api/external_sites_to_grade/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    '''
    __________________________________________________  Get
    __________________________________________________
    '''
    def test_get_externalSiteToGrade(self): 
        client = APIClient()
        request = client.get(path='/api/external_sites_to_grade/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.get(path='/api/external_sites_to_grade/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 

    

    '''
    __________________________________________________  Post (Not A Feature)
    __________________________________________________
    '''
    
    def test_post_externalSiteToGrade(self): 
        client = APIClient()
        request = client.post(path='/api/external_sites_to_grade/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.post(path='/api/external_sites_to_grade/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 
        
    
    
    '''
    __________________________________________________  Put (Not A Feature)
    __________________________________________________
    '''

    def test_put_externalSiteToGrade(self): 
        client = APIClient()
        request = client.put(path='/api/external_sites_to_grade/',format='json')
        self.assertEqual(406, request.status_code, "PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "PK => Fail") 
        request = client.put(path='/api/external_sites_to_grade/1',format='json')
        self.assertEqual(406, request.status_code, "No PK => Fail")
        self.assertEqual('Currently not a feature of SPT', request.data['result'], "No PK => Fail") 





