import falcon
from Agent.urls import paths


def create_app():
    api = falcon.API()
    for path in paths:
        api.add_route(*path)
    return api


def get_app():
    return create_app()
