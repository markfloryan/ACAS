from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse

# For making requests
import json
import requests

# Import models
from .models import *

# Import responses
from .responses import *


# This will update all topics in a class to have the correct grades
def update_class_grades(request, class_pk, student_pk):
  # Get the topics associated to a class
    try:
        course = Course.objects.get(pk=class_pk)
        student = Student.objects.get(pk=student_pk)
        topics = StudentToTopic.objects.filter(
            course=course, student=student)
    except Course.DoesNotExist:
        return object_not_found_response()
    except Student.DoesNotExist:
        return object_not_found_response()
    # The topics and their grades
    topics_updated = []
    # This topic pk is the topic that is associated to the student
    for topic in topics:

        # So we want to get the origional topic pk
        # Get the student to topic
        # The existence of topic is always true because it was retrieved form the query, so we no need for exception
        student_topic = StudentToTopic.objects.get(pk=topic.pk)

        # Get the origional topic
        # student_to_topic can't exist without exisitng topic, so no need for exception check
        org_topic = Topic.objects.get(pk=student_topic.topic.pk)

        total_grades = []
        # Get the topic to cats
        topics_to_cats = TopicToCategory.objects.filter(topic=org_topic.pk)
        # if topics_to_cats.count() == 0:
        #     return HttpResponse(json.dumps("", indent=4), content_type='application/json')
        #     return object_not_found_response()

        # Get the quiz associated to a topic
        topic_quizzes = Quiz.objects.filter(topic=org_topic.pk)
        quizzes = True
        if topic_quizzes.count() == 0:
            quizzes = False

        quiz_grades = []
        # If there is a quiz, then we need to use the grade
        # This makes the assumption that a teacher has setup a topic to category with quiz
        if quizzes:
            for quiz in topic_quizzes:
                # Update the quiz grades
                try:
                    student_quiz = StudentToQuiz.objects.get(
                        quiz=quiz.pk, student=student_pk)
                except StudentToQuiz.DoesNotExist:
                    continue
                quiz_grades.append(student_quiz.grade)

        # For each topic, we then get the grades associated with a student
        for topics_to_cat in topics_to_cats:
            # Get the grades
            grades = Grade.objects.filter(
                topic_to_category=topics_to_cat.pk, student=student_pk)

            # For each grade do the math and find the average + the weight
            if len(grades) != 0:
                grade_vals = 0
                for grade in grades:
                    grade_vals += grade.value
                # If there is a quiz category, then we need to take into account the quizzes that were taken
                if topics_to_cat.category.name == 'Quiz':
                    quiz_total = 0
                    for quiz_grade in quiz_grades:
                        quiz_total += quiz_grade

                    total_grades.append(topics_to_cat.weight *
                                        (grade_vals + quiz_total) / (len(grades) + len(quiz_grades)))
                else:
                    total_grades.append(topics_to_cat.weight *
                                        grade_vals / len(grades))
        # Sum the grades. This is the grade of the student out of 100
        total_grade = 0
        for grade in total_grades:
            total_grade += grade

        # After we have gotten the student grade for a topic. We must also take into account the nodes that it inherits from
        # We make an assumption that all of the weights for a topic sum to 1
        topic_to_topics = TopicToTopic.objects.filter(topic_node=org_topic)

        weighted_average = 0
        for topic_to_topic in topic_to_topics:
            # This should always exist because we are getting it from another list. So we dont have to check
            topic_to_topic_grade = StudentToTopic.objects.get(
                topic=topic_to_topic.ancestor_node, student=student_pk)
            # Create the weighted average for the topic
            weighted_average += topic_to_topic_grade.grade * topic_to_topic.weight



        # Calculate what the topic is worth
        topic_weight = 1 - org_topic.ancestor_weight

        # make the new total grade
        total_grade = (topic_weight * total_grade) + \
            (org_topic.ancestor_weight * weighted_average)

        # Get the topic and update the total grade
        topic = StudentToTopic.objects.get(
            topic=org_topic.pk, student=student_pk)
        topic.grade = total_grade
        # Save the new grade
        topic.save()

        topics_updated.append({"topic": topic.pk, "grade": total_grade})
        # Get all of the grades and calculate the total for a node
    return HttpResponse(json.dumps(topics_updated, indent=4), content_type='application/json')































