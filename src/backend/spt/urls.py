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
from sptApp import api_views, views

# View sets have default methods for handling GET/POST/etc, so this is explicitly overriding that
request_override_map = {
    'get': 'get',
    'post': 'post',
    'put': 'put',
    'delete': 'delete'
}

course_list = api_views.CourseViewSet.as_view(request_override_map)
student_list = api_views.StudentViewSet.as_view(request_override_map)
topic_list = api_views.TopicViewSet.as_view(request_override_map)
student_to_topic_list = api_views.StudentToTopicViewSet.as_view(
    request_override_map)
topic_to_topic_list = api_views.TopicToTopicViewSet.as_view(
    request_override_map)
resources_list = api_views.ResourcesViewSet.as_view(request_override_map)
settings_list = api_views.SettingsViewModel.as_view(request_override_map)
grade_list = api_views.GradeViewSet.as_view(request_override_map)
category_list = api_views.CategoryViewSet.as_view(request_override_map)
topic_to_category_list = api_views.TopicToCategoryViewSet.as_view(
    request_override_map)
student_to_course_list = api_views.StudentToCourseViewSet.as_view(
    request_override_map)
student_to_quiz_list = api_views.StudentToQuizViewSet.as_view(
    request_override_map)
student_to_topic_list = api_views.StudentToTopicViewSet.as_view(
    request_override_map)
topic_to_topic_list = api_views.TopicToTopicViewSet.as_view(
    request_override_map)
quiz_list = api_views.QuizViewSet.as_view(request_override_map)
quiz_question_list = api_views.QuizQuestionViewSet.as_view(
    request_override_map)
quiz_question_answer_list = api_views.QuizQuestionAnswerViewSet.as_view(
    request_override_map)

external_import_grades = api_views.ExternalImportGradesViewSet.as_view(request_override_map)
external_sites = api_views.ExternalSiteViewSet.as_view(request_override_map)
external_sites_to_course = api_views.ExternalSiteToCourseViewSet.as_view(request_override_map)
external_sites_to_grade = api_views.ExternalSiteToGradeViewSet.as_view(request_override_map)
external_import_grades_test = api_views.ExternalImportGradesTestViewSet.as_view(request_override_map)

update_class_grade = views.update_class_grades
students_in_topic = api_views.CourseTopicToStudentViewSet.as_view(request_override_map)

search_list = api_views.SearchViewSet.as_view(
    request_override_map)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Courses - FIXED
    url(r'^api/courses/(?P<pk>[0-9]+)', course_list, name='course-detail'),
    url(r'^api/courses/', course_list, name='course-list'),
    url(r'^api/courses/(?P<pk>[0-9]+)/graph-data', api_views.CourseViewSet.as_view(
        {"get": "graph_data"}
    ), name='course-graph-data'),

    #search and students
    url(r'^api/search/', search_list, name='search-detail'),
    url(r'^api/students/', student_list, name='student-list'),
    
    # url(r'^api/professors/', professor_list, name='professor-list'),
    # url(r'^api/professors/(?P<pk>[0-9]+)',
    #     professor_list, name='professor-detail'),
    
    url(r'^api/topics/(?P<pk>[0-9]+)', topic_list, name='topic-detail'),
    url(r'^api/topics/', topic_list, name='topic-list'),
    
    url(r'^api/student/course/(?P<pk>[0-9]+)',
        student_to_course_list, name='student-to-quiz-detail'),
    url(r'^api/student/course/', student_to_course_list,
        name='student-to-quiz-list'),
    
    url(r'^api/student/quiz/(?P<pk>[0-9]+)',
        student_to_quiz_list, name='student-to-quiz-detail'),
    url(r'^api/student/quiz/', student_to_quiz_list, name='student-to-quiz-list'),
    
    url(r'^api/student/topics/(?P<class_id>[0-9]+)/(?P<student_id>[0-9]+)',
        student_to_topic_list, name='student-to-topic-detail'),
    url(r'^api/student/topics/', student_to_topic_list,
        name='student-to-topic-list'),
    
    url(r'^api/topic/topics/(?P<pk>[0-9]+)',
        topic_to_topic_list, name='topic-to-topic-detail'),
    url(r'^api/topic/topics/', topic_to_topic_list, name='topic-to-topic-list'),
    
    url(r'^api/resources/(?P<pk>[0-9]+)',
        resources_list, name='resources-detail'),
    url(r'^api/resources/', resources_list, name='resources-list'),
    
    # ********************************************************************************************************  External API

    url(r'^api/external_import_grades/(?P<pk>[0-9]+)',external_import_grades),
    url(r'^api/external_import_grades/',external_import_grades),

    
    url(r'^api/external_sites/(?P<pk>[0-9]+)',external_sites),
    url(r'^api/external_sites/',external_sites),
    
    url(r'^api/external_sites_to_course/(?P<pk>[0-9]+)',external_sites_to_course),
    url(r'^api/external_sites_to_course/',external_sites_to_course),
    
    url(r'^api/external_sites_to_grade/(?P<pk>[0-9]+)',external_sites_to_grade),
    url(r'^api/external_sites_to_grade/',external_sites_to_grade),

    url(r'^api/external_import_grades_test/(?P<pk>[0-9]+)',external_import_grades_test),
    url(r'^api/external_import_grades_test/',external_import_grades_test),

    # ********************************************************************************************************

    # Settings
    url(r'^api/settings/(?P<pk>[0-9]+)', settings_list),
    url(r'^api/settings/', settings_list),

    # Quiz
    url(r'^api/quiz/(?P<pk>[0-9]+)', quiz_list, name='quiz-detail'),
    url(r'^api/quiz/', quiz_list, name='quiz-list'),

    # Quiz Question
    url(r'^api/quiz-question/(?P<pk>[0-9]+)',
        quiz_question_list, name='student-to-quiz-detail'),
    url(r'^api/quiz-question/', quiz_question_list, name='student-to-quiz-list'),

    # Quiz Question Answer
    url(r'^api/quiz-question-answer/(?P<pk>[0-9]+)',
        quiz_question_answer_list, name='student-to-quiz-detail'),
    url(r'^api/quiz-question-answer/',
        quiz_question_answer_list, name='student-to-quiz-list'),

    # Grades - FIXED
    url(r'^api/grades/(?P<course_pk>[0-9]+)/(?P<topic_pk>[0-9]+)/(?P<category_pk>[A-z]+)',
        grade_list, name='grade-detail'),
    url(r'^api/grades/(?P<course_pk>[0-9]+)/(?P<topic_pk>[0-9]+)',
        grade_list, name='grade-detail'),
    url(r'^api/grades/(?P<course_pk>[0-9]+)',
        grade_list, name='grade-detail'),

    # Get the total grade for a class
    url(r'^api/class_grades/(?P<class_pk>[0-9]+)/(?P<student_pk>[0-9]+)',
        update_class_grade, name='update-class-grades'),

    # Get a list of students in a course for a topic
    url(r'^api/coursetopictostudent/(?P<course_pk>[0-9]+)/(?P<topic_pk>[0-9]+)',
        students_in_topic, name='get-student-in-topic'),

    # Category
    url(r'^api/categories/(?P<pk>[A-z]+)',
        category_list, name='category-detail'),
    url(r'^api/categories',
        category_list, name='category-list'),

    # Topic to Category
    url(r'^api/topic/category/(?P<topic_pk>[0-9]+)/(?P<category_pk>[A-z]+)',
        topic_to_category_list, name='topic-to-category-detail'),
    url(r'^api/topic/category/(?P<topic_pk>[0-9]+)/',
        topic_to_category_list, name='topic-to-category-detail'),
    url(r'^api/topic/category',
        topic_to_category_list, name='topic-to-category-list'),

]
