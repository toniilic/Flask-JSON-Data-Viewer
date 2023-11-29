# db.py
import sqlite3
import logging

def get_page_data(page, per_page):
    total_pages = 0
    try:
        with sqlite3.connect('api_data.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM endpoint_data")
            total_records = cursor.fetchone()[0]
            total_pages = (total_records + per_page - 1) // per_page

            start = (page - 1) * per_page
            cursor.execute("SELECT * FROM endpoint_data LIMIT ? OFFSET ?", (per_page, start))
            page_data = cursor.fetchall()

        page_data_dicts = [dict(row) for row in page_data]
        return page_data, total_pages

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return [], 0
