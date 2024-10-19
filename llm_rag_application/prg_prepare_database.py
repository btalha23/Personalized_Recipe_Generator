import pandas as pd
import os

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import mysql.connector


# # Database connection details
# # Database connection details
server = 'rag_application_server'
prg_database_name = 'personalized_recipe_generator'
user = 'root'
password = 'root'
host="localhost"
port="3306"

def get_file_path() -> str:
    current_path = os.getcwd()
    print(current_path)

    os.chdir('../dataset/')
    path_base_dataset = os.getcwd()
    print(path_base_dataset)

    os.chdir('../llm_rag_application/')
    path_base_llm_rag_app = os.getcwd()
    print(path_base_llm_rag_app)

    NUM_DATA_SAMPLES = 50000
    file_name = '/sampled_dataset_' + str(NUM_DATA_SAMPLES) + '.csv'
    sampled_data_file_path = path_base_dataset + file_name

    return sampled_data_file_path

def db_establish_connection(user: str, password: str, host: str, database: str):
    # Connect to MySQL (without specifying a database)
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    cursor = connection.cursor()
    
    print(f"Connection to MySQL server successfully established with username {user}, password {password}, and host {host}") 

    # Create a new database
    prg_database_name = database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {prg_database_name};")
    print(f"Database {prg_database_name} created successfully.")

    # Commit changes and close connection
    connection.commit()
    cursor.close()
    connection.close()

def get_db_uri(user: str, password: str, host: str, port: str, database: str):
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return db_uri

def read_csv_data(filename: str) -> pd.DataFrame:

    """   
    Read out the data from the specified CSV File
    This function is used to load the data sampled from a large dataset for training the model (X_train).
    The same function is used to load the simulated user responses that make the labels (y_train) for the model.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """

    print(f"Loading data from {filename}")
    
    df = pd.read_csv(filename)

    return df

def db_populate_table(db_uri: str, df: pd.DataFrame):
    # Create a connection engine using SQLAlchemy
    engine = create_engine(db_uri)

    # Write the DataFrame to the MySQL database as a table
    table_name = 'recipe_knowledge_base'  # Name the table you want to create in the database
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    print(f"Table {table_name} populated successfully.")

def prg_prepare_database():
   
   filename = get_file_path()
   print(f"File path {filename}")
   
   df = read_csv_data(filename=filename)
   print(f"{df.head()}")
   print("Now calling db_establish_connection() function")
   
   db_establish_connection(user=user, password=password, host=host, database=prg_database_name)
   print(f"Connection with the database established successfully")
   print("Now calling get_db_uri() function")
   
   db_uri = get_db_uri(user=user, password=password, host=host, port=port, database=prg_database_name)
   db_populate_table(db_uri=db_uri, df=df)
