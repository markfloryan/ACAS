from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from .models import *

"""
A Model Serialzier that allows force excluding fields from serialization
The standard exclude meta field does not apply to nested fields
fields specified in force_exclude will not be serialzied even inside nested_fields
"""
class SecureModelSerializer(serializers.ModelSerializer):
    force_exclude = ['id_token','password']

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships using SecureModelSerializer
        """
        class NestedSerializer(SecureModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = '__all__'

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs  

    def get_fields(self):
        fields = super().get_fields()

        # Remove any fields defined by force_exclude to ensure not serialzing them
        for field in self.force_exclude:
            if field in fields:
                del fields[field]

        return fields


class TopicSerializer(SecureModelSerializer):
    class Meta:
        model = Topic
        fields = (
            'pk',
            'name',
            'course',
            'ancestor_weight',
            'locked'
        )


# ASSIGNMENT
# The only currently needed field to create an assignment is a name
class AssignmentSerializer(SecureModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            'pk',
            'name',
            'topic'
        )


class TopicToTopicSerializer(SecureModelSerializer):
    class Meta:
        model = TopicToTopic
        fields = (
            'pk',
            'topic_node',
            'topic_name',
            'course',
            'ancestor_node',
            'ancestor_name',
            'weight',
        )

# We do not use the SecureModelSerialzier here becuase it would not let us serialize id_token which is necessary for creating accounts and loggin in
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
            'join_date',
            'username'
        )


class StudentToTopicSerializer(SecureModelSerializer):
    class Meta:
        model = StudentToTopic
        fields = (
            'pk',
            'course',
            'student',
            'topic',
            'grade',
            'competency'
        )
        depth = 1

# StudentToTopic, but just the student (used to improve performance for student to topic last name queries)
class StudentToTopicSerializerMini(SecureModelSerializer):
    class Meta:
        model = StudentToTopic
        fields = (
            'student',
        )
        depth = 1

class StudentToAssignmentSerializer(SecureModelSerializer):
    class Meta:
        model = StudentToAssignment
        fields = (
            'grade',
            'student',
            'assignment'
        )

class CourseSerializer(SecureModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    #nodes = StudentToTopicSerializer(many=True, read_only=True)
    edges = TopicToTopicSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'pk',
            'name',
            'course_code',
            'subject_code',
            'topics',
            'edges',
            'professor',
        )

class CompetencyThresholdSerializer(SecureModelSerializer):

    course = CourseSerializer(many=False, read_only=True)
    class Meta:
        model = CompetencyThreshold
        fields = (
            'pk',
            'competency_threshold',
            'mastery_threshold',
            'course',
        )

class GradeThresholdSerializer(SecureModelSerializer):

    course = CourseSerializer(many=False, read_only=True)
    class Meta:
        model = GradeThreshold
        fields = (
            'pk',
            'a_plus_mastery',
            'a_plus_competency',
            'a_mastery',
            'a_competency',
            'a_minus_mastery',
            'a_minus_competency',
            
            'b_plus_mastery',
            'b_plus_competency',
            'b_mastery',
            'b_competency',
            'b_minus_mastery',
            'b_minus_competency',
            
            'c_plus_mastery',
            'c_plus_competency',
            'c_mastery',
            'c_competency',
            'c_minus_mastery',
            'c_minus_competency',
            
            'd_plus_mastery',
            'd_plus_competency',
            'd_mastery',
            'd_competency',
            'd_minus_mastery',
            'd_minus_competency',

            'course',
        )

class QuizSerializer(SecureModelSerializer):
    next_open_date = serializers.DateTimeField()
    next_close_date = serializers.DateTimeField()

    class Meta:
        model = Quiz
        fields = (
            'pk',
            'assignment',
            'pool',
            'practice_mode',
            'next_open_date',
            'next_close_date',
        )

    def to_representation(self, instance):
        """Set allow_submissions to a computed valued based on the function is_open"""
        data = super().to_representation(instance)
        data['allow_submissions'] = instance.is_open()
        return data

class StudentToQuizSerializer(SecureModelSerializer):
    class Meta:
        model = StudentToQuiz
        fields = (
            'pk',
            'completed_quiz',
        )

class QuizQuestionSerializer(SecureModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = (
            'pk',
            'quiz',
            'question_type',
            'answered_correct_count',
            'answered_total_count',
            'question_parameters',
        )

    
    def to_representation(self, instance):
        """Don't send the question answer from question_parameters"""
        ret = super().to_representation(instance)
        question_parameters= json.loads(ret['question_parameters'])
        if 'answer' in question_parameters:
            del question_parameters['answer']
            ret['question_parameters'] = json.dumps(question_parameters)
        return ret


class SettingsSerializer(SecureModelSerializer):
    class Meta:
        model = Settings
        fields = (
            'color',
            'nickname',
        )
        depth = 1


class StudentToCourseSerializer(SecureModelSerializer):
    class Meta:
        model = StudentToCourse
        fields = (
            'pk',
            'student',
            'course',
            'grade',
        )
        depth = 1

# Dont include course
# Used for viewing grades on the student roster
class StudentToCourseSlimSerializer(SecureModelSerializer):
    class Meta:
        model = StudentToCourse
        fields = (
            'pk',
            'student',
            'grade',
        )
        depth = 1

# Just the student name, email, and their grade for the course
class StudentToCourseSlimSerializer(SecureModelSerializer):
    class Meta:
        model = StudentToCourse
        fields = (
            'pk',
            'student',
            'course',
            'grade',
        )
        depth = 1


class ResourcesSerializer(SecureModelSerializer):

    class Meta:
        model = Resources
        fields = (
            'pk',
            'name',
            'link',
            'topic'
        )


class ClassGraphSerializer(SecureModelSerializer):
    nodes = StudentToTopicSerializer(many=True, read_only=True)
    edges = TopicToTopicSerializer(many=True, read_only=True)

    class Meta:
        model = StudentToCourse
        fields = (
            'pk',
            'student',
            'course',
            'nodes',
            'edges',
            'grade',
            'letterGrade', # TODO: change serializer to update REST
        )
        depth = 2
