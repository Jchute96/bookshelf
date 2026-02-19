# BookShelf - Personal Book Tracking Application

## About

BookShelf is a full-stack Django web application for tracking your personal reading journey. Users can manage their book collection, track books by reading status, organize custom book lists, view reading statistics, and export their book lists to share with others. 

Built as a way to demonstrate full-stack web development skills including Django MVT architecture, user authentication, database design, and responsive UI development. 

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

## Tech Stack
- Backend: Django 6.0.1
- Language: Python 3.14
- Database: SQLite
- Frontend: HTML, Bootstrap 5.2.0
- Forms: django-crispy-forms with Bootstrap 5
- Image Handling: Pillow
- PDF Generation: WeasyPrint
- Fonts: Inter(Google Fonts)

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/jchute/bookshelf.git
cd bookshelf

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```



## Project Structure
```
bookshelf/
├── books/          # Core book management app
├── accounts/       # User authentication and profiles
├── lists/          # Custom and essential book lists
├── config/         # Django project settings and URLs
├── static/         # Static files (images, CSS)
└── templates/      # HTML templates
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


