### Setup for a basic PERN App

0. Install dependencies using npm install for server and client dependencies

1. Setup the database locally
   a. Database users table should have: user_id, password (you can use the initialize-user-table.sql script to build a basic table)
   
2. create your .env file with the following format so that it can run locally:
PORT=
SALTROUNDS=
SESSIONSECRET=
USER=
HOST=
DATABASE=
DATABASEPASSWORD=
DATABASEPORT=
*Any api keys here*

3. Use the files in the database/ directory to initialize the store 

4. In the client library, change the names of the base pages (home, login, dashboard)

5. Set up the necessary paths in client/src/redux/config to make the api work

6. Setup git and create the github repo

7. Create a new project in heroku. Test the front end first
   a. Deploy the github project under the deploy tab
   b. Check the logs to make sure there were no immedaite errors
   c. Check to make sure the home page initialized properly

8. Provision the postgres database under add-ons. Get the credentials add them to the envirornment variables for the project in heroku

9. Use the credentials to add the server in pgadmin. Find the gold server based on the database name. Right-click and use the Query Tool 

10. Use the database .sql files to initialize the boilerplate tables

11. Insert a user for testing auth

11. Test auth

### Running project dev tools:

* cd client; npm run tail -> runs tailwind dev tool
* cd client; npm run start -> runs react 
* cd server; npm run server -> runs server
* create another command line for usage