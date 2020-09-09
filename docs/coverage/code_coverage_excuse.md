# Code Coverage Excuses

## Main
- sptApp/api_views
	- This file contains all of our api endpoints. We've written tests for every endpoint but ran into issues with Django interacting with the unit tests that were not allowing us to test specific portions of the code base. Our coverage report generator also doesn't notify us as to which lines are not covered, so we cannot implement tests that cover those lines. 

- sptApp/auth.py
	- This file contains authentication code for the users. This code communicated with Google's Oath feature so we did not write test cases for the portions of code that communicated with Oath. 

- sptApp/cascade_grades.py
	- We did not write test cases for this file as the file will be updated in the near future when we receive an algorithm for grading from the client. 

- sptApp/exampleExternalJSON.py
	- This file contains example json formats for external sites, and performs no live functions as of right now, thus we do not have tests for it. 

- sptApp/permissions
	- We have not yet used TA permission functionality in our live code, thus we have no tests covering this portion yet. 

- sptApp/responses.py
	- A few of the responses in this file have yet to be called upon and may be deprecated in the near future, so we do not have tests covering them. 

- sptApp/tests.py 
	- Our testing file. Due to the coverage report generator we are using, we are unable to see the 6 lines it reports as not covered, so we cannot determine which 6 lines are not covered. 