import falcon


class HelloViews:
    def on_get(self, req, resp):
        resp.body = "OK"
        resp.status = falcon.HTTP_200
