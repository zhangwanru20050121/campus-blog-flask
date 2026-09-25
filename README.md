# Campus Blog Web System

A campus-oriented blog web application built with Python Flask, allowing users to register, publish articles, browse posts, and interact through likes.

## Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite + SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Jinja2
- **Authentication**: Flask-Login, Flask-WTF

## Features

- User registration and login
- User profile with avatar upload
- Article creation, editing, and deletion (CRUD)
- Article browsing and detail view
- Ajax-based asynchronous like/unlike
- Duplicate like prevention via composite unique constraint
- Role-based access control (guest vs. logged-in user)
- Form validation and secure session management

## Project Structure

```
blog/
├── app.py              # Main application entry
├── forms.py            # Flask-WTF form definitions
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── blog.css
│   ├── js/
│   │   ├── article_likes.js
│   │   └── password_toggle.js
│   └── uploads/        # User avatar uploads
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── profile.html
    ├── article_list.html
    ├── article_view.html
    ├── article_edit.html
    └── navbar.html
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/zhangwanru20050121/campus-blog-flask.git
cd campus-blog-flask
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit:
```
http://127.0.0.1:5000
```

## Key Design Decisions

- **Composite unique constraint**: The Like model uses a composite unique constraint on (`user_id`, `article_id`) to prevent duplicate likes at the database level.
- **Role-based permissions**: Guests can browse articles but cannot like or publish; logged-in users have full access.
- **Asynchronous interaction**: Like actions are handled via Ajax for a smoother user experience without page reload.

## Author

Wanru Zhang - Shanghai Jianqiao University, Network Engineering
