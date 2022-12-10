from bs4 import BeautifulSoup
import requests
import sys
import os
import re

url = input("Enter the thread URL(2ch of 4chan): ")

try:
    html_content = requests.get(url).content
except requests.exceptions.HTTPError as e:
    print("Can not access:", e)
    sys.exit(0)


soup = BeautifulSoup(html_content, "html.parser")

site = url.replace("https://", "").split("/")[0:1][0]

if site == "2ch.hk":
    figures = soup.find_all("figure", class_="post__image")
if site == "boards.4chan.org":
    figures = soup.find_all("div", class_="file")

folder_path = re.sub(r"[/|\\?*<>:\"]", "", site + " " + soup.find("title").text)
if site == "boards.4chan.org":
    folder_path = folder_path.split("-")[0] + "-" + folder_path.split("-")[1][:-1]

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

totalFileCount = len(figures)
currentFileCount = 1

for figure in figures:

    a_tag = figure.find("a")

    if site == "2ch.hk":
        img_url = "https://" + site + a_tag["href"]
    if site == "boards.4chan.org":
        img_url = "https://" + a_tag["href"][2:]

    img_data = requests.get(img_url).content

    with open(folder_path + "/" + img_url.split("/")[-1], "wb") as f:
        f.write(img_data)
        print(f.name.split("/")[-1] + " was downloaded! " + str(currentFileCount) + "/" + str(totalFileCount))
        currentFileCount += 1