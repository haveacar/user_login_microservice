
## Overview

This Microservice for user registration is designed to provide a backend service with user authentication, registration, and email confirmation functionalities. It integrates Flask with Flask-RESTful for resource-based routes, Flask-JWT-Extended for JWT authentication, and SQLAlchemy for ORM. The application also utilizes AWS Secrets Manager for securely managing application secrets and AWS SES for sending emails.

### Features

- User registration with email confirmation
- User sign-in and token refresh
- JWT authentication for protected routes
- Admin interface for managing users
- Email sending functionality through AWS SES
- Configuration management through AWS Secrets Manager

### Technical Documentation
[http://web3mtest-env.eba-hwukpuqp.eu-central-1.elasticbeanstalk.com/](http://web3mtest-env.eba-hwukpuqp.eu-central-1.elasticbeanstalk.com/)

### Requirements

To run this application, you'll need:

- Python 3.x
- Flask and associated extensions as listed in `requirements.txt`
- AWS account with configured Secrets Manager and Simple Email Service (SES)
- MySQL database

### Setup

1. Clone the repository to your local machine.
2. Install the dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

3. Ensure you have a MySQL database accessible and AWS SES and Secrets Manager properly configured.
4. Update the `settings.json` file with your AWS credentials and other configurations. Note: This file is not included in the git repository for security reasons; you need to create it manually based on the provided template.
5. Initialize the database schema by running the application once, which will create the necessary tables.

## .ebextensions Configuration

In order to customize the AWS Elastic Beanstalk environment, you can use the `.ebextensions` directory to provide custom configuration files. One of these configurations is the `python.config` file, which allows you to specify how your application is set up beyond the default settings. Below is an example of how to configure the `python.config` file to customize the Apache server settings for a Python application.

### python.config

This configuration file is used to create a custom Apache server configuration file. The `files` section of `python.config` specifies the creation of a new file at `/etc/httpd/conf.d/wsgi_custom.conf` with the specified permissions, owner, and group. The content of this file sets the `WSGIApplicationGroup` directive to `%{GLOBAL}`, which can help resolve issues with some Python applications running under mod_wsgi.

```yaml
files:
  "/etc/httpd/conf.d/wsgi_custom.conf":
    mode: "000644"
    owner: root
    group: root
    content: |
      WSGIApplicationGroup %{GLOBAL}


### Running the Application

To start the application, use the following command:

```
python application.py
```

The application will start on `http://web3m-login-microservice.eu-central-1.elasticbeanstalk.com/` by default. You can access the admin interface at `/web3m-admin` with the configured credentials.

## API Endpoints

The application provides the following API endpoints:

- `POST /api/v1/register`: Register a new user.

- `POST /api/v1/resend-confirmation`: Resend the email confirmation.

- `GET /api/v1/protected`: Access a JWT-protected resource.

- `POST /api/v1/signin`: Sign in a user and return JWT tokens.

- `POST /api/v1/refresh_token`: Refresh the JWT access token.

- `PUT /api/v1/users/<string:user_id>`: Update user data.

- `DELETE /api/v1/users/<string:user_id>`: Delete a user.

### Security Considerations

- Ensure your `settings.json` file is securely stored and not included in any version control systems.
- Regularly rotate your AWS credentials and keep them confidential.
- Use HTTPS in production to protect sensitive data in transit.

### Troubleshooting

If you encounter issues with database connectivity or AWS services, ensure your configuration in `settings.json` is correct and that your AWS credentials have the necessary permissions.

For more detailed error information, consult the application logs and AWS service dashboards.
