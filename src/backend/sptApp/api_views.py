# First external includes
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse

# Making calls to google (get and post)
import requests
from sptApp import views
# For reading API
import ast
import json
import urllib.request
# decode urls
import urllib.parse

# Then internal
from .models import (
    Course,
    ExternalSite,
    ExternalSiteToCourse,
    ExternalSiteToGrade,
    Quiz,
    QuizQuestion,
    QuizQuestionAnswer,
    Resources,
    Student,
    Settings,
    StudentToCourse,
    StudentToQuiz,
    StudentToQuizQuestion,
    StudentToTopic,
    Topic,
    TopicToTopic,
    Grade,
    Category,
    TopicToCategory,
    User,
)
from .responses import *
from .external import *
from .exampleExternalJSON import *
from django.contrib.auth import login
from .serializers import (
    CourseSerializer,
    # External Sites
    ExternalSiteSerializer,
    ExternalSiteToCourseSerializer,
    ExternalSiteToGradeSerializer,
    QuizSerializer,
    QuizQuestionSerializer,
    QuizQuestionAnswerSerializer,
    ResourcesSerializer,
    StudentSerializer,
    StudentToCourseSerializer,
    StudentToQuizSerializer,
    SettingsSerializer,
    TopicSerializer,
    StudentToTopicSerializer,
    TopicToTopicSerializer,
    GradeSerializer,
    CategorySerializer,
    TopicToCategorySerializer,
    ClassGraphSerializer
)

''' true iff the debug user can login (to bypass google auth) '''
API_DEBUG = True
PROF_DEBUG_TOKEN = '12345'
STUD_DEBUG_TOKEN = '54321'

''' Checks for authentication '''
''' Returns user data or None if authentication fails '''
def authenticateUser(token, format=None, pk=None):
    
    if API_DEBUG and token == PROF_DEBUG_TOKEN:
        # Set up the user's data
        data = {
            'first_name': 'Mark',
            'last_name': 'Floryan',
            'email': 'mrf8t@virginia.edu',
            'id_token': PROF_DEBUG_TOKEN,
            'is_professor': 't'
        }
        return data

    elif API_DEBUG and token == STUD_DEBUG_TOKEN:
        
        data = {
            'first_name': 'Jonny',
            'last_name': 'Studential',
            'email': 'js@virginia.edu',
            'id_token': STUD_DEBUG_TOKEN,
            'is_professor': 'f'
        }
        return data

    else:

        # Call out to google here
        URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
        PARAMS = {'id_token': token}
        r = requests.post(url=URL, params=PARAMS)
        fullProfile = r.json()

        # If the request from google was bad
        if(not fullProfile.get('sub')):
            #return external_error()
            return None

        # Check if they are a professor
        is_prof = 'f'
        try:
            professor = Student.objects.get(id_token=professor_id)
        except Student.DoesNotExist:
            is_prof = 'f'

        # Check if professor
        if ( professor.get_is_professor() ): 
            is_prof = 't'

        # Set up the user's data
        data = {
            'first_name': fullProfile.get('given_name'),
            'last_name': fullProfile.get('family_name'),
            'email': fullProfile.get('email'),
            'id_token': token,
            'is_professor': is_prof
        }

        return data

''' End authenticateUser() '''






''' API ENDPOINTS '''


'''
______________________________________________________________________________________________      Course
    Course:
______________________________________________________________________________________________
'''


class CourseViewSet(viewsets.ModelViewSet):
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
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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

        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        try:
            userObj = Student.objects.get(id_token=token)
        except Student.DoesNotExist:
            return object_not_found_response();

        #grab that user's primary key
        userId = userObj.pk;

        #get the courses associated with that student
        courses = Course.objects.filter(courses__student__pk=userId)
        
        #handle case where user is requesting one specific course
        if pk is not None:
            try:
                course = courses.get(pk=pk)
                serializer = self.serializer_class(course, many=False)
                #if not serializer.is_valid():
                #    return invalid_serializer_response(serializer.errors)

            except self.model.DoesNotExist:
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

        token = request.data.get('token', None)
        
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Only professors can create courses
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

        if pk is None:
            serializer = self.serializer_class(data=request.data)
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
        if pk is None:
            return missing_id_response()
        
        token = request.data.get('token', None)
        
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Only professors can create courses
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
______________________________________________________________________________________________      Grade
    Grade:
______________________________________________________________________________________________
'''


class GradeViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    model = Grade

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/grades/?gradeId=<GRADE_PK>
     function: Removes a given grade
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

        grade_id = request.GET.get('gradeId', None)
        if grade_id is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=grade_id)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

        return successful_delete_response()

    '''
    __________________________________________________  get
     url: GET :: <WEBSITE>/api/grades/student_pk/ OR
          GET :: <WEBSITE>/api/grades/student_pk/topic_pk/ OR
          GET :: <WEBSITE>/api/grades/student_pk/topic_pk/category_pk OR
     function: Retrieves all or a single grade for a student
    __________________________________________________
    '''

    #change get grades to use courseId and id_token
    #if token is prof, send all the grades.
    def get(self, request, format=None, course_pk=None, topic_pk=None, category_pk=None):
        
        #get token of the requesting user
        token = request.GET.get('id_token', None)
        if token is None:
            print("Bad token!")
            return unauthorized_access_response();

        # Token is fine, so let's get user's data and make sure they have a profile
        profile = authenticateUser(token)
        # If no user for that token, then fail
        if profile is None:
            print("No profile!")
            return unauthorized_access_response();

        # Grab the user from the Student table and get their pk
        try:
            userObj = Student.objects.get(id_token=token)
        except Student.DoesNotExist:
            print("Bad id token!")
            return object_not_found_response();
        #grab that user's primary key
        user_pk = userObj.pk;

        #make sure the user is in the given course
        try:
            StudentToCourse.objects.get(student=user_pk, course=course_pk)
        except StudentToCourse.DoesNotExist:
            print("User not in course!")
            return unauthorized_access_response();

        #see if this user is the professor of the course
        is_prof = True
        print ("Assuming user is prof")
        try:
            Course.objects.get(pk=course_pk, professor_id=user_pk)
        except:
            print ("User NOT Prof")
            is_prof = False


        is_many = True
        
        result = self.model.objects.filter(topic_to_category__topic__course=course_pk)

        if topic_pk is not None:
            result = result.filter(topic_to_category__topic=topic_pk)

        if category_pk is not None:
            result = result.filter(topic_to_category__category=category_pk)

        if not is_prof:
            print("Filtering by user " + str(user_pk))
            result = result.filter(student=user_pk)

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/grades/
     function: Creates a given grade
    __________________________________________________
    '''

    def post(self, request, format=None, student_pk=None):
        token = request.data.get('token', None)

        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

        if student_pk is None:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/grade/pk
     function: Edits a given existing grade
    __________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        token = request.data.get('token', None)
        
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Only professors can create courses
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();


        grade_id = request.GET.get('gradeId', None)
        if grade_id is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=grade_id)
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________      Topic To Category
    Topic To Category:
______________________________________________________________________________________________
'''


class TopicToCategoryViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = TopicToCategory.objects.all()
    serializer_class = TopicToCategorySerializer
    model = TopicToCategory

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/topic/category
     function: Removes a given topic to category relationship
    __________________________________________________
    '''

    def delete(self, request, format=None, topic_pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

        # topic_id = id of topic to category
        if topic_pk is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=topic_pk)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
    __________________________________________________  get
     url: GET :: <WEBSITE>/api/topic/category/ OR
          GET :: <WEBSITE>/api/topic/category/topic_pk/category_pk OR
     function: Retrieves all or a single topic to category relationship
    __________________________________________________
    '''

    def get(self, request, format=None, topic_pk=None, category_pk=None):
        is_many = True
        # Get all topic to categories for everything
        if topic_pk is None and category_pk is None:
            result = self.model.objects.all()

        # Get all topic to categories to a topic
        elif topic_pk is not None and category_pk is None:
            try:
                topic = Topic.objects.get(pk=topic_pk)
                result = self.model.objects.all().filter(topic=topic)
                is_many = True
            except Topic.DoesNotExist:
                return object_not_found_response()
        # Get one topic to category for one topic and one category
        elif topic_pk is not None and category_pk is not None:
            try:
                result = self.model.objects.get(
                    topic=topic_pk, category=category_pk)
                is_many = False
            except self.model.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)
    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/topic/category/
     function: Creates a given topic to category relationship
    __________________________________________________
    '''

    def post(self, request, format=None, topic_pk=None):
        if topic_pk is not None:
            return colliding_id_response()
        # Get the topic id
        topic_id = request.data['topic']
        new_weight = float(request.data['weight'])

        # Search for all topic to category relations
        results = self.model.objects.filter(topic=topic_id)
        total = 0

        # Loop through and add up the weights
        for result in results:
            total += result.weight

        # If the weight is over 1, then we dont add it
        if((total + new_weight) > 1):
            return bad_weight_response()

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return invalid_serializer_response(serializer.errors)

        serializer.save()
        return successful_create_response(request.data)
    '''
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/topic/category/pk
     function: Edits a given existing topic to category relationship
    __________________________________________________
    '''

    def put(self, request, format=None, topic_pk=None):
        if topic_pk is None:
            return missing_id_response()
        else:
            try:
                topic = Topic.objects.get(pk=topic_pk)
                result = self.model.objects.get(topic=topic)
            except self.model.DoesNotExist:
                return object_not_found_response()
            except Topic.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________      Category
    Category:
______________________________________________________________________________________________
'''


class CategoryViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category

    '''
    __________________________________________________  Delete
     url: DELETE :: <WEBSITE>/api/categories/
     function: Removes a given Category
    __________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
    __________________________________________________  get
     url: GET :: <WEBSITE>/api/categories/ OR
          GET :: <WEBSITE>/api/categories/pk OR
     function: Retrieves all or a single Category
    __________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        if pk is None:
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
     url: POST :: <WEBSITE>/api/categories/
     function: Creates a given category
    __________________________________________________
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
    __________________________________________________  Put
     url: PUT :: <WEBSITE>/api/categories/pk
     function: Edits a given existing category
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
______________________________________________________________________________________________      Student
    Student:
______________________________________________________________________________________________
'''


class StudentViewSet(viewsets.ModelViewSet):
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
        return unauthorized_access_response();

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/students/?id_token=
     function: Signs a user in by checking if they exist in the DB
    __________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        id_token = request.GET.get('id_token', None)

        if id_token is None:
            return unauthorized_access_response();

        try:
            fullProfile = authenticateUser(id_token, format, pk)
            if(fullProfile is None):
                return object_not_found_response()

            student = Student.objects.get(email=fullProfile["email"])

            if student.id_token != id_token:
                #if student has account but no token set, then just set the token
                #this means prof made account and student logging in for first time
                #otherwise reject the login
                if student.id_token == "":
                    student.id_token = id_token
                    student.save()
                else:
                    return object_not_found_response();

        except self.model.DoesNotExist:
            return object_not_found_response()

        serializer = self.serializer_class(student, many=False)
        return successful_create_response(serializer.data)


    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/students/
     function: Creates a given student if that student does not exist
     post data contains 'token' with id token
    __________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        
        token = request.data.get('token')
        if token is None:
            return external_error()

        data = authenticateUser(token, format, pk)
        if data is None:
            return object_not_found_response()

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            if(serializer.errors['email'][0] == "user with this email already exists."):
                return colliding_id_response();

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
        return unauthorized_access_response();


""" Professor """
""" This is not implemented yet """
#
# class ProfessorViewSet(viewsets.ModelViewSet):
#     renderer_classes = (JSONRenderer, )
#     queryset = Professor.objects.all()
#     serializer_class = ProfessorSerializer
#     model = Professor

#     def post(self, request, format=None, pk=None):
#         if pk is None:
#             # Call out to google here
#             URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
#             PARAMS = {'id_token': request.data.get('token')}
#             r = requests.post(url=URL, params=PARAMS)
#             fullProfile = r.json()

#             
#             # If the request from google was bad

#             if(not fullProfile.get('sub')):
#                 return external_error()
#             data = {
#                 'first_name': fullProfile.get('given_name'),
#                 'last_name': fullProfile.get('family_name'),
#                 'email': fullProfile.get('email'),
#                 'id_token': request.data.get('token'),
#                 'is_professor': request.data.get('isProfessor')
#             }
#             serializer = self.serializer_class(data=data)
#             if not serializer.is_valid():
#                 if(serializer.errors['email'][0] == "user with this email already exists."):
#                     # If they already have an email and this is the verification, then log them in
#                     if(not request.data.get('isCreate')):
#                         profile = {
#                             'first_name': fullProfile.get('given_name'),
#                             'last_name': fullProfile.get('family_name'),
#                             'email': fullProfile.get('email')
#                         }
#                         return successful_create_response(profile)
#                 return invalid_serializer_response(serializer.errors)
#             try:
#                 validatedData = serializer.validated_data
#                 self.model.objects.get(email=validatedData.get('email'))
#                 # If they already have an email and this is the verification, then log them in
#                 if(not request.data.get('isCreate')):
#                     profile = {
#                         'first_name': fullProfile.get('given_name'),
#                         'last_name': fullProfile.get('family_name'),
#                         'email': fullProfile.get('email')
#                     }
#                     return successful_create_response(profile)
#                 # Otherwise we need to block them from creating a new account twice
#                 else:
#                     return successful_create_already_found_response()
#             except self.model.DoesNotExist:
#                 serializer.save()
#                 # Create the profile for the account
#                 profile = {
#                     'first_name': fullProfile.get('given_name'),
#                     'last_name': fullProfile.get('family_name'),
#                     'email': fullProfile.get('email')
#                 }
#                 return successful_create_response(profile)
#         else:
#             return colliding_id_response()

'''
______________________________________________________________________________________________      Student
    Student List:
    GET :: <WEBSITE>/api/student/list
_________________________________________________________________________
'''

# This View Set retrieves all student objects from the database
# It then uses a filter based on first names, last names, and emails
# Next it takes the information and translates it to a json object
# Finally, it returns an HttpResponse of the json object
# This feature does not need a put, post, or delete operation that why 'pass' is there


class SearchViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    model = Student

    def get(self, request, format=None, pk=None):
        is_many = True
        result = self.model.objects.all()
        id_token = request.GET.get('id_token', None)

        if id_token is not None:
            try:
                fullProfile = authenticateUser(id_token, format, pk)

                if(fullProfile is None):
                    return external_error()
                student = Student.objects.get(email=fullProfile["email"])

                # Get courses professor teaches
                courses_professor_owns = Course.objects.all().filter(
                    professor=student
                )
                searchQuery = request.GET.get('query', None)  # url decode
                if searchQuery != "" and searchQuery != "All":
                    url = urllib.parse.unquote(searchQuery)
                    students = Student.objects.all().filter((Q(first_name=url) or Q(last_name=url)
                                                             or Q(email=url))).filter(~Q(email=fullProfile["email"]))
                else:
                    students = Student.objects.all().filter(
                        ~Q(email=fullProfile["email"]))

                student_to_courses = StudentToCourse.objects.all().filter(
                    course_id__in=courses_professor_owns,
                    student_id__in=students
                )

                # student_to_courses = student_to_courses.filter((Q(student_first_name=url) or Q(student_last_name=url) or Q(student_email=url)))

                # # How do I filter then?
                # searchlist = self.queryset.filter((Q(first_name=url) or Q(
                #     last_name=url) or Q(email=url)) and Q(email=fullProfile["email"]))

                serializer = StudentToCourseSerializer(
                    student_to_courses, many=True)
                return successful_create_response(serializer.data)

                # searchlist_json = serializers.serialize('json', searchlist)
                # return HttpResponse(searchlist_json, content_type='application/json')

            except self.model.DoesNotExist:
                return object_not_found_response()

    # Pass because not used

    def post(self, request, format=None, pk=None):
        return object_not_found_response()

    def put(self, request, format=None, pk=None):
        return object_not_found_response()

    def delete(self, request, format=None, pk=None):
        return object_not_found_response()


'''
______________________________________________________________________________________________      Topic
    Topic: 

______________________________________________________________________________________________
'''


class TopicViewSet(viewsets.ModelViewSet):
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
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
            result = self.model.objects.all()

            course_id = request.GET.get('courseId', None)
            if course_id is not None:
                try:
                    course = Course.objects.get(pk=course_id)
                except Course.DoesNotExist:
                    return object_not_found_response()
                result = self.model.objects.all().filter(course=course)
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
            for topic in request.data:
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
                            student=student, topic=newly_created_topic)
                    except StudentToTopic.DoesNotExist:
                        student_to_topic = StudentToTopic(
                            course=course,
                            student=student,
                            topic=newly_created_topic,
                            locked=False
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
 TopicToTopic: 
______________________________________________________________________________________________
'''


class TopicToTopicViewSet(viewsets.ModelViewSet):
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
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
            result = self.model.objects.all().filter(topic_node=pk)
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
                print("topictotopic")
                print(topictotopic)

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
    StudentToTopic: 
______________________________________________________________________________________________
'''


class StudentToTopicViewSet(viewsets.ModelViewSet):
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
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

        studentToTopicId = request.GET.get('studentToTopicId', None)
        if studentToTopicId is None:
            return missing_id_response()
        else:
            try:
                result = self.model.objects.get(pk=studentToTopicId)
                result.delete()
            except self.model.DoesNotExist:
                return object_not_found_response()

            return successful_delete_response()

    '''
    __________________________________________________  Get
     url: GET :: <WEBSITE>/api/student/topics/ OR
          GET :: <WEBSITE>/api/student/topics/<COURSE_ID>/<STUDENT_ID> OR
     function: Retrieves all or a single topic related to a student
    __________________________________________________
    '''

    def get(self, request, format=None, class_id=None, student_id=None):
        is_many = True
        if class_id is None:
            result = self.model.objects.all()
        else:
            try:
                result = StudentToTopic.get_topics(
                    self.model, class_id, student_id)
                # result = self.model.objects.get_topics()
                is_many = True
            except Student.DoesNotExist:
                return object_not_found_response()
            except Course.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
    __________________________________________________  Post
     url: POST :: <WEBSITE>/api/student/topics/
     function: Creates a given topic for a student
    __________________________________________________
    '''

    def post(self, request, format=None, class_id=None):
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
                    locked=False
                )
                newstudenttotopic.save()
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

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


'''
______________________________________________________________________________________________      QuizViewSet
QuizViewSet
______________________________________________________________________________________________
'''


class QuizViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    model = Quiz

    '''
      url: DELETE :: <WEBSITE>/api/quiz/
      function: Removes a given quiz
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
      url: GET :: <WEBSITE>/api/quiz/ OR
          GET :: <WEBSITE>/api/quiz/<QUIZ_ID> OR
      function: Retrieves all or a single quiz
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        if pk is None:
            result = self.model.objects.all()
        else:
            try:
                try:
                    topic = Topic.objects.get(pk=pk)
                except Topic.DoesNotExist:
                    return object_not_found_response()
                result = self.model.objects.get(topic=topic)
                is_many = False
            except self.model.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
      url: POST :: <WEBSITE>/api/quiz/
      function: Creates a given quiz
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            data = request.data
            if "name" not in data or "topic" not in data:
                return malformed_request_response(fields=["name", "topic"])

            name = data["name"]
            weight = data["weight"]
            topicId = data["topic"]
            topic = None

            try:
                topic = Topic.objects.get(pk=topicId)
            except Topic.DoesNotExist:
                return object_not_found_response()

            quiz = Quiz(name=name, topic=topic)
            quiz.save()

            category = Category.objects.get(name="Internal Quiz")

            topic_to_category = None
            try:
                topic_to_category = TopicToCategory.objects.get(
                    topic=topic, category=category)
            except TopicToCategory.DoesNotExist:
                results = TopicToCategory.objects.filter(topic=topic)
                total = 0

                # Loop through and add up the weights
                for result in results:
                    total += result.weight

                # If the weight is over 1, then we dont add it
                if((total + float(weight)) > 1):
                    return bad_weight_response()

                topic_to_category = TopicToCategory(
                    topic=topic, category=category, weight=float(weight))

                topic_to_category.save()

            if "questions" in data:
                for question in data["questions"]:
                    # Now create and save the model
                    quiz_question = QuizQuestion(
                        text=question["text"],
                        question_type=question["question_type"],
                        quiz=quiz,
                        total_points=question["total_points"],
                        index=question["index"]
                    )
                    quiz_question.save()

                    if "answers" in question:
                        for answer in question["answers"]:

                            # Now create and save the model
                            quiz_question_answer = QuizQuestionAnswer(
                                text=answer["text"],
                                question=quiz_question,
                                correct=answer["correct"],
                                index=answer["index"]
                            )
                            quiz_question_answer.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/quiz/<QUIZ_ID>
      function: Edits a given existing quiz
    '''

    def put(self, request, format=None, pk=None):
        if pk is not None:
            data = request.data
            if "name" not in data or "topic" not in data:
                return malformed_request_response(fields=["name", "topic"])

            name = data["name"]
            topicId = data["topic"]
            weight = data["weight"]
            topic = None

            try:
                topic = Topic.objects.get(pk=topicId)
            except Topic.DoesNotExist:
                return object_not_found_response()

            Quiz.objects.all().filter(topic=topic).update(
                name=name
            )
            quiz = Quiz.objects.get(topic=topic)
            topic_to_category = None

            try:
                category = Category.objects.get(name="Internal Quiz")

                topic_to_category = TopicToCategory.objects.filter(topic=topic)
                total = 0
                old_quiz_weight = TopicToCategory.objects.get(topic=topic, category=category).weight
                # Loop through and add up the weights
                for result in topic_to_category:
                    total += result.weight

                # If the weight is over 1, then we dont add it
                if((total + float(weight)) - old_quiz_weight > 1 ):
                    return bad_weight_response()

                topic_to_category.update(
                  weight=float(weight)
                )

            except TopicToCategory.DoesNotExist:
                pass 
                

            if "questions" in data:

                for question in data["questions"]:

                    question_pk = None
                    if "pk" in question:
                        question_pk = question["pk"]

                    # Now create and save the model
                    if question_pk is None:
                        # If no pk, create a new question
                        quiz_question = QuizQuestion(
                            text=question["text"],
                            question_type=question["question_type"],
                            quiz=quiz,
                            total_points=question["total_points"],
                            index=question["index"]
                        )
                        quiz_question.save()
                    else:
                        # If there is a pk edit that new question
                        QuizQuestion.objects.all().filter(pk=question_pk).update(
                            text=question["text"],
                            question_type=question["question_type"],
                            total_points=question["total_points"],
                            index=question["index"]
                        )
                        quiz_question = QuizQuestion.objects.get(
                            pk=question_pk)

                    if "answers" in question:
                        for answer in question["answers"]:
                            # Now create and save the model
                            answer_pk = None
                            if "pk" in answer:
                                answer_pk = answer["pk"]

                            try:
                                correct = answer["correct"]
                            except KeyError:
                                correct = False

                            if answer_pk is None:
                                quiz_question_answer = QuizQuestionAnswer(
                                    text=answer["text"],
                                    question=quiz_question,
                                    correct=correct,
                                    index=answer["index"]
                                )
                                quiz_question_answer.save()
                            else:
                                QuizQuestionAnswer.objects.all().filter(pk=answer_pk).update(
                                    text=answer["text"],
                                    correct=correct,
                                    index=answer["index"]
                                )

                    if "deletedAnswers" in question:
                        for deleted_answer in question["deletedAnswers"]:
                            answer_pk = None
                            if "pk" in deleted_answer:
                                answer_pk = deleted_answer["pk"]

                            if answer_pk is not None:
                                quiz_question_answer = QuizQuestionAnswer.objects.all().filter(pk=answer_pk).delete()

            if "deletedQuestions" in data:
                for question in data["deletedQuestions"]:
                    question_pk = None
                    if "pk" in question:
                        question_pk = question["pk"]

                    # Now create and save the model
                    if question_pk is not None:
                        # If no pk, create a new question
                        quiz_question = QuizQuestion.objects.all().filter(
                            pk=question_pk
                        ).delete()

            return successful_create_response(request.data)
        else:
            return object_not_found_response()


'''
______________________________________________________________________________________________      QuizQuestionViewSet
QuizQuestionViewSet
______________________________________________________________________________________________
'''


class QuizQuestionViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    model = QuizQuestion

    '''
      url: DELETE :: <WEBSITE>/api/quiz-question/<quiz-question-id>
      function: Removes a given question
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
      url: GET :: <WEBSITE>/api/quiz-question/ OR
          GET :: <WEBSITE>/api/quiz-question/<quiz-question_id> OR
      function: Retrieves all or a single quiz questions
    '''

    def get(self, request, format=None, pk=None):
        # quizId = request.GET.get('quizId', None)
        # result = self.model.objects.all()
        # if quizId is not None:
        #   result = self.model.objects.all().filter(
        #     quiz=Quiz.objects.
        #   )
        is_many = True
        if pk is None:
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
      url: POST :: <WEBSITE>/api/quiz-question/
      function: Creates a given quiz-question
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            data = request.data

            # Check if all fields were provided
            fields = ["text", "question_type", "quiz", "total_points", "index"]
            missing_fields = {}
            for field in fields:
                if field not in data:
                    # Mocks drf serializer error
                    missing_fields[field] = ["This field is required."]

            if len(missing_fields.keys()) > 0:
                return malformed_request_response(fields=missing_fields)

            # Once we know they exist, extract them to vars
            text = data["text"]
            question_type = data["question_type"]
            quizId = data["quiz"]
            total_points = data["total_points"]
            index = data["index"]
            quiz = None

            # Try to access the foreign key necessary for the model
            try:
                quiz = Quiz.objects.get(pk=quizId)
            except Quiz.DoesNotExist:
                return object_not_found_response()

            # Now create and save the model
            quiz_question = QuizQuestion(
                text=data["text"],
                question_type=data["question_type"],
                quiz=quiz,
                total_points=data["total_points"],
                index=data["index"]
            )
            quiz_question.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/quiz-question/
      function: Edits a given quiz-question
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
______________________________________________________________________________________________      QuizQuestionAnswerViewSet
QuizQuestionAnswerViewSet
______________________________________________________________________________________________
'''


class QuizQuestionAnswerViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionAnswerSerializer
    model = QuizQuestionAnswer

    '''
      url: DELETE :: <WEBSITE>/api/quiz-question-answer/<quiz-question-answer-id>
      function: Removes a given question answer
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
      url: GET :: <WEBSITE>/api/quiz-question-answer/ OR
          GET :: <WEBSITE>/api/quiz-question-answer/<quiz_question_id> OR
      function: Retrieves all or a single answer 
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        if pk is None:

            result = self.model.objects.all()
        else:
            is_many = False
            try:
                result = self.model.objects.get(pk=pk)
            except QuizQuestionAnswer.DoesNotExist:
                return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
      url: POST :: <WEBSITE>/api/quiz-question-answer/
      function: Creates a given quiz-question-answer
    '''

    def post(self, request, format=None, pk=None):
        # Check if all fields were provided
        if pk is None:
            data = request.data
            fields = ["text", "question", "correct", "index"]
            missing_fields = {}
            for field in fields:
                if field not in data:
                    # Mocks drf serializer error
                    missing_fields[field] = ["This field is required."]

            if len(missing_fields.keys()) > 0:
                return malformed_request_response(fields=missing_fields)

            # Once we know they exist, extract them to vars
            text = data["text"]
            question_id = data["question"]
            correct = data["correct"]
            index = data["index"]
            question = None

            # Try to access the foreign key necessary for the model
            try:
                question = QuizQuestion.objects.get(pk=question_id)
            except QuizQuestion.DoesNotExist:
                return object_not_found_response()

            # Now create and save the model
            quiz_question_answer = QuizQuestionAnswer(
                text=text,
                question=question,
                correct=correct,
                index=index
            )
            quiz_question_answer.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/quiz-question-answer/
      function: Edits a given quiz-question-answer
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
______________________________________________________________________________________________      ResourcesViewSet
ResourcesViewSet
______________________________________________________________________________________________
'''


class ResourcesViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = Resources.objects.all()
    serializer_class = ResourcesSerializer
    model = Resources

    '''
      url: DELETE :: <WEBSITE>/api/resources/
      function: Removes a given resource
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
    renderer_classes = (JSONRenderer, )
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    model = Settings

    '''
      url: DELETE :: <WEBSITE>/api/settings/
      function: Removes a given setting
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
        id_token = request.GET.get('id_token', None)
        print("Settings requested. IN get")

        if id_token is None:
            print("Returning object not found")
            return object_not_found_response()

        fullProfile = authenticateUser(id_token, format, pk);

        if(fullProfile is None):
            print("fullProfile is none")
            return external_error()
        try:
            print("Email is: " + fullProfile["email"])
            student = Student.objects.get(email=fullProfile["email"])
            result = Settings.objects.get(user=student)
            is_many = False
        except self.model.DoesNotExist:
            print("Object not found 2")
            return object_not_found_response()

        serializer = self.serializer_class(result, many=is_many)
        return successful_create_response(serializer.data)

    '''
      url: POST :: <WEBSITE>/api/settings/
      function: Creates a given setting
    '''

    def post(self, request, format=None, pk=None):
        if pk is None:
            id_token = request.data.get('token')

            fullProfile = authenticateUser(id_token, format, pk)

            if(fullProfile is None):
                return external_error()

            student = Student.objects.get(email=fullProfile["email"])
            settings = Settings.objects.all().filter(user=student)
            if len(settings) > 0:
                return colliding_id_response()
            else:
                settings = Settings(
                    color='#FFFFFF',
                    user=student
                )
                settings.save()
                return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/settings/<SETTING_ID>
      function: Edits a given existing setting
    '''

    def put(self, request, format=None, pk=None):

        id_token = request.data.get('token')

        fullProfile = authenticateUser(id_token, format, pk)

        if(fullProfile is None):
            return external_error()

        try:
            student = Student.objects.get(email=fullProfile["email"])
            students_settings = self.model.objects.get(user=student)
            result = self.model.objects.all().filter(user=student)
            colors = request.data.get("colors")
            result.update(
                color=colors["hex"],
                nickname=request.data.get("nickname")
            )
        except self.model.DoesNotExist:
            return object_not_found_response()

        return successful_edit_response(request.data)


'''
______________________________________________________________________________________________      StudentToQuizViewSet
StudentToQuizViewSet
______________________________________________________________________________________________
'''


class StudentToQuizViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = StudentToQuiz.objects.all()
    serializer_class = StudentToQuizSerializer
    model = StudentToQuiz

    '''
      url: DELETE :: <WEBSITE>/api/student/quiz
      function: Removes a given Student from a quiz
    '''

    def delete(self, request, format=None, pk=None):
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
      url: GET :: <WEBSITE>/api/students/quiz OR
          GET :: <WEBSITE>/api/students/quiz/<QUIZ_ID> OR
      function: Retrieves all or a single quizzes a student is assigned to
    '''

    def get(self, request, format=None, pk=None):
        is_many = True
        # pk of student professor is trying to view
        view_as = request.GET.get('view_as', None)

        if pk is None:
            result = self.model.objects.all()
        else:
            is_many = False
            result = {}

            id_token = request.GET.get('id_token', None)
            # TODO: Extract student id from auth token
            fullProfile = authenticateUser(id_token, format, pk)

            if(fullProfile is None):
                return external_error()

            user = Student.objects.get(email=fullProfile["email"])
            student = user

            topic = Topic.objects.get(pk=pk)

            # If a professor is trying to view one of their students' grades for a course
            if view_as is not None and view_as.isdigit():
                # 1) is the user the professor of the chose course?
                professor_of_course = topic.course.professor
                if professor_of_course.pk != user.pk:
                    # not a missing id response, it's an unauthorized request, update later
                    return missing_id_response()

                # Now that we've gotten rid of lookieloos
                student = Student.objects.get(pk=view_as)

            try:
                quiz = Quiz.objects.get(topic=topic)
            except Quiz.DoesNotExist:
                return object_not_found_response()

            try:
                result = StudentToQuiz.objects.get(student=student, quiz=quiz)
            except StudentToQuiz.DoesNotExist:
                return object_not_found_response()

        serializer = StudentToQuizSerializer(result, many=is_many)

        return successful_create_response(serializer.data)

    '''
      url: POST :: <WEBSITE>/api/student/quiz/<QUIZ_ID>
      function: Creates a given students responses to a quiz
    '''

    def post(self, request, format=None, pk=None):
        if pk is not None:

            id_token = request.data.get('id_token', None)

            fullProfile = authenticateUser(id_token, format, pk)

            if(fullProfile is None):
                return external_error()

            student = Student.objects.get(email=fullProfile["email"])
            topic = Topic.objects.get(pk=pk)
            quiz = Quiz.objects.get(topic=topic)
            answers = request.data["answers"]

            # Check if student has already taken the quiz
            student_to_quiz = None
            student_to_quiz_queryset = StudentToQuiz.objects.all().filter(
                quiz=quiz,
                student=student
            )

            # If none are found, they haven't taken the test before this so create a new one
            if len(student_to_quiz_queryset) == 0:
                student_to_quiz = StudentToQuiz(
                    quiz=quiz, student=student).save()
            else:
                student_to_quiz = student_to_quiz_queryset[0]

            student_to_quiz = StudentToQuiz.objects.get(
                quiz=quiz, student=student)
            total_points = 0
            for answer in answers:
                question = QuizQuestion.objects.get(pk=answer["question_id"])
                answer = QuizQuestionAnswer.objects.get(pk=answer["answer_id"])

                if answer.correct:
                    total_points += 1

                # If they've never answer this question before, create a new one
                student_to_quiz_question = None
                student_to_quiz_question_queryset = StudentToQuizQuestion.objects.all().filter(
                    question=question,
                    student=student
                )

                if len(student_to_quiz_question_queryset) == 0:
                    student_to_quiz_question = StudentToQuizQuestion(
                        student_to_quiz=student_to_quiz,
                        answer=answer,
                        question=question,
                        student=student,
                        correct=answer.correct
                    ).save()
                else:
                    student_to_quiz_question = student_to_quiz_question_queryset[0]
                    student_to_quiz_question_queryset.update(
                        student_to_quiz=student_to_quiz,
                        answer=answer,
                        correct=answer.correct
                    )

            grade = (total_points/len(answers))*100

            # Update grade for student's quiz based on new answers
            student_to_quiz_queryset.update(
                grade=grade
            )

            # student_to_topic_queryset = StudentToTopic.objects.all().filter(
            #     student=student,
            #     topic=topic
            # )

            # student_to_topic_queryset.update(
            #     grade=grade
            # )

            category = Category.objects.get(name="Internal Quiz")
            topic_to_category = TopicToCategory.objects.get(
                topic=topic, category=category)
            student_to_grade_queryset = Grade.objects.all().filter(
                topic_to_category=topic_to_category,
                student=student
            )
            if student_to_grade_queryset.count() != 0:
                student_to_grade_queryset.update(
                    value=grade
                )
            else:
                student_to_grade = Grade(
                    topic_to_category=topic_to_category,
                    student=student,
                    value=grade,
                    name="Quiz grade"
                )
                student_to_grade.save()

            return successful_create_response(request.data)
        else:
            return colliding_id_response()

    '''
      url: PUT :: <WEBSITE>/api/students/quiz/<QUIZ_ID>
      function: Edits a given existing student's responses to quesitons
    '''

    def put(self, request, format=None, pk=None):
        return missing_id_response()  # Not implemented


'''
______________________________________________________________________________________________      StudentToCourseViewSet
StudentToCourseViewSet
______________________________________________________________________________________________
'''


class StudentToCourseViewSet(viewsets.ModelViewSet):
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
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();

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
                result.delete()

                # Delete the student to topic
                topics = StudentToTopic.objects.all().filter(student=student, course=course)
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
            result = self.model.objects.all()

            course_id = request.GET.get('courseId', None)
            id_token = request.GET.get('id_token', None)
            # pk of student professor is trying to view
            view_as = request.GET.get('view_as', None)

            # if course_id and id_token, get detailed info about student's course enrollment
            if course_id is not None and id_token is not None:
                try:
                    # Try to parse the id token
                    fullProfile = authenticateUser(id_token, format, pk)

                    if(fullProfile is None):
                        return external_error()

                    user = Student.objects.get(email=fullProfile["email"])
                    student = user

                    course = Course.objects.get(pk=course_id)

                    # If a professor is trying to view one of their students' grades for a course
                    if view_as is not None and view_as.isdigit():
                        # 1) is the user the professor of the chose course?
                        professor_of_course = course.professor
                        if professor_of_course.pk != user.pk:
                            # not a missing id response, it's an unauthorized request, update later
                            return missing_id_response()

                        # Now that we've gotten rid of lookieloos
                        student = Student.objects.get(pk=view_as)

                    grade_update = views.update_class_grades(
                        None, course.pk, student.pk)
                    student_to_course = StudentToCourse.objects.get(
                        course=course, student=student)

                    serializer = ClassGraphSerializer(
                        student_to_course, many=False)
                    return successful_create_response(serializer.data)

                except Course.DoesNotExist:
                    return object_not_found_response()
                except Student.DoesNotExist:
                    return object_not_found_response()
                except StudentToCourse.DoesNotExist:
                    return object_not_found_response()

            elif course_id is not None:
                try:
                    course = Course.objects.get(pk=course_id)
                except Course.DoesNotExist:
                    return object_not_found_response()
                result = self.model.objects.all().filter(
                    course=course
                )
            else:
                # Try to parse the id token
                fullProfile = authenticateUser(id_token, format, pk)

                if(fullProfile is None):
                    return external_error()

                student = Student.objects.get(email=fullProfile["email"])
                result = self.model.objects.all().filter(
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

            id_token = request.data.get('id_token', None)

            if id_token is not None:
                fullProfile = authenticateUser(id_token, format, pk)

                if(fullProfile is None):
                    return external_error()

            if len(missing_fields.keys()) > 0 and id_token is None:
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

            if id_token is not None:
                student = Student.objects.get(email=fullProfile["email"])
            else:
                student_id = data["student"]
                try:
                    student = Student.objects.get(pk=student_id)
                except Student.DoesNotExist:
                    return object_not_found_response()

            studentToCourse = StudentToCourse.objects.all().filter(
                course=course,
                student=student
            )

            if len(studentToCourse) > 0:
                return colliding_id_response()

            studentToCourse = StudentToCourse(
                course=course,
                student=student
            )
            # Save the student to course relationship
            studentToCourse.save()

            # Add the student to topic relationships

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
            except self.model.DoesNotExist:
                return object_not_found_response()

            serializer = self.serializer_class(result, data=request.data)

            if not serializer.is_valid():  # pragma: no cover This serializer is always valid, but serializer requires is_valid to be called to save()
                return invalid_serializer_response(serializer.errors)

            serializer.save()
            return successful_edit_response(serializer.data)


















'''
______________________________________________________________________________________________      External Import Grades
 ExternalImportGrades:
______________________________________________________________________________________________
'''
class ExternalImportGradesViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )

    '''
    _______________________________________________________ Delete
     <WEBSITE>/api/external_import_grades/<pk>?<id>
    _______________________________________________________
    '''

    def delete(self, request, format=None, pk=None):

        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();
        
        # Token is fine, so let's get user's data
        profile = authenticateUser(token)

        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table
        if not profile['is_professor'] == 't':
            return unauthorized_access_response();
        
        # Get Param
        professor_id = request.GET.get('id_token')
        externalSiteToCourse_pk = pk
        
        # Validate parameters
        try: 
            # Check params
            if professor_id is None:
                raise Exception('Missing ID')
            if externalSiteToCourse_pk is None:
                raise Exception('Missing ExternalSiteToCourse pk')


            # Check if professor in users
            try:
                professor = Student.objects.get(id_token=professor_id)
            except Student.DoesNotExist:
                raise Exception('Invalide ID') 

            
            # Check if professor
            if ( profile['is_professor'] == 'f' ): 
                raise Exception('Student ID passed in')


            # Validate externalSite_pk
            try:
                externalSiteToCourse = ExternalSiteToCourse.objects.get(pk=externalSiteToCourse_pk,course__professor= professor)
            except ExternalSiteToCourse.DoesNotExist:
                raise Exception('ExternalSiteToCourse does not exist')
                
                
        except Exception as ex:
            return Response(data={
                'status': '406 - Bad Request',
                'result': str(ex)
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Delete all connected ExternalSiteToGrade and associated grades
        externalSitesToGrade = ExternalSiteToGrade.objects.filter(external_site_to_course = externalSiteToCourse)
        for externalSiteToGrade in externalSitesToGrade:
            externalSiteToGrade.delete()

        # Delete externalSite
        externalSiteToCourse.delete()

        return Response({
            'status': '200 - Ok',
            'result': "Successfully Deleted",
        }, status=status.HTTP_200_OK)


    '''
    _______________________________________________________ Get
     <WEBSITE>/api/external_import_grades/<pk>?<id>&<course_pk>
    _______________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        
        
        # Validate Parameters
        try: 
            # Get Param
            professor_id = request.GET.get('id')
            course_pk = request.GET.get('course_pk')
            externalSiteToCourse_pk = pk

            # Check params
            if professor_id is None:
                raise Exception('Missing ID')
            if course_pk is None: 
                raise Exception('Missing course pk')

            # Check if professor in users
            try:
                professor = Student.objects.get(id_token=professor_id)
            except Student.DoesNotExist:
                raise Exception('Invalide ID') 

            # Check if professor
            if ( not professor.get_is_professor() ): 
                raise Exception('Student ID passed in')

            # Check course_pk
            try: 
                course = Course.objects.get(pk=course_pk, professor= professor)
            except Course.DoesNotExist:
                raise Exception('Invalid course pk')

            # Check that there are students in course
            studentsToCourse = StudentToCourse.objects.filter(course= course)
            if not studentsToCourse.exists():
                raise Exception('No students in course')

            # Get ExternalSiteToCourse objects
            if externalSiteToCourse_pk is None:
                # Get all external course links for professor
                externalSiteToCourse = ExternalSiteToCourse.objects.filter(course = course) # pragma: no cover
            else: 
                try:
                    externalSitesToCourse = ExternalSiteToCourse.objects.get(pk=externalSiteToCourse_pk, course= course)
                except ExternalSiteToCourse.DoesNotExist:
                    raise Exception('Invalid ExternalSiteToCourse pk')

        except Exception as ex:
            return Response(data={
                'status': '406 - Bad Request',
                'result': str(ex)
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        

        link =  externalSitesToCourse.external_site.base_url + externalSitesToCourse.url_ending
        # TODO FIX THIS ERROR
        '''
        print()
        try:
            print(link)
            print('--------------------------')
            data = requests.get(link)
            print(data)
        except requests.exceptions.ConnectionError as err:
            print(err)
        except Exception as ex:
            print('ex: ' + str(ex))
        #json.loads(request.content.decode("utf-8"))
        '''

        return Response({
            'status': '200 - Ok',
            'result': "Successfully Deleted",
        }, status=status.HTTP_200_OK)

        return import_grades(externalSitesToCourse, course, studentsToCourse) # pragma: no cover 
        

    '''
    _______________________________________________________ Post
     <WEBSITE>/api/external_import_grades/
    _______________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        
        if not (pk is None):
            return Response(data={
                'status': '406 - Bad Request',
                'result': 'PK should not be passed'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # Validate Parameters
        try: 

            # Check Param
            data = request.data
            if "professor_id" not in data:
                raise Exception('Missing professor_id')
            if "course_pk" not in data:
                raise Exception('Missing course_pk')
            if "externalSite_pk" not in data:
                raise Exception('Missing externalSite_pk') 
            if "url_ending" not in data:
                raise Exception('Missing url_ending')
            

            # Get Parameters
            professor_id = data['professor_id']
            course_pk = data['course_pk']
            externalSite_pk = data['externalSite_pk']
            url_ending = data['url_ending']

            # Check if professor in users
            try:
                professor = Student.objects.get(id_token=professor_id)
            except Student.DoesNotExist:
                raise Exception('Invalide ID') 

            # Check if professor
            if ( not professor.get_is_professor() ): 
                raise Exception('Student ID passed in')

            # Check course_pk
            try: 
                course = Course.objects.get(pk=course_pk, professor= professor)
            except Course.DoesNotExist:
                raise Exception('Invalid course pk')


            # Get ExternalSiteToCourse objects
            try:
                externalSite = ExternalSite.objects.get(pk=externalSite_pk)
            except ExternalSite.DoesNotExist:
                raise Exception('Invalid ExternalSite pk')

            # Check to make sure ExternalSiteToCourse doesn't exist
            externalSiteToCourse = ExternalSiteToCourse.objects.filter(course= course, external_site=externalSite, url_ending= url_ending)
            if externalSiteToCourse.exists():
                raise Exception('ExternalSiteToCourse already exists')

        except Exception as ex:
            return Response(data={
                'status': '406 - Bad Request',
                'result': str(ex)
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        

        return Response({
            'status': '200 - Ok',
            'result': "Successfully Deleted",
        }, status=status.HTTP_200_OK)

        return create_import_grades(externalSite, url_ending, course)  # pragma: no cover 

    '''
    _______________________________________________________ Put
     <WEBSITE>/api/external_import_grades/, data
    _______________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


















'''
______________________________________________________________________________________________      External Site
 ExternalSite: The urls for the SPT approved API's
    delete: We currently don't want anyone to be able to delete but admin
    get: If professor, they can either get the ExternalSite for one or all approved API's
    post: We don't want anyone externally able to create API's
    put: We don't want anyone externally able to edit our API's
______________________________________________________________________________________________
'''
class ExternalSiteViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = ExternalSite.objects.all()
    serializer_class = ExternalSiteSerializer
    model = ExternalSite

    '''
    _______________________________________________________ Delete
      <WEBSITE>/api/external_sites/
    _______________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Get
      <WEBSITE>/api/external_sites/<pk>?id=<professor_id>
    _______________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        
        
        # Check Param
        professor_id = request.GET.get('id')
        externalSite_pk = pk
        
        # Validate professor_id
        try: 
            # Check if professor_id
            if professor_id is None:
                raise Exception('Missing ID')

            # Check if professor in users
            try:
                professor = Student.objects.get(id_token=professor_id)
            except Student.DoesNotExist:
                raise Exception('Invalide ID') 

            
            # Check if professor
            if ( not professor.get_is_professor() ): 
                raise Exception('Student ID passed in')

        except Exception as ex:
            return Response(data={
                'status': '406 - Bad Request',
                'result': str(ex)
            }, status=status.HTTP_406_NOT_ACCEPTABLE)



        is_many = True
        if pk is None:
            result = self.model.objects.all()
        else:
            try:
                result = ExternalSite.objects.get(pk=externalSite_pk)
                is_many = False
            except self.model.DoesNotExist:
                return Response(data={
                    'status': '406 - Bad Request',
                    'result': 'Invalid externalSite pk'
                }, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.serializer_class(result, many=is_many)
        response = successful_create_response(serializer.data)
        return successful_create_response(serializer.data)
        

    '''
    _______________________________________________________ Post
     <WEBSITE>/api/external_sites/<pk>  , data
    _______________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Put
      <WEBSITE>/api/external_sites/<pk>, data
    _______________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)




















'''
______________________________________________________________________________________________      ExternalSite To Course
 ExternalSiteToCourse:
 Give professor's active External Links for each Course
______________________________________________________________________________________________
'''
class ExternalSiteToCourseViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = ExternalSiteToCourse.objects.all()
    serializer_class = ExternalSiteToCourseSerializer
    model = ExternalSiteToCourse

    '''
    _______________________________________________________ Delete
     <WEBSITE>/api/external_sites_to_course/
    _______________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Get
     <WEBSITE>/api/external_sites_to_course/<pk>?id=<professor_id>
     -Give professor's active External Links for each Course
    _______________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        
        
        # Check Param
        professor_id = request.GET.get('id')
        course_pk = pk
        
        
        # Validate Parameters
        try: 
            if professor_id is None:
                raise Exception('Missing ID')

            # Check if professor in users
            try:
                professor = Student.objects.get(id_token=professor_id)
            except Student.DoesNotExist:
                raise Exception('Invalide ID') 
            
            # Check if professor
            if ( not professor.get_is_professor() ): 
                raise Exception('Student ID passed in')

             # Check if course is in Courses and belongs to professor
            try:
                course = Course.objects.get(pk= course_pk, professor= professor)
            except Course.DoesNotExist:
                raise Exception('Course not found')

        except Exception as ex:
            return Response(data={
                'status': '406 - Bad Request',
                'result': str(ex)
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

       

        # Get ExternalSite links associated with course
        externalSiteToCourse = ExternalSiteToCourse.objects.filter(course= course)
        
        if (externalSiteToCourse.count() == 1):
            externalSiteToCourse = ExternalSiteToCourse.objects.get(course= course)
            serializer = self.serializer_class(externalSiteToCourse, many= False)
        else:
            serializer = self.serializer_class(externalSiteToCourse, many= True)
        
        return successful_create_response(serializer.data)
        

    '''
    _______________________________________________________ Post
     <WEBSITE>/api/external_sites_to_course/
    _______________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Put
     <WEBSITE>/api/external_sites_to_course/, data
    _______________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


















'''
______________________________________________________________________________________________      ExternalSite To Grade
 ExternalSiteToGrade:
______________________________________________________________________________________________
'''
class ExternalSiteToGradeViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, )
    queryset = ExternalSiteToGrade.objects.all()
    serializer_class = ExternalSiteToGradeSerializer
    model = ExternalSiteToGrade

    '''
    _______________________________________________________ Delete
     <WEBSITE>/api/external_sites_to_course/
    _______________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Get
     <WEBSITE>/api/external_sites_to_course/ 
    _______________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Post
     <WEBSITE>/api/external_sites_to_course/
    _______________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Put
     <WEBSITE>/api/external_sites_to_course/, data
    _______________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)










'''
______________________________________________________________________________________________      ExternalImportGrades (Test)
 ExternalImportGradesTest: URL Made for Testing JSON returns to 
______________________________________________________________________________________________
'''
class ExternalImportGradesTestViewSet(viewsets.ModelViewSet):

    '''
    _______________________________________________________ Delete
     <WEBSITE>/api/external_import_grades_test/
    _______________________________________________________
    '''

    def delete(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Get
     <WEBSITE>/api/external_import_grades_test/ 
    _______________________________________________________
    '''

    def get(self, request, format=None, pk=None):
        # AABBCCDD
        if (pk is None):
            return JsonResponse({'status':'false','message':'BAD'}, status=400)
        elif (pk == '1'):
            return JsonResponse( grades_good() )
        elif pk == '2':
            return JsonResponse( grades_missing_exams() )
        elif (pk == '3'):
            return JsonResponse( grades_missing_topicName() )
        elif (pk == '4'):
            return JsonResponse( grades_missing_gradeName() )
        elif (pk == '5'):
            return JsonResponse( grades_missing_students() )
        elif (pk == '6'):
            return JsonResponse( grades_missing_email() )
        elif (pk == '7'):
            return JsonResponse( grades_missing_gradeValue() )

        else: 
            return JsonResponse({'status':'false','message':'BAD'}, status=400)


    '''
    _______________________________________________________ Post
     <WEBSITE>/api/external_import_grades_test/
    _______________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Put
     <WEBSITE>/api/external_import_grades_test/, data
    _______________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


'''
______________________________________________________________________________________________      
 CourseTopicToStudentViewSet : Gets students associated with a given course and topic
 (just the student unless user is the professor)
______________________________________________________________________________________________
'''
class CourseTopicToStudentViewSet(viewsets.ModelViewSet):

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
     <WEBSITE>/api/coursetopictostudent/course_pk/topic_pk/?id_token=xxxxx 
    _______________________________________________________
    '''

    def get(self, request, format=None, course_pk=None, topic_pk=None):
        #get token of the requesting user
        token = request.GET.get('id_token', None)
        if token is None:
            return unauthorized_access_response();

        # Token is fine, so let's get user's data and make sure they have a profile
        profile = authenticateUser(token)
        # If no user for that token, then fail
        if profile is None:
            return unauthorized_access_response();

        # Grab the user from the Student table and get their pk
        try:
            userObj = Student.objects.get(id_token=token)
        except Student.DoesNotExist:
            return object_not_found_response();
        #grab that user's primary key
        user_pk = userObj.pk;

        #make sure the user is in the given course
        try:
            StudentToCourse.objects.get(student=user_pk, course=course_pk)
        except StudentToCourse.DoesNotExist:
            return unauthorized_access_response();

        #see if this user is the professor of the course
        is_prof = True
        try:
            Course.objects.get(pk=course_pk, professor_id=user_pk)
        except:
            is_prof = False


        students = []
        # Get all student to topic relations
        student_to_topics = StudentToTopic.objects.filter(
            course=course_pk, topic=topic_pk)

        if not is_prof:
            student_to_topics = student_to_topics.filter(student=user_pk)

        # For each relation, get the student
        for student in student_to_topics:
            # students.append({"text": student.student.email})
            students.append({"text": student.student.get_name(),
                             "value": student.student.pk})
        # Return the data
        return HttpResponse(json.dumps(students, indent=4), content_type='application/json')


    '''
    _______________________________________________________ Post
     <WEBSITE>/api/external_import_grades_test/
    _______________________________________________________
    '''

    def post(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    '''
    _______________________________________________________ Put
     <WEBSITE>/api/external_import_grades_test/, data
    _______________________________________________________
    '''

    def put(self, request, format=None, pk=None):
        return Response(data={
            'status': '406 - Bad Request',
            'result': 'Currently not a feature of SPT'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    
