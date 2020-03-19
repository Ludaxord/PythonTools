import os

import psycopg2
from psycopg2.extras import RealDictCursor


class Postgre:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def remove_file(self, filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    def connect(self, with_query=None, with_factory=False):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

            # create a cursor
            if with_factory:
                cur = conn.cursor(cursor_factory=RealDictCursor)
            else:
                cur = conn.cursor()

            # execute a statement
            if with_query is not None:
                cur.execute(with_query)
                # return cur
            else:
                print('PostgreSQL database version:')
                cur.execute('SELECT version()')
                # display the PostgreSQL database server version
                db_version = cur.fetchone()
                print(db_version)
                # close the communication with the PostgreSQL
                cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            # if with_query is None:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    def save_to_sql(self, filename, filedata):
        with open(filename, 'a') as file:
            file.write(filedata)
        file.close()
