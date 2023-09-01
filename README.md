# catalyst_count

## Setting up the environment
1. requirements.txt contains the list of packages to install firsthand into the virtual environment necessary to run the project
2. if you are using VENV to create the environment then use
     python3 -m venv env_name
3. use pip install -r requirements.txt to install the requirements

## Running the project
1. Add the env file in the project folder
2. use python manage.py runserver to start the server, after this the server will start at localhost:8000/ by default

## Using the file upload tab
1. Here if the file is in correct format then only the data will be added i.e., it should only be in the csv format
2. Below is the list of columns that should exists in the csv file
  - name
  - domain
  - year_founded
  - industry
  - size_range
  - locality
  - country
  - linkedin_url
  - current employee estimate
  - total employee estimate
