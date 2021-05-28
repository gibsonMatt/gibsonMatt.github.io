#!/usr/bin/env python3

import argparse
import collections
import os
from datetime import datetime


parser = argparse.ArgumentParser(description = "Update news")

parser.add_argument("-p", "--push", help = "Automatically push to github repo", action = "store_true")
parser.add_argument("-n", "--num", help = "Number of news items to display", default = 5)

args = parser.parse_args()

args.num = int(args.num)

def convert2Html(k,v):
    
    html = "<li> "
    v = v.replace("{", '<a href="')
    v = v.replace("}", '">')
    v = v.replace("[", "")
    v = v.replace("]", "</a>")
    html = html + v + " [" + datetime.strftime(k, "%b %Y") + "]" +  "</li>"
    return(html)

newsFile = open("news.txt", 'r')

newsItems = {}

for i, line in enumerate(newsFile):
    l = line.replace('\n', '').split(";")
    text = l[0]
    date = l[1].replace(' ', '')
    date = datetime.strptime(date, "%m/%d/%Y")
    newsItems[date] = text

formattedItems = {}

for k, v in newsItems.items():
    formattedItems[k] = convert2Html(k,v)

od = collections.OrderedDict(sorted(formattedItems.items(), reverse = True))
newsFile.close()


htmlFile = open("_includes/news.html", "w")

if (args.num > len(formattedItems.keys())):
    args.num = len(formattedItems.keys())

lst_di = list(od.items())

for i in range(0, args.num):
    htmlFile.write(lst_di[i][1] + '\n')

htmlFile.close()


if (args.push):
    os.system("git add --all")
    os.system("git commit -m 'update news'")
    os.system("git push")


