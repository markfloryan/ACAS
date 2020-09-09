## Requirements
- Unix based OS (Linux, MacOS)
  - These install instructions were written for Ubuntu 18.04 LTS
- 4GB of ram
  - 8GB is recommended, although we have used as little as 2GB for development and 3GB for production deployments
  - In general, the application takes around 300 MB to run properly, but requires more ram when building the docker containers

## Setup
- Clone the repo
- Download Docker and docker-compose ([Docker Install Instructions](docker_install_instructions.md))
- Setup Google OAuth from the Google API Console ([OAuth Setup Instructions](oauth_setup.md))

## Development mode installation instructions
To enable Google oauth locally in develop mode for sign-up and sign-in, add the following line to your /etc/hosts file (on linux or mac)
`
127.0.0.1   spt-acas.com
`
- Naviage to src 
```bash
cd src
```
- Run the server. Note: you may have to use sudo when executing docker-compose commmands
```bash
docker-compose up
```
- Load the debug users into the database. While docker-compose is up, execute the following command in another terminal
```bash
docker exec backend python3 manage.py loaddata debug_users.json
```

Frontend Application: spt-acas.com:8080. 
Backend API: spt-acas:8000. 
Django Admin: spt-acas.com:8000/admin

To login to the admin page, create an admin account by following the instructions below.

The databse is stored at src/db. Warning: During our testing, the command `docker-compose down` sometimes caused us to lose data in the db. To stop the containers without losing data, use CTRL + C instead.

Note: Accessing the application from spt-acas.com is done to allow OAuth to work locally since Google OAuth requires accessing the application from authorized top level domains. Accessing from spt-acas.com is not required for logging into the debug users. You can access the application from localhost:8080, but oauth will not work for regular sign in and account creation.

## Production installation instructions
The following commands must be ran on the production server itself which is accessible by a public domain on the internet
- Set DOMAIN in src/config/deployment_vars to the domain that you will be deploying on
- Set the EMAIL variable to associate the certificates with your email. This not required but recommended.
- Set the CLIENT_ID variable to the CLIENT_ID that you got from the Google OAuth setup if you have not done so already.
- Navigate to the src folder

Create the docker volume to store the database data
```bash
docker volume create --name=postgres_data
```

Build the production files
```bash
docker-compose -f docker-compose.prod.yml build
```

Collect certificates
```bash
sudo ./init-letsencrypt.sh
```
- IMPORTANT: You must execute this command on a public server accessible at the domain specified in /src/config/deployment_vars
- Port 80 must be open and not in use by another program

Start the server
```bash
docker-compose -f docker-compose.prod.yml up
```
- To run the server in the backround instead of the foreground, use the -d flag: `docker-compose -f docker-compose.prod.yml up -d`

The database is stored in an external docker volume for production because it prevents accidential deletion of the databse with `docker-compose down`. If you actually want delete the database, do so with the command `docker volume rm postgres_data`

### Creating an admin account
While the application is running, execute this command in another terminal:
```bash
docker exec -it backend python3 manage.py createsuperuser
```

### Creating a professor account
- Log into an admin account
- Navigate the the 'Users' page
- From here, you may either create a new account and set "is_professor" to true, or you can modify an existing user and set "is_professor" to true.

### Running tests
- Navigate to the src folder
- Add executable permissions to test-backend.sh with `chmod +x test-backend.sh`
- Run tests with the following command. Note: The application must not be running before running tests.
```bash
./test-backend.sh
```