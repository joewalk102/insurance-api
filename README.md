note: this is a programming exercise

# Insurance Quote API

## Setup and Run Server

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
Navigating to `http://localhost:8000/quote/` (by default) will display a GUI
for Django Rest Framework.

Also added: 
- `http://localhost:8000/swagger/` - Swagger UI with the option 
for `?format=openapi` to include a json swagger doc.
- `http://localhost:8000/redoc/` - ReDoc UI 

## API Endpoints
Note: there is a file `Insurance Api.postman_collection.json` with all
the endpoints and examples of each available in the root directory of 
this project.

Note 2: Swagger and ReDoc UI and json is available through the `drf_yasg` package

### Quote App
Available Tested Quote Methods:
- GET
  - Get All URL (paginated): `/quote/quotes/?format=json`
  - Get One URL: `/quote/quotes/<quote_qid>/?format=json`
- PATCH
  - Edit Quote: `/quote/quotes/<quote_qid>/` (+json payload required)
- POST
  - Create Quote: `/quote/quotes/` (+json payload required)
- DELETE
  - Delete Quote: `/quote/quotes/<quote_qid>/`

Available Tested Purchase Methods:
- GET
  - Get All URL (paginated): `/quote/purchase/?format=json`
  - Get One URL: `/quote/purchase/<purchase_fk>/?format=json`
- POST
  - Create Quote: `/quote/purchase/` (+json payload required)

## Testing
To run all the tests (with venv enabled, no server running):
```shell
python manage.py test
```
