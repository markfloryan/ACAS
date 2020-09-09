* Dummy accounts should be placed manually for testing, no need for automatic creation
* No error corrections for dummy accounts
   * Not a priority at the moment
* A lot of backend computations are done on the front end. Refactor api requests to return specific information (backend views requests less data)
* Consider refactoring endpoints to have a singular “router” endpoint handling traffic to and from the others
* Weird function calls when calling login models
   * Refactor login methods and user models
* They can practice quiz any time they want and give preview grade, but as a professor can set the time window for when the quiz is real, and recorded into your grade.
   * Could be repeating time. (ex. Every week during lab time)
   * Let professor set how many times they can take it per session
   * Add checkbox to allow/disallow practicing of the quiz
   * Publish pool in PDF form
* Already quiz functionality. Could completely rebuild it or use it as a base