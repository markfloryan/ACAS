# Student-Performance-Tracker-1

TravisCI status: [![Build Status](https://travis-ci.com/UVA-Capstone-Practicum-1819/Student-Performance-Tracker-1.svg?token=zrpu68ydy2osA7tAdwBJ&branch=master)](https://travis-ci.com/UVA-Capstone-Practicum-1819/Student-Performance-Tracker-1)

I want to build a system that allows me to structure my course as a DAG of topics and their dependencies. Then, I want to be able to "link" different outside resources to the individual topics. For example, there might be a node for "Arrays" and the resources might be things like 
links to outside readings, hw assignments related to that topic, extra practice on that topic, etc.

The student will earn a grade for each topic, and I also want the ability to customize how this grade is calculated. The scores for this grade are uploaded and become one of the "resources" mentioned above for that topic. A grade may also be partially calculated as a function of
other topic grades.

The system will have student accounts, student logins, etc.

Lastly, if time I'd like to build a separate drill and practice system for students. They would be given questions and answers and go through problems I specify. These scores would be fed into the DAG above and be one of the things that composes the score for each topic.

### Contact Information

Mark Floryan

mrf8t@virginia.edu

### Server Number

174

## How to access the application
- http://student-performance-tracker.s3-website-us-east-1.amazonaws.com/welcome

## How to install the application for production

Visit our [install instructions](./docs/install_instructions.md)

## How to run the application for development

- Clone the repo
- Download Docker CE
- Navigate to `Student-Performance-Tracker-1/src`
- run `docker-compose up`
- Navigate to `localhost:8080` to view the running application
- API Calls are routed `localhost:8000`
