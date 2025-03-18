import streamlit as st
import sqlite3

def init_db():
    conn = sqlite3.connect("library.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    year INTEGER,
                    status TEXT DEFAULT 'Available')''')
    conn.commit()
    conn.close()

def add_book(title, author, year):
    with sqlite3.connect("library.db") as conn:
        conn.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))

@st.cache_data
def list_books():
    with sqlite3.connect("library.db") as conn:
        return conn.execute("SELECT * FROM books").fetchall()

def update_status(book_id, status):
    with sqlite3.connect("library.db") as conn:
        conn.execute("UPDATE books SET status = ? WHERE id = ?", (status, book_id))

def delete_book(book_id):
    with sqlite3.connect("library.db") as conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))

st.title("📚 Library Manager")
init_db()

title = st.text_input("Title")
author = st.text_input("Author")
year = st.number_input("Year", min_value=0, max_value=2100, step=1)

if st.button("Add Book") and title and author and year > 0:
    add_book(title, author, year)
    st.cache_data.clear()
    st.rerun()

for book in list_books():
    st.write(f"{book[1]} by {book[2]} ({book[3]}) - {book[4]}")
    
    if st.button(f"Toggle Status {book[0]}", key=f"toggle_{book[0]}"):
        new_status = 'Available' if book[4] == 'Checked Out' else 'Checked Out'
        update_status(book[0], new_status)
        st.cache_data.clear()
        st.rerun()

    if st.button(f"Delete {book[0]}", key=f"del_{book[0]}"):
        delete_book(book[0])
        st.cache_data.clear()
        st.rerun()
