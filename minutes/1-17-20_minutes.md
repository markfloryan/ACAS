Quizzes:
How many per topic?
Do we treat quizzes as assignments?
Verify the backend formatting?
Should people be able to view/review previous events?
If so, should they be able to see the correct answers?
How satisfactory is “just see your previous score”?
Clarify the whole quiz-taking process
Clarify the whole gamut of quiz parameters
For instance, having a time period where the quiz “counts” and everything else is just practice

Other:
Stable code is now on master

Notes
One pool per topic. Each quiz defines how many of each type of question to pull. Different possible questions per student
Start time and end time for each quiz and max number of attempts
Record the scores of previous attemptions, but no need to see exactly which questions were correct
Highest score is the recorded one; not most recent
Potentially look into storing % each question is answered correctly (within the question model)
Is graded flag (practice times for quizzes)
CSV upload schema is acceptable (as long as a non-CS user could reasonably use it)
In general, prioritize student side usability over instructor side usability (setup hackiness is acceptable)
