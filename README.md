# Flask Blog

A feature-rich blog application built with Flask that allows users to create, edit, and manage blog posts. This application serves as a robust starting point for developers looking to build a content-focused web application, complete with user authentication, post management, and a clean, responsive interface.

## Key Features

-   **User Authentication**: Secure registration, login, and logout functionality.
-   **Password Reset**: Email-based password reset for account recovery.
-   **Post Management**: Full CRUD (Create, Read, Update, Delete) operations for blog posts.
-   **Profile Customization**: Users can update their account information and profile picture.
-   **Post Interaction**: Users can "like" and comment on posts.
-   **Database Integration**: Uses SQLAlchemy for ORM-based database management.
-   **Responsive Design**: Built with Bootstrap for a seamless experience on all devices.

## Getting Started

Follow these instructions to get a local copy of the project up and running.

### Prerequisites

-   Python 3.6+
-   `pip` for package management

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amaan-ur-raheman/APP-Project-FlaskBlog.git
    cd APP-Project-FlaskBlog
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *On Windows, use `venv\\Scripts\\activate`*

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Create a `.env` file in the root directory by copying the example file:
        ```bash
        cp .env.example .env
        ```
    -   Open the `.env` file and update the following variables with your own settings:
        -   `SECRET_KEY`: A long, random string for security.
        -   `SQLALCHEMY_DATABASE_URI`: The connection string for your database (defaults to SQLite).
        -   `MAIL_USERNAME` and `MAIL_PASSWORD`: Your email credentials for password reset emails.

5.  **Initialize and upgrade the database:**
    ```bash
    flask db init  # Run this only once to initialize migrations
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6.  **Run the application:**
    ```bash
    flask run
    ```

7.  **Access the application** by navigating to `http://127.0.0.1:5000/` in your web browser.

## Technologies Used

-   **Flask**: A lightweight WSGI web application framework.
-   **Flask-SQLAlchemy**: An extension for Flask that adds support for SQLAlchemy.
-   **Flask-WTF**: A Flask extension for working with WTForms.
-   **Flask-Login**: An extension to manage user sessions.
-   **Flask-Bcrypt**: A Flask extension for hashing passwords.
-   **Flask-Mail**: A Flask extension for sending emails.
-   **Flask-Migrate**: An extension that handles SQLAlchemy database migrations for Flask applications using Alembic.
-   **Bootstrap**: A popular front-end framework for developing responsive, mobile-first projects on the web.

## Future Enhancements

-   [ ] Add categories and tags for organizing posts.
-   [ ] Implement a search feature to find posts.
-   [ ] Enable pagination for comments.
-   [ ] Introduce user roles and permissions.

## Made By

1.  Abhijit Raut: 202301103115
2.  Amaan Ur Raheman: 202301103120
3.  Soham Vaidya: 202301103124
4.  Aditya Lokhande: 202301103127