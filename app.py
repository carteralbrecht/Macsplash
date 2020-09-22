import requests
import rumps
from unsplash.api import Api
from unsplash.auth import Auth
import appscript
import random
import json

RED = "🍎"
YELLOW = "🌼"
BLUE = "🦋"
PURPLE = "☂️"
BLACK = "♣️"

with open("secret.json") as f:
    keys = json.load(f)

client_id = keys["client_id"]
client_secret = keys["client_secret"]
redirect_uri = keys["redirect_uri"]
code = keys["code"]

auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)


class UnsplashPhoto:
    def __init__(self, url, photo_id):
        self.url = url
        self.photo_id = photo_id


def download_image(url, filename):
    response = requests.get(url)
    file = open("images/" + filename, "wb")
    file.write(response.content)
    file.close()
    return file


def get_unsplash_photo(color):
    images = api.search.photos(color, random.randrange(10), random.randrange(10))
    photo_id = random.choice(images['results']).id
    url = "https://unsplash.com/photos/%s/download" % photo_id
    photo = UnsplashPhoto(url, photo_id)
    return photo


def random_desktop(query):
    photo = get_unsplash_photo(query)
    file = download_image(photo.url, "%s.png" % photo.photo_id)
    change_desktop_image(file)


def change_desktop_image(file):
    print(file.name)
    se = appscript.app('System Events')
    desktops = se.desktops.display_name.get()
    for d in desktops:
        desk = se.desktops[appscript.its.display_name == d]
        desk.picture.set(appscript.mactypes.File(file.name))


class MenuBarApp(rumps.App):
    def __init__(self):
        super(MenuBarApp, self).__init__("🎨")
        self.menu = [RED, BLUE, YELLOW, PURPLE, BLACK]

    # TODO: Find cleaner way to call random_desktop()
    @rumps.clicked(RED)
    def change_to_red(self):
        random_desktop("red")

    @rumps.clicked(BLUE)
    def change_to_blue(self):
        random_desktop("blue")

    @rumps.clicked(YELLOW)
    def change_to_yellow(self):
        random_desktop("yellow")

    @rumps.clicked(PURPLE)
    def change_to_purple(self):
        random_desktop("purple")

    @rumps.clicked(BLACK)
    def change_to_black(self):
        random_desktop("black")


if __name__ == "__main__":
    MenuBarApp().run()
