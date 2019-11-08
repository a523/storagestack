import falcon
from Agent.urls import paths


def add_routes(api, paths):
    for path in paths:
        api.add_route(*path)


def create_app():
    api = falcon.API()
    add_routes(api, paths)
    return api


api = create_app()
