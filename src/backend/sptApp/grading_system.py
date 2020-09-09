from .models import *

# Determines the number grade given to students who acheive a given letter grade
letter_number_grade_tuples = [
        ("a_plus", 100),
        ("a", 95),
        ("a_minus", 90),
        ("b_plus", 88),
        ("b", 85),
        ("b_minus", 82),
        ("c_plus", 78),
        ("c", 75),
        ("c_minus", 72),
        ("d_plus", 68),
        ("d", 65),
        ("d_minus", 62),
    ]

# Check if a given grade (e.g. "a", or "a_plus") meets the grade threshold
def meets_grade_threshold(grade,grade_threshold,num_competent,num_mastery):
    # False if we don't meet mastery threshold
    if num_mastery < getattr(grade_threshold, grade + "_mastery"):
        return False
    
    # True if we also meet competency threshold through competent topics
    if num_competent >= getattr(grade_threshold, grade + "_competency"):
        return True

    # True If we meet competency threshold through extra mastered topics
    elif num_mastery - getattr(grade_threshold, grade + "_mastery") >= getattr(grade_threshold, grade + "_competency"):
        return True

    return False
    

# Update student_to_course based on topic competencies
def update_course_grade(student_pk=None, course_pk=None):
    student_to_topics = StudentToTopic.objects.filter(student=student_pk, course=course_pk)
    course = Course.objects.get(pk=course_pk)

    # Initialize variables to track the number of competent and mastered topics
    num_competent = 0
    num_mastery = 0

    for stt in student_to_topics:
        if stt.competency == 1: # If competent
            num_competent += 1
        elif stt.competency == 2: # If mastery
            num_mastery += 1

    try:
        grade_threshold = GradeThreshold.objects.get(course=course)
    except:
        grade_threshold = GradeThreshold.objects.create(course=course)

    # If no grade criteria is met, the grade is 50
    grade = 50

    # Check if various grades are met, set them if so
    for letter_number in letter_number_grade_tuples:
        if meets_grade_threshold(letter_number[0],grade_threshold,num_competent,num_mastery):
            grade = letter_number[1]
            break

    try:
        student_to_course = StudentToCourse.objects.get(student=student_pk, course=course_pk)
    except:
        print("No StudentToCourse for the given student and course")
        return
    student_to_course.grade = grade
    student_to_course.save()

# Collect all student_to_assigment grades for a given topic and update the topic competency and grade for that student
def update_topic_grade(student_pk=None, topic_pk=None):
    student_to_assignments = StudentToAssignment.objects.filter(student=student_pk, assignment__topic=topic_pk)

    # If no assignments in the topic, set topic grade to zero
    if len(student_to_assignments) == 0:
        try:
            student_to_topic = StudentToTopic.objects.get(student=student_pk,topic=topic_pk)
        except:
            print("No associated student to topic.")
            return
        student_to_topic.competency = 0
        student_to_topic.grade = 0
        student_to_topic.save()

        update_course_grade(student_pk, student_to_topic.course.pk)
        return

    course = student_to_assignments[0].assignment.topic.course # All these assignments will have the same course, so this is safe

    sum_assignment_weights = 0
    sum_grades = 0.0

    for sta in student_to_assignments:
        sum_grades += sta.grade * sta.assignment.weight # Add grade while taking into account the wight
        sum_assignment_weights += sta.assignment.weight

    avg_grade = sum_grades / sum_assignment_weights

    competency = 0


    try:
        comp_thresholds = CompetencyThreshold.objects.get(course=course)
    except:
        comp_thresholds = CompetencyThreshold.objects.create(course=course)



    if avg_grade < comp_thresholds.competency_threshold:
        competency = 0 # Incomplete
    elif avg_grade < comp_thresholds.mastery_threshold:
        competency = 1 # Competent
    else:
        competency = 2 # Mastered
    
    try:
        student_to_topic = StudentToTopic.objects.get(student=student_pk,topic=topic_pk)
    except:
        print("No associated student to topic.")
        return
    student_to_topic.competency = competency
    student_to_topic.grade = avg_grade
    student_to_topic.save()

    update_course_grade(student_pk, student_to_topic.course.pk)

######################################################
# Carrington's evaluation function for quizzes.
# Takes in an old probability (@currentScore), and a correctness bool (@response), and returns a new probability.
######################################################
def getScore(response, currentScore = 0.3):
    p_L0 = currentScore
    p_G = 0.4
    p_S = 0.2
    p_T = 0.2
    if (response):
        numerator = ((1 - p_T)*(1 - p_L0)*(p_G))
        denominator = (p_G + (1 - p_S - p_G)*(p_L0))
    else:
        numerator = ((1 - p_T)*(1 - p_L0)*(1 - p_G))
        denominator = (1 - p_G - (1 - p_S - p_G)*(p_L0))
    retVal = 1 - (numerator/denominator)
    return retVal