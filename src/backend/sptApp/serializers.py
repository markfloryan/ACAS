from rest_framework import serializers
from .models import Course, Quiz, QuizQuestion, QuizQuestionAnswer, Resources, Settings, Student, StudentToCourse, StudentToQuiz, StudentToQuizQuestion, StudentToTopic, Topic, TopicToTopic, Grade, Category, TopicToCategory
from .models import ExternalSite, ExternalSiteToCourse, ExternalSiteToGrade 

# Serializer: converts model to JSON data


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            'pk',
            'name',
            'course',
            'ancestor_weight'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class GradeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Grade
        fields = (
            'pk',
            'name',
            'value',
            'topic_to_category',
            'category',
            'student',
            'weight'
        )


class TopicToCategorySerializer(serializers.ModelSerializer):
    grades = GradeSerializer(many=True, read_only=True)

    class Meta:
        model = TopicToCategory
        fields = (
            'pk',
            'topic',
            'category',
            'weight',
            'grades'
        )


class TopicToTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicToTopic
        fields = (
            'pk',
            'topic_node',
            'course',
            'ancestor_node',
            'ancestor_name',
            'weight',
        )


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'pk',
            'first_name',
            'last_name',
            'email',
            'id_token',
            'is_professor',
            'join_date'
        )


class StudentToTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToTopic
        fields = (
            'pk',
            'course',
            'student',
            'topic',
            'grade',
            'locked'
        )
        depth = 1


class CourseSerializer(serializers.ModelSerializer):
    nodes = StudentToTopicSerializer(many=True, read_only=True)
    edges = TopicToTopicSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'pk',
            'name',
            'course_code',
            'subject_code',
            'nodes',
            'edges',
            'professor'
        )


class QuizQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestionAnswer
        fields = (
            'pk',
            'text',
            'correct',  # TODO: FIGURE OUT WAY TO CONDITIONALLY SHOW THIS FOR PROFESSOR REQUESTS
            'question',
            'index'
        )


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizQuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = (
            'pk',
            'text',
            'question_type',
            'total_points',
            'index',
            'answers'
        )


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = (
            'color',
            'nickname',
        )
        depth = 1


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)
    
    class Meta:
        model = Quiz
        fields = (
            'pk',
            'name',
            'topic',
            'questions',
            'weight'
        )
        depth = 2


class StudentToCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToCourse
        fields = (
            'pk',
            'student',
            'course'
        )
        depth = 1


class StudentToQuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToQuizQuestion
        fields = (
            'pk',
            'student',
            'question',
            'answer',
            'correct'
        )


class StudentToQuizSerializer(serializers.ModelSerializer):
    # questions = StudentToQuizQuestionSerializer(many=True)
    student_answers = StudentToQuizQuestionSerializer(many=True)
    quiz = QuizSerializer()

    class Meta:
        model = StudentToQuiz
        fields = (
            'pk',
            'student',
            'quiz',
            'grade',
            'student_answers'
        )
        depth = 5


class ResourcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resources
        fields = (
            'pk',
            'name',
            'link',
            'topic'
        )


'''
______________________________________________________________________________________________      External Sites 
 ExternalSiteSerializer
______________________________________________________________________________________________
'''
class ExternalSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSite
        fields = (
            'pk',
            'name',
            'base_url'
        )
        depth = 1


class ExternalSiteToCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSiteToCourse
        fields = (
            'pk',
            'course',
            'external_site',
            'url_ending'
        )
        depth = 2


class ExternalSiteToGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSiteToGrade
        fields = (
            'pk',
            'external_site',
            'grade',
            'link'
        )


class ClassGraphSerializer(serializers.ModelSerializer):
    nodes = StudentToTopicSerializer(many=True, read_only=True)
    edges = TopicToTopicSerializer(many=True, read_only=True)

    class Meta:
        model = StudentToCourse
        fields = (
            'pk',
            'student',
            'course',
            'nodes',
            'edges'
        )
        depth = 2
