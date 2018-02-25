
## SETUP ##
To clone this repository use the following command 
```
$ git clone https://github.com/harprasad/UDFullStack1.git
```

If you are uisng a virtual environment run the following commands as well.

```
$ pip install flask
$ pip install sqlalchemy
$ pip install oauth2client
```

## ADD SECRET FILES ##
* Add fb_client_secrets.json & client_secrets.json file to project root directory.


## RUN ##
If Everything is setup correctly, You should be able to run the application by running the **run.py** from the project root directory.



## FEATURES ##
This application has the follwoing features.
* View Recent Entries by visiting the home page
* View detailed information about any Item by clicking on the **more** link.
* You can add Items after you login .
* you can update or delete items addded by you.


## API ##

**http://localhost:5000/api/v1.0/catalog**

Returns a json object of all the items and categories avilable 

**http://localhost:5000/api/api/v1.0/category/id**

Returns a json object containing items of the specified category

**http://localhost:5000/api/api/v1.0/items/id**

Returns a json object for the specified item

## CODE STRUCTURE ##
Most of the code exist inside **app/site** & **app/api** directory. Site dirctory and api directory contain views hanlers and api endpoint handlers respectively.

