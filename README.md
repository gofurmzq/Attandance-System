# :octocat: Attandance-System
by Muhamad Gofur Muzaqi

## :wrench: Requirements
1. Python : Programming Language
2. Flask : Web Framework
3. SQLAlchemy : Object Relational Mapper
4. Marshmallow : Serializer and Validator
5. Postgresql : Persistance database
6. Redis : Flask Caching<SimpleCache>
7. Flask JWT Exended : Authentication/Authorization
8. Docker Compose : Container
9. Swagger : Documentation

## :traffic_light:  How to Run
1. Build with 'docker-compose build'
2. Run with 'docker-compose up -d' for detach mode or if there is bugs you can try <docker-compose up --remove-orphans --force-recreate> and close your console

## :trolleybus: How to Migrate DB Models 
If you changes the db models or schema, please migrate and upgrade DB via alembic with :
1. Make sure services are all running
2. Enter container app with 'docker exec -it hospital_service bash'
3. Run 'python manage.py db init' for migrating
4. Run 'python manage.py db migrate' for migrating
5. Run 'python manage.py db upgrade' for applying those migrations to the DB
6. Exit

## :bar_chart: Project Structure
No need to explain the project structure, I think everything served is clear enough.

## :clipboard: How To Check Documentation(Function and Guideline)
1. Run in browser "http://0.0.0.0:8001/"

2. Click default namespace and you can see all endpoint

3. For the first you can check the endpoint can be access, check alive endpoint => try it out => response == alive <success>

4. Register User/Employee with endpoint /user/registration and execute with example body json:

{
  "name": "Muhamad Gofur Muzaqi",
  "email": "muhamadgofurmuzaqi@gmail.com",
  "password": "password",
  "gender": "Pria",  
  "birthdate": "2022-07-29"
}
Noted: 
a. Gender is type enumerate from the 2 option 'Pria' or 'Perempuan'
b. Get your access token and skip step 5 or you want get access token from endpoint /user/login just continue the step

5. Get your access token from /user/login with example body json
{
  "email": "muhamadgofurmuzaqi@gmail.com",
  "password": "password"
}

6. When response appear get access token in response

7. Place your acces token with example <Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....> in authorization with the symbol padlock after than insert and the padlock will be closed

8. You can try access all endpoint with fields served, for field's activity if there is more one activity i think better using String List with example => {"activity" : "['create documantation', 'Bug Fix']"} and for Column Status there is some choice like Gender ['DONE', 'IN_QUEUE', 'CANCELLED ] and for example => {"status" : "DONE"} or other.

9. if you want log out just click padlock again and execute botton logout.

10. Finish
