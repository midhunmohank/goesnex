# Assignment-3

This document presents the design of a service plan that offers a free plan and two premium plans with different limits. The service plan includes a user registration page that allows users to choose their preferred plan, change their password, and store it securely with hashing. Additionally, the enhanced logging feature helps track user activity and compare it with their plan limits. Two dashboards are provided, one for admin/developers/owners and another for individual users, that provide a range of analytics, such as total API calls, success and failure rates, and more. To make the service more accessible, Typer is used to create a CLI with multiple functionalities. Finally, a Python package is created, and an airflow dag is scheduled to update the metadata file.

## Links:
[API Link](http://3.17.64.250:8000/docs) <br>
[Application Link](http://3.17.64.250:8081) <br>
[Code Labs](https://codelabs-preview.appspot.com/?file_id=1cid4cJvBFoZxRi4cHUvoH25GjSrnjbZ2QABmoRlvxTs#2) <br>

## Goesnex CLI
#### How to access it?

Install the package
Link: https://pypi.org/project/goesnex-cli-package/0.0.2/
```
pip install goesnex-cli-package==0.0.2
```
Accessing the package
```
goesnex_cli --help
```
Available Commands
```
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ get-files-goes                                                                                                                                          │
│ get-files-nexrad                                                                                                                                        │
│ get-mi6-url-goes                                                                                                                                        │
│ get-mi6-url-nexrad                                                                                                                                      │
│ get-public-url-goes                                                                                                                                     │
│ get-public-url-nexrad                                                                                                                                   │
│ user-login
|
| user-signup
|
| user-logout
```
## Architecture

<img src="https://lh4.googleusercontent.com/EXfQxGITI0fhS6rJjNBxIVfrAp1IYqOe59Izd5ZbWMKOfejza-nhrm6Cyn7IXfp7WQexzPqHHYvHZIiUXGQEQROgD9-jzs2VuHLO0RWxa1OvJoJi96Qc-ivZ8w94efBuRmPPclkrzIKxK7bfY6kOwvU" width="1000" height="800">

## File Structure

```
.
├── Book.csv
├── README.md
├── airflow_ge                                                #Airflow
│   ├── airflow
│   │   ├── dags
│   │   │   ├── __pycache__
│   │   │   │   ├── goes.cpython-37.pyc
│   │   │   │   └── nexrad.cpython-37.pyc
│   │   │   ├── goes.py
│   │   │   └── nexrad.py
│   │   ├── logs
│   │   │   └── scheduler
│   │   │       ├── 2023-03-09
│   │   │       │   ├── goes.py.log
│   │   │       │   └── nexrad.py.log
│   │   │       └── latest -> /opt/airflow/logs/scheduler/2023-03-09
│   │   ├── plugins
│   │   └── working_dir
│   ├── db_data
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── test.ipynb
│   └── test.py
├── backend                                                     #FastAPI
│   ├── Book.csv
│   ├── Dockerfile
│   ├── __pycache__
│   │   ├── fastapi_test.cpython-310.pyc
│   │   ├── fastapi_test.cpython-38-pytest-7.2.1.pyc
│   │   ├── fastapi_test.cpython-38.pyc
│   │   ├── jwt.cpython-310.pyc
│   │   ├── jwt.cpython-38.pyc
│   │   ├── snowflake.cpython-38.pyc
│   │   └── test_main.cpython-38-pytest-7.2.1.pyc
│   ├── fastapi_test.py
│   ├── helper_functions
│   │   ├── Book.csv
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   ├── cw_logs.cpython-38.pyc
│   │   │   ├── goes_module.cpython-38.pyc
│   │   │   ├── helper.cpython-38.pyc
│   │   │   ├── login.cpython-38.pyc
│   │   │   └── noes_module.cpython-38.pyc
│   │   ├── cw_logs.py
│   │   ├── goes_module.py
│   │   ├── helper.py
│   │   ├── login.py
│   │   └── noes_module.py
│   ├── jwt.py
│   ├── requirements.txt
│   ├── snowflake_testing.py
│   ├── test.py
│   ├── test_api.py
│   ├── test_files_json
│   │   ├── response_goes.json
│   │   └── response_nexrad.json
│   ├── test_main.py
│   ├── update_snowflake_hist.py
│   └── usersegtest.py
├── cli_package                                                  #CLI Package
│   ├── build
│   │   └── lib
│   │       └── goesnex_cli_package
│   │           ├── __init__.py
│   │           ├── helper.py
│   │           └── main.py
│   ├── dist
│   │   └── goesnex_cli_package-0.0.1-py3-none-any.whl
│   ├── goesnex_cli_package
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── helper.cpython-310.pyc
│   │   ├── config.ini
│   │   ├── helper.py
│   │   └── main.py
│   ├── goesnex_cli_package.egg-info
│   │   ├── PKG-INFO
│   │   ├── SOURCES.txt
│   │   ├── dependency_links.txt
│   │   ├── entry_points.txt
│   │   ├── requires.txt
│   │   └── top_level.txt
│   ├── requirements.txt
│   └── setup.py
├── docker-compose.yml
├── requirements.txt
└── streamlit                                                     #Streamlit Site
    ├── Dockerfile
    ├── Login.py                                          
    ├── __pycache__
    │   └── helper.cpython-38.pyc
    ├── helper.py
    ├── pages
    │   ├── DashboardAdmin.py
    │   ├── DashboardUser.py
    │   ├── GOES.py
    │   ├── NEXRAD.py
    │   └── nexrad.xlsx
    ├── requirements.txt
    ├── test_api copy.py
    └── testlogin.py
```

## How to run the app?

Create a Virtual Environment
```
python3 -m venv venv
```
Install requirements for backend and frontend
```
pip3 install -r backend/requirements.txt
pip3 install -r frontend/requirements.txt
```

Running the FastAPI
```
cd backend/
uvicorn fastapi_test:app
```
Running the Streamlit App
```
cd streamlit
streamlit run Login.py
```

#### Attestations
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT

AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

Contribution: 

* Midhun Mohan Kudayattutharayil: 25%
* Sanjay Kashyap: 25%
* Snehil Aryan: 25%
* Vikash Singh: 25%
