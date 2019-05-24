from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField

# How users and superusers are created
# Some help from https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4


'''
______________________________________________________________________________________________      Custom Account Manger
 CustomAccountManager
______________________________________________________________________________________________
'''
""" Used to create a new user and super user. Because we are using a custom model, this code had to be written to take into account the lack of a password and unique username """


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


'''
______________________________________________________________________________________________      Student
 Student
______________________________________________________________________________________________
'''

""" Student Model: used as the default user. The USERNAME field is the default and is used to log a user in. The username is the email. """


class Student(AbstractUser):
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    join_date = models.DateTimeField(auto_now=True)
    id_token = models.CharField(max_length=5000, blank=True, null=True)

    # Temporary
    is_professor = models.BooleanField(null=True)

    # For creating a superuser
    username = models.CharField(blank=True, null=True, max_length=150)

    def __str__(self):
        name = ""
        if self.first_name is not None:
            name += self.first_name
        if self.last_name is not None:
            if self.first_name is not None:
                name += " "
            name += self.last_name

        return name

    def get_id(self):
        return self.id_token

    def get_is_professor(self):
        return self.is_professor

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

# Model to be implemented for more robust professor capabilities


# class Professor(models.Model):
#     user = models.OneToOneField(Student, on_delete=models.CASCADE)
#     school = models.CharField(
#         max_length=250, blank=True, null=True, default="UVA")
#     teacher_id = models.AutoField(primary_key=True)

#     def __str__(self):
#         name = ""
#         if self.user.first_name is not None:
#             name += self.user.first_name
#         if self.user.last_name is not None:
#             if self.user.first_name is not None:
#                 name += " "
#             name += self.user.last_name

#         return name


'''
______________________________________________________________________________________________      Course
 Course
______________________________________________________________________________________________
'''


class Course(models.Model):
    name = models.CharField(max_length=250)
    course_code = models.CharField(max_length=250)
    subject_code = models.CharField(max_length=250)
    professor = models.ForeignKey(
        Student, related_name='professor', on_delete=models.CASCADE, blank=True, default="0")

    def __str__(self):
        return self.subject_code + " " + self.course_code


'''
______________________________________________________________________________________________      Student To Course
 Student To Course
______________________________________________________________________________________________
'''


class StudentToCourse(models.Model):
    student = models.ForeignKey(
        Student, related_name='student', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='courses', on_delete=models.CASCADE)
    semester = models.CharField(max_length=250, null=True, blank=True)

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


'''
______________________________________________________________________________________________      Topic
 Topic
______________________________________________________________________________________________
'''


class Topic(models.Model):
    name = models.CharField(max_length=250)
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
    ancestor_weight = models.FloatField(
        null=True,
        blank=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    def __str__(self):
        return self.name


'''
______________________________________________________________________________________________      Category
Category of a grade
______________________________________________________________________________________________
'''


class Category(models.Model):
    name = models.CharField(max_length=250,  primary_key=True)

    def __str__(self):
        return self.name


'''
______________________________________________________________________________________________      TopicToCategory
TopicToCategory
______________________________________________________________________________________________
'''


class TopicToCategory(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.FloatField(
        null=True,
        blank=True,
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    def __str__(self):
        return self.category.__str__() + " is related to topic " + self.topic.__str__() + " with a weight of " + str(self.weight)


'''
______________________________________________________________________________________________      Grade
Grade
______________________________________________________________________________________________
'''


class Grade(models.Model):
    name = models.CharField(max_length=250)
    value = models.FloatField(default=0, validators=[
                              MinValueValidator(0), MaxValueValidator(100)])
    topic_to_category = models.ForeignKey(
        TopicToCategory, related_name='grades', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def category(self):
        return self.topic_to_category.category

    def weight(self):
        return self.topic_to_category.weight

    def __str__(self):
        return self.student.__str__() + " got a " + str(self.value) + " on " + self.name + " in " + self.topic_to_category.category.__str__()


'''
______________________________________________________________________________________________      Student To Topic
 Student To Topic
______________________________________________________________________________________________
'''


class StudentToTopic(models.Model):
    course = models.ForeignKey(
        Course, related_name='nodes', on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    grade = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    locked = models.BooleanField()

    def __str__(self):
        return self.student.__str__() + " is in " + self.topic.__str__()

    def get_topics(self, course_id, student_id):
        student = Student.objects.get(pk=student_id)
        course = Course.objects.get(pk=course_id)

        topics = self.objects.filter(
            student=student,
            course=course
        )

        return topics

    def save(self, *args, **kwargs):
        if self.course is None:
            self.course = self.topic.course
        super(StudentToTopic, self).save(*args, **kwargs)

    # course = models.ForeignKey(Course, on_delete=models.CASCADE, default=self.course_default)


'''
______________________________________________________________________________________________      Quiz
 Quiz
______________________________________________________________________________________________
'''
# Quizzes


class Quiz(models.Model):
    name = models.CharField(max_length=250, default="Quiz")
    topic = models.ForeignKey(
        Topic, related_name='topic', on_delete=models.CASCADE)

    def __str__(self):
        return "Quiz for " + self.topic.__str__()

    def weight(self):
        category = Category.objects.get(name="Internal Quiz")
        try: 
            topic_to_category = TopicToCategory.objects.get(topic=self.topic, category=category)
            return topic_to_category.weight
        except TopicToCategory.DoesNotExist: 
            return 0


'''
______________________________________________________________________________________________      QuizQuestion
 QuizQuestion
______________________________________________________________________________________________
'''


class QuizQuestion(models.Model):
    QUESTION_TYPES = (
        (0, 'multiple-choice'),
        (1, 'free-response'),
        (2, 'all-that-apply'),
    )

    text = models.CharField(max_length=250)
    question_type = models.IntegerField(choices=QUESTION_TYPES)
    quiz = models.ForeignKey(Quiz, related_name='questions',
                             on_delete=models.CASCADE, null=True, blank=True)
    total_points = models.IntegerField(default=1)
    index = models.IntegerField(default=1)

    def __str__(self):
        return "Quiz id: " + str(self.quiz.pk) + ", question: " + self.text


'''
______________________________________________________________________________________________   QuizQuestionAnswer
 QuizQuestionAnswer
______________________________________________________________________________________________
'''


class QuizQuestionAnswer(models.Model):
    text = models.CharField(max_length=250)
    question = models.ForeignKey(
        QuizQuestion, related_name='answers', on_delete=models.CASCADE)
    weight = models.FloatField(
        null=True,
        blank=True,
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    correct = models.BooleanField()
    index = models.IntegerField(default=1)

    def __str__(self):
        return "Question id: " + str(self.question.pk) + " answer: " + self.text


'''
______________________________________________________________________________________________      StudentToQuiz
 StudentToQuiz
______________________________________________________________________________________________
'''


class StudentToQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def generate_score(self):
        pass

    def __str__(self):
        return "Student took quiz for " + self.quiz.__str__()


'''
______________________________________________________________________________________________      StudentToQuizQuestion
 StudentToQuizQuestion
______________________________________________________________________________________________
'''


class StudentToQuizQuestion(models.Model):
    student_to_quiz = models.ForeignKey(
        StudentToQuiz, related_name='student_answers', on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.ForeignKey(
        QuizQuestionAnswer, on_delete=models.CASCADE, null=True, blank=True)
    correct = models.BooleanField(default=False)


'''
______________________________________________________________________________________________      Settings
 Settings
______________________________________________________________________________________________
'''


class Settings(models.Model):
    color = models.CharField(max_length=250)
    nickname = models.CharField(max_length=250, null=True, blank=True)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "Settings for " + self.user.__str__()


'''
______________________________________________________________________________________________      Resources
 Resources
______________________________________________________________________________________________
'''


class Resources(models.Model):
    link = models.CharField(max_length=2000)
    topic = models.ForeignKey(Topic,  on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, blank=True, null=True)


'''
______________________________________________________________________________________________      Topic to Topic
 Topic to Topic
______________________________________________________________________________________________
'''


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

    def ancestor_name(self):
        return self.ancestor_node.name


'''
______________________________________________________________________________________________      ExternalSitesList
 ExternalSitesList: The list of websites that can be used for external interaction (API's)
______________________________________________________________________________________________
'''


class ExternalSitesList(models.Model):
    website_name = models.CharField(max_length=250, default='Site 1')
    website_nickname = models.CharField(max_length=250, default='Site 1')
    is_website_used = models.BooleanField(null=False, default=False)

    def set_website_used(self, value):
        self.is_website_used = value

    def __str__(self):
        return self.website_name + ' (' + self.website_nickname + ')'


'''
______________________________________________________________________________________________      ExternalQuizStatic
 ExternalQuizStatic
______________________________________________________________________________________________
'''


class ExternalQuizStatic(models.Model):
    quizName = models.CharField(max_length=250, default="Quiz Default")
    quizScore = models.IntegerField(default=0)

    question1 = models.CharField(max_length=250, default="Question1")
    question1answer1 = models.CharField(
        max_length=250, default="Question1 Answer1")
    question1answer2 = models.CharField(
        max_length=250, default="Question1 Answer2")
    question1answer3 = models.CharField(
        max_length=250, default="Question1 Answer3")
    question1answer4 = models.CharField(
        max_length=250, default="Question1 Answer4")
    correctIndex1 = models.IntegerField(default=1)
    isCorrectAnswer1 = models.BooleanField(null=False)

    def getIsCorrect(self):
        return self.isCorrectAnswer1

    def getQuizScore(self):
        return self.quizScore

    def getModel(self):
        return "{\"quizName\": \"" + self.quizName + "\", \"quizScore\": " + str(self.quizScore) + "}"

    def __str__(self):
        return self.quizName

'''
______________________________________________________________________________________________      External Sites
 ExternalSites: Approved External API base-url's that work well with SPT
______________________________________________________________________________________________
'''

class ExternalSite(models.Model):
    name = models.CharField(max_length=250, null=False)
    base_url = models.TextField(validators=[URLValidator()], null=False,  unique=True)
    
    def __str__(self):
        return self.name + ' (' + self.base_url + ')'


'''
______________________________________________________________________________________________      ExternalSite To Course
 ExternalSites: Approved External API base-url's that work well with SPT
______________________________________________________________________________________________
'''

class ExternalSiteToCourse(models.Model):
    course = models.ForeignKey(Course,  on_delete=models.CASCADE) 
    external_site = models.ForeignKey(ExternalSite, on_delete=models.CASCADE)  
    url_ending = models.CharField(max_length=200, null=False)

    class Meta:
        unique_together = ('external_site', 'url_ending',)


    def __str__(self):
        return  str(self.course.course_code + " " + self.course.subject_code) + ' (' +  self.external_site.name + self.url_ending + ')'


'''
______________________________________________________________________________________________      ExternalSite To Grade
 ExternalSiteToGrade: Connects each grade back to an external site
______________________________________________________________________________________________
'''
class ExternalSiteToGrade(models.Model): 
    external_site_to_course = models.ForeignKey(ExternalSiteToCourse, on_delete=models.CASCADE, null=False)   
    grade = models.OneToOneField(Grade, on_delete=models.CASCADE, null=False)
    link = models.CharField(max_length=100, null=True, blank=True) # Link for grade to external url that gave grade 

    def delete(self, *args, **kwargs):
        self.grade.delete()
        super(self.__class__, self).delete(*args, **kwargs)


    def __str__(self):
        return 'Grade: ' + str(self.grade.value) + ' (' +  self.link + ')'




