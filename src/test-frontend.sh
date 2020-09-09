#!/bin/bash

docker-compose -f docker-compose.test.frontend.yml up --exit-code-from frontend
