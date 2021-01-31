from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone
from django.db.models.signals import post_save, post_init
from django.db.models import Min
import json, random

# How users and superusers are created
# Some help from https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4


"""
PREFERRED DATABASE STRUCTURE
** = unsure
User(user_id, first_name, last_name, email, **username, **encrypted_password, profile_picture)
Course(course_id, course_name, course_department, course_number)
ProfessorToCourse(user_id, course_id) //For professor users
StudentToCourse(user_id, course_id, grade) //For student users

Topic(foreign course_id, topic_id, topic_name)
TopicToTopic(topic_id, parent_topic_id) //For course graph
StudentToTopic(foreign user_id, foreign topic_id, grade)

********* (really iffy on the whole quiz system right now. Not to be implemented until later so put on backlog)
Quiz(foreign topic_id, QuestionPoolType1, QuestionPoolType2, QuestionPoolType3, numType1, numType2, numType3)
QuizQuestion(foreign topic_id, question_type, question_id, question, answer)
StudentToQuiz(foreign user_id, foreign topic_id, grade)
"""


'''
______________________________________________________________________________________________      Custom Account Manger
 CustomAccountManager
______________________________________________________________________________________________
'''
""" Used to create a new user and super user. Because we are using a custom model, this code had to be written
to take into account the lack of a password and unique username """


class CustomAccountManager(BaseUserManager):  # pragma: no cover

    # Creating the user
    def create_user(self, email, first_name, last_name, password):
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    # Creating the superuser

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_ket(self, email_):
        return self.get(email=email_)


"""
______________________________________________________________________________________________
 STUDENT (USER)
 User(user_id, first_name, last_name, email, join_date, id_token)

 The core class for all users of the system. The previous system was planning on making
 separate classes for each type of user, but that is really unnecessary, as the only things
 that change are permissions, which can be done with a simple check. Therefore, we are
 going for a simple enumeration of Student, Professor, or TA, which allows for more types later.
______________________________________________________________________________________________
"""
""" Student Model: used as the default user. The USERNAME field is the default and is used to log a user in.
The username is the email. """


class Student(AbstractUser):
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    join_date = models.DateTimeField(auto_now=True)
    id_token = models.CharField(max_length=5000, blank=True, null=True)

    is_professor = models.BooleanField(default=False)

    # TODO: Username is not just used for superuser. It is included in the CSV uploads
    # For creating a superuser
    username = models.CharField(blank=True, null=True, max_length=150)
    password = models.CharField(_('password'), max_length=128, blank=True, null=True)

    def get_id(self):
        return self.id_token

    def get_is_professor(self):
        return self.is_professor

    def get_is_staff(self):
        return self.is_staff

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def get_name(self):
        name = ""
        if self.first_name is not None:
            name += self.first_name
        if self.last_name is not None:
            if self.first_name is not None:
                name += " "
            name += self.last_name

        return name


"""
______________________________________________________________________________________________
 COURSE
 Course(course_id, course_name, course_department, course_number, professor)

 Courses are the center-point of the entire application. Everything stems from it effectively.
 Users either teach or take courses, and Courses teach a variety of Topics.
______________________________________________________________________________________________
"""


class Course(models.Model):
    name = models.CharField(max_length=250)

    course_code = models.CharField(max_length=250)
    subject_code = models.CharField(max_length=250)

    professor = models.ForeignKey(
        Student, related_name='professor', on_delete=models.CASCADE, blank=True, default="0")

    teaching_assistants = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.subject_code + " " + self.course_code + " " + self.name



"""
______________________________________________________________________________________________
 STUDENT TO COURSE
 StudentToCourse(user_id, course_id, semester, year, grade) //For student users
______________________________________________________________________________________________
"""


# TODO: Consider Section model

class StudentToCourse(models.Model):
    student = models.ForeignKey(
        Student, related_name='student', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='courses', on_delete=models.CASCADE)
    semester = models.CharField(max_length=250, null=True, blank=True)

    grade = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    letterGrade = models.CharField(max_length=2, default='?')

    def set_grade(self, val):
        grade = val

    def get_grade(self):
        return grade

    def nodes(self):
        student_to_topics = StudentToTopic.objects.filter(
            student=self.student, course=self.course
        )

        return student_to_topics

    def edges(self):
        topic_to_topics = TopicToTopic.objects.filter(
            course=self.course
        )

        return topic_to_topics

    def __str__(self):
        return self.student.__str__() + " is taking " + self.course.__str__()


"""
______________________________________________________________________________________________
 TOPIC
 Topic(foreign course_id, topic_id, topic_name)

 One node in a course graph. Contains a name, resources for practice, homework, and quizzes.
______________________________________________________________________________________________
"""


class Topic(models.Model):
    # Topics within a course should have a unique name
    name = models.CharField(max_length=250)
    course = models.ForeignKey(Course, related_name='topics', on_delete=models.CASCADE)
    ancestor_weight = models.FloatField(
        null=True,
        blank=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


"""
______________________________________________________________________________________________
 STUDENT TO TOPIC
 StudentToTopic(foreign user_id, foreign topic_id, grade)
______________________________________________________________________________________________
"""


class StudentToTopic(models.Model):
    course = models.ForeignKey(
        Course, related_name='nodes', on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    COMPETENCY_SCALE = (
        (0, 'Incomplete'),
        (1, 'Competency'),
        (2, 'Mastery'),
    )
    competency = models.IntegerField(default=0, choices=COMPETENCY_SCALE)
    grade = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.student.__str__() + " is in " + self.topic.__str__()

    def get_competency(self):
        if self.grade < 0.50:
            self.competency = 0
        elif self.grade < 0.75:
            self.competency = 1
        else:
            self.competency = 2
        return self.competency

    # Get competency as the string defined by COMPETENCY_SCALE
    def get_competency_str(self):
        return self.COMPETENCY_SCALE[self.competency][1]


    def get_topics(self, course_id, student_id):
        student = Student.objects.get(pk=student_id)
        course = Course.objects.get(pk=course_id)

        topics = self.objects.filter(
            student=student,
            course=course
        )

        return topics

    def get_studentToTopics_of_topic(self, topic_id, query=None):

        if query == None:
            return []
            
        studentsToTopics = self.objects.filter(
            topic_id = topic_id,
            student__last_name__icontains = query # If query is provided, limit results to only include students with that last name
        )[:10]

        return studentsToTopics


    def save(self, *args, **kwargs):
        if self.course is None:
            self.course = self.topic.course
        super(StudentToTopic, self).save(*args, **kwargs)

    # course = models.ForeignKey(Course, on_delete=models.CASCADE, default=self.course_default)


"""
______________________________________________________________________________________________
 ASSIGNMENT
 Assignments are related many-to-one with a topic. In addition, each student enrolled in
 a class will have a StudentToAssignment relationship with each assignment.

 Assignments are currently being implemented as a superclass for various tasks that can be
 done within a topic, and are replacing the planned functionality of Categories
______________________________________________________________________________________________
"""

# Currently just a name and an identifying topic.
# TODO: Figure out what other functionality this needs
class Assignment(models.Model):
    name = models.CharField(max_length = 250,default="Assignment")
    topic = models.ForeignKey(Topic,related_name='topic_assignment',on_delete=models.CASCADE, default=None)
    weight = models.IntegerField(default=1)

    def __str__(self):
        # return self.name
        return self.topic.name + " - " + self.name

# This relationship is currently just a grade
# TODO: In the future, should keep track of other metadata such as number of submissions,
# last submission date, received_new_feedback, etc like you would see in UVA Collab.
class StudentToAssignment(models.Model):
    grade = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    previous_grade = None # Store previous grade so that grade cascading can occur after grade changes
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='assignment', on_delete=models.CASCADE)

    def __str__(self):
        return self.student.email + ", " + self.assignment.name


"""
______________________________________________________________________________________________
 QUIZ
______________________________________________________________________________________________
"""

'''
callable for initializing @pool
'''
def quiz_jason_default():
    return dict({"parsons": 0, "multiple_choice": 0, "select_all": 0, "free_response": 0})

class Quiz(models.Model):
    assignment = models.OneToOneField(Assignment, related_name='quiz_assignment', on_delete=models.CASCADE, default=None)

    # Need to manually convert to and from JSON
    pool = models.CharField(max_length=2048, default=json.dumps(quiz_jason_default()))

    allow_resubmissions = models.BooleanField(default=True)
    practice_mode = models.BooleanField(default=False)
    next_open_date = models.DateTimeField(default=datetime.now)
    next_close_date = models.DateTimeField(default=datetime.now)

    # Validate the json when updating the Quiz in a django form (such as the admin page)
    def clean(self):
        super().clean()
        try:
            json.loads(self.pool)
        except:
            raise ValidationError(_('Invalid JSON'))

    # The number of questions defined by the pool json
    # Note: a quiz pool might contain more questions than are defined by the pool json
    # E.g. a quiz pool might contain 20 questions but the pool json says to only pull 10 for the quiz. In this example, this function would return 10.
    def get_num_questions(self):
        num = 0
        try:
            pool = json.loads(self.pool)
            num += pool['parsons']
            num += pool['multiple_choice']
            num += pool['select_all']
            num += pool['free_response']
        except:
            print("Invalid json")
        
        return num

    # Returns true if the current time is between the open and close dates
    def is_open(self):
        now = datetime.now(timezone.utc)
        return (now > self.next_open_date and now < self.next_close_date)
    is_open.boolean = True # Tells django admin that this is function is a boolean function
        

    def __str__(self):
        return "Quiz for " + self.assignment.__str__()



"""
______________________________________________________________________________________________
 QUIZ QUESTION
______________________________________________________________________________________________
"""

'''
callable for initializing @pool
'''
def quiz_question_jason_default():
    return dict({
        "question": "Which is correct?",
        "choices": [
            "a",
            "b",
            "c",
            "d"
        ],
        "answer": 2
        })

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='question_quiz', on_delete=models.CASCADE, default=None)

    QUESTION_TYPES = (
        (0, 'multiple_choice'),
        (1, 'free_response'),
        (2, 'all_that_apply'),
        (3, 'parsons'),
    )

    question_type = models.IntegerField(choices=QUESTION_TYPES)

    answered_correct_count = models.IntegerField(default=0)
    answered_total_count = models.IntegerField(default=0)

    # Need to manually convert to and from JSON
    question_parameters = models.CharField(max_length=2048, default=json.dumps(quiz_question_jason_default()))
    """
    Multiple Choice:
    {
        "question": <question_text>,
        "choices": [<choiceA>, <choiceB>, <choiceC>, <choiceD>, ...],
        "answer": <answer_index>
    }

    Free Response:
    {
        "question": <question_text>,
        "answer": <reference_answer_text>
    }

    All that apply:
    {
        "question": <question_text>,
        "choices": [<choiceA>, <choiceB>, <choiceC>, <choiceD>, ...],
        "answer": [<answer_index1>, <answer_index2>,...]
    }

    Parsons:
    {
        "question": <question_text>,
        "code_lines": [<line0>, <line1>, <line2>, ...],
        "code_fixed": [T/F, T/F, T/F, ...],
        "code_dependencies": [[], [0], [0,1], ...]
    }
    """
    
    # Validate the json when updating the QuizQuestion in a django form (such as the admin page)
    def clean(self):
        super().clean()
        try:
            json.loads(self.question_parameters)
        except:
            raise ValidationError(_('Invalid JSON'))

    # Get the quiz questions that students are allowed to submit
    def get_submittable_questions(student, quiz):
        result = QuizQuestion.objects.filter(quiz=quiz) # Get quiz questions for the quiz

        num_questions_by_type = json.loads(quiz.pool) # How many of each question type are allowed for the quiz

        # Get the pks for the questions of each type
        parsons_pks = list(result.filter(question_type=3).order_by("id").values_list('id', flat=True))
        select_all_pks = list(result.filter(question_type=2).order_by("id").values_list('id', flat=True))
        #free_response_pks = result.filter(question_type=1).values_list('id', flat=True) # Commented out since free response is not implemented
        multiple_choice_pks = list(result.filter(question_type=0).order_by("id").values_list('id', flat=True))

        # Limit pks to a random sample seeded by the user pk
        random.seed(student.pk)
        parsons_pks = random.sample(parsons_pks,num_questions_by_type['parsons'])
        select_all_pks = random.sample(select_all_pks,num_questions_by_type['select_all'])
        multiple_choice_pks = random.sample(multiple_choice_pks,num_questions_by_type['multiple_choice'])

        # Combine primary keys
        quiz_question_pks = parsons_pks + select_all_pks + multiple_choice_pks

        result = QuizQuestion.objects.filter(quiz=quiz,id__in=quiz_question_pks)

        stqq = StudentToQuizQuestion.objects.filter(quiz_question__quiz=quiz, student=student) # Get student answers for the quiz
        num_submissions = len(stqq)
        
        # If the quiz doesn't allow resubmissions, exclude already submitted questions
        if not quiz.allow_resubmissions:
            result = result.exclude(id__in=stqq.values_list('quiz_question__id', flat=True))
        else:
            min_num_submissions = stqq.aggregate(Min('num_submissions'))['num_submissions__min']
            # If some questions have not yet been submitted by the user, exclude questions that have been submitted
            if num_submissions < len(result):
                result = result.exclude(id__in=stqq.values_list('quiz_question__id', flat=True))
            # Otherwise, only return the questions with the least number of submissions by the user
            elif min_num_submissions is not None:
                result = QuizQuestion.objects.filter(quiz=quiz,student_quizquestion__num_submissions=min_num_submissions)

        return result

    def calculate_percent_correct():
        return float(self.answered_correct_count)/self.answered_total_count

    def num_to_question_type(self, index):
        if index >= 0 and index < len(self.QUESTION_TYPES):
            return str(self.QUESTION_TYPES[index][1]).replace('_', ' ')
        else:
            return 'Unknown Type'

    def __str__(self):
        s = self.quiz.assignment.__str__() + " - " + self.num_to_question_type(self.question_type)
        try:
            s += ": " + json.loads(self.question_parameters)["question"]
        except:
            pass
        return s



"""
______________________________________________________________________________________________
 STUDENT TO QUIZ
 Stores the raw quiz score as a float from 0 to 1
______________________________________________________________________________________________
"""


class StudentToQuiz(models.Model):
    quiz = models.ForeignKey(Quiz,related_name='student_quiz', on_delete=models.CASCADE, default=None)
    grade = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    student_to_assignment = models.OneToOneField(StudentToAssignment,related_name='quiz_assignment', on_delete=models.CASCADE, default=None, )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    completed_quiz = models.BooleanField(default=False)

    def generate_score(self):
        pass

    def __str__(self):
        return "Student took quiz for " + self.quiz.__str__()


"""
______________________________________________________________________________________________
 STUDENT TO QUIZ QUESTION
 Stores student answers to quiz questions, the number of attempts, and whether or not it was correct
______________________________________________________________________________________________
"""


class StudentToQuizQuestion(models.Model):
    quiz_question = models.ForeignKey(QuizQuestion,related_name='student_quizquestion', on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    correct = models.BooleanField(default=False) # Whether or not the most recent submission was correct
    submitted_answer = models.CharField(max_length=512, default="") # The most recent submission
    num_submissions = models.IntegerField(default=1) # The number of times the student submitted this question

    def generate_score(self):
        pass

    def __str__(self):
        return "Student answered quiz question " + self.quiz_question.__str__()


"""
______________________________________________________________________________________________
 COMPETENCY THRESHOLDS
 Defines how numeric grades (0-100) translate to competency for topics in a course
 The weighted assignment grade for a particular topic is compared to these thresholds
______________________________________________________________________________________________
"""

class CompetencyThreshold(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE) # The class that these thresholds apply to
    competency_threshold = models.IntegerField(default=33) # The threshold to achieve competency
    mastery_threshold = models.IntegerField(default=66) # The threshold to achieve mastery
    

"""
______________________________________________________________________________________________
 GRADE THRESHOLDS
 Defines the minimum number of competent and mastered topics for a particular grade
______________________________________________________________________________________________
"""

class GradeThreshold(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE) # The class that these thresholds apply to
    a_plus_mastery = models.IntegerField(default=6)
    a_plus_competency = models.IntegerField(default=6)
    a_mastery = models.IntegerField(default=6)
    a_competency = models.IntegerField(default=5)
    a_minus_mastery = models.IntegerField(default=5)
    a_minus_competency = models.IntegerField(default=5)
    b_plus_mastery = models.IntegerField(default=5)
    b_plus_competency = models.IntegerField(default=4)
    b_mastery = models.IntegerField(default=4)
    b_competency = models.IntegerField(default=4)
    b_minus_mastery = models.IntegerField(default=4)
    b_minus_competency = models.IntegerField(default=3)
    c_plus_mastery = models.IntegerField(default=3)
    c_plus_competency = models.IntegerField(default=3)
    c_mastery = models.IntegerField(default=3)
    c_competency = models.IntegerField(default=2)
    c_minus_mastery = models.IntegerField(default=2)
    c_minus_competency = models.IntegerField(default=2)
    d_plus_mastery = models.IntegerField(default=2)
    d_plus_competency = models.IntegerField(default=1)
    d_mastery = models.IntegerField(default=1)
    d_competency = models.IntegerField(default=1)
    d_minus_mastery = models.IntegerField(default=0)
    d_minus_competency = models.IntegerField(default=1)

    def __str__(self):
        return "Grade threshold for " + self.course.__str__()
    

"""
______________________________________________________________________________________________
 SETTINGS
 Purely cosmetics.
______________________________________________________________________________________________
"""


class Settings(models.Model):
    color = models.CharField(max_length=250)
    nickname = models.CharField(max_length=250, null=True, blank=True)
    user = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "Settings for " + self.user.__str__()


"""
______________________________________________________________________________________________
 RESOURCES
______________________________________________________________________________________________
"""


class Resources(models.Model):
    link = models.CharField(max_length=2000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, blank=True, null=True)


"""
______________________________________________________________________________________________
 TOPIC TO TOPIC (used for graph.
______________________________________________________________________________________________
"""


class TopicToTopic(models.Model):
    course = models.ForeignKey(
        Course, related_name='edges', on_delete=models.CASCADE)
    topic_node = models.ForeignKey(
        Topic, related_name='topic_node', on_delete=models.CASCADE)
    ancestor_node = models.ForeignKey(
        Topic, related_name='ancestor_node', on_delete=models.CASCADE)

    weight = models.FloatField(
        null=True,
        blank=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    def __str__(self):
        return self.ancestor_node.__str__() + " -> " + self.topic_node.__str__()

    def topic_name(self):
        return self.topic_node.name

    def ancestor_name(self):
        return self.ancestor_node.name
