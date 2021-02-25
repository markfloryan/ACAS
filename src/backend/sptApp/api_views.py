# Django and REST Framework
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.core.exceptions import *
from django.contrib.auth import login


# Making calls to google (get and post)
import requests
import ast
import json
import urllib.request
import urllib.parse

# Regex
import re

# Reading CSVs
import csv

# Data manipulation
from collections import defaultdict

# Grading system
from sptApp.grading_system import getScore, update_topic_grade
from sptApp import grading_system

# Pagination
from .pagination import *

# Permissions
from sptApp.permissions import IsProfessor, ReadOnly, ReadOnly, CreateOnly, IsOwner
from rest_framework.permissions import IsAuthenticated

# Authentication
from sptApp.auth import GoogleOAuth, get_bearer_token
from sptApp.auth import API_DEBUG

#Decorators
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt

#Errors
from django.utils.datastructures import MultiValueDictKeyError

# Internal imports
from .models import *
from .responses import *
from .serializers import *

# GradeScope
from sptApp.gradescopeAPI.pyscope.pyscope import *


''' API ENDPOINTS '''


'''
______________________________________________________________________________________________      Course
    Course: All courses. Contains functionality for viewing, creating, deleting, and editing a course
______________________________________________________________________________________________
'''


# CRUD for courses.
class CourseViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly) ]
    renderer_classes = (JSONRenderer, )
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    model = Course

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/courses/
     function: Removes a given Course
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

        #Don't allow courses to be deleted right now
        return successful_delete_response()

    '''
    __________________________________________________  get
     url: GET :: <WEBSITE>/api/courses/ OR
          GET :: <WEBSITE>/api/courses/<COURSE_ID> OR
     function: Retrieves all or a single Course
    __________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        #grab that user's primary key
        userId = request.user.pk

        #get the courses associated with that student, professor, or TA
        courses = Course.objects.filter(courses__student__pk=userId) | Course.objects.filter(professor=userId) | Course.objects.filter(teaching_assistants=userId)

        #handle case where user is requesting one specific course
        if pk is not None:
            try:
                course = courses.filter(pk=pk)[0]
                serializer = self.serializer_class(course, many=False)
                #if not serializer.is_valid():
                #    return invalid_serializer_response(serializer.errors)

            except self.model.DoesNotExist:
                return object_not_found_response()
            except IndexError:
                return object_not_found_response()
        else:
            #otherwise just return all courses associated with this user
            serializer = self.serializer_class(courses, many=True)
            #if not serializer.is_valid():
            #   return invalid_serializer_response(serializer.errors)

        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/courses/
     function: Creates a given course
    __________________________________________________
    '''

    def post(self, request, format=None, pk=None):

        params = json.loads(request.body)

        if pk is None:
            serializer = self.serializer_class(data=params)
            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/courses/<COURSE_ID>
     function: Edits a given existing Course
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        if pk is None or request.body is None:
            return missing_id_response()
        try:
            params = json.loads(request.body)
        except:
            return missing_id_response()

        try:
            result = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return object_not_found_response()

        serializer = self.serializer_class(result, data=params)

        if not serializer.is_valid():
            return invalid_serializer_response(serializer.errors)

        serializer.save()
        return successful_edit_response(serializer.data)

'''
______________________________________________________________________________________________      CompetencyThreshold
    CompetencyThreshold: Contains functionality for viewing and editing competency thresholds
______________________________________________________________________________________________
'''
class CompetencyThresholdViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly) ]
    renderer_classes = (JSONRenderer, )
    queryset = CompetencyThreshold.objects.all()
    serializer_class = CompetencyThresholdSerializer
    model = CompetencyThreshold

    '''
    __________________________________________________  get
     url: GET :: <WEBSITE>/api/courses/<COURSE_ID>/competency-threshold
     function: Retrieves competency thresholds for a single Course
    __________________________________________________
    '''
    def get(self, request, format=None, pk=None):
        if pk is not None:
            try:
                threshold = CompetencyThreshold.objects.filter(course__pk=pk)[0]
                serializer = self.serializer_class(threshold, many=False)
            except self.model.DoesNotExist:
                return object_not_found_response()
            except IndexError:
                return object_not_found_response()
        return successful_create_response(serializer.data)

    def post(self, request, format=None, pk=None):
        return object_not_found_response()

    def put(self, request, format=None, pk=None):
        return object_not_found_response()

    def delete(self, request, format=None, pk=None):
        return object_not_found_response()

'''
______________________________________________________________________________________________      GradeThreshold
    GradeThreshold: Contains functionality for viewing and editing grade thresholds
______________________________________________________________________________________________
'''
class GradeThresholdViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly) ]
    renderer_classes = (JSONRenderer, )
    queryset = GradeThreshold.objects.all()
    serializer_class = GradeThresholdSerializer
    model = GradeThreshold

    '''
    __________________________________________________  get
     url: GET :: <WEBSITE>/api/courses/<COURSE_ID>/competency-threshold
     function: Retrieves competency thresholds for a single Course
    __________________________________________________
    '''
    def get(self, request, format=None, pk=None):
        if pk is not None:
            try:
                threshold = GradeThreshold.objects.filter(course__pk=pk)[0]
                serializer = self.serializer_class(threshold, many=False)
            except self.model.DoesNotExist:
                return object_not_found_response()
            except IndexError:
                return object_not_found_response()
        return successful_create_response(serializer.data)

    def post(self, request, format=None, pk=None):
        return object_not_found_response()

    def put(self, request, format=None, pk=None):
        return object_not_found_response()

    def delete(self, request, format=None, pk=None):
        return object_not_found_response()
     

'''
______________________________________________________________________________________________      Student
    Student: Student in the course
______________________________________________________________________________________________
'''


class StudentViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly ) | CreateOnly]
    renderer_classes = (JSONRenderer, )
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    model = Student

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/students/
     function: Removes a given Student
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        return unauthorized_access_response()

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/students/?id_token=
     function: Signs a user in by checking if they exist in the DB
    __________________________________________________
    '''
    # If no pk is specified, get the current user. Otherwise, get the user specified by the pk
    def get(self, request, format=None, pk=None):

        # Update the id_token in the database of the current user
        auth_str = request.META.get('HTTP_AUTHORIZATION')
        token = get_bearer_token(auth_str)
        request.user.id_token = token
        request.user.save()

        #Get current user
        try:
            student = Student.objects.get(pk=request.user.pk)
        except:
            return user_not_found_response()

        #If pk is specified, get that user instead
        try:
            if pk is not None:
                student = Student.objects.get(pk=pk)
        except:
            return user_not_found_response()

        # Create student settings if they do not have any created for them (required to log in)
        try:
            Settings.objects.get(user=student)
        except:
            student_settings = Settings.objects.create(user=student,color='#FFFFFF')
            student_settings.save()

        serializer = self.serializer_class(student, many=False)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/students/
     function: Creates a given student if that student does not exist
     post data contains 'token' with id token
    __________________________________________________
    '''

    # This method changed a lot. Need to verify it works
    def post(self, request, format=None, pk=None):
        PROF_DEBUG_TOKEN = '12345'
        STUD_DEBUG_TOKEN = '54321'
        token = request.data.get('id_token')
        params = {'id_token': token }

        data = {}

        if API_DEBUG and token == PROF_DEBUG_TOKEN:
            # Set up the user's data
            data = {
                'first_name': 'Mark',
                'last_name': 'Floryan',
                'email': 'mrf8t@virginia.edu',
                'id_token': PROF_DEBUG_TOKEN,
                'is_professor': 't'
            }

        elif API_DEBUG and token == STUD_DEBUG_TOKEN:

            data = {
                'first_name': 'Jonny',
                'last_name': 'Studential',
                'email': 'js@virginia.edu',
                'id_token': STUD_DEBUG_TOKEN,
                'is_professor': 'f'
            }
        else:
            # Call out to google here to get profile info
            URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
            r = requests.post(url=URL, params=params)
            fullProfile = r.json()

            #print(fullProfile)

            # Setup user data for the new account based on google profile info
            data = {
                'first_name': fullProfile.get('given_name'),
                'last_name': fullProfile.get('family_name'),
                'email': fullProfile.get('email'),
                'id_token': params['id_token'],
                'is_professor': 'f',
                'username': fullProfile.get('email') # TODO: Temp username fix
            }
            print(data['username'])

        #If the id_token was bad and did not create a profile for us, return an error
        if data['email'] is None:
            return id_token_error_response()

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            if(serializer.errors['email'][0] == "user with this email already exists."):
                return colliding_id_response()

            return invalid_serializer_response(serializer.errors)

        # Create the profile for the account
        serializer.save()

        return successful_create_response(data)

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/students/<STUDENT_ID>
     function: Edits a given existing student
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return unauthorized_access_response()


'''
______________________________________________________________________________________________      Search
    Student List:
    GET :: <WEBSITE>/api/search/?query=<STUDENT|All>&page=<#>
    GET :: <WEBSITE>/api/search/?query=<STUDENT|All>&courseId=<COURSE_ID>&page=<#>
    GET :: <WEBSITE>/api/search/?query=<STUDENT|All>&courseId=<COURSE_ID>&page=<#>&invert=<1>
_________________________________________________________________________
'''

# This View Set retrieves all student objects from the database
# It then uses a filter based on first names, last names, and emails
# Next it takes the information and translates it to a json object
# Finally, it returns an HttpResponse of the json object
# This feature does not need a put, post, or delete operation that why 'pass' is there
# If we do not pass in a course Id, then get all students in all courses taught by a professor
# If we do pass in a course Id, then get all students in that course.
# If invert flag is set to 1, then instead of getting students in a course, get all students not in that course


class SearchViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & IsProfessor]
    renderer_classes = (JSONRenderer, )
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    model = Student

    def get(self, request, format=None, pk=None):
        is_many = True
        result = self.model.objects.all()

        student = request.user

        # Get courses professor teaches or get course by course id
        courseId = request.GET.get('courseId', None)
        invert = request.GET.get('invert', '0')
        # If we pass in a course Id, then get the course by that Id
        # By default, set the query to all courses. This is further filtered if we pass in a courseId
        course_query = Course.objects.all()
        if courseId != None:
            course_query = Course.objects.filter(
                id=courseId
            )

        searchQuery = request.GET.get('query', None)  # url decode
        # If we pass a specific student, find that student
        if searchQuery != "" and searchQuery != "All":
            url = urllib.parse.unquote(searchQuery)
            students = Student.objects.filter((Q(first_name=url) or Q(last_name=url)
                                                        or Q(email=url)))
        # If we do not specify or specify "All" then retrieve all students
        else:
            students = Student.objects.all()  # This will be filtered further below

        # Get page start and end
        page_start, page_end = get_page_indices(request.GET.get('page', None))

        # If we do not pass a courseId, then filter students among all courses
        if courseId == None:
            student_set = students
        # If we do pass a courseId, then filter students in that course
        else:
            if invert != '1':
                # Retrieve a page of students in query
                student_to_courses = StudentToCourse.objects.filter(
                    course_id__in=course_query,
                    student_id__in=students
                )[page_start:page_end]

                # Use student to course serializer here to include student grades
                serializer = StudentToCourseSlimSerializer(
                    student_to_courses, many=True)
                return successful_create_response(serializer.data)

            # If invert flag is set, then get all students who are not in the course; all students not in query
            else:
                # Retrieve students in query
                student_to_courses = StudentToCourse.objects.filter(
                    course_id__in=course_query,
                    student_id__in=students
                )
                # Converts StudentToCourse objects into Student objects (Quite slow with lots of students)
                # This contains all students in the specified query
                student_set = [s.student for s in student_to_courses]
                # Get a page of all other students not in the query
                student_set = students.exclude(
                    id__in=[s.id for s in student_set]
                ).filter(
                    # Ensure we get only students
                    is_staff=False,
                    is_professor=False,
                    is_superuser=False
                )[page_start:page_end]


        # Get page
        #student_set = student_set[page_start:page_end]

        # student_to_courses = student_to_courses.filter((Q(student_first_name=url) or Q(student_last_name=url) or Q(student_email=url)))


        # Serialize student objects
        serializer = StudentSerializer(
            student_set, many=True)
        return successful_create_response(serializer.data)

        # searchlist_json = serializers.serialize('json', searchlist)
        # return HttpResponse(searchlist_json, content_type='application/json')

    # Pass because not used

    def post(self, request, format=None, pk=None):
        return object_not_found_response()

    def put(self, request, format=None, pk=None):
        return object_not_found_response()

    def delete(self, request, format=None, pk=None):
        return object_not_found_response()


'''
______________________________________________________________________________________________      Topic
    Topic: Each node in the graph / course
        Contains functionality for viewing, creating, deleting, or editing a topic

______________________________________________________________________________________________
'''


class TopicViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly ) ]
    renderer_classes = (JSONRenderer, )
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    model = Topic

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/topics/
     function: Removes a given Topic
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/topics/ OR
          GET :: <WEBSITE>/api/topics/<TOPIC_ID> OR
          GET :: <WEBSITE>/api/topics/?courseId=<COURSE_ID> OR
     function: Retrieves all or a single topic related to a course (if given)
    __________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        if pk is None:

            course_id = request.GET.get('courseId', None)
            if course_id is not None:
                try:
                    course = Course.objects.get(pk=course_id)
                except Course.DoesNotExist:
                    return object_not_found_response()
                result = self.model.objects.filter(course=course)
            else:
                result = self.model.objects.all()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                is_many = False
            except self.model.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/topics/
     function: Creates a given topic
    __________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            data = json.loads(request.body)
            # If topics are not at the root but instead inside the topic key, use that instead
            if 'topics' in data:
                data = data['topics']
            for topic in data:
                serializer = self.serializer_class(data=topic)
                if not serializer.is_valid():
                    return invalid_serializer_response(serializer.errors)
                serializer.save()

                course = Course.objects.get(pk=topic["course"])
                newly_created_topic = Topic.objects.get(
                    name=topic["name"], course=course)

                students_in_course = StudentToCourse.objects.filter(
                    course=course)
                for student_to_course in students_in_course:
                    student = student_to_course.student
                    try:
                        student_to_topic = StudentToTopic.objects.get(
                            student=student, topic=newly_created_topic,)
                    except StudentToTopic.DoesNotExist:
                        student_to_topic = StudentToTopic(
                            course=course,
                            student=student,
                            topic=newly_created_topic,
                        )
                        student_to_topic.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/topics/<TOPIC_ID>
     function: Edits a given existing topic
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________      Topic to Topic
 TopicToTopic: Used in graph representation
    Contains functionality for viewing, creating, deleting, or editing a topic to topic relation
    (or an edge in the graph)
______________________________________________________________________________________________
'''


class TopicToTopicViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly )]
    renderer_classes = (JSONRenderer, )
    queryset = TopicToTopic.objects.all()
    serializer_class = TopicToTopicSerializer
    model = TopicToTopic

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/topic/topics/
     function: Removes a given Topic
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            if len(request.data) > 0:
                try:
                    for pk in request.data:
                        result = self.model.objects.get(pk=pk)
                        result.delete()
                except self.model.DoesNotExist:
                    return object_not_found_response()

                return successful_delete_response()
            else:
                return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/topic/topics/ OR
          GET :: <WEBSITE>/api/topic/topics/<TOPIC_ID> OR
     function: Retrieves all or a single Topic
    __________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        if pk is None:
            result = self.model.objects.all()
        else:
            result = self.model.objects.filter(topic_node=pk)
            is_many = True
        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/topic/topics/
     function: Creates a given Topic
    __________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            for topictotopic in request.data:
                serializer = self.serializer_class(data=topictotopic)

                if not serializer.is_valid():
                    return invalid_serializer_response(serializer.errors)

                try:
                    ancestor = Topic.objects.get(
                        pk=topictotopic["ancestor_node"])
                    topic = Topic.objects.get(pk=topictotopic["topic_node"])
                    TopicToTopic.objects.get(
                        topic_node=topic, ancestor_node=ancestor)
                    # return mal
                except TopicToTopic.DoesNotExist:
                    serializer.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/topic/topics/<TOPIC_ID>
     function: Edits a given existing Topic
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________      Student to Topic
    StudentToTopic: Going to be representing student grade for a topic
______________________________________________________________________________________________
'''


class StudentToTopicViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ( IsOwner & ReadOnly))]
    renderer_classes = (JSONRenderer, )
    queryset = StudentToTopic.objects.all()
    serializer_class = StudentToTopicSerializer
    model = StudentToTopic

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/students/topics
     function: Removes a given Student from a topic
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        studentToTopicId = request.GET.get('studentToTopicId', None)
        if studentToTopicId is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=studentToTopicId)
                self.check_object_permissions(self.request, result)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/student/topics/ OR
          GET :: <WEBSITE>/api/student/topics/<TOPIC_ID> OR
     function: Retrieves all related to a topic
          GET :: <WEBSITE>/api/student/topics/<COURSE_ID>/<STUDENT_ID> OR
     function: Retrieves all or a single topic related to a student
    __________________________________________________
    '''

    def get(self, request, format=None, course_id=None, student_id=None, topic_id = None):
        is_many = True
        is_search_query = False
        if course_id is None and student_id is None and topic_id is None:
            result = self.model.objects.all()
        elif student_id is None and course_id is None:
            try:
                query = request.GET.get('last_name_query',None) # Search by student last name
                is_search_query = True if query else False
                result = StudentToTopic.get_studentToTopics_of_topic(
                    self.model, topic_id = topic_id, query = query)
                # result = self.model.objects.get_topics()
                is_many = True
            except Student.DoesNotExist:
                return object_not_found_response()
            except Course.DoesNotExist:
                return object_not_found_response()
        else:
            try:
                result = StudentToTopic.get_topics(
                    self.model, course_id = course_id, student_id = student_id)
                # result = self.model.objects.get_topics()
                is_many = True
            except Student.DoesNotExist:
                return object_not_found_response()
            except Course.DoesNotExist:
                return object_not_found_response()
        self.check_object_permissions(self.request, result)
        if is_search_query:
            serializer = StudentToTopicSerializerMini(result, many=is_many) # Use mini serialzier to improve performance for search queries
        else:
            serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/student/topics/
     function: Creates a given topic for a student
    __________________________________________________
    '''

    def post(self, request, format=None, topic_id=None):
        student_id = request.data.get('student')
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return object_not_found_response()
        for studenttotopic in request.data.get('topics'):
            # student = Student.objects.get(pk=studenttotopic["student"])
            topic = Topic.objects.get(pk=studenttotopic["topic"])
            try:
                StudentToTopic.objects.get(student=student, topic=topic)
            except StudentToTopic.DoesNotExist:
                newstudenttotopic = StudentToTopic(
                    course=topic.course,
                    student=student,
                    topic=topic,
                    grade=0,
                )
                self.check_object_permissions(self.request, newstudenttotopic)
                newstudenttotopic.save()
            update_topic_grade(student.pk,topic.pk) # Cascade topic grade based on assignments in the topic
        return successful_create_response(request.data)

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/student/topics/<STUDENT_ID>
     function: Edits a given existing topic for a student
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        studentToTopicId = request.GET.get('studentToTopicId', None)
        if studentToTopicId is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=studentToTopicId)
            except self.model.DoesNotExist:
                return object_not_found_response()

            self.check_object_permissions(self.request, result)
            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________
    Quiz
______________________________________________________________________________________________
'''
class QuizViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly)]
    renderer_classes = (JSONRenderer, )
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    model = Quiz

    '''
      url: DELETE :: <WEBSITE>/api/quizzes/<quiz-id>
      function: Removes a given Quiz
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
      url: GET :: <WEBSITE>/api/quizzes/ OR
          GET :: <WEBSITE>/api/quizzes/<quiz_id> OR
      function: Retrieves all or a single quiz
    '''

    def get(self, request, format=None, pk=None):
        is_many = True

        if pk is None:
            topic_id = request.GET.get('topicId', None)
            if topic_id is not None:
                try:
                    topic = Topic.objects.get(pk=topic_id)
                    result = self.model.objects.get(assignment__topic=topic)
                    is_many = False
                except Quiz.DoesNotExist:
                    return object_not_found_response()
            else:
                #TODO What should the default response contain without topic id?
                result = self.model.objects.all()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                is_many = False
            except self.model.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
      url: POST :: <WEBSITE>/api/quizzes/
      function: Creates a new quiz
    '''
    def post(self, request, format=None, pk=None):
        if pk is None:
            data = json.loads(request.body)
            # If topics are not at the root but instead inside the topic key, use that instead
            if 'quizzes' in data:
                data = data['quizzes']

            for quiz in data:
                serializer = self.serializer_class(data=quiz)
                if not serializer.is_valid():
                    return invalid_serializer_response(serializer.errors)
                serializer.save()

                assignment = Assignment.objects.get(pk=quiz["assignment"])
                newly_created_quiz = Quiz.objects.get(
                    assignment=assignment,
                    pool=quiz["pool"],
                    practice_mode=quiz["practice_mode"],
                    next_open_date=quiz["next_open_date"],
                    next_close_date=quiz["next_close_date"]
                    )
                students_in_assignment = StudentToAssignment.objects.filter(
                    assignment=assignment)
                for student_to_assignment in students_in_assignment:
                    student = student_to_assignment.student
                    try:
                        student_to_quiz = StudentToQuiz.objects.get(
                            student=student, quiz=newly_created_quiz)
                    except StudentToTopic.DoesNotExist:
                        student_to_quiz = StudentToQuiz(
                            student=student,
                            quiz=newly_created_quiz,
                            student_to_assignment=student_to_assignment
                        )
                        student_to_quiz.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/quizzes/
      function: Edits a given quiz
    '''

    def put(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________
    QuizQuestion
______________________________________________________________________________________________
'''
class QuizQuestionViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly)]
    renderer_classes = (JSONRenderer, )
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    model = QuizQuestion

    '''
      url: DELETE :: <WEBSITE>/api/quiz-questions/<quiz-question-id>
      function: Removes a given Quiz
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
      url: GET :: <WEBSITE>/api/quiz-questions/ OR
          GET :: <WEBSITE>/api/quiz-questions/<quiz_question_id>
      function: Retrieves all or a single quiz
    '''

    def get(self, request, format=None, pk=None):
        is_many = True

        if pk is None:
            quiz_id = request.GET.get('quiz', None)
            if quiz_id is not None:
                try:
                    quiz = Quiz.objects.get(pk=quiz_id)
                    mode = request.GET.get('mode', None)
                    result = []
                    # When taking the real quiz, only get submittaable questions
                    if mode == 'regular':
                        result = QuizQuestion.get_submittable_questions(request.user, quiz)
                    # In practice mode, get the whole quiz pool for that quiz
                    elif mode == 'practice':
                        result = QuizQuestion.objects.filter(quiz=quiz)
                
                except QuizQuestion.DoesNotExist:
                    return object_not_found_response()
            else:
                #TODO What should the default response contain without topic id?
                result = self.model.objects.all()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                is_many = False
            except self.model.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
      url: POST :: <WEBSITE>/api/quiz-questions/
      function: Creates a new quiz question
    '''
    def post(self, request, format=None, pk=None):
        if pk is None:
            data = json.loads(request.body)
            # If topics are not at the root but instead inside the topic key, use that instead
            if 'quiz-questions' in data:
                data = data['quiz-questions']

            # Assignment becomes Quiz
            # Topic becomes Assignment
            for quiz_question in data:
                serializer = self.serializer_class(data=quiz_question)
                if not serializer.is_valid():
                    return invalid_serializer_response(serializer.errors)
                serializer.save()

                quiz = Quiz.objects.get(pk=quiz_question["quiz"])
                newly_created_quiz_question = QuizQuestion.objects.get(
                    quiz=quiz,
                    question_type=quiz_question["question_type"],
                    answered_correct_count=0,
                    answered_total_count=0,
                    question_parameters=quiz_question["question_parameters"]
                    )
                students_in_quiz = StudentToQuiz.objects.filter(quiz=quiz)
                for student_to_quiz in students_in_quiz:
                    student = student_to_quiz.student
                    try:
                        student_to_quiz_question = StudentToQuizQuestion.objects.get(
                            student=student, quiz_question=newly_created_quiz_question)
                    except StudentToQuizQuestion.DoesNotExist:
                        student_to_quiz_question = StudentToQuizQuestion(
                            student=student,
                            quiz_question=newly_created_quiz_question,
                            grade=0
                        )
                        student_to_quiz_question.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/quiz-questions/
      function: Edits a given quiz question
    '''

    def put(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)



class QuizInterfaceViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & IsOwner]
    renderer_classes = (JSONRenderer, )

    def delete(self, request,pk=None, format=None):
        return no_implementation_response()

    def get(self, request, pk=None, format=None):
        return no_implementation_response()

    '''
__________________________________________________  Post
    url: POST :: <WEBSITE>/api/quiz-interface/<pk>
    function: Submits a quiz question and returns whether or not it was correct, and the current quiz grade
    pk: The pk of the quiz question
__________________________________________________
    '''
    def post(self,request,pk=None, format=None):
        data = json.loads(request.body)
        quizPK = data['quizPK']
        assignmentPK = data['assignmentPK']
        response_data = {}

        quiz = Quiz.objects.get(pk=quizPK)

        # Make sure the user is submitting for their own quiz and not for another student's quiz
        try:
            quiz = Quiz.objects.get(pk=quizPK)
            student_to_quiz = StudentToQuiz.objects.get(quiz=quiz, student=request.user)
            student_to_assignment = student_to_quiz.student_to_assignment
            self.check_object_permissions(request,student_to_quiz)
        except Exception as e:
            quiz = Quiz.objects.get(pk=quizPK)
            assignment = Assignment.objects.get(pk=assignmentPK)
            # If taking the real quiz, check if student_to_assignment exists and create on if it doesn't
            if not data['practice_mode']:
                try:
                    student_to_assignment = StudentToAssignment.objects.get(student=request.user, assignment=assignment)
                except:
                    student_to_assignment = StudentToAssignment.objects.create(student=request.user, assignment=assignment)
                student_to_quiz = StudentToQuiz.objects.create(quiz=quiz, student=request.user, student_to_assignment=student_to_assignment)

        # If the quiz is not open, return a message letting the user know
        # For practice mode, allow submissions at any time
        if data['practice_mode']:
            pass
        elif not quiz.is_open():
            response_data['info'] = "This quiz is not accepting submissions at this time"
            return forbidden_response(response_data)

        # Get quiz question
        quiz_question = QuizQuestion.objects.get(pk=pk)

        # Return if the user is attemping to submit a question that they are not allowed to submit
        # This code prevents someone from resending the same HTTP Post request with a correct answer and artifically boosting their score
        # Students instead must answer all the questions in the quiz pool before being allowed to try answering the same question again
        # For practice mode, allow submitting any question
        if data['practice_mode']:
            pass
        elif quiz_question.pk not in QuizQuestion.get_submittable_questions(request.user, quiz).values_list('id', flat=True):
            response_data['info'] = "Submitting this question is forbidden"
            return forbidden_response(response_data)


        # Check if the answer was correct
        question_parameters = json.loads(quiz_question.question_parameters)
        question_type = quiz_question.question_type
        is_correct = False
        # Multiple choice question
        if question_type == 0:
            is_correct = (data['selection'] == question_parameters['answer'])
            submitted_answer = data['selection']
        # Select all question
        elif question_type == 2:
            submitted_answer = data['all_selections']
            submitted_answer.sort()
            correct_answer = question_parameters['answer']
            correct_answer.sort()
            is_correct = (submitted_answer == correct_answer)
        # Parsons problem
        elif question_type == 3:
            is_correct = True
            submitted_answer = data['code_order']
            dependencies = question_parameters['answer']
            
            # Get list of lines that are expected to be present
            # (Prevents partially correct answers)
            expected_lines_dict = {}
            expected_lines = []
            for line in dependencies:
                for index in line:
                    if index not in expected_lines_dict:
                        expected_lines_dict[index] = True
                        expected_lines.append(index)

            # Checks dependency list and makes sure lines are in correct order
            previous_lines = {}
            code_order = []
            for line in submitted_answer:
                line_id = line['id']
                code_order.append(line_id)
                if line_id < 0:
                    continue
                for predecessor in dependencies[line_id]:
                    if predecessor not in previous_lines:
                        is_correct = False
                        break
                previous_lines[line_id] = True

            # Compare lines submitted to lines expected
            for line in expected_lines:
                if line not in previous_lines:
                    is_correct = False
                    break
            
            # Set submitted_answer to code order so that the code_order is saved in the StudentToQuizQuestion as the submitted answer
            submitted_answer = code_order

        response_data["correct"] = is_correct

        # If practice mode, return now and don't actually update their grade
        if data['practice_mode']:
            return successful_submission_response(response_data)

        # Fetch previous grade value, update using Carrington's metric, and then store.
        prev_grade = student_to_quiz.grade
        new_grade = getScore(is_correct, prev_grade)
        student_to_quiz.grade = new_grade
        student_to_quiz.save()

        # Update grade of associated student_to_assignment
        student_to_assignment.grade = round(new_grade*100)
        student_to_assignment.save()

        # Update quiz grade
        response_data["currentQuizGrade"] = new_grade

        try:
            student_to_qq = StudentToQuizQuestion.objects.get(student=request.user,quiz_question=quiz_question)
            student_to_qq.correct = is_correct
            student_to_qq.submitted_answer = submitted_answer
            student_to_qq.num_submissions = student_to_qq.num_submissions + 1
            student_to_qq.save()
        except ObjectDoesNotExist: # Create if DNE
            StudentToQuizQuestion(student=request.user,quiz_question=quiz_question,correct=is_correct,submitted_answer=submitted_answer).save()
        except MultipleObjectsReturned: # Delete them all then create one
            Student.objects.filter(student=request.user, quiz_question=quiz_question).delete()
            StudentToQuizQuestion(student=request.user,quiz_question=quiz_question,correct=is_correct,submitted_answer=submitted_answer).save()

        return successful_submission_response(response_data)

    def put(self, request, pk=None, format=None):
        return no_implementation_response()
'''
______________________________________________________________________________________________      ResourcesViewSet
ResourcesViewSet
______________________________________________________________________________________________
'''


class ResourcesViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly )]
    renderer_classes = (JSONRenderer, )
    queryset = Resources.objects.all()
    serializer_class = ResourcesSerializer
    model = Resources

    '''
      url: DELETE :: <WEBSITE>/api/resources/
      function: Removes a given resource
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
      url: GET :: <WEBSITE>/api/resources/ OR
          GET :: <WEBSITE>/api/resources/<RESOURCE_ID> OR
      function: Retrieves all or a single resource
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        if pk is None:
            result = self.model.objects.all()
        else:
            try:
                topic = Topic.objects.get(pk=pk)
                result = self.model.objects.filter(topic=topic)
                is_many = True
            except Topic.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    url: POST :: <WEBSITE>/api/resources/
    function: Creates a given resource
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
    url: PUT :: <WEBSITE>/api/resources/<RESOURCE_ID>
    function: Edits a given existing resource
    '''

    def put(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________      SettingsViewModel
 SettingsViewModel:
______________________________________________________________________________________________
'''


class SettingsViewModel(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | IsOwner )]
    renderer_classes = (JSONRenderer, )
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    model = Settings

    '''
      url: DELETE :: <WEBSITE>/api/settings/
      function: Removes a given setting
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                student = Student.objects.get(pk=pk)
                result = self.model.objects.get(user=student)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
      url: GET :: <WEBSITE>/api/settings/ OR
            GET :: <WEBSITE>/api/settings/<SETTING_ID> OR
      function: Retrieves all or a single settings
    '''

    def get(self, request, format=None, pk=None):
        result = Settings.objects.get(user=request.user)
        is_many = False

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
      url: POST :: <WEBSITE>/api/settings/
      function: Creates a given setting
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            settings = Settings(
                color='#FFFFFF',
                user=request.user
            )
            try:
                settings.save()
            except IntegrityError:
                return conflict_response('A settings object already exists for the specified user')
            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/settings/<SETTING_ID>
      function: Edits a given existing setting
    '''

    def put(self, request, format=None, pk=None):
        try:
            student = request.user
            students_settings = self.model.objects.get(user=student)
            result = self.model.objects.filter(user=student)
            colors = request.data.get("colors")
            result.update(
                color=colors["hex"],
                nickname=request.data.get("nickname")
            )
        except self.model.DoesNotExist:
            return object_not_found_response()

        return successful_edit_response(request.data)




'''
______________________________________________________________________________________________      StudentToCourseViewSet
StudentToCourseViewSet: This shows the course that a student is taking and shows the topics
        in a graph.
______________________________________________________________________________________________
'''


class StudentToCourseViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ( IsOwner & ReadOnly) )]
    renderer_classes = (JSONRenderer, )
    queryset = StudentToCourse.objects.all()
    serializer_class = StudentToCourseSerializer
    model = StudentToCourse

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/student/course/?courseId=<STUDENT_TO_COURSE_ID>
     function: Removes a given student to topic relationship
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                courseId = request.GET.get('courseId', None)
                course = Course.objects.get(pk=courseId)
                student = Student.objects.get(pk=pk)
                result = self.model.objects.get(
                    student=student,
                    course=course
                )
                self.check_object_permissions(self.request,result)
                result.delete()

                # Delete the associated student to topic
                topics = StudentToTopic.objects.filter(student=student, course=course)
                topics.delete()

            except self.model.DoesNotExist:
                return object_not_found_response()
            except Course.DoesNotExist:
                return object_not_found_response()
            except Student.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/student/course/ OR
          GET :: <WEBSITE>/api/student/course/<STUDENT_ID> OR
          GET :: <WEBSITE>/api/student/course/?courseId=<COURSE_ID> OR
     function: Retrieves all or a single student course relationship
     courseId
     id_token => student_id
     view_as

     1) get user id
     2) get course
     3) if view_as, check if they're allowed to be here
     4) update class_grades
     5) get studentToTopics using course and student
    __________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        if pk is None:

            course_id = request.GET.get('courseId', None)
            # pk of student professor is trying to view
            view_as = request.GET.get('view_as', None)
            # if course_id and id_token, get detailed info about student's course enrollment
            if course_id is not None:
                try:

                    student = request.user

                    course = Course.objects.get(pk=course_id)

                    # If a professor is trying to view one of their students' grades for a course
                    if view_as is not None and view_as.isdigit():
                        try:
                            student = Student.objects.get(pk=view_as)
                        except Student.DoesNotExist:
                            return object_not_found_response()

                    student_to_course = StudentToCourse.objects.get(
                        course=course, student=student)
                    serializer = ClassGraphSerializer(
                        student_to_course, many=False)
                    self.check_object_permissions(self.request, student_to_course)
                    return successful_create_response(serializer.data)

                except Course.DoesNotExist:
                    return object_not_found_response()
                except Student.DoesNotExist:
                    return object_not_found_response()
                except StudentToCourse.DoesNotExist:
                    return object_not_found_response()
            else:

                student = request.user
                result = self.model.objects.filter(
                    student=student
                )
                is_many = True

        else:
            try:
                student = Student.objects.get(pk=pk)
                result = StudentToCourse.objects.filter(student=student)
                is_many = True
            except Student.DoesNotExist:
                return object_not_found_response()
        self.check_object_permissions(self.request, result)
        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/student/course/
     function: Creates a given student course relationship (ie enrolls them in that class)
    __________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            data = request.data
            fields = ["course", "student"]
            missing_fields = {}
            for field in fields:
                if field not in data:
                    # Mocks drf serializer error
                    missing_fields[field] = ["This field is required."]

            if len(missing_fields.keys()) > 0:
                return malformed_request_response(fields=missing_fields)

            # Once we know they exist, extract them to vars
            course_id = data["course"]

            course = None
            student = None

            # Try to access the foreign key necessary for the model
            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                return object_not_found_response()

            student_id = data["student"]
            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return object_not_found_response()

            studentToCourse = StudentToCourse.objects.filter(
                course=course,
                student=student
            )

            if len(studentToCourse) > 0:
                return colliding_id_response()
            '''serializer = self.serializer_class(data={'course':course_id,'student':student_id})
            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()'''



            studentToCourse = StudentToCourse(
                course=course,
                student=student
            )
            # Save the student to course relationship
            studentToCourse.save()

            return successful_create_response(request.data)

        else:
            return colliding_id_response()

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/student/course/<STUDENT_ID>
     function: Edits a given student course relationship
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                self.check_object_permissions(self.request, result)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():  # pragma: no cover This serializer is always valid, but serializer requires is_valid to be called to save()
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)

'''
______________________________________________________________________________________________
CourseRosterUpload: Functionality for uploading a file with existing grades
______________________________________________________________________________________________
'''


class CourseRosterUpload(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & IsProfessor]
    renderer_classes = (JSONRenderer, )
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    model = Student

    '''
    __________________________________________________  Delete
     url: DELETE :: NO FUNCTIONALITY
    __________________________________________________
    '''

    def delete(self, request, format=None, coursePk=None):
        return no_implementation_response()

    '''
    __________________________________________________  Get
     url: GET :: NO FUNCTIONALITY
    __________________________________________________
    '''

    def get(self, request, format=None, coursePk=None):
        return no_implementation_response()

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/student/course/
     function: Creates a given student course relationship (ie enrolls them in that class)
    __________________________________________________
    '''

    def post(self, request, format=None, coursePk=None):
        prof = request.user

        #Make sure this is the prof of the given course
        try:
            course = Course.objects.get(pk=coursePk, professor_id=prof.pk)
        except Course.DoesNotExist:
            return object_not_found_response()


        #grab the file
        file = request.FILES['file']
        if file is None:
            print("File is NONE")
            return object_not_found_response()

        emails = []

        #start parsing the file
        file_data = file.read().decode("utf-8-sig").splitlines()
        reader = csv.DictReader(file_data)

        students = []

        #loop over the lines and save them in db. If error , store as string and then display
        for line in reader:
            #print(line)

            #for now, assuming this is in order
            email = line[ 'email' ]
            first = line[ 'firstname' ]
            last = line[ 'lastname' ]
            username = line[ 'username' ]

            emails.append(email)


            #make the student object
            student = Student(email=email, first_name=first, last_name=last, username=username, id_token="", is_professor='f')
            students.append(student)
        
        Student.objects.bulk_create(students, ignore_conflicts=True)

        #Students are created, let's make the student course pairs
        students = Student.objects.filter(email__in=emails)

        stcObjects = StudentToCourse.objects.filter(course=course)

        stcList = []
        for student in students:
            stc = StudentToCourse(course=course, student=student, semester='')
            #check to make sure that the students aren't already in the course
            sentinel = True
            for courseObject in stcObjects:
                if(courseObject.student.email == stc.student.email):
                    sentinel = False
            #for new students, first enroll them in all the topics for the course
            if(sentinel):
                topics = Topic.objects.filter(course=course)
                student = stc.student
                for topic in topics:
                    try:
                        student_to_topic = StudentToTopic.objects.get(
                            student=student, topic=topic,)
                    except StudentToTopic.DoesNotExist:
                        student_to_topic = StudentToTopic(
                            course=course,
                            student=student,
                            topic=topic,
                        )
                        student_to_topic.save()
                stcList.append(stc)

        StudentToCourse.objects.bulk_create(stcList, ignore_conflicts=False)


        return JsonResponse({
            'ok': True
        })

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/student/course/<STUDENT_ID>
     function: Edits a given student course relationship
    __________________________________________________
    '''

    def put(self, request, format=None, coursePk=None):
        return no_implementation_response()


'''
______________________________________________________________________________________________
 CourseTopicToStudentViewSet : Gets students and their assignment grades associated with a given course and topic
 (just the student unless user is the professor)
______________________________________________________________________________________________
'''
class CourseTopicToStudentViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [ IsAuthenticated & ( IsProfessor | ReadOnly) ]
    renderer_classes = (JSONRenderer, )
    queryset = StudentToTopic.objects.all()
    serializer_class = StudentToTopicSerializer
    model = StudentToTopic

    '''
    _______________________________________________________ Delete
     <WEBSITE>/api/coursetopictostudent/
    _______________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Get
     <WEBSITE>/api/coursetopictostudent/course_pk/topic_pk/
    _______________________________________________________
    '''

    def get(self, request, format=None, course_pk=None, topic_pk=None):
        user_pk = request.user.pk

        page_start, page_end = get_page_indices(request.GET.get('page', None))

        # Get the course
        try:
            course = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            return object_not_found_response()

        # See if this user is the professor of the course
        is_prof = True
        try:
            Course.objects.get(pk=course_pk, professor_id=user_pk)
        except:
            is_prof = False

        # Get student to assignments for the current page
        assignments = Assignment.objects.filter(topic=topic_pk)
        student_to_assignments = None

        if is_prof:
            student_to_assignments = StudentToAssignment.objects.filter(assignment__topic=topic_pk).order_by('student')[page_start:page_end]
        else:
            student_to_assignments = StudentToAssignment.objects.filter(student=user_pk, assignment__topic=topic_pk).order_by('student')[page_start:page_end]

        # Get student topic competencies for students that are in the student_to_assignment set
        student_to_topics = StudentToTopic.objects.filter(topic__topic_assignment__assignment__id__in=student_to_assignments.values_list('id', flat=True)).distinct()

        students = defaultdict(list) # Defaultdict is used here so we can append to an array inside a dictionary
        response = []

        # Construct dictionary of primary keys mapping to students and their assignment grades
        for sta in student_to_assignments:
            if sta.student.pk not in students:
                students[sta.student.pk] = {"name": sta.student.get_name(), "assignments": []}
            students[sta.student.pk]["assignments"].append({"name": sta.assignment.name, "grade": sta.grade})

        # Convert dictionary to a list of students and their grades
        for pk in students:
            student = students[pk]
            try:
                competency = student_to_topics.get(student_id=pk).get_competency_str()
                response.append({"name": student['name'], "pk": pk, "competency": competency, "assignments": student['assignments']})
            except StudentToTopic.DoesNotExist:
                pass # pass if the student is not associated with the topic (likely becuase a student was un-enrolled from a course)

        # Return list of students and their grades for each assignment
        return HttpResponse(json.dumps(response, indent=4), content_type='application/json')


    '''
    _______________________________________________________ Post
     <WEBSITE>/api/coursetopictostudent/
    _______________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Put
     <WEBSITE>/api/coursetopictostudent/
    _______________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


'''
______________________________________________________________________________________________
 CourseGradesUpload : Bulk upload grades in csv format
______________________________________________________________________________________________
'''

'''
__________________________________________________  Post
    url: POST :: <WEBSITE>/api/courseGradesUpload/
    function: Uploads grades through a bulk csv upload
__________________________________________________
'''
@csrf_exempt
@api_view(['POST'])
@authentication_classes([GoogleOAuth])
@permission_classes([IsAuthenticated & IsProfessor])
def courseGradesUpload(request,pk):
    try:
        csv_file = request.FILES['csv']
    except MultiValueDictKeyError:
        return malformed_request_response(fields={'csv': "No csv found in request"})

    #estimates show that we don't need to use chunks -- may need to revise this assumption if used for files > ~2.5mb.
    csv_content_raw = csv_file.read().decode('utf-8')

    #print(csv_content_raw)

    #parse into individual lines.
    csv_lines = csv_content_raw.split('\n')

    #grab first row (with column names) and split into columns.
    #columns 1-n of this are the names of assignments.
    header_elements = csv_lines[0].split(',')

    course = None

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({
            'ok':False,
            'errors':['Could not find course with primary key {}'.format(pk)]
        })

    errors = []
    #operate on each non-header row
    for i in range(1, len(csv_lines)):
        #split this row into columns.
        #column 0 is student computing id, k \in 1-n is grade for assignment k.
        tokens = csv_lines[i].split(',')
        if len(tokens) < 2:
            continue
        row_username = tokens[0]
        try:
            student = Student.objects.get(username=row_username)
            #operate on each non-student column
            for k in range(1, len(tokens)):
                try:
                    #get the associated assignment
                    if '\r' in header_elements[k]:
                        header_elements[k] = header_elements[k].strip("\r")
                    assignment = Assignment.objects.get(name=header_elements[k], topic__course = course)
                    grade = tokens[k]

                    #record grade:
                    try: # If grade exists, update it
                        existing_grade = StudentToAssignment.objects.get(student=student, assignment=assignment)
                        existing_grade.grade = grade
                        existing_grade.save()
                    except: # If grade does not exist, create it
                        StudentToAssignment(student=student, assignment=assignment, grade=grade).save()
                except Assignment.DoesNotExist:
                    errors.append('Could not find assignment with name {}.'.format(header_elements[k]))
        except Student.DoesNotExist:
            errors.append('Could not find student with username {}.'.format(row_username))

    if len(errors) == 0:
        return JsonResponse({
            'ok': True
        })
    else:
        #print(str(errors))
        return JsonResponse({
            'ok': False,
            'errors': errors
        })

'''
__________________________________________________  Get
    url: GET :: <WEBSITE>/api/courseGradescopeUpload/
    function: Fetches corresponding GradeScope data and uploads it
__________________________________________________
'''
@csrf_exempt
@api_view(['GET'])
@authentication_classes([GoogleOAuth])
@permission_classes([IsAuthenticated])
def courseGradescopeUpload(request,pk):

    course = None
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({
            'ok':False,
            'errors':['Could not find course with primary key {}'.format(pk)]
        })

    conn = GSConnection()
    #conn.login('email', 'pass')

    print(conn.state)
    conn.get_account()

    grades = None
    for cnum in conn.account.instructor_courses:
        gs_course = conn.account.instructor_courses[cnum]

        if gs_course.name != course.name:
            shortname = course.subject_code + ' ' + course.course_code
            if gs_course.shortname != shortname:
                continue

        print('Grabbing grades from: ' + str(gs_course))
        gs_course._force_load_data()
        grades = gs_course.get_grades()

    if grades is None:
        return JsonResponse({
            'ok': False,
            'errors':['Could not get grade data from course: '.format(course.name)]
        })

    ## Make post request with new csv
    # TODO: hardcoded url
    url = 'http://localhost:8000/api/courseGradesUpload/' + pk
    
    with open('gradescopeUpload.csv','w+') as f:
        f.write(grades)
        f.flush()
        f.seek(0)
        headers = {'Authorization' : request.headers['Authorization']}
        r = requests.post(url, headers=headers, files = {'csv': ('grades.csv', f, 'text/csv', {'Expires': '0'})})
    return JsonResponse({
        'ok': r.text
    })


#Assignment uploading feature
#/api/courseAssignmentUpload/<pk>
@csrf_exempt
@api_view(['POST'])
@authentication_classes([GoogleOAuth])
@permission_classes([IsAuthenticated & IsProfessor])
def assignmentUpload(request,pk):
    try:

        csv_file = request.FILES['csv']
    except MultiValueDictKeyError:
        return malformed_request_response(fields={'csv': "No csv found in request"})

    #estimates show that we don't need to use chunks -- may need to revise this assumption if used for files > ~2.5mb.
    csv_content_raw = csv_file.read().decode('utf-8')

    #print(csv_content_raw)

    #parse into individual lines.
    csv_lines = csv_content_raw.split('\n')

    #grab first row (with column names) and split into columns.
    #Assignment names are in the first column,
    #Topic name in the second
    header_elements = csv_lines[0].split(',')
    course = None

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({
            'ok':False,
            'errors':['Could not find course with primary key {}'.format(pk)]
        })

    errors = []
    #operate on each non-header row
    for i in range(1, len(csv_lines)):
        #split this row into columns.
        #column 0 is student computing id, k \in 1-n is grade for assignment k.
        tokens = csv_lines[i].split(',')
        if len(tokens) < 2:
            continue
        #grab the name of the assignment and the topic it is attached to
        assignment_name = tokens[0]
        topic_name = tokens[1]
        if '\r' in topic_name:
            topic_name = topic_name.strip("\r")
        try:
            topic = Topic.objects.get(name=topic_name, course=course)
            try:
                assignment_exists = Assignment.objects.get(name=assignment_name, topic = topic)
                assignment = assignment_exists
            except Assignment.DoesNotExist:

                assignment = Assignment(topic=topic,name=assignment_name)
                assignment.save()
        except:
            errors.append("Topic with name " + topic_name + " does not exist")
    if len(errors) == 0:
        return JsonResponse({
            'ok': True
        })
    else:
        print(str(errors))
        return JsonResponse({
            'ok': False,
            'errors': errors
        })
'''
ASSIGNMENT
______________________________________________________________________________________________
    Assignment
        Contains functionality for viewing, creating, deleting, and editing an assignment
______________________________________________________________________________________________
'''

class AssignmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [IsAuthenticated & ( IsProfessor | ReadOnly ) ]
    renderer_classes = (JSONRenderer, )
    queryset = Topic.objects.all()
    serializer_class = AssignmentSerializer
    model = Assignment

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/assignments/<ASSIGNMENT_ID>
     function: Removes a given assignment
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/assignments/ OR
          GET :: <WEBSITE>/api/assignments/<ASSIGNMENT_ID> OR
          GET :: <WEBSITE>/api/assignments/?topicId=<TOPIC_ID> OR
     function: Retrieves all or a single assignment related to a course (if given)
    __________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        is_many = True

        if pk is None:
            topic_id = request.GET.get('topicId', None)
            course_id = request.GET.get('courseId', None)
            if topic_id is not None:
                try:
                    topic = Topic.objects.get(pk=topic_id)
                except Topic.DoesNotExist:
                    return object_not_found_response()
                result = self.model.objects.filter(topic=topic)
            elif course_id is not None:
                try:
                    course = Course.objects.get(pk=course_id)
                except Course.DoesNotExist:
                    return object_not_found_response()
                result = self.model.objects.filter(topic__course=course)
            else:
                result = self.model.objects.all()
        else:
            try:
                result = self.model.objects.get(pk=pk)
                is_many = False
            except self.model.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/assigments/
     function: Creates a given assignment
    __________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            data = json.loads(request.body)
            # If topics are not at the root but instead inside the topic key, use that instead
            if 'assignments' in data:
                data = data['assignments']

            # Topic becomes Assignment
            # Course becomes Topic
            for assignment in data:
                serializer = self.serializer_class(data=assignment)
                if not serializer.is_valid():
                    return invalid_serializer_response(serializer.errors)
                serializer.save()

                topic = Topic.objects.get(pk=assignment["topic"])
                newly_created_assignment = Assignment.objects.get(
                    name=assignment["name"], topic=topic)
                students_in_topic = StudentToTopic.objects.filter(
                    topic=topic)
                for student_to_topic in students_in_topic:
                    student = student_to_topic.student
                    try:
                        student_to_assignment = StudentToAssignment.objects.get(
                            student=student, assignment=newly_created_assignment,)
                    except StudentToTopic.DoesNotExist:
                        student_to_assignment = StudentToAssignment(
                            topic=topic,
                            student=student,
                            assignment=newly_created_assignment,
                        )
                        student_to_topic.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/assignments/<ASSIGNMENT_ID>
     function: Edits a given existing assignment
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        if pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________
    StudentToAssignment
        Contains basic restAPI CRUD functionality and custom functionality for deleting a
        StudentToAssignment
______________________________________________________________________________________________
'''
class StudentToAssignmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [GoogleOAuth]
    permission_classes = [ IsAuthenticated & ( IsProfessor | ReadOnly)]

    serializer_class = StudentToAssignmentSerializer
    model = StudentToAssignment

    
    def get_queryset(self):
        queryset = StudentToAssignment.objects.all()
        if self.request.user.is_professor == True: # If professor, provide acess to all grades.
            return queryset
        else:
            queryset = queryset.filter(student=self.request.user)  # If a student, limit access to their own grades
        return queryset

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>api/studenttoassignments/<STUDENT_PK>/<ASSIGNMENT_PK>
     function: Removes studentToAssignment for a given student and assignment if
     it exists; returns DoesNotExist otherwise
    __________________________________________________
    '''

    def delete(self, request, format=None, studentpk=None, assignmentpk=None):
        if studentpk is None or assignmentpk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(student=studentpk, assignment=assignmentpk)
                result.delete()
                return successful_delete_response()
            except self.model.DoesNotExist:
                return object_not_found_response()


#Quiz Question uploading feature
#/api/assignmentQuizUpload/<pk>
@csrf_exempt
@api_view(['POST'])
@authentication_classes([GoogleOAuth])
@permission_classes([IsAuthenticated & IsProfessor])
def assignmentQuizUpload(request,pk):
    try:

        csv_file = request.FILES['csv']
    except MultiValueDictKeyError:
        return malformed_request_response(fields={'csv': "No csv found in request"})
    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return malformed_request_response(fields={
            'ok':False,
            'error':'Could not find assignment with primary key {}'.format(pk)
        })

    # Define question types
    question_types = ["0","1","2","3"] # Corresponding to multiple choice, free response, select all that apply, and parsons problems

    #estimates show that we don't need to use chunks -- may need to revise this assumption if used for files > ~2.5mb.
    csv_content_raw = csv_file.read().decode('utf-8')

    #print(csv_content_raw)

    #parse into individual lines.
    csv_lines = csv_content_raw.split('\n')

    #grab first row (with column names) and split into columns.
    #Header elements: # of multiple choice | # of free response | # of select all that apply | # of parsons problems
    if '\r' in csv_lines[0]:
        csv_lines[0]=csv_lines[0].strip('\r')
    header_elements = csv_lines[0].split(',')
    multiple_choice_count = int(header_elements[0])
    free_response_count = int(header_elements[1])
    select_all_that_apply_count = int(header_elements[2])
    parsons_problem_count = int(header_elements[3])
    question_type_count = dict({"parsons": parsons_problem_count,
                                "multiple_choice": multiple_choice_count,
                                "select_all": select_all_that_apply_count,
                                "free_response": free_response_count})

    #if the quiz already exists, delete the old one and create this new one.
    try:
        quiz = Quiz.objects.get(assignment=assignment)
        questions_old = QuizQuestion.objects.filter(quiz=quiz)
        for i in questions_old:
            i.delete()
    except Quiz.DoesNotExist:
        try:
            quiz = Quiz(assignment=assignment, pool=json.dumps(question_type_count))
            quiz.save()
        except:
            return malformed_request_response(fields={
                'ok':False,
                'errors':"Headers not in correct formation."
            })
    errors = []

    # Operate through each quiz question, which is defined by 2 rows.
    for i in range(1, len(csv_lines), 2):
        # The first row of contains quiz type followed by the answer indicies. (Ex: 0,3) where 0 indicates mutltiple choice and 3 indicates the answer
        # The second row contains the question followed by the answer choices(Ex: What is the answer?,A,B,C,D)
        tokens = csv_lines[i].split(',')
        if len(tokens) < 2:
            continue

        try:
            # Operate on the first row of the question definiton
            question_type = tokens[0]
            if question_type not in question_types:
                errors.append("Invalid question type. Must be one of the following: 0,1,2,3")
            answer_pool = []
            # Iterate through the following tokens, skipping the first one
            for option in tokens[1:]:
                # Strip carriage returns
                if '\r' in option:
                    option = option.strip("\r")
                # Check if multiple choice or select_all
                if question_type == "0" or question_type == "2":
                    answer_pool.append(int(option)) # Add answer to pool as integer
                else:
                    answer_pool.append(option) # Add answer to pool as string
            # Verify answer(s) exists
            if len(answer_pool)==0:
                errors.append("No answer specified. Please include the answer(s) after the question type")
            # For mutliple choice questions, the answer becomes the single index instead of an array
            if question_type=="0":
                answer_pool=answer_pool[0]

            # Operate on the second row of the question
            # Use regex to escape commas with a backslash
            tokens_row_2 = [each.replace("\,",",") for each in re.split(r'(?<!\\),', csv_lines[i+1])]
            quiz_question = tokens_row_2[0]
            option_pool = []
            # Iterate through the following tokens, skipping the first one
            for option in tokens_row_2[1:]:
                # Strip carriage returns
                if '\r' in option:
                    option = option.strip("\r")
                option_pool.append(option) # Add answer to pool

            # Define the question_params
            question_parameters = dict({
            "question": quiz_question,
            "choices": option_pool,
            "answer": answer_pool
            })

            #For parsons problems, need some additional parsing.
            if question_type=="3":
                #first token is a space-separated list of fixed lines
                #i.e. if lines 0, 4, and 9 are fixed, then the token is "0 4 9"
                #parse into an array of values (empty array if empty string)
                fixed_list = [] if answer_pool[0] == "" else list(map(lambda k: int(k), answer_pool[0].split(" ")))
                answer_pool = answer_pool[1:]

                #each answer is also a space-separated array of indices, we need to parse this into a proper array.
                try:
                    parsed_answer_pool = list(map(lambda l: [] if l == "" else list(map(lambda k: int(k), l.split(" "))), answer_pool))
                except ValueError:
                    errors.append('Invalid space surrounding a parsons answer pool. (e.g. "1 2 " instead of "1 2")')
                    return JsonResponse({
                        'ok': False,
                        'errors': errors
                    })
                #generate an array of true/false values for each line, based on whether that line is fixed.
                fixed_array = [(i in fixed_list) for i in range(0, len(answer_pool))]

                #also need to strip one token out of the option_pool, as one cell is left empty for spacing.
                option_pool = option_pool[1:]
                question_parameters = dict({
                "question": quiz_question,
                "choices": option_pool,
                "answer": parsed_answer_pool,
                "fixed": fixed_array
                })

            # Create and save quiz
            if len(errors) == 0:
                qq = QuizQuestion(quiz=quiz,question_type=int(question_type),question_parameters=json.dumps(question_parameters))
                qq.save()
            else:
                print(errors)
        except Exception as e:
            print(e)
            errors.append(e.__class__.__name__)
            return JsonResponse({
                'ok': False,
                'errors': errors
            })
    if len(errors) == 0:
        return JsonResponse({
            'ok': True
        })
    else:
        print(str(errors))
        return JsonResponse({
            'ok': False,
            'errors': errors
        })
