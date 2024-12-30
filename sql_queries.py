import sqlite3

def fetch_tracking_data():
    """
    Retrieve all tracking data from the SQLite database.

    Returns:
        list: A list of tuples, where each tuple represents a row of tracking data.
    """
    # Connect to the SQLite database
    sql_connection = sqlite3.connect("tracking_data.db")
    cursor = sql_connection.cursor()

    # Fetch all rows from the tracking_data table
    cursor.execute("SELECT * FROM tracking_data")
    rows = cursor.fetchall()

    # Close the database connection
    sql_connection.close()

    return rows

def fetch_tracking_data_for_id(object_id):
    """
    Retrieve tracking data for a specific object ID from the SQLite database.

    Args:
        object_id (int): The ID of the object for which tracking data is requested.

    Returns:
        list: A list of tuples, where each tuple represents a row of tracking data for the given object ID.
    """
    # Connect to the SQLite database
    sql_connection = sqlite3.connect("tracking_data.db")
    cursor = sql_connection.cursor()

    # Fetch all rows for the given object ID
    cursor.execute("SELECT * FROM tracking_data WHERE object_id = ?", (object_id,))
    rows = cursor.fetchall()

    # Close the database connection
    sql_connection.close()

    return rows

def print_tracking_data(data):
    """
    Display tracking data in a human-readable format.

    Args:
        data (list): A list of tuples, where each tuple represents a row of tracking data.

    Prints:
        The tracking data as a formatted table. If no data is provided, it informs the user.
    """
    if not data:
        print("No tracking data found in the database.")
        return

    print("Frame | Object ID | X1 | Y1 | X2 | Y2 | Confidence")
    print("---------------------------------------------------")
    for row in data:
        frame_number, object_id, x1, y1, x2, y2, confidence = row
        print(f"{frame_number:5} | {object_id:9} | {x1:3} | {y1:3} | {x2:3} | {y2:3} | {confidence if confidence is not None else 0.00:.2f}")

def setup_database():
    """
    Set up the SQLite database for tracking data storage.

    Ensures the `tracking_data` table exists with the required schema.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    sql_connection = sqlite3.connect("tracking_data.db")
    cursor = sql_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracking_data (
            frame_number INTEGER,
            object_id INTEGER,
            x1 INTEGER,
            y1 INTEGER,
            x2 INTEGER,
            y2 INTEGER,
            confidence REAL
        )
    """)
    sql_connection.commit()
    return sql_connection

def batch_insert_tracking_data(sql_connection, data_batch):
    """
    Insert a batch of tracking data into the database.

    Args:
        sql_connection (sqlite3.Connection): The SQLite connection object.
        data_batch (list): A list of tuples, where each tuple represents a row of tracking data.
    """
    cursor = sql_connection.cursor()
    cursor.executemany("""
        INSERT INTO tracking_data (frame_number, object_id, x1, y1, x2, y2, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data_batch)
    sql_connection.commit()

if __name__ == "__main__":
    """
    Main script execution.

    Demonstrates fetching and printing all tracking data, 
    and fetching data for a specific object ID.
    """
    print_tracking_data(fetch_tracking_data())
    print_tracking_data(fetch_tracking_data_for_id(1))
