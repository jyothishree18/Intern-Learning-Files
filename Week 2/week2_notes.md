# Week 2 Notes

## 1. What is 127.0.0.1? Is it a special IP address?

`127.0.0.1` is the **localhost** IP address. It points back to your own computer.

It is a **special/reserved IP address** used for testing applications locally.

**Example:** `http://127.0.0.1:5000` means your Flask/FastAPI application is running on your own computer.

---

## 2. What is Base64 encoding and decoding?

**Base64 encoding** converts binary/text data into a text format using characters like A-Z, a-z, 0-9, `+`, and `/`.

**Decoding** converts Base64 back to the original data.

It is commonly used in:
- Sending data through APIs
- Email attachments
- HTTP Basic Authentication
- Encoding small files or binary data

**Important:** Base64 is **encoding, not encryption**. It does not protect data from being read.

---

# Security & Encryption

## 3. Public key, private key, symmetric keys, asymmetric keys

### Symmetric key
The **same key** is used to encrypt and decrypt data.

**Example:** A password-protected file using one secret key.

### Asymmetric keys
Two related keys are used:
- **Public key** – can be shared
- **Private key** – must be kept secret

**Simple idea:**
- Symmetric = **one key**
- Asymmetric = **two keys**

---

## 4. What is a digital certificate / public certificate?

A **digital certificate** is like a digital ID card for a website or organization.

It helps prove that a public key belongs to the claimed website or organization.

**Example:** When you visit an HTTPS website, its certificate helps establish a trusted secure connection.

---

## 5. What is a Certificate Authority (CA)?

A **Certificate Authority (CA)** is a trusted organization that issues digital certificates.

Its role is to:
- Verify the identity of the certificate holder
- Issue/sign certificates
- Help browsers and systems trust the certificate

**Simple example:** CA = trusted organization that says, “This public key really belongs to this website.”

---

# Python Decorators & Dependency Injection

## 6. What are decorators in Python?

A **decorator** is a function that adds or changes the behavior of another function without changing its main code.

They are written using `@`.

**Example:**
```python
@app.get("/students")
def get_students():
    return students
```

Here, `@app.get()` is a decorator used to connect the function to an HTTP GET route.

### Why are decorators used?

They are commonly used for:
- Routing
- Authentication
- Authorization
- Logging
- Validation
- Middleware-like functionality

### What is `@router` in FastAPI?

In FastAPI, `APIRouter` helps organize related API routes.

Example:
```python
router = APIRouter()

@router.get("/students")
def get_students():
    return students
```

The decorator tells FastAPI that this function handles a GET request for `/students`.

---

## 7. What is Dependency Injection?

**Dependency Injection (DI)** means giving a function or class the resources it needs instead of making it create those resources itself.

It makes code easier to:
- Reuse
- Test
- Maintain

### In FastAPI

FastAPI commonly uses `Depends()`.

Example:
```python
@app.get("/students")
def get_students(db = Depends(get_db)):
    ...
```

Here, FastAPI provides the database dependency to the function.

---


## 8. Why should passwords be sent in headers or payloads, not URLs?

Passwords should **not** be placed in URLs or query parameters because URLs can be stored in:
- Browser history
- Server logs
- Proxy logs
- Analytics systems

For APIs, credentials are normally sent in the **request body** or **Authorization header**, depending on the authentication method.


---

## 9. What is the SOLID principle?

**SOLID** is a set of principles that helps developers write clean, maintainable, and flexible code.

It stands for:
- **S** – Single Responsibility
- **O** – Open/Closed
- **L** – Liskov Substitution
- **I** – Interface Segregation
- **D** – Dependency Inversion

**Simple idea:** SOLID helps keep code organized and easier to change.

---

## 10. Separation of Duties / Separation of Concerns

It means **different parts of an application should have different responsibilities**.

For example:
- `routes.py` → handles API routes
- `auth.py` → handles authentication
- `crud.py` → handles database operations
- `models.py` → defines data models

In Flask/FastAPI, this is commonly achieved by splitting the application into modules, routers, services, models, and database layers.

---

## 11. What is boilerplate code?

**Boilerplate code** is common code that needs to be written repeatedly in many applications.

**Example:** Setting up routes, database connections, configuration, or application structure.

Frameworks reduce boilerplate by providing ready-made features and structures.

---

## 12. How is boilerplate related to frameworks and libraries?

Frameworks provide ready-made structures and features, so developers do not have to write everything from scratch.

**Example:** FastAPI already provides routing, request validation, dependency injection, and automatic API documentation.

Libraries usually provide specific reusable functionality that you call when needed.

---

## 13. What is Pydantic Settings and when is it used?

**Pydantic Settings** is used to manage application configuration safely and conveniently.

It can load settings such as:
- Database URL
- Secret key
- API keys
- Environment variables

**Example:**
```python
class Settings(BaseSettings):
    database_url: str
    secret_key: str
```

It is useful for keeping configuration separate from application code.

---

## 14. What is the equivalent of Swagger in Python/FastAPI?

FastAPI has **automatic OpenAPI documentation**.

It provides:
- **Swagger UI** → usually available at `/docs`
- **ReDoc** → usually available at `/redoc`

So, in FastAPI, you normally do not need to install Swagger separately.

---


## 16. What is Swagger or OpenAPI?

**OpenAPI** is a standard for describing REST APIs.

**Swagger** is a set of tools commonly used around the OpenAPI standard.

It describes things like:
- API endpoints
- HTTP methods
- Parameters
- Request bodies
- Responses
- Authentication

---

### 16.1 What is it used for?

It is mainly used to:
- Document APIs
- Understand available endpoints
- Test APIs through a UI
- Help developers integrate with the API

**Example:** FastAPI automatically generates OpenAPI documentation and provides Swagger UI at `/docs`.
