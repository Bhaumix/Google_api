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
    api_url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyB8PfpHmME_aX_26gdYMo09D0AFrMNQDw4&cx= :qhn85v-mmf8&q="

    def download_image(self, url, filename):
        print(url, filename)
        try:
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        except:
            pass

    def ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def find(self, key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.find(key, d):
                        yield result

    def get(self):
        ean = self.get_argument("ean", None, True)
        self.set_header("Content-Type", "application/json")
        response = requests.get(self.api_url + ean)
        print(self.api_url + ean)
        urls = []
        file_location = "C:/Users/jabh8001/Documents/GoogleApi/Files" + "/" + str(ean)
        image_download_dir = "C:/Users/jabh8001/Documents/GoogleApi/Photos" + "/" + str(ean) + "/"
        json_data = json.loads(response.text)
        for i in json_data["items"]:
            urls.append(i['link'])
        print(len(urls))

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

        url_list = list(set(url_list))
        print(len(url_list))

        self.write(response.text)
        src_list = list(self.find('image', json_data))

        if not os.path.exists(file_location + ".csv"):

            with open(file_location + ".csv", 'a') as csvfile:
                wr = csv.writer(csvfile, dialect='excel')
                wr.writerow(["Total webpages found: " + str(len(url_list))])
                wr.writerow(["\n\n====Webpage List=====\n"])

            for url in url_list:
                with open(file_location + ".csv", 'a') as csvfile:
                    wr = csv.writer(csvfile, dialect='excel')
                    wr.writerow([url, ])

            with open(file_location + ".csv", 'a') as csvfile:
                wr = csv.writer(csvfile, dialect='excel')
                wr.writerow(["\n\n====Image URLs=====\n"])
            file_count = 0

            for s, i in zip(src_list, range(0,5)):
                file_count += 1
                file_name = image_download_dir + str(ean) + "_" + str(file_count) + "_0.jpg"
                with open(file_location + ".csv", 'a') as csvfile:
                    wr = csv.writer(csvfile, dialect='excel')
                    wr.writerow([s, ])
                self.ensure_dir(image_download_dir)
                self.download_image(s, file_name)
        # self.write(response.text) ## this is string -- so before sending result convert your list or dictionary into json string json.dumps
        self.write(response.text)
        # self.write(json_data['imageobject'])"""


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8055)
    tornado.ioloop.IOLoop.current().start()
