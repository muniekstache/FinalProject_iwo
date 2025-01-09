import requests
import json
import os

def get_romance_and_scifi_books():
    """
    Fetch all books from Project Gutenberg (via Gutendex) and separate them
    into two lists: one for Romance books and one for Science Fiction books.
    """
    romance_books = []
    scifi_books = []
    next_url = "https://gutendex.com/books"

    # Define subjects to include and exclude
    romance_includes = ["love stories", "romance fiction", "romantic fiction", "man-woman relationships -- fiction", "domestic fiction"]
    scifi_includes = ["science fiction", "science fiction -- fiction"]
    excludes = ["short stories", "poetry", "drama", "essays", "juvenile fiction", "non-fiction"]

    while next_url:
        response = requests.get(next_url)
        data = response.json()

        for book in data["results"]:
            # Convert each subject to lowercase to make filtering easier
            subjects = [subject.lower() for subject in book["subjects"]]

            # Filter out non-English books
            if book["languages"][0] != "en":
                continue

            # Check for exclusions first
            if any(exclude in subj for subj in subjects for exclude in excludes):
                continue

            # If a book matches romance criteria, store it in romance_books
            if any(include in subj for subj in subjects for include in romance_includes):
                print("add romance book: " + book["title"])
                print(book["subjects"])
                print("---------------")
                romance_books.append(book)

            # If a book matches science fiction criteria, store it in scifi_books
            if any(include in subj for subj in subjects for include in scifi_includes):
                print("add scifi book: " + book["title"])
                print(book["subjects"])
                print("---------------")
                scifi_books.append(book)

        # The 'next' field is a link to the next page of results
        next_url = data["next"]

    return romance_books, scifi_books

def store_books_as_json(romance_books, scifi_books, folder="."):
    """
    Stores the two lists of books (romance and science fiction) into separate
    JSON files in the specified folder.
    """
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    romance_path = os.path.join(folder, "romance_books.json")
    scifi_path = os.path.join(folder, "scifi_books.json")

    # Write each list of books to a JSON file
    with open(romance_path, "w", encoding="utf-8") as f:
        json.dump(romance_books, f, ensure_ascii=False, indent=2)

    with open(scifi_path, "w", encoding="utf-8") as f:
        json.dump(scifi_books, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Fetch and separate the books
    romance_books, scifi_books = get_romance_and_scifi_books()

    # Store results in the current directory's 'book_data' folder
    store_books_as_json(romance_books, scifi_books, folder="book_data")

    # Print summary
    print(f"Total Romance Books: {len(romance_books)}")
    print(f"Total Science Fiction Books: {len(scifi_books)}")
