# yatam-web-cloud

## Project Setup

### Linux
1. Having installed in Python virtualenv:
	* Open terminal and enter: 	`pip install virtualenv`
2. Download this repository and change the working directory in terminal to the repository folder using `cd` comand.
3. Create a Python Virtual Environment:
	* `virtualenv env`
4. Activate virtual enviroment:
	* `source venv/bin/activate`
5. Install dependencies:
	* `pip install -r requirements.txt`

### Windows
1. Install Python in Windows
2. Install in Python *virtualenv*
	* Open CMD and use: `pip install virtualenv`
3. Create virtual environment:
	* `python -m venv c:\path\to\myenv`
4. Activate virtual environment:
	* `c:\path\to\myenv\activate.bat`
 5. Install dependencies:
	* `pip install -r requirements.txt`
 
 ## Configure .env file for Firebase Config
 1. Create a new file called env
 2. Edit the file and add:
	 * `firebaseConfig = { "apiKey": "[apikey]", "authDomain": "[authdomain]", "databaseURL": "[databaseurl]", "projectId": "[projectid]", "storageBucket": "[storagebucket]", "messagingSenderId": "[messagingsenderid]", "appId": "[appid]", "measurementId": "[measurementid]" }   
sessionPrivateKey = "yatam-web-cloud-private-key-for-session"`
	* Changing the words in brackets ([ ]) for the real firebase configuration that can be found in Firebase Console > yatam-web-tourism-app > Project Configuration > Your apps > Firebase SDK snippet.
	* CAUTION: **firebaseConfig** and **sessionPrivateKey** are different environment variables, therefore, each one must go in a single line.
3. Change the file name from *env* to *.env*

## How to run the project
### Locally
1. Navigate to _~/yatam-web-cloud_ in terminal
2. Enter:
	* `python main.py`

* CAUTION: The server will run by default on *localhost:5000/*. In *localhost* we will be able to see the images from IMGUR but if we want to upload an image to IMGUR we need to change the URL to
	* `127.0.0.1:5000/`
This is because IMGUR only accepts *localhost* to download and see the images and only accepts *127.0.0.1* to upload images. *127.0.0.1* is the IP direction for *localhost* so we don't need to open the server again. 

### Remote
1. First, we need an app in Heroku. We create it in our dashboard.
2. Now, choose an App Name and select a region and press Create App
3. Download the Heroku CLI from [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
4. Open a terminal and Login in Heroku with:
	* `heroku login`
	It will open a new tab in your browser to enter your credentials.
5. Add and commit your changes with:
	* `git add .`
	* `git commit -am "commit message"`
	5.1. If your project doesn't have a Git Repository, first you need to initialize the local repository with:
	* `git init`
	* `heroku git:remote -a [heroku_app]`
6. Push the changes to your Heroku app:
	* `heroku git:remote -a [heroku_app]`
7. You can find the URL in the Settings of your Heroku App.

### Local execution with Heroku
If you are using **Windows**:
	1. Create a file called: *Procfile.windows* with:
		* `web: python main.py runserver 0.0.0.0:5000`
	2. Enter this on CMD:
		* `heroku local web -f Procfile.windows`
If you are using **Linux**:
	1. You will have the Procfile inside this repository. Just run in terminal:
		* `heroku local web`
		
The web will be deployed in *localhost:5000*

## External APIs:
* IMGUR
* Climacell APIv3
* Leaflet 
