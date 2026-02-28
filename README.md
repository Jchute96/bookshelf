# BookShelf - Personal Book Tracking Application

## Live Demo

**[Try the Demo — no sign up required](https://web-production-6dbf7.up.railway.app/demo-login/)** — click to instantly log in as a demo user pre-loaded with books, lists, and reviews.

Or browse the app as a logged-in user at [BookShelf Live](https://web-production-6dbf7.up.railway.app/books).

## About

BookShelf is a deployed full-stack Django web application for tracking your personal reading journey. Users can manage their book collection, track books by reading status, organize custom book lists, view reading statistics, and export their book lists to share with others.

Built to demonstrate full-stack web development skills including Django MVT architecture, user authentication, PostgreSQL database design, cloud media storage, and production deployment.

## Features

### Book Management
- Add, view, edit, and delete books
- Track reading status: Want to Read, Currently Reading, Finished
- 1-5 star rating system with dynamic star display
- Write and store personal book reviews
- Upload book cover images
- Store purchase links for easy access
- Organize books by 10 different genres
- Track reading completion dates

### Search, Filter & Sort
- Search books by title or author
- Filter by genre, reading status, star rating, and year finished
- Sort by title, author, rating, and date finished

### User Authentication & Profiles
- Full multi-user support with private bookshelves
- User registration, login, logout
- Profile management - edit username and email
- Profile picture upload
- Password change and reset via email
- Secure account deletion with password confirmation
- Authenticated user redirects on login/register pages

### Book Lists
- Three automatic essential lists created based off of book reading statuses
- Create unlimited custom book lists
- Add and remove books from lists
- Dynamic list cover previews (1,2, or 2x2 grid based on book count)
- Edit and delete custom lists

### Export Functionality
- Export any list to CSV for spreadsheet use
- Export any list to formatted PDF for sharing
- Exports available for both essential and custom lists

### Statistics Dashboard
- Total books read and average rating overview
- Recent 5-star favorites display
- Detailed reading stats broken down by genre with custom icons
- Top 5 most read authors
- Books read per year breakdown

## Testing & CI/CD

The project includes a suite of automated tests covering core functionality across all apps, run automatically on every push and pull request to `main` via GitHub Actions.

### Test Coverage

**Books** (`books/tests.py`)
- Book model — star display rendering (1, 3, and 5 stars, and no rating)
- Home view — login redirect, page load, user data isolation
- Add book — creates book in database and redirects
- Delete book — removes from database, redirects, blocks unauthenticated users, returns 404 for another user's book
- Edit book — saves changes and redirects, returns 404 for another user's book
- Search — by title, by author, case insensitivity, no results
- Filter — by genre, status, rating, and year finished
- Statistics — total book count, average rating calculation, zero-state average, top 3 recent 5-star books, date requirement for top 3

**Accounts** (`accounts/tests.py`)
- Registration — user created in database, profile auto-created, auto-login after registration, duplicate username rejected

**Lists** (`lists/tests.py`)
- Create list — saves to database and redirects
- Delete list — removes from database and redirects
- Add/remove books — book added and removed from list with correct redirects
- Export — CSV returns correct content type and filename with book data; PDF returns correct content type and filename
- List detail — page loads and shows books in the list
- Edit list — renames list and redirects
- Essential lists — Finished, Currently Reading, and Want to Read each show only books with the matching status

### Running Tests Locally

```bash
python manage.py test
```

## Tech Stack
- Backend: Django 6.0.1
- Language: Python 3.14
- Database: PostgreSQL (production), SQLite (development)
- Frontend: HTML, Bootstrap 5.2.0
- Forms: django-crispy-forms with Bootstrap 5
- Image Storage: Cloudinary
- Image Handling: Pillow
- PDF Generation: ReportLab
- Deployment: Railway
- Fonts: Inter (Google Fonts)

## Setup & Installation

A live demo is available at [BookShelf](https://web-production-6dbf7.up.railway.app/books)

To run locally:
```bash
# Clone the repository
git clone https://github.com/jchute/bookshelf.git
cd bookshelf

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file with the following variables
SECRET_KEY=generate_a_random_secret_key  # Generate one at https://djecrety.ir
DEBUG=True
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Credits 

Inspired by [The Python Code's Django Bookstore tutorial](https://thepythoncode.com/article/build-bookstore-app-with-django-backend-python) and expanded into a fully featured multi-user personal book tracking application.

## License

    Copyright 2026 Jordan Chute

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


