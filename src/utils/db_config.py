"""Database Configuration for Recipe Manager

This module contains the configuration details required to connect to the MySQL database for the Recipe Manager application.

DB_CONFIG is a dictionary that holds the following keys:
- 'host': The hostname or IP address of the MySQL server.
- 'user': The username used to authenticate with the MySQL server.
- 'password': The password used to authenticate with the MySQL server.
- 'database': The name of the database to be used for the Recipe Manager application.

Ensure that the values for 'host', 'user' and 'password' are set according to your MySQL server configuration.
"""

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'user',
    'password': 'pass',
    'database': 'recipe_manager'
}
