# README File For Webretrieval

## section (1) - Production Environment

A production/demo environment of the GUI-app can be found at:
> http://109.238.10.185:8000/

## Section (2) - Database connection

You can connect with mongo database via a GUI client like for example; RoboMongo (many others are out there). In your client, use the following credidentials:

> serveraddress:    109.238.10.185 <br />
> port:                     27000 <br />
> use_authentication: yes <br />
> database: webretrieval <br />
> username: webretrieval <br />
> password: tue <br />


We need a so called ‘driver’ to enable our python scripts to communicate with the database. You can install it like so:



#### MAC/LINUX mongoDB driver:

 1. install mongoDB driver for python: download pip-installer script at
    https://bootstrap.pypa.io/get-pip.py open a terminal
 2. in the same window as the script you just downloaded
 3. run: python get-pip.py
 4. run: python -m pip install pymongo


#### WINDOWS:
google

## Section (3) -Contribution description

### Component 1: 
Tomas Sostak: 0853329
Main Code file:/app/search/vsr.pyN

### Component 2a: 
Zelong Hu: 0942976
Main Code file: /Component2/ID_Keywords.py
                        /Component2/version3.py
                       /Component2/version4.py
                      /Component2/upload.py

### Component 2b:
Jiapeng Li: 1285130
Main Code file:Component2/component2b/

### Component 3a
Chin-Fang Lin: 1035955
Main Code file: /Component3/dtm.ipynb

### Component 3b:
Qifan Dai : 1034548
Main Code file: /Component3/ATM_final.ipynb


### Component 4 and 5:

Jeroen Brouns: 0856180
Component1/
   reference_improved.py	   - Reference mining script
   repository.py			   - Repostiory class that contains calls to MongoDB rep.
   authentication.py		   - File that configures connection to the self-hosted MongoDB
   PageRank_exportToDb.py     - Pagerank calculation of MongoDB entries
   Graph.py			   - Creates a graph from mined references in database

All not mentioned files are ‘supporting scripts’. They are functional and necessary, but not worth mentioning. There are also some script (for example, reference_fuzzywuzzy.py) which are experimental and not used in the final product.

Main Code file: app/manage.py
Potentially start your own server by firing the terminal command: 
python manage.py runserver

It is however recommended to visit the deployed production version of our platform at:
109.238.10.185:8000 

The graphical user interface that encapsulates all our system’s functionality is created in Django. Django’s files are structured as follows:
app/			 - Root folder
    manage.py		- Startpoint for the system
    app/	                        - Main component root
        __init__.py	-  Initializing file
        urls.py		- URL routes that map urlrequest to view-controllers
        wsgi.py		- Specification file for setting up a communication gateway*
        settings.py	- Framework settings. A.o. static files declaration, allowed hosts.
    search/
        migrations/
        templates/	- Folder with .html files that serve as ‘views’ for the MVC.
        authentication.py   - File that configures connection to the self-hosted MongoDB
        repository.pyp	- Decoupled repostiory class that contains calls to MongoDB rep.
        view.py		- Controller class. 
        urls.py		- URL routes that map urlrequest to view-controllers
        vsr.py		- Decoupled VectorSpaceRetrieval class
        youtube.py	- Youtube crawler, used in view.py
        model.py		- Model class with models of sqlite databases
    static/serch		- Static assets such as .css / .js files		


*It uses Web Server Gateway Interface (WSGI) technology. WSGI is a specification for simple and universal interface between web servers and web applications or frameworks for the Python programming language. Django requires the creation of a virtual environment with specific python versions, configuration of apache handlers and path variables to be able to deploy the system on a dedicated server. 

