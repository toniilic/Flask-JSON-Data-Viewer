import db

def print_first_page():
    page = 1
    per_page = 5  # Adjust the number of items per page as needed

    page_data, total_pages = db.get_page_data(page, per_page)

    print(f"Total Pages: {total_pages}")
    for row in page_data:
        print(row)

if __name__ == "__main__":
    print_first_page()
