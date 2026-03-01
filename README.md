# GESP C++ Study Plan System

## Project Structure

```
GESPC++_studyPlan/
├── frontend/             # Frontend files
│   ├── core/             # Core functionality
│   │   └── study_plan.html  # Main study plan page
│   ├── course/           # Course system
│   │   └── course_system.html
│   ├── programming/      # Online programming tool
│   │   └── online_programming.html
│   ├── tests/            # Test files
│   │   ├── test_all_features.html
│   │   └── test_features.html
│   ├── materials/        # Study materials
│   │   └── real_test_question_materials/  # Past exam papers
│   ├── auth/             # Authentication pages
│   │   └── login.html        # Login page
├── backend/              # Backend files (Python + Flask)
│   ├── routes/           # API routes
│   │   ├── auth.py       # Authentication routes
│   │   ├── notes.py      # Note management routes
│   │   └── users.py      # User management routes
│   ├── app.py            # Flask application
│   ├── models.py         # Database models
│   ├── init_db.py        # Database initialization
│   ├── requirements.txt  # Python dependencies
│   └── .env              # Environment configuration
└── database/             # Database configuration
    └── db_config.py      # Database setup and initialization
```

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, Flask, Flask-SQLAlchemy, JWT
- **Database**: MySQL
- **Authentication**: JWT tokens

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Configure environment variables in `.env` file:
   ```
   DATABASE_URL=mysql+pymysql://root:password@localhost/gesp_study_plan
   JWT_SECRET_KEY=your_jwt_secret_key
   FLASK_APP=app.py
   FLASK_ENV=development
   ```

4. Initialize database:
   ```bash
   python init_db.py
   ```

5. Start the backend server:
   ```bash
   python app.py
   ```

### 2. Frontend Setup

1. Open the frontend home page in your browser:
   ```
   frontend/index.html
   ```

2. Use the demo account to login:
   - Username: demo
   - Password: 123456

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

### Notes
- `GET /api/notes` - Get all notes
- `GET /api/notes/<id>` - Get single note
- `POST /api/notes` - Create note
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note
- `POST /api/notes/upload` - Upload image

### Users
- `GET /api/users/me` - Get current user info
- `PUT /api/users/me` - Update current user info
- `GET /api/users/<id>` - Get user info

## Features

1. **User Authentication**: Secure login and registration system
2. **Study Plan Management**: 8-week study plan for GESP C++ Level 2
3. **Note Taking**: Create, edit, and delete notes with text and images
4. **Online Programming**: Access to online programming tools
5. **Course System**: Course management functionality
6. **Past Exam Papers**: Access to real test question materials

## Usage

1. Login to the system using your credentials
2. Access the study plan from the dashboard
3. View weekly study topics and core knowledge points
4. Access past exam papers for practice
5. Take notes and track your progress
6. Use the online programming tool for coding practice

## Database Schema

### Users Table
- id (INT, PRIMARY KEY)
- username (VARCHAR(50), UNIQUE)
- password (VARCHAR(255))
- email (VARCHAR(100), UNIQUE)
- created_at (DATETIME)
- updated_at (DATETIME)

### Notes Table
- id (INT, PRIMARY KEY)
- user_id (INT, FOREIGN KEY)
- title (VARCHAR(255))
- content (TEXT)
- type (VARCHAR(20))
- images (JSON)
- created_at (DATETIME)
- updated_at (DATETIME)

## License

This project is for educational purposes only.
