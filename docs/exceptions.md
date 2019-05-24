# Exceptions for code coverage

## [external.py](../src/backend/sptApp/external.py)

- Lines 133 - 137
  - These lines will not be hit because the data is hard-coded. This code is here for the furture proofing of the code for when it is no longer hard-coded in the application
- Line 145
  - This is a similar situation. Because the data above was hard-coded and is known to work, then the code will never fail.
- Line 150 - 154
  - This is a similar situation. Because the data above was hard-coded and is known to work, then the code will never fail.


## [api_views.py](../src/backend/sptApp/api_views.py)

- Lines 2260, 2546, 2569, 2575
  - These were various hard coded unreachable pieces of code from the xternal service and were thus not testable.

- Line 2185
  - This serializer is always valid, but serializer requires is_valid to be called to save() 

## [models.py](../src/backend/sptApp/models.py)

- Lines 19-42
  - CustomAccountManager is an extension of vanilla Django and was untestable as a result.

## [external.py](../src/backend/sptApp/external.py)
 Due to time, we were not able to fully finish the restructuring of SPT so that it could handle the managing of JSON data from external sites. There was an issue with trying to test an internal call so that all checks were called.