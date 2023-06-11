# DIS_Project

For developing the webapplication as part of the project for DIS.

# Running the Web-App

Assumes a working Python 3 installation (with `python`=`python3` and `pip`=`pip3`).
Also assumes that a PostgreSQL database has been created

1. Open terminal and navigate to solution-folder

2. Create virtual environment
   ```
   python -m venv venv
   ```
3. Activate virtual environment
   ```
   .\venv\Scripts\activate
   ```
4. Install dependencies in the virtual environment
   ```
   pip install -r requirements.txt
   ```
5. Database initialization

   1. Set the database name and user in the `helpers/db.py`
   2. Run `db_setup.py`
      ```
      python db_setup.py
      ```

6. Run wep-app
   ```
   python app.py
   ```

Now the application is running, and you can open http://localhost:5000/ in a browser

For more information about interacting with the website, read the [guide](GUIDE.md)
