import sqlite3

def list_tables(database_path):
    """
    Retrieve and list all table names from an SQLite database.

    Args:
        database_path (str): Path to the SQLite database file.

    Returns:
        list: A list of tuples, where each tuple contains the name of a table in the database.
              If no tables exist, returns an empty list.
    """
    # Establish a connection to the SQLite database
    sql_connection = sqlite3.connect(database_path)
    cursor = sql_connection.cursor()

    # Query to retrieve all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Close the database connection
    sql_connection.close()

    return tables

if __name__ == "__main__":
    """
    Main entry point for the script. Connects to a specified SQLite database and lists all tables.
    """
    # Specify the path to the database
    db_path = "tracking_data.db"

    # Retrieve the list of tables
    tables = list_tables(db_path)

    # Print the tables, if any exist
    if tables:
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the database.")
