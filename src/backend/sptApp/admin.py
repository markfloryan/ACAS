from django.contrib import admin
# Register your models here.
from .models import *

def associated_course(obj):
    if isinstance(obj, Assignment):
        return Course.objects.get(topics__topic_assignment=obj)
    elif isinstance(obj, Quiz):
        return Course.objects.get(topics__topic_assignment__quiz_assignment=obj)
    elif isinstance(obj, QuizQuestion):
        return Course.objects.get(topics__topic_assignment__quiz_assignment__question_quiz=obj)
    elif isinstance(obj, Resources):
        return Course.objects.get(topics__resources=obj)
    elif isinstance(obj, StudentToAssignment):
        return Course.objects.get(topics__topic_assignment__assignment=obj)
    return "Unknown"

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name','topic','weight',associated_course]
    list_filter = ('topic__course__name','topic',)

class CompetencyThresholdAdmin(admin.ModelAdmin):
    list_display = ['course','competency_threshold','mastery_threshold']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['__str__','professor']

class GradeThresholdAdmin(admin.ModelAdmin):
    pass

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz',associated_course,'question_type','question_parameters']

class QuizAdmin(admin.ModelAdmin):
    list_display = ['assignment',associated_course,'pool','allow_resubmissions','practice_mode','is_open','next_open_date','next_close_date']

class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'topic', associated_course]

class StudentToAssignmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'grade', associated_course]
    list_filter = ('assignment__topic__course__name',)
    search_fields = ['assignment__name','assignment__topic__name','assignment__name','student__email','student__first_name','student__last_name']


class StudentToCourseAdmin(admin.ModelAdmin):
    list_display = ['student','course','letterGrade']
    list_filter = ('course__name','letterGrade',)
    search_fields = ['student__email','student__first_name','student__last_name']

class StudentToQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['student','quiz_question','correct','num_submissions']
    list_filter = ('correct','quiz_question',)

class StudentToQuizAdmin(admin.ModelAdmin):
    list_display = ['student','quiz','grade']

class StudentToTopicAdmin(admin.ModelAdmin):
    list_display = ['student','topic','competency','course']
    list_filter = ('topic__course__name','topic',)
    search_fields = ['student__email','student__first_name','student__last_name']

class TopicToTopicAdmin(admin.ModelAdmin):
    list_display = ['__str__','course']
    list_filter = ('course__name',)
    search_fields = ['topic_node__name','ancestor_node__name']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name','course','locked']
    list_filter = ('course__name',)
    search_fields = ['name']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['email','first_name','last_name','username','is_professor']
    list_filter = ('is_professor'),
    search_fields = ['email','first_name','last_name','username',]

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CompetencyThreshold, CompetencyThresholdAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(GradeThreshold, GradeThresholdAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Resources, ResourcesAdmin)
admin.site.register(Settings)
admin.site.register(StudentToAssignment, StudentToAssignmentAdmin)
admin.site.register(StudentToCourse, StudentToCourseAdmin)
admin.site.register(StudentToQuizQuestion, StudentToQuizQuestionAdmin)
admin.site.register(StudentToQuiz, StudentToQuizAdmin)
admin.site.register(StudentToTopic, StudentToTopicAdmin)
admin.site.register(TopicToTopic, TopicToTopicAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Student, StudentAdmin) # Note: appears as 'Users' in the admin page