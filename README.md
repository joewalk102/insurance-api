note: this is a programming exercise

# Insurance Quote API

## How to run server

Linux/Mac
```shell
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate  # by default, will create a db.sqlite3 in run dir
python manage.py runserver  # --help for additional run info
```
After these commands have been run, there should be a fully functional
API running locally on the terminal. For this example there is no
authentication (currently commented out), but if auth is enabled, an
additional `python manage.py createsuperuser` would need to be 
run before running the server, after the migration.

## Web UI
Navigating to localhost:8000/ (by default) will display a GUI
for Django Rest Framework.

## API Endpoints
Note: there is a file `Insurance Api.postman_collection.json` with all
the endpoints and examples of each available in the root directory of 
this project.
### Quote App
Available Tested Methods:
- GET
  - Get All URL (paginated): `/quotes/?format=json`
  - Get One URL: `/quotes/<quote_qid>/?format=json`
- PATCH
  - Edit Quote: `/quotes/<quote_qid>/` (+json payload required)
- POST
  - Create Quote: `/quotes/<quote_qid>/` (+json payload required)
- DELETE
  - Delete Quote: `/quotes/<quote_qid>/`

## Testing
To run all the tests (with venv enabled, no server running):
```shell
python manage.py test
```
