# -*- coding: utf-8 -*-
#
# バーコードリーダーで読み込んだJANコード一覧を読み込んで商品情報一覧を得る
#
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import re
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

# 定数
base_url = "http://www.getchu.com/"
base_url_item = "http://www.getchu.com/soft.phtml?gc=gc&id="
base_url_search = base_url + \
    "php/search.phtml?genre=all&check_key_dtl=1&submit=&genre=all&gc=gc&search_keyword="

file_in = "jancodes.txt"
file_out = "result.txt"

r_cv = re.compile("CV：([^< ]+)")

# 処理


def read():
    f = open(file_in)
    codes = f.readlines()
    f.close()

    for code in codes:
        c = code.rstrip('\r\n')
        if len(c) > 0:
            if c.startswith('http://'):
                get_item('', c)
            elif c.isdigit():
                search(c)


def write(data):
    with open(file_out, 'a') as f:
        f.write(data)


def get_item(code, url):
    jan_code = ""
    title = ""
    url_image = ""
    brand = ""
    price = ""
    pub_date = ""
    genre = ""
    product_number = ""
    animator = ""
    scenario = ""
    music = ""
    artist = ""
    privilege = ""
    sub_genre = ""
    category = ""
    cvs = ""

    try:
        res = urllib.request.urlopen(url)
        html = res.read().decode("eucjp")
        soup = BeautifulSoup(html, "html.parser")
        soft_table = soup.find("table", id="soft_table")
        url_image = soft_table.find("a", class_="highslide").attrs["href"]
        url_image = url_image.replace("./", base_url)
        title = soft_table.find(
            "h1", id="soft-title").text.replace("\n", "").split(" （このタイトルの関連商品）")[0]
        table = soft_table.find("table")
        lines = table.find_all("tr")
        for line in lines:
            if line.text.startswith("ブランド："):
                brand = line.text.replace("ブランド：", "").replace(
                    "\n", "").replace("（このブランドの作品一覧）", "")
            elif line.text.startswith("定価："):
                price = line.text.replace("定価：", "").replace(
                    "\n", "").split(" (税込￥")[0].replace("￥", "").replace(",", "")
            elif line.text.startswith("発売日："):
                pub_date = line.text.replace("発売日：", "").replace(
                    "\n", "")
            elif line.text.startswith("ジャンル："):
                genre = line.text.replace("ジャンル：", "").replace(
                    "\n", "")
            elif line.text.startswith("JANコード："):
                jan_code = line.text.replace("JANコード：", "").replace(
                    "\n", "")
            elif line.text.startswith("品番："):
                product_number = line.text.replace("品番：", "").replace(
                    "\n", "")
            elif line.text.startswith("原画："):
                animator = line.text.replace("原画：", "").replace(
                    "\n", "")
            elif line.text.startswith("シナリオ："):
                scenario = line.text.replace("シナリオ：", "").replace(
                    "\n", "")
            elif line.text.startswith("音楽："):
                music = line.text.replace("音楽：", "").replace(
                    "\n", "")
            elif line.text.startswith("アーティスト："):
                artist = line.text.replace("アーティスト：", "").replace(
                    "\n", "")
            elif line.text.startswith("商品同梱特典："):
                privilege = line.text.replace("商品同梱特典：", "").replace(
                    "\n", "")
            elif line.text.startswith("サブジャンル："):
                sub_genre = line.text.replace("サブジャンル：", "").replace(
                    "\n", "").replace(" [一覧] ", "")
            elif line.text.startswith("カテゴリ："):
                category = line.text.replace("カテゴリ：", "").replace(
                    "\n", "").replace(" [一覧]", "")

        actors = soup.find_all("h2", class_="chara-name")
        for actor in actors:
            try:
                cv_name = r_cv.search(actor.text)
                if len(cv_name.group(1)) > 0:
                    cvs = cvs + cv_name.group(1) + ","
            except AttributeError:
                pass

        data = jan_code if len(code) < 13 else code
        data = data + "\t" + title
        data = data + "\t" + url_image
        data = data + "\t" + brand
        data = data + "\t" + price
        data = data + "\t" + pub_date
        data = data + "\t" + genre
        data = data + "\t" + jan_code
        data = data + "\t" + product_number
        data = data + "\t" + animator
        data = data + "\t" + scenario
        data = data + "\t" + music
        data = data + "\t" + artist
        data = data + "\t" + privilege
        data = data + "\t" + sub_genre
        data = data + "\t" + category
        data = data + "\t" + cvs
        data = data + "\n"

        print(data)
        write(data)

    except UnicodeDecodeError:
        pass


def search(code):
    try:
        res = urllib.request.urlopen(base_url_search + code)
        html = res.read().decode("eucjp")
        soup = BeautifulSoup(html, "html.parser")
        detail_block = soup.find("div", id="detail_block")
        href = detail_block.find("a", class_="blueb").attrs["href"]
        href = href.replace("../soft.phtml?id=", base_url_item)
        get_item(code, href)
    finally:
        pass


if __name__ == "__main__":
    read()
