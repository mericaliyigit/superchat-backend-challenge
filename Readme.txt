Hi Superchat team,

As dicussed I have created a simple api
with the following functionalities
-Create contact
-List all contacts
-Send a message to a contact
-List conversations
-Receieve messages from an external service via webhook

I have also implemented (as far as I understand) the placeholder system
so if your message body contains #name# or #btc# in it the api will autmatically fill those placeholders
with the receivers name and the current price of bitcoin. For the name filling I queried the receivers name from the backend
and simply substituted with a string replacement (I am aware that this approach is not the best but it works in this simple 
setting). Bitcoin price replacement will also work in a similar manner only difference is a small service class is asking
coindesk about the current price of btc then doing the same operation (I wont guarentee the price will be correct but if
it fails there is a cached value or even if that doesnt exists a simple 0 value)


I have also used the authentication system that is built in django and created a super-user with rights to all the operations.

The username is :
admin
The password is :
12345

You must include theese as a basic authentication key value pair in postman or whatever system you will use for this system.
If you dont provide the credentials in the request you will receive a unathorized error message and wont see any data.

An example for every request is down below

--Create contact 

Send a post to url below

URL  = http://127.0.0.1:8000/create_contact

{"name":"meric ali",
"surname":"yigit",
"email" : "mericaliyigit@gmail.com"}


--Contacts

Send a get to url below

URL = http://127.0.0.1:8000/contacts

--Send message

Send a post to url below

URL = http://127.0.0.1:8000/send_message

    {"receiver":"mericaliyigit@gmail.com",
    "content": "Hi #name# this is a place holder test "}

--Conversations

Send a get to url below 

URL = http://127.0.0.1:8000/conversations

--External service via a webhook is a little bit tricky

I have used github webhook services to do this.

I made a simple function to check the incoming requests ip 

If the ip belongs to github webhooks network I accept the request and return todays datetime as a reponse.
Otherwise I will return forbidden. 

This part is to test if my app can receive external messages this could have triggered some other behaviour as well
I just choose not to as its an example task.

To test it i used ngrok to open up my local port to the web for 2 hours then provide the redirection url to github webhook test and triggered a response. 

I have created this with django rest framework and python reason being I havent used java with a web framework for a long time and I dont want to spend time configuring an IDE which I currently dont have.

You can run the app by simply going to the directory where the docker files are located
and use the command

docker compose up --build 

This will create the required environment and run the experimental server for you to access the features
For any questions please email me.

Thanks 
Meric