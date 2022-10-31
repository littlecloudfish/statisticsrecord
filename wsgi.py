"""Application entry point."""
from asgiref.wsgi import WsgiToAsgi
from jinja2 import Environment, FileSystemLoader
from flask_wengui_statistics import create_app

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve


app = create_app()


if __name__ == "__main__":

    if app.config["FLASK_ENV"] == "development":
        # 1, flask server
        app.run(host="0.0.0.0", port=2025)

        # # 2, hypercorn server
        # asgi_app = WsgiToAsgi(app)
        # config = Config()
        # config.bind = ["127.0.0.1:2025"]
        # # config.ca_certs = 'cert/ca.cer'
        # # config.certfile = 'cert/vic.cer'
        # # config.keyfile = 'cert/vic.key'
        # config.accesslog = 'hypercorn_log.log'
        # config.access_log_format = '%(h)s %(l)s %(t)s %(s)s %(b)s "%(f)s" "%(a)s"'
        # # config.server_names = ['fkccp', 'fkznk']
        # asyncio.run(serve(asgi_app, config))

        print(u'😂Development😂')
    else:
        print(u'Production')
        # 1, flask server
        # app.run(host="0.0.0.0", port=2025, ssl_context=(
        #     'cert/cocowang-vic.cer', 'cert/cocowang-vic.key'))

        # 2, hypercorn server
        asgi_app = WsgiToAsgi(app)

        config = Config()
        config._bind = ["0.0.0.0:2025"]
        config.ca_certs = 'cert/ca.cer'
        config.certfile = 'cert/vic.cer'
        config.keyfile = 'cert/vic.key'
        config.accesslog = 'hypercorn_log.log'
        config.access_log_format = '%(h)s %(l)s %(t)s %(s)s %(b)s "%(f)s" "%(a)s"'

        asyncio.run(serve(asgi_app, config))
