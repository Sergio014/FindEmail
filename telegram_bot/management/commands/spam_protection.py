import sqlite3
from datetime import datetime, timedelta

# Function to check the number of messages sent by a user and impose escalating bans
def check_message_count(user_id):
    # Connect to the database
    conn = sqlite3.connect('message_db.sqlite')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_messages (
                        user_id TEXT PRIMARY KEY,
                        message_count INTEGER DEFAULT 0,
                        ban_expiry_date TEXT
                    )''')
    conn.commit()

    # Get the user's current message count and ban expiry date
    cursor.execute("SELECT message_count, ban_expiry_date FROM user_messages WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    # Check if the user is banned and calculate the ban duration
    if result and result[1] and datetime.now() < datetime.strptime(result[1], "%Y/%m/%d"):
        ban_expiry_date = datetime.strptime(result[1], "%Y/%m/%d")
        ban_duration = (ban_expiry_date - datetime.now()).days
        return True
    else:
        # User is not banned or the ban has expired, proceed to check message count
        if result:
            message_count = result[0]
        else:
            message_count = 0

        # Increment the message count by 1 and update the database
        message_count += 1
        cursor.execute("REPLACE INTO user_messages (user_id, message_count) VALUES (?, ?)", (user_id, message_count))
        conn.commit()

        # Check if the user has crossed the ban threshold
        if message_count > 8:
            ban_duration = message_count - 7
            ban_expiry_date = (datetime.now() + timedelta(days=ban_duration)).strftime("%Y/%m/%d")
            cursor.execute("UPDATE user_messages SET ban_expiry_date = ? WHERE user_id = ?", (ban_expiry_date, user_id))
            conn.commit()
            return True
        else:
            return False