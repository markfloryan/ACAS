Meeting 4
Overall Notes:
  Check the DSA syllabus for the stairstep competency chart
  Floryan has made email contact with someone from the previous team, incase that will be important
Security:
  We added auth for users, and only profs can do post, put, delete
    TAs should have their access restricted on a per-class basis
      Admin level should be denoted in the user -> class relation
      Still need an overall Admin to do regular Django stuff (and it should be Floryan)
    Later, we should be sure to use https as well as OAuth- security vuln.
      Also, can't send token as a part of the URL once https is in there
    we renamed is_professor to is_staff- Floryan says that's alright
  Google says to use profile_id instead of the email, since the email can change when the id doesn't
Performance:
  we have begun to streamline a bit, but it's hard to demo performance changes
Course Alignment:
  Corey finished the topic locking and unlocking feature- just need profs to be able to toggle these things
    Toggle should be on an all-students basis, not per-student (all students in the class are locked at once)
  Jack finished the competency / non-competency style for grades (as opposed to numbers)
    Quizzes to Topics will be 1-1 in DSA, not necessarily the case for all classes (can change in Spring)
      Topics should only see a pool of Quiz questions and just make a quiz based off of this
Quizzes:
  These have been pushed back, but when frontend tests and models work as intended, we will start work as early as next sprint.
Testing:
  Backend tests run correctly, are broken right now because of new auth features
  Frontend tests used PhantomJS which has been discontinued for years, since moving to Chrome we have made progress
    Should be working by the end of the week
  It would be wise to use Dockerfiles to help start up earlier
  TravisCI is working, you can see it in the readme.
