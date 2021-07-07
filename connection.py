from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

### --- Db connection

## --- PostgreSql
## 'db_connection_string' = 'postgresql+psycopg2://user:password@host:port/dbname'
# <<<<<<< To use PostgreSQL, uncomment below line >>>>>>>>
# engine = create_engine('postgresql+psycopg2://postgres:@127.0.0.1:5432/dsi_task_1', connect_args={"options": "-c timezone=utc"}, echo=False)
 
## --- MySql
## 'db_connection_string' = 'mysql+mysqldb://user:password@host:port/dbname'
# <<<<<<< To use MySQL, uncomment below line >>>>>>>>
engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/dsi_task_1', connect_args={"init_command": "SET SESSION time_zone='+00:00'"}, echo=False)

class Db:

    @staticmethod
    ### Creating (sqlAlchemy) session to make db operations
    def startSession():
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    @staticmethod
    ### Ending (sqlAlchemy) session after db operations
    def closeSession(session):
        session.close()


