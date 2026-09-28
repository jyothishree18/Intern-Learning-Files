# Research Set 2

## Fundamentals, Revisited Deeper

### 1. Front end vs Back end
**Front end** is the part of a website the user sees and interacts with, such as pages, buttons, forms, and menus. It commonly uses HTML, CSS, and JavaScript.

**Back end** works behind the scenes. It handles business logic, APIs, authentication, and database operations.

**Example:** In a student management system, the student form is the front end, while Flask/FastAPI and the database handle the back end.

---

### 2. Three-tier architecture in a web application
Three-tier architecture divides an application into three main layers:

1. **Presentation layer** – what the user interacts with.
2. **Application layer** – processes requests and contains business logic.
3. **Data layer** – stores and retrieves data from the database.

**Example:** Student page → Flask/FastAPI → MySQL database.

---

### 3. Three-tier architecture from a web-development point of view
From a web-development view:

- **Presentation tier:** Browser and front-end code.
- **Application tier:** Web server/API that processes HTTP requests.
- **Data tier:** Database such as MySQL, PostgreSQL, or SQLite.

This separation makes the application easier to develop, maintain, test, and scale.

---

### 4. SSL / TLS encryption
**TLS (Transport Layer Security)** protects data while it travels between the client and server. It encrypts the connection so others cannot easily read or change the data.

**SSL** is the older technology; TLS is its modern replacement.

**Example:** `https://` means the website is using HTTPS, which normally uses TLS to secure the connection.

---

### 5. HTTP methods
HTTP methods tell the server what action the client wants to perform.

- **GET** – retrieve data
- **POST** – create/send new data
- **PUT** – update or replace data
- **PATCH** – partially update data
- **DELETE** – remove data

**Example:** `GET /students` gets students, while `POST /students` creates a student.

---

### 6. HTTP status codes
HTTP status codes tell the client what happened to its request.

- **200 OK** – request was successful
- **201 Created** – new resource was created
- **400 Bad Request** – request has invalid data
- **401 Unauthorized** – authentication is required or failed
- **403 Forbidden** – user is authenticated but not allowed
- **404 Not Found** – resource was not found
- **500 Internal Server Error** – server-side problem

They help the client understand the result without reading the full response.

---

### 7. CRUD operations
CRUD means the four basic operations on data:

- **Create** → POST
- **Read** → GET
- **Update** → PUT/PATCH
- **Delete** → DELETE

**Example:** In a student system, adding a student is Create, viewing students is Read, editing a student is Update, and removing a student is Delete.

---

### 8. Stateful vs stateless communication in web applications
**Stateful** communication means the server remembers information about a client between requests.

**Stateless** communication means each request contains the information needed to process it, and the server does not depend on previous requests.

**Example:** Traditional server sessions are stateful. REST APIs are generally designed to be stateless.

---

# Authentication & Authorization

### 1. What is authentication? What are the different types?
**Authentication** means checking **who the user is**.

Common types include:

- **Password authentication** – username and password
- **Token authentication** – API token or JWT
- **Session-based authentication** – server keeps a login session
- **OAuth / social login** – login using Google, GitHub, etc.
- **Multi-factor authentication (MFA)** – password plus another verification method

**Example:** Logging into a student portal with an email and password is authentication.

---

### 2. What is authorization? What are the different types?
**Authorization** means checking **what an authenticated user is allowed to do**.

Common approaches include:

- **Role-Based Access Control (RBAC)** – permissions based on roles such as admin or student
- **Permission-based access** – specific permissions are assigned to users
- **Attribute-Based Access Control (ABAC)** – access depends on attributes such as role, department, or resource

**Example:** A student can view their details, while an admin can add, edit, and delete students.

---

### 3. How does authentication differ from authorization?
The simple difference is:

- **Authentication = Who are you?**
- **Authorization = What are you allowed to do?**

Usually, authentication happens first, followed by authorization.

**Example:** Logging in proves you are a student; checking whether you can delete another student's record is authorization.

---

# Serialization & Data Formats

### 1. What is serialization? What is deserialization? Why do APIs need them?
**Serialization** converts data in a program into a format that can be sent or stored.

**Deserialization** converts that formatted data back into a form the program can use.

APIs need them because the client and server must exchange data in a common format.

**Example:** A Python student object can be serialized into JSON before sending it through an API.

---

### 2. Name some serialization formats
Common formats include:

- JSON
- XML
- YAML
- Protocol Buffers (Protobuf)
- MessagePack

JSON is one of the most commonly used formats for modern web APIs.

---

### 3. JSON and XML: what they are, how each is used in HTTP responses, and how they differ
**JSON (JavaScript Object Notation)** stores data using objects, arrays, and key-value pairs. It is commonly used in REST APIs.

Example:
```json
{
  "name": "Joe",
  "age": 21
}
```

**XML (Extensible Markup Language)** uses tags to describe data.

Example:
```xml
<student>
  <name>Joe</name>
  <age>21</age>
</student>
```

In an HTTP response, the server can return either format and indicate it using the `Content-Type` header, such as `application/json` or `application/xml`.

**Main difference:** JSON is generally more compact and easier to work with in modern web applications, while XML supports more detailed document structures and is still used in some systems.

---

# Tools & HTTP Concepts

### 1. Postman: what it is, how you test an API with it
**Postman** is a tool used to send HTTP requests and test APIs without building a front end.

Basic steps:
1. Open Postman.
2. Select a method such as GET or POST.
3. Enter the API URL.
4. Add headers, parameters, or a request body if needed.
5. Click **Send**.
6. Check the status code and response.

**Example:** Send `GET /students` and check whether the API returns the student list.

---

### 2. cURL: what it is, how you send an HTTP request with it
**cURL** is a command-line tool used to send requests to servers.

Example:
```bash
curl http://127.0.0.1:5000/students
```

For a POST request:
```bash
curl -X POST http://127.0.0.1:5000/students -H "Content-Type: application/json" -d "{"name":"Joe"}"
```

It is useful for quickly testing APIs from a terminal.

---

### 3. Postman vs cURL — when you'd use each
**Postman** is easier when you want a visual interface, save requests, add authentication, and inspect responses comfortably.

**cURL** is useful when you prefer the command line, want quick tests, or need to use requests in scripts and automation.

Both can send HTTP requests and test APIs.

---

### 4. Query parameter, path variable, request payload — and how query parameters differ from path variables
**Query parameter** gives extra information in the URL after `?`.

Example:
```text
/students?department=AI
```

**Path variable** identifies a specific resource as part of the URL path.

Example:
```text
/students/101
```

**Request payload** is data sent in the request body, commonly with POST, PUT, or PATCH.

Example:
```json
{
  "name": "Joe",
  "department": "AI"
}

---

### 5. Request headers and response headers — what they carry
**Request headers** carry information from the client to the server.

Examples:
- `Authorization` – authentication information
- `Content-Type` – format of the request body
- `Accept` – response format the client can handle

**Response headers** carry information from the server to the client.

Examples:
- `Content-Type` – format of the response
- `Content-Length` – response size
- `Set-Cookie` – tells the browser to store a cookie

Headers provide extra information about how the request or response should be handled.
