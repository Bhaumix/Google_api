import google_api1
import unittest
import tornado.ioloop
import tornado.web

class TestApp(unittest.TestCase):
    def test_app(self):
        app = google_api1.make_app()
        app.listen(8055)
        tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    unittest.main()