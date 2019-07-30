"""
Main entry point
"""
import logging
from aiohttp import web
from aiohttp.web_app import Application
from server.handlers.get_flow_handler import get_flow_handler


def create_web_app(version: str) -> Application:
    """
    :return: aiohttp web application
    """
    app: Application = web.Application()
    app['version'] = version

    app.add_routes([
        web.get('/api/v1/flow/{uuid}', get_flow_handler)
    ])
    return app


def main():
    """
    main function
    """
    project_name = 'flows-viewer'
    version = '0.0.0'
    logging.info("starting %s v%s", project_name, version)
    app = create_web_app(version)
    web.run_app(app, port=5555)


if __name__ == '__main__':
    main()
