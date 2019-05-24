from django.contrib import admin
# Register your models here.
from .models import Course, Quiz,Grade, Category, TopicToCategory, QuizQuestion, QuizQuestionAnswer, Resources, Settings, Student, StudentToCourse, StudentToQuiz, StudentToQuizQuestion, StudentToTopic, Topic, TopicToTopic
from .models import ExternalSite, ExternalSiteToCourse, ExternalSiteToGrade


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(ExternalSite) 
admin.site.register(ExternalSiteToCourse) 
admin.site.register(ExternalSiteToGrade)
admin.site.register(Grade)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizQuestionAnswer)
admin.site.register(Resources)
admin.site.register(Settings)
admin.site.register(Student)
admin.site.register(StudentToQuiz)
admin.site.register(StudentToQuizQuestion)
admin.site.register(StudentToTopic)
admin.site.register(StudentToCourse)
admin.site.register(Topic)
admin.site.register(TopicToTopic)
admin.site.register(TopicToCategory)
