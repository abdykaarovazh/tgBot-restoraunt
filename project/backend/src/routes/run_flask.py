from project.backend.src.db.db_app import app
from project.config import config


if __name__ == '__main__':
    import ssl
    from pathlib import Path

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    cert_dir = Path(str(config.ssl.ssl_path))

    cert_file = cert_dir / str(config.ssl.ssl_cert)
    key_file = cert_dir / str(config.ssl.ssl_key)

    ssl_context.load_cert_chain(certfile = str(cert_file), keyfile = str(key_file))

    app.run(host = str(config.flask.flask_host),
            port = str(config.flask.flask_port),
            ssl_context = ssl_context)