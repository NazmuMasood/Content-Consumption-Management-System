# Content-Consumption-Management-System

## A Python shell program to help keep track of all your contents i.e. Books, Series, Movies consumptions.

Main requirements: Python v3.2+, MySql/PostgreSQL.

Please kindly do the following to setup the program:
1. After pulling project from github, open terminal and cd into project directory
```
cd project_directory
```

2. Create python virtual environment, activate it and install required libraries
```
python -m venv env 
source env/Scripts/activate
pip install -r requirements.txt
```

3. In your local MySql/PostgreSql server, create a database named 'dsi_task_1.db'
4. Update the db_connection_string in connection.py 
```
engine = create_engine('mysql+mysqldb://user:password@host:port/dbname',...)
```
5. Run models.py to create the necessary tables in 'dsi_task_1.db'
```
python models.py
```

6. (optional) Run db_seed.py to seed some dummy data into database
```
python db_seed.py
```

7. Finally, run app.py ! 
```
python app.py
```