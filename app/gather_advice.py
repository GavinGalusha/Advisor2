import psycopg2
from urllib.parse import urlparse
import os
import shutil

print("starting")

database_url = os.getenv('DATABASE_URL')
parsed_url = urlparse(database_url)

# Extract components from the URL
dbname = parsed_url.path[1:]  # Skip the leading '/'
user = parsed_url.username
password = parsed_url.password
host = parsed_url.hostname
port = parsed_url.port

print("database accessed")

def list_tables_and_columns(dbname, user, password, host, port):
    """Lists all tables and their columns in the specified database."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        
        # Query to fetch all table names
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cur.fetchall()
        
        # Dictionary to hold table names and their columns
        table_info = {}
        
        # Fetch columns for each table
        for table in tables:
            table_name = table[0]
            cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}'")
            columns = cur.fetchall()
            table_info[table_name] = [column[0] for column in columns]
        
        return table_info
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()






def fetch_text_column(dbname, user, password, host, port, table_name, text_column_name):
    """Fetches the text column from all rows in the specified table."""
    print("fetching text column")
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        # Execute the query
        cur.execute(f"SELECT {text_column_name} FROM {table_name}")
        # Fetch all rows
        rows = cur.fetchall()
        # Extract the text column from each row
        text_data = [row[0] for row in rows]
        return text_data
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()



def update_casual_knowledge():
    advice_text = fetch_text_column(dbname = dbname, user = user, password = password, host = host, port = port, table_name = "advice", text_column_name = "text")
    # this is not efficient, but gets the job done
    import os
    directory = "app/data/Advice"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted {file_path}")

    
    storage_dir = "index_storage2"
    if os.path.exists(storage_dir):
        shutil.rmtree(storage_dir)
        print(f"Deleted {storage_dir}")


    for text in advice_text:
        with open("app/data/Advice/advice.txt", "a") as file:
            file.write(text)
            file.write("\n")



#advice_text = fetch_text_column(dbname = dbname, user = user, password = password, host = host, port = port, table_name = "advice", text_column_name = "text")
# this will show you the text in the database under the advice table, 
# just need to iterate through this list and add it all to the Advice directory here app/data/Advice, not sure if it's important if it's in individual text files or not





#update_casual_knowledge()
#print(advice_text)




