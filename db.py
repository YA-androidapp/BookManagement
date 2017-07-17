# -*- coding: utf-8 -*-
#
# SQLiteへのアクセス
#
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import sys
import csv
import sqlite3

csv_in = "‪%USERPROFILE%\\Documents\\works\\Python\\getchu\\infos.csv"
db_out = "‪%USERPROFILE%\\Documents\\works\\SQLite\\Getchu\\Getchu.db"

con = sqlite3.connect(db_out)
cur = con.cursor()

# 表の新規作成
cur.execute(
    """create table campany(
    code text,
    url_image text,
    title text,
    brand text,
    price integer,
    date_pub numeric,
    genre text,
    jan_code text,
    number text,
    picture text,
    scenario text,
    music text,
    artist text,
    privilege text,
    subgenre text,
    category text,
    actor text
    )"""
)


conn = None
try:
    conn = sqlite3.connect(db_out, isolation_level='EXCLUSIVE')
    #
except Exception:
    if conn:
        conn.rollback()
finally:
    if conn:
        conn.commit()
