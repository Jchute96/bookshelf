# BookShelf - Personal Book Tracker

A Django web application for tracking the books I have read, including ratings, reviews, and dates finished.

## About This Project

This is my first project using and learning Django. I followed [The Python Code's Django Bookstore tutorial](https://thepythoncode.com/article/build-bookstore-app-with-django-backend-python) as a foundation and customized it for personal book tracking.

### Changes I made from Tutorial
- Replaced bookstore fields (price, ISBN) with personal tracking fields (rating, review, genre, date_finished)
- Added 10 genre categories with dropdown selection
- Implemented 1-5 star rating system with validation
- Added optional date tracking for completion dates
- Customized all templates and forms for book tracking workflow


## Features

- Add, view, edit, and delete books
- Purchase link to book listings
- 1-5 star rating system
- Write and store book reviews
- Upload book cover images
- Organize by 10 different genres
- Track reading completion dates
- Alphabetically sorted book display
- Bootstrap-styled responsive interface
- Dynamically display star ratings on home page book cards
- Filter books by genre, star rating, and completion date

## Future Features

- [ ] Enhanced UI design with more vibrant/fun styling
- [ ] Expanded navigation menu with additional options
- [ ] Improved code documentation and comments
- [ ] Statistics dashboard:
  - Total books read
  - Books per genre breakdown
  - Most read genre
  - Average rating
  - Reading trends over time
     
## Tech Stack
- **Backend:** Django 6.0.1
- **Language:** Python 3.14
- **Database:** SQLite
- **Frontend:** HTML, Bootstrap 5




