import falcon


class HelloViews:
    def on_get(self, req, resp):
        resp.body = "Hello, World"
        resp.status = falcon.HTTP_200
