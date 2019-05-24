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
______________________________________________________________________________________________      Grades - Good
______________________________________________________________________________________________
'''
def grades_good():  # pragma: no cover
    return {
        'exams': [{
            'topic_name': 'Arrays',
            'grade_name': 'External Site Grade',
            'students': [
                {
                    'email': 'das5fa@virginia.edu',
                    'grade_value': 90
                },
                {
                    'email': 'ceb4aq@virginia.edu',
                    'grade_value': 101
                },
                {
                    'email': 'abs4cr@virginia.edu',
                    'grade_value': -1
                },
                {
                    'email': 'smm2zr@virginia.edu',
                    'grade_value': 100
                },
                {
                    'email': 'lsm5fm@virginia.edu',
                    'grade_value': 0
                }

            ]
        }]
    }




'''
______________________________________________________________________________________________      Grades - Missing exams
______________________________________________________________________________________________
'''
def grades_missing_exams():
    return {
        
    }


'''
______________________________________________________________________________________________      Grades - Missing topic_name
______________________________________________________________________________________________
'''
def grades_missing_topicName():
    return {
        'exams': [{
            'grade_name': 'External Site Grade',
            'students': [
                {
                    'email': 'das5fa@virginia.edu',
                    'grade_value': 90
                },
                {
                    'email': 'ceb4aq@virginia.edu',
                    'grade_value': 101
                },
                {
                    'email': 'abs4cr@virginia.edu',
                    'grade_value': -1
                },
                {
                    'email': 'smm2zr@virginia.edu',
                    'grade_value': 100
                },
                {
                    'email': 'lsm5fm@virginia.edu',
                    'grade_value': 0
                }

            ]
        }]
    }


'''
______________________________________________________________________________________________      Grades - Missing grade_name
______________________________________________________________________________________________
'''
def grades_missing_gradeName():
    return {
        'exams': [{
            'topic_name': 'Arrays',
            'students': [
                {
                    'email': 'das5fa@virginia.edu',
                    'grade_value': 90
                },
                {
                    'email': 'ceb4aq@virginia.edu',
                    'grade_value': 101
                },
                {
                    'email': 'abs4cr@virginia.edu',
                    'grade_value': -1
                },
                {
                    'email': 'smm2zr@virginia.edu',
                    'grade_value': 100
                },
                {
                    'email': 'lsm5fm@virginia.edu',
                    'grade_value': 0
                }

            ]
        }]
    }

'''
______________________________________________________________________________________________      Grades - Missing students
______________________________________________________________________________________________
'''
def grades_missing_students():
    return {
        'exams': [{
            'topic_name': 'Arrays',
            'grade_name': 'External Site Grade',
        }]
    }



'''
______________________________________________________________________________________________      Grades - Missing email
______________________________________________________________________________________________
'''
def grades_missing_email():
    return {
        'exams': [{
            'topic_name': 'Arrays',
            'grade_name': 'External Site Grade',
            'students': [
                {
                    'grade_value': 90
                },
                {
                    'grade_value': 101
                },
                {
                    'grade_value': -1
                },
                {
                    'grade_value': 100
                },
                {
                    'grade_value': 0
                }

            ]
        }]
    }

'''
______________________________________________________________________________________________      Grades - Missing grade_value
______________________________________________________________________________________________
'''
def grades_missing_gradeValue():
    return {
        'exams': [{
            'topic_name': 'Arrays',
            'grade_name': 'External Site Grade',
            'students': [
                {
                    'email': 'das5fa@virginia.edu'
                },
                {
                    'email': 'ceb4aq@virginia.edu'
                },
                {
                    'email': 'abs4cr@virginia.edu'
                },
                {
                    'email': 'smm2zr@virginia.edu'
                },
                {
                    'email': 'lsm5fm@virginia.edu'
                }

            ]
        }]
    }


