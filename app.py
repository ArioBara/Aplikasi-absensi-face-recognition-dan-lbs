from flask import Flask, render_template
from config import db_connection, db_cursor
from user_routes import *
from admin_routes import *

if __name__ == '__main__':
    app.run(debug=True)
    db_cursor.close()
    db_connection.close()
