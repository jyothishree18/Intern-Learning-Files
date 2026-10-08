# Week 4 

## 1. What does Pydantic give you for free?

Pydantic automatically checks and validates the data we send. If the
data is wrong, we get a **422 error**.

## 2. Why use `?` / `%s` in SQL?

We use placeholders to safely pass values to SQL and prevent **SQL
injection**. We shouldn't put user values directly into an f-string.

## 3. What is a primary key and foreign key?

A **primary key** uniquely identifies a record in a table. A **foreign
key** connects one table to another.

## 4. What does an ORM do?

An ORM lets us work with database tables using programming objects
instead of writing SQL for everything. In Python, **SQLAlchemy** is an
example.

## 5. What is CORS?

CORS controls which websites can access our API through a browser. It
doesn't affect tools like **Postman** or backend-to-backend requests.

## 6. Why use an environment variable for the database URL?

It keeps sensitive details like the **database password** out of our
code and GitHub.

## 7. What is Dependency Injection?

It means giving a function or class the things it needs instead of
creating them itself.

-   **FastAPI:** `Depends()`
-   **Spring:** `@Autowired`

## 8. What is Separation of Concerns?

It means keeping different responsibilities separate. In my project,
**`app.py` handles the API and authentication, while `crud.py` handles
database operations**.
