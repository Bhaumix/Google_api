import tornado.ioloop
import tornado.web
import json
import requests
import codecs
import os
import time
import shutil
import csv


class MainHandler(tornado.web.RequestHandler):
    # dont keep this api key in code
    # save it in some file and load file here ... neever commit this credential file in repo .... manually copy paste it on server as config file
    api_url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyB8PfpHmME_aX_26gdYMo09D0AFrMNQDw4&cx=003329888468530643586:qhn85v-mmf8&q="

    def get(self):
        ean = self.get_argument("ean", None, True)
        self.set_header("Content-Type", "application/json")
        response = requests.get(self.api_url + ean)
        urls = []
        #print(self.api_url + ean)
        file_location = "C:/Users/jabh8001/Documents/GoogleApi/Files" + "/" + str(ean)
        image_download_dir = "C:/Users/jabh8001/Documents/GoogleApi/Photos" + "/" + str(ean) + "/"

        json_data = json.loads(response.text)
        for i in json_data["items"]:
            urls.append(i['link'])
        print(len(urls))

        for l in urls:
            print(l)

        url_list = []
        for u in urls:
            if str(int(ean)) in u:
                url_list.append(u)
            try:
                r = requests.get(u)
            except:
                pass
            if ean in r.text:
                url_list.append(u)

        print(len(url_list))
        url_list = list(set(url_list))
        for li in url_list:
            print(li)


    # self.write(response.text) ## this is string -- so before sending result convert your list or dictionary into json string json.dumps
        self.write(response.text)
    # self.write(json_data['imageobject'])"""


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
