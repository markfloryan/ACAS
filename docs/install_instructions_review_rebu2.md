# Notes

## Recommended Grade 8.5/10
  The instructions generally worked well, with some minor problems with the site assets and connecting to the paris server.

## Mac Testing (VENV)

- Small issue in installing pip `Uninstalling pip-19.0.3: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: ‘/Library/Python/2.7/site-packages/pip-19.0.3.dist-info/RECORD’`

  - Consider using the `--user` option or check the permissions.

  - But likely due to me already having pip installed

- “This will take you to the Amazon Web Services Console. Login with your AWS Account”

  - Preassumes that users have an AWS account, maybe could use a part on registering for an account.

- You can access the site, but it seems like a lot of the assets are missing (css)

## Linux Testing (Docker)

- Cannot access git repo, so I had to look up how to SCP files onto new linux instance because I was only using the terminal

- Cannot SSH onto PARIS instance so I had to create an EC2 instance

  - Got an `ssh: connect to host paris.cs.virginia.edu port 22114: Connection refused`
  - This could greatly effect the following install

- Pretty minor, but does not tell you what to accept when installing.

- When creating the IAM user role, the picture shows that there are 0 attached policies, this is a contradiction. It should say `AmazonS3FullAccess`

- Creating the S3 bucket for non-technical users is not easily followable

  - `rebu2-assets-test`
  - Personally not a fan of un-checking the reccommended options from amazon. Maybe there could have been a better way. This opens a lot of security issues

- Because Paris was not accessable, I had to SCP the files over. This is non-trivial for a user

  - Had to install special software to unzip .zip file on linux

- Got a `DisallowedHost at / Invalid HTTP_HOST header: 'ec2-52-55-50-122.compute-1.amazonaws.com:8000'. You may need to add 'ec2-52-55-50-122.compute-1.amazonaws.com' to ALLOWED_HOSTS.` When trying to serve the docker container because I did not have access to Paris

- Similar to the Mac install, the S3 Bucket did not seem to link with the styles
    - Does not look good
    
    
## Windows Testing (VENV)
  - You can access the site, but it seems like a lot of the assets are missing (css).
