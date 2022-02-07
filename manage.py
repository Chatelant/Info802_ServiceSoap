from werkzeug.middleware.dispatcher import DispatcherMiddleware

from spyne.server.wsgi import WsgiApplication

from flaskrSoap import spyned
from flaskrSoap.flasked import app
import os

# SOAP services are distinct wsgi applications, we should use dispatcher
# middleware to bring all aps together
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap': WsgiApplication(spyned.create_app(app))
})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 35000))
