import tornado.ioloop
import tornado.web
import json
import requests

class MainHandler(tornado.web.RequestHandler):
    #dont keep this api key in code
    # save it in some file and load file here ... neever commit this credential file in repo .... manually copy paste it on server as config file
    api_url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyB8PfpHmME_aX_26gdYMo09D0AFrMNQDw4&cx=003329888468530643586:qhn85v-mmf8&q="

    def get(self):
        ean = self.get_argument("ean", None, True)

        response = requests.get(self.api_url + ean)
        json_data = json.loads(response.text)


        print(json_data)
        self.write(response.text) ## this is string -- so before sending result convert your list or dictionary into json string json.dumps

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8085)
    tornado.ioloop.IOLoop.current().start()
