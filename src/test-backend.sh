#!/bin/bash

docker-compose -f docker-compose.test.backend.yml up --exit-code-from backend
