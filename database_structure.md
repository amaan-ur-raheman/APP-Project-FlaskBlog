# Database Structure

This document outlines the database schema for the Flask blog application. The database consists of four tables: `User`, `Post`, `Like`, and `Comment`.

## `User` Table

Represents a user in the database.

| Column      | Type        | Constraints                               | Description                               |
|-------------|-------------|-------------------------------------------|-------------------------------------------|
| `id`        | Integer     | Primary Key                               | The primary key for the user.             |
| `username`  | String(20)  | Unique, Not Nullable                      | The user's unique username.               |
| `email`     | String(120) | Unique, Not Nullable                      | The user's unique email address.          |
| `image_file`| String(20)  | Not Nullable, Default: "default.jpg"      | The filename of the user's profile picture. |
| `password`  | String(60)  | Not Nullable                              | The user's hashed password.               |

**Relationships:**
- Has a one-to-many relationship with the `Post` table (`posts`).
- Has a one-to-many relationship with the `Like` table.
- Has a one-to-many relationship with the `Comment` table.


## `Post` Table

Represents a blog post in the database.

| Column    | Type       | Constraints                               | Description                                   |
|-----------|------------|-------------------------------------------|-----------------------------------------------|
| `id`      | Integer    | Primary Key                               | The primary key for the post.                 |
| `title`   | String(100)| Not Nullable                              | The title of the post.                        |
| `date`    | DateTime   | Not Nullable, Default: `datetime.utcnow`  | The date and time the post was created.       |
| `content` | Text       | Not Nullable                              | The content of the post.                      |
| `user_id` | Integer    | Foreign Key (`user.id`), Not Nullable     | The foreign key of the user who created the post. |

**Relationships:**
- Belongs to one `User` (`author`).
- Has a one-to-many relationship with the `Like` table (`likes`).
- Has a one-to-many relationship with the `Comment` table.


## `Like` Table

Represents a "like" on a post by a user. This table facilitates a many-to-many relationship between users and posts.

| Column    | Type    | Constraints                             | Description                                  |
|-----------|---------|-----------------------------------------|----------------------------------------------|
| `id`      | Integer | Primary Key                             | The primary key for the like.                |
| `user_id` | Integer | Foreign Key (`user.id`), Not Nullable   | The foreign key of the user who liked the post. |
| `post_id` | Integer | Foreign Key (`post.id`), Not Nullable   | The foreign key of the post that was liked.  |

**Relationships:**
- Belongs to one `User`.
- Belongs to one `Post`.


## `Comment` Table

Represents a comment on a blog post.

| Column        | Type     | Constraints                               | Description                                     |
|---------------|----------|-------------------------------------------|-------------------------------------------------|
| `id`          | Integer  | Primary Key                               | The primary key for the comment.                |
| `content`     | Text     | Not Nullable                              | The text content of the comment.                |
| `date_posted` | DateTime | Not Nullable, Default: `datetime.utcnow`  | The date and time the comment was posted.       |
| `user_id`     | Integer  | Foreign Key (`user.id`), Not Nullable     | The foreign key of the user who wrote the comment. |
| `post_id`     | Integer  | Foreign Key (`post.id`), Not Nullable     | The foreign key of the post that was commented on. |

**Relationships:**
- Belongs to one `User` (`author`).
- Belongs to one `Post`.