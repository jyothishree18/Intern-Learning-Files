# Call 1 - GET GitHub User

 ## Command
curl.exe -i https://api.github.com/users/torvalds

## Status Code
     200 OK - The request was successful.

## Three Response Headers
 Content-Type - Tells us the type of data returned by the server.
 Content-Length - Tells us the size of the response.
 Server - Shows information about the server software.

## Response Body
  The GitHub user information appeared in the JSON response body. The login field contained torvalds.

What I Learned:

A GET request is used to retrieve information from a server.

# Call 2 - GET httpbin

## Command

curl.exe -v https://httpbin.org/get

## Status Code

200 OK - The request was successful.

## Three Response Headers

Content-Type - Tells us the response is JSON.
Content-Length - Shows the size of the response.
Server - Shows the server software.

## Response Body

The response body contained information about the request, including the request headers, URL, and origin.

What I Learned:

The -v option shows more details about the request and response. The > lines show what the client sends, and the < lines show what the server sends back.

# Call 3 - POST JSON

## Command

$body = @{name="jyothishree"; week=1} | ConvertTo-Json -Compress
curl.exe -i -X POST https://httpbin.org/post -H "Content-Type: application/json" -d $body

## Status Code

200 OK - The POST request was successful.

## Three Response Headers
Content-Type - Tells us the response is JSON.
Content-Length - Shows the size of the response.
Server - Shows the server software.

## Response Body

The JSON I sent appeared under the json field.
{
  "name": "jyothishree",
  "week": 1
}

What I Learned

A POST request can be used to send data to a server. I sent JSON data in the request body, and httpbin returned the same data in its response.

# Call 4 - Query Parameters

## Command
curl.exe -i "https://httpbin.org/get?role=intern&track=python"

## Status Code

200 OK - The request was successful.

## Three Response Headers
Content-Type - Tells us the response is JSON.
Content-Length - Shows the size of the response.
Server - Shows the server software.

## Response Body
The query parameters appeared under the args field:
{
  "role": "intern",
  "track": "python"
}

What I Learned:
      A POST request can be used to send data to a server. I sent JSON data in the request body, and httpbin returned the same data in its response.

# Call 4 - Query Parameters

## Command
curl.exe -i "https://httpbin.org/get?role=intern&track=python"

## Status Code

200 OK - The request was successful.

## Three Response Headers

Content-Type - Tells us the response is JSON.
Content-Length - Shows the size of the response.
Server - Shows the server software.

## Response body
The query parameters appeared under the args field:
{
  "role": "intern",
  "track": "python"
}

What I Learned
   Query parameters are values added to the URL after ?. Here, role=intern and track=python were sent to the server, and httpbin returned them under args.

# Call 5 - Non-existent User

## Command
curl.exe -i https://api.github.com/users/this-user-does-not-exist-99999

## Status Code

404 Not Found - The requested user does not exist, so GitHub could not find the requested resource.

## Three Response Headers
Content-Type - Tells us the response data type.
Content-Length - Shows the size of the response.
Server - Shows information about the server.

## Response Body
The response body contained an error message saying that the requested user was not found.

What I Learned
      A 404 Not Found status means that the server could not find the requested resource.

# Postman Comparison

## Call 1

I repeated the GET request in Postman and received the same successful response and GitHub user information as with curl.

## Call 3

I repeated the POST request in Postman with the same JSON body. The response was successful and httpbin returned the JSON data I sent.



# Conclusion:

 ### Both curl and Postman can be used to make HTTP requests. 
### When I used the same URL, method, and data, both tools produced the same result.