
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .responses import *
from django.core.serializers import serialize

from copy import copy

import json
# json.load(request):      JSON string     -->     to object
# json.dumps(request):     object          -->     JSON string:
from collections import namedtuple

import ast
import urllib.request
import urllib.parse
#import urllib2 
import requests 

from .models import ( ExternalSite, ExternalSiteToCourse, ExternalSiteToGrade)
from .models import (Course, Grade, Quiz, QuizQuestion, QuizQuestionAnswer, Student, Topic, TopicToCategory)
from .serializers import (ExternalSiteSerializer, ExternalSiteToCourseSerializer, ExternalSiteToGradeSerializer)






'''
______________________________________________________________________________________________      Create Import Grades
create_import_grades: 
______________________________________________________________________________________________
'''
def create_import_grades(externalSite, url_ending, course):  # pragma: no cover This serializer is always valid, but serializer requires is_valid to be called to save() # external.py  

    # Check Link before adding to database
    try:
        # Get Link
        link = externalSite.base_url + url_ending

        # Get JSON of quiz from external API
        try:
            request = requests.get(link)
            data = json.loads(request.content.decode("utf-8"))
        except:
            raise Exception('Failed to get data from link')

        # Check data
        if ('exams' not in data):
            raise Exception('Missing attribute \'exams\'')
        
        # Get Students in course (put here to speed up seach for student email in the for loop below)
        studentsToCourse = StudentToCourse.objects.filter(course= course)
        if not StudentToCourse.exists():
            raise Exception('No students in course')

    except Exception as ex:
        return Response(data={
            'status': '406 - Bad Request',
            'result': str(ex)
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


    # If Valid link, then proceed
    failed_exams = []
    for exam_index, exam in data['exams']:
        
        # Check data
        try:
            # Validate Parameters
            if ( ('topic_name' in exam) and ('students' in exam) and (len(exam['students']) > 0) and ('grade_name' in exam)):
                raise Exception('Improper JSON configuration')
            
            # Get and Validate Topic
            try:
                topic = Topic.objects.get(course= course, name= data['topic_name'])
                topicToCategory = TopicToCategory.objects.get(topic= topic, category__name = 'External Site')
            except Topic.DoesNotExist:
                raise Exception('Topic not in Course')
            except TopicToCategory.DoesNotExist:
                raise Exception('Topic does not have an \'External Site\' category')

        except Exception as ex:
            failed_exams.append( {'exam_index': exam_index, 'reason': str(ex), 'students': []} )
            continue

        # Students in course (put here to speed up search for student email)
        students = studentsToCourse
        failed_students = []


        # For Each Student 
        for index_student, student_external in data['students']:

            if ( ('email' in student_external) and ('grade_value' in student_external) ):
                email = student_external['email']
                grade_value = student_external['grade_value']

                try:
                    # Get and Validate Student
                    try:
                        studentToCourse = students.get(student__email= email)
                    except:
                        raise Exception('Invalid student email: ' + str(email))

                    
                    # create grade
                    grade = Grade.objects.create(
                        name= grade_name,
                        value= grade_value,
                        topic_to_category= topicToCategory,
                        student= studentToCourse
                    )
                    # Save Grade
                    grade.save()
                    # Narrow the search for student emails
                    students.exclude(student__email= email)

                except Exception as ex:
                    failed_students.append( {'student_index': index_student, 'reason': str(ex)} )    
                    # NOTE If the same email is passed in more than once, the repeated email will be logged as an error

            else:
                # If email or grade_value missing
                failed_students.append({'student_index': index_student, 'reason': 'Missing email or grade_value'})
        
        # If failed to add any students
        if ( len(failed_students) > 0 ):
            failed_exams.append( {'exam_index': exam_index, 'reason': str(ex), 'students': failed_students} )


    # Return Valid Response with Data
    return Response({
        'status': '200 - Ok',
        'result': failed_exams,
    }, status=status.HTTP_200_OK)


        



    









'''
______________________________________________________________________________________________      Import Grades
import_grades: 
______________________________________________________________________________________________
'''

def import_grades(externalSitesToCourse, course, studentsToCourse): # pragma: no cover This serializer is always valid, but serializer requires is_valid to be called to save()
    
    failed_sites  = []

    # For Each Link Associated to course
    for externalSiteToCourse in externalSitesToCourse:

        # Validate Link
        try: 
            link = externalSiteToCourse.external_site.base_url + externalSiteToCourse.url_ending

            # Get JSON of quiz from external API
            try:
                request = requests.get(link)
                data = json.loads(request.content.decode("utf-8"))
            except:
                raise Exception('Failed to get data from link')

            # Check data
            if ('exams' not in data):
                raise Exception('Missing attribute \'exams\'')

        except Exception as ex:
            failed_sites.append( { 'site': externalSiteToCourse.__str__ , 'reason': str(ex), 'exams': [] } )
            continue
        
        
        
        # If Valid Link
        failed_exams = []
        for exam_index, exam in data['exams']:
            
            # Check data
            try:
                # Validate Parameters
                if ( ('topic_name' in exam) and ('students' in exam) and (len(exam['students']) > 0) and ('grade_name' in exam)):
                    raise Exception('Improper JSON configuration')
                
                # Get and Validate Topic
                try:
                    topic = Topic.objects.get(course= course, name= data['topic_name'])
                    topicToCategory = TopicToCategory.objects.get(topic= topic, category__name = 'External Site')
                except Topic.DoesNotExist:
                    raise Exception('Topic not in Course')
                except TopicToCategory.DoesNotExist:
                    raise Exception('Topic does not have an \'External Site\' category')

            except Exception as ex:
                failed_exams.append( {'exam_index': exam_index, 'reason': str(ex), 'students': []} )
                continue






            # Get Grades in course associated to topic (put here to speed up for search for grade if grades)
            grade_name = data['grade_name']
            grades = Grade.objects.filter(topic_to_category= topicToCategory, name= grade_name)
            
            # Students in course (put here to speed up search for student email)
            students = studentsToCourse
            failed_students = []




            # For Each Student 
            for index_student, student_external in data['students']:

                if ( ('email' in student_external) and ('grade_value' in student_external) ):
                    email = student_external['email']
                    grade_value = student_external['grade_value']

                    try:
                        # Get and Validate Student
                        try:
                            studentToCourse = students.get(student__email= email)
                        except:
                            raise Exception('Invalid student email: ' + str(email))

                        if grades.exists():
                            # If Grade => Get Grade
                            grade = grades.get(student= student)

                            # Validate grade value
                            if grade_value > 100:
                                grade_value = 100
                            elif grade_value < 0:
                                grade_value = 0

                            # Edit grade value
                            grade.value = grade_value

                            # Save Grade
                            grade.save()
                            
                            # Narrow the search of grades
                            grades.exclude(student__email= email)
                        else:
                            # If no grade => create grade
                            grade = Grade.objects.create(
                                name= grade_name,
                                value= grade_value,
                                topic_to_category= topicToCategory,
                                student= studentToCourse
                            )
                            # Save Grade
                            grade.save()

                        # Narrow the search for student emails
                        students.exclude(student__email= email)

                    except Exception as ex:
                        failed_students.append( {'student_index': index_student, 'reason': str(ex)} )    
                        # NOTE If the same email is passed in more than once, the repeated email will be logged as an error

                else:
                    # If email or grade_value missing
                    failed_students.append({'student_index': index_student, 'reason': 'Missing email or grade_value'})
            

            # If failed to add any students
            if ( len(failed_students) > 0 ):
                failed_exams.append( {'exam_index': exam_index, 'reason': str(ex), 'students': failed_students} )


    # Return Valid Response with Data
    return Response({
        'status': '200 - Ok',
        'result': failed_sites,
    }, status=status.HTTP_200_OK)



