from flask import Flask
import psycopg2
from psycopg2 import sql

conf_host = 'localhost'
conf_port = 37780
conf_db_name = 'school'
conf_user = 'postgres'
conf_password = 'password'
conf_teachers_table = 'teachers'


def connect_to_db():
    """
    Function to establish connection to database

    :return: psycopg2.connection object
    """

    try:
        conn = psycopg2.connect(host=conf_host,
                                port=conf_port,
                                dbname=conf_db_name,
                                user=conf_user,
                                password=conf_password)
        print("PostgreSQL connection established")
        return conn
    except psycopg2.OperationalError as error:
        raise error


def get_median_value(table: str, attribute: str):
    """
    Get the median value across all values in the specified table attribute.

    :param table: sql.Identifier object of target table
    :param attribute: string attribute to filter on
    :return: median value
    """

    median_query = sql.SQL("""
    SELECT percentile_disc(0.5) 
    WITHIN GROUP (
        ORDER BY {table}.{attribute}
        )
    FROM {table}
    """).format(table=sql.Identifier(table),
                attribute=sql.Identifier(attribute))

    try:
        with connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute(median_query)
                return cur.fetchone()[0]
    except psycopg2.Error as error:
        raise error


def create_app():
    app = Flask(__name__)

    @app.route('/median/<string:variable>', methods=['GET'])
    def get_median(variable):
        try:
            median_value = get_median_value(conf_teachers_table, variable)
            return f"Median value for attribute {variable} is {median_value}\n"
        except psycopg2.Error:
            return f"{variable} is not a valid parameter. Please use 'height', 'weight', 'age' or 'male'\n"

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
