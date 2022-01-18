from os import getenv


def get_postgres_uri():
    host = getenv('DB_HOST', 'localhost')
    porta = 54321 if host == 'localhost' else 5432

    senha = getenv('DB_PASSWORD', 'abc123')
    usuario, db_name = 'allocation', 'allocation'

    return f'postgresql://{usuario}:{senha}@{host}:{porta}/{db_name}'


def get_api_url():
    host = getenv('API_HOST', 'localhost')
    port = 5005 if host == 'localhost' else 80
    return f'http://{host}:{port}'