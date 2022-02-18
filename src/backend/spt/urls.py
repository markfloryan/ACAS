"""spt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from sptApp import api_views
from rest_framework import routers

# View sets have default methods for handling GET/POST/etc, so this is explicitly overriding that
request_override_map = {
    'get': 'get',
    'post': 'post',
    'put': 'put',
    'delete': 'delete'
}

# Allows overriding of specifically the delete functionality for the StudentToAssignment model
request_override_map_delete = {
    'delete': 'delete'
}

gitpull = api_views.gitPull
course_list = api_views.CourseViewSet.as_view(request_override_map)
competency_threshold_list = api_views.CompetencyThresholdViewSet.as_view(request_override_map)
grade_threshold_list = api_views.GradeThresholdViewSet.as_view(request_override_map)
section_list = api_views.SectionViewSet.as_view(request_override_map)
student_list = api_views.StudentViewSet.as_view(request_override_map)
topic_list = api_views.TopicViewSet.as_view(request_override_map)
student_to_topic_list = api_views.StudentToTopicViewSet.as_view(request_override_map)
topic_to_topic_list = api_views.TopicToTopicViewSet.as_view(request_override_map)
resources_list = api_views.ResourcesViewSet.as_view(request_override_map)
settings_list = api_views.SettingsViewModel.as_view(request_override_map)
student_to_course_list = api_views.StudentToCourseViewSet.as_view(request_override_map)
student_to_section_list = api_views.StudentToSectionViewSet.as_view(request_override_map)
student_progress_list = api_views.studentProgress
student_to_topic_list = api_views.StudentToTopicViewSet.as_view(request_override_map)
topic_to_topic_list = api_views.TopicToTopicViewSet.as_view(request_override_map)
assignment_list = api_views.AssignmentViewSet.as_view(request_override_map)
quiz_list = api_views.QuizViewSet.as_view(request_override_map)
quiz_question_list = api_views.QuizQuestionViewSet.as_view(request_override_map)
quiz_interface = api_views.QuizInterfaceViewSet.as_view(request_override_map)
question_file_upload = api_views.questionFileUpload
course_roster_upload = api_views.CourseRosterUpload.as_view(request_override_map)
course_grades_upload = api_views.courseGradesUpload
course_gradescope_upload = api_views.courseGradescopeUpload
course_assignment_upload = api_views.assignmentUpload
# assignment_quiz_upload = api_views.assignmentQuizUpload - commented out as we are no longer doing csv uploads for quizzes
students_in_topic = api_views.CourseTopicToStudentViewSet.as_view(request_override_map)
search_list = api_views.SearchViewSet.as_view(request_override_map)
student_to_assignment_list = api_views.StudentToAssignmentViewSet.as_view(request_override_map_delete)

router = routers.DefaultRouter()
# Allows RestAPI support for studentToAssignments objects
router.register(r'studenttoassignments', api_views.StudentToAssignmentViewSet,'studenttoassignments')




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/gitpull/', gitpull, name='git-pull'),
    

    # Courses
    url(r'^api/courses/(?P<pk>[0-9]+)/competency-threshold', competency_threshold_list, name='course-competency-threshold'),
    url(r'^api/courses/(?P<pk>[0-9]+)/grade-threshold', grade_threshold_list, name='grade-competency-threshold'),
    url(r'^api/courses/(?P<pk>[0-9]+)/graph-data', api_views.CourseViewSet.as_view(
        {"get": "graph_data"}
    ), name='course-graph-data'),
    url(r'^api/courses/(?P<pk>[0-9]+)', course_list, name='course-detail'),
    url(r'^api/courses/', course_list, name='course-list'),

    # Sections
    url(r'^api/sections/(?P<pk>[0-9]+)', section_list, name='section-detail'),
    url(r'^api/sections/', section_list, name='section-list'),

    #search and students
    url(r'^api/search/', search_list, name='search-detail'),
    url(r'^api/students/(?P<pk>[0-9]+)', student_list, name='student-detail'),
    url(r'^api/students/', student_list, name='student-list'),

    url(r'^api/courseRosterUpload/(?P<coursePk>[0-9]+)', course_roster_upload, name='course-roster-upload'),
    url(r'^api/courseGradesUpload/(?P<pk>[0-9]+)', course_grades_upload, name='course-grades-upload'),
    url(r'^api/courseGradescopeUpload/(?P<pk>[0-9]+)', course_gradescope_upload, name='course-gradescope-upload'),
    
    url(r'^api/courseAssignmentUpload/(?P<pk>[0-9]+)', course_assignment_upload, name='course-assignment-upload'),
    #url(r'^api/assignmentQuizUpload/(?P<pk>[0-9]+)', assignment_quiz_upload, name='assignment-quiz-upload'), - commented out as we are no longer doing csv quiz uploads

    # url(r'^api/professors/', professor_list, name='professor-list'),
    # url(r'^api/professors/(?P<pk>[0-9]+)',
    #     professor_list, name='professor-detail'),

    url(r'^api/topics/(?P<pk>[0-9]+)', topic_list, name='topic-detail'),
    url(r'^api/topics/', topic_list, name='topic-list'),

    url(r'^api/student/course/(?P<pk>[0-9]+)/progress',
        student_progress_list, name='student-progress'),
    url(r'^api/student/course/(?P<pk>[0-9]+)',
        student_to_course_list, name='student-to-course-detail'),
    url(r'^api/student/course/', student_to_course_list,
        name='student-to-course-list'),

    url(r'^api/student/section/(?P<pk>[0-9]+)', student_to_section_list, name='student-to-section-detail'),
    url(r'^api/student/section/', student_to_section_list, name='student-to-section-list'),

    # url(r'^api/student/quiz/(?P<pk>[0-9]+)',
    #     student_to_quiz_list, name='student-to-quiz-detail'),
    # url(r'^api/student/quiz/', student_to_quiz_list, name='student-to-quiz-list'),

    url(r'^api/student/topics/(?P<course_id>[0-9]+)/(?P<student_id>[0-9]+)',
        student_to_topic_list, name='student-to-topic-detail'),
    url(r'^api/student/topics/(?P<topic_id>[0-9]+)', student_to_topic_list,
        name='student-to-topic-topics'),
    url(r'^api/student/topics/', student_to_topic_list,
        name='student-to-topic-list'),

    url(r'^api/topic/topics/(?P<pk>[0-9]+)',
        topic_to_topic_list, name='topic-to-topic-detail'),
    url(r'^api/topic/topics/', topic_to_topic_list, name='topic-to-topic-list'),

    url(r'^api/resources/(?P<pk>[0-9]+)',
        resources_list, name='resources-detail'),
    url(r'^api/resources/', resources_list, name='resources-list'),

    # ********************************************************************************************************  External API

    #

    # ********************************************************************************************************

    # Settings
    url(r'^api/settings/(?P<pk>[0-9]+)', settings_list),
    url(r'^api/settings/', settings_list),

    # # Quiz
    url(r'^api/quizzes/(?P<pk>[0-9]+)', quiz_list, name='quiz-detail'),
    url(r'^api/quizzes/', quiz_list, name='quiz-list'),

    # Quiz Question
    # url(r'^api/quiz-questions/(?P<pk>[0-9]+)',
    #     quiz_question_list, name='student-to-quiz-detail'),
    url(r'^api/quiz-questions/(?P<pk>[0-9]+)', quiz_question_list, name='quiz-question-detail'),
    url(r'^api/quiz-questions/', quiz_question_list, name='quiz-question-list'),
    url(r'^api/questionFileUpload/(?P<pk>[0-9]+)', question_file_upload, name="question-file-upload"),
    # Submit Quiz Question
    url(r'^api/quiz-interface/(?P<pk>[0-9]+)', quiz_interface, name='quiz-interface'),
    
    # Student to Quiz    
    # url(r'^api/student/quiz/(?P<pk>[0-9]+)',
        # student_to_quiz_list, name='student-to-quiz-detail'),
    # url(r'^api/student/quiz/', student_to_quiz_list, name='student-to-quiz-list'),

    # Get a list of students in a course for a topic
    url(r'^api/coursetopictostudent/(?P<course_pk>[0-9]+)/(?P<topic_pk>[0-9]+)',
        students_in_topic, name='get-student-in-topic'),
    
    # Assignment
    url(r'^api/assignments/(?P<pk>[0-9]+)',
        assignment_list, name='assignment-detail'),
    url(r'^api/assignments',
        assignment_list, name='assignment-list'),

    # RestAPI support
    path('api/', include(router.urls)),

    # Student to Assignment (delete functionality)
    url(r'api/studenttoassignments/(?P<studentpk>[0-9]+)/(?P<assignmentpk>[0-9]+)',
        student_to_assignment_list, name='student-to-assignment-list'),
]
