from django.db.models.signals import post_save, post_init, post_delete
from sptApp.grading_system import update_topic_grade, update_course_grade
from django.dispatch import receiver
from .models import *


# Execute update_topic_grade when StudentToAssignment grades are changed
@receiver(post_save, sender=StudentToAssignment)
def grade_save(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance.previous_grade != instance.grade or created:
        update_topic_grade(instance.student.pk, instance.assignment.topic.pk)

# Store StudentToAssignment grades when StudentToAssignments are initialized
@receiver(post_init, sender=StudentToAssignment)
def remember_state(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.previous_grade = instance.grade

# Cascade when StudentToAssignment grades are deleted
@receiver(post_delete, sender=StudentToAssignment)
def grade_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    update_topic_grade(instance.student.pk, instance.assignment.topic.pk)