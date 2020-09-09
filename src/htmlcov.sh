#!/bin/bash

docker-compose -f docker-compose.htmlcov.yml up --exit-code-from backend
echo "Open backend/htmlcov/index.html in your web browser to view the full coverage report"
