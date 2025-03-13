import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()


hostname = os.getenv('HOSTNAME')
username = os.getenv('USERNAME')
database = os.getenv('DATABASE')
port_id = os.getenv('PORT_ID')
pswd = os.getenv('PSWD')

def import_data():
    '''This is a function to query the database and return a dataframe with the
    result set'''

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        query = f"""SELECT disease, patient_response
	                FROM ars.patient_risks
	                WHERE disease in ('Diabetes', 'Tuberculosis', 'HIV')
                    and "createdAt" between '{start_date}' and '{end_date}'
	                """
                    
                    # and "createdAt" between '{start_date}' and '{end_date}'
                    
                    # """

        conn = psycopg2.connect(
                host=hostname,
                database=database,
                user=username,
                password=pswd,
                port=port_id
            )
        
        df = pd.read_sql_query(query, conn)

        conn.close()

        # If the result set is empty:
        if df.empty:
            print("No records found for the past week.")
            return None
        
        return df
    
    except Exception as e:
        print(f"Error: {e}")
        return None