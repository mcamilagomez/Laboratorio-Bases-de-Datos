import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'LAPTOP-1LCPBRUM'
DATABASE_NAME = 'Movies'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
    uid=roberto gil garcia;
    pwd=3012;
    """

odbc_connection = odbc.connect(connection_string)
cursor = odbc_connection.cursor()

query = """
select top 1 *
from MoviesInfo
"""

cursor.execute(query)

for row in cursor:
    print(row)

cursor.close()
odbc_connection.close()