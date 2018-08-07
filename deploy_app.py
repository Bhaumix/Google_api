import google_api1
import tornado.ioloop
import tornado.web

app = google_api1.make_app()
app.listen(8055)
tornado.ioloop.IOLoop.current().start()