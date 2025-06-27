## How does your app handle form validation?

It checks if all fields are filled and if the date of birth is in the past.Errors are then shown above the form if there are issues.

## How would you extend the app for therapist logins?

We can add a `therapists` table with usernames and hashed passwords. We can then use Flask sessions for login/logout and protect the internal routes with login-required decorators.

## How would you deploy this app to a HIPAA-compliant cloud?

We will use a HIPAA-compliant provider like AWS with encryption (RDS + EC2 + SSL)
EC2 for the Flask app server. RDS for secure database and Cloudwatch for monitoring and logging. i'd also use https encryption using a aws acm certificate and configure my nginx server to enforce https only. I'd also restrict access to the database using IAM roles and security groups. I'd also enable cloudtrail for all actions taken on the server and database

## Where is the database init code and why?

It’s in the `init_db()` function, called once at app startup which ensures the database table exists before the app runs.
