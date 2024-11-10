import psycopg2
from psycopg2.extras import RealDictCursor
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/healthcare_chatbot")

def init_db():
    """
    Connects to PostgreSQL and creates necessary tables (conversations, messages) if they do not exist.
    It will not replace or modify existing tables or data.
    """
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cur:
        
        # Create 'conversations' table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                chat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_uuid UUID NOT NULL,  -- Stores UUID to identify the user without needing a users table
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                conversation_name VARCHAR(255),
                ended_at TIMESTAMP
            );
        """)
        
        # Create 'messages' table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id SERIAL PRIMARY KEY,
                chat_id UUID REFERENCES conversations(chat_id) ON DELETE CASCADE,
                sender VARCHAR(10) CHECK (sender IN ('user', 'bot')),
                message_text TEXT NOT NULL,
                diagnosis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
    print("Database tables checked and created if they did not exist.")
    conn.close()

# PostgreSQL connection helper
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
