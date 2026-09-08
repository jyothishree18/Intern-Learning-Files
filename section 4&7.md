# What I learned
Through this section, I learned how a URL is structured and what each part means, such as the scheme, host, port, path, query string, and fragment. I also understood how URLs help clients locate and access resources on the web.

# HTTP, line by line
       HTTP is how clients and servers communicate.

## POST /api/users HTTP/1.1  

## Host: example.com                

## Content-Type: application/json

## Authorization: Bearer a1b2c3

## {"name": "Priya", "role": "intern"}   

### Method -POST; means send/create data

### Path - /api/users ; tells the server where to send the request

### HTTP/1.1 → HTTP version being used

### Host → The website/server you are communicating with. 
example.com → Server's domain name

### Content-Type: application/json

### Authorization: Bearer a1b2c3

### {"name": "Priya", "role": "intern"}  --- This is the body. It contains the actual data being sent to the server.

## Response

### HTTP/1.1 201 Created
### Content-Type: application/json
### Location: /api/users/42
### {"id": 42, "name": "Priya", "role": "intern"}
        This is the response body.The server sends back the details of the newly created user.


# URLs: path vs query

https://api.example.com:443/users/42/orders?status=open&limit=10#section
└─┬─┘   └───────┬───────┘└┬┘└──────┬───────┘└────────┬────────┘└──┬──┘
scheme        host      port     path            query string  fragment

Scheme → https -  Tells us how to communicate with the server.

Host → api.example.com - Identifies the server/website we want to communicate with.

Port → 443 - Identifies the network port on the server.

Path → /users/42/orders - This tells the server which resource we want.

Query String → ?status=open&limit=10 - Used to provide additional options or filters like showing upto 10 

Fragment → #section - Points to a specific section of the resource/page.