# DIS_Project

For developing the webapplication as part of the project for DIS.

# Running the Web-App

Assumes a working Python 3 installation (with `python`=`python3` and `pip`=`pip3`).

1) Create virtual environment  
   ```
   python -m venv venv
   ```
2) Activate virtual environment
   ```
   .\venv\Scripts\activate
   ```
3) Install dependencies in the virtual environment
   ```
   pip install -r requirements.txt
   ```
4) Database initialization
   1) Set the database name and user in the `db.py`
   2) Run `db_setup.py`

5) Run wep-app
   ```
   python app.py
   ```
