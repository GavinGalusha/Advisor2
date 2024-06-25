import psycopg2
from urllib.parse import urlparse


'''

db_url = "postgres://u52dsk3si0k6ia:pf08abb93f28e105ac8c4d3001ab478e029bc71d2ee2e39eb348ee9abb741fc14@c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7b3q6b26t3n4i"
parsed_url = urlparse(db_url)

# Extract components from the URL
dbname = parsed_url.path[1:]  # Skip the leading '/'
user = parsed_url.username
password = parsed_url.password
host = parsed_url.hostname
port = parsed_url.port


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



tables = list_tables_and_columns(dbname = dbname, user = user, password = password, host = host, port = port)
print(tables)



def fetch_text_column(dbname, user, password, host, port, table_name, text_column_name):
    """Fetches the text column from all rows in the specified table."""
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




advice_text = fetch_text_column(dbname = dbname, user = user, password = password, host = host, port = port, table_name = "advice", text_column_name = "text")
# this will show you the text in the database
print(advice_text)  
'''