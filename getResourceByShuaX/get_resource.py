import os
import urllib
import requests
import zlib
import json
import hashlib
from lxml import etree

# PYTHONIOENCODING=utf-8
# export PYTHONIOENCODING=UTF-8

baseurl = "https://raw.githubusercontent.com/scheib/chromium/"
tree = ""
apiurl = "https://api.github.com/repos/scheib/chromium/commits?path="
resource_ids_url = "tools/gritsettings/resource_ids"

resource_ids_md5 = json.load(open('resource_ids.json', 'r'))
complete_list = json.load(open('complete.json', 'r'))

def md5(content):
	return hashlib.md5(content).hexdigest()

# 下载内容
def get(url):
	r = requests.get(baseurl + tree + "/" + url)
	if r.status_code==200:
		return r.content

def analyze_grd(content, path):
	root = etree.fromstring(content)
	for name in root.xpath("//@file"):
		fullname = urllib.request.pathname2url(path+"/"+name)
		print("下载"+fullname)
		file_content = get(fullname)
		if file_content:
			md5str = md5(file_content)
			print("md5 " + md5str )
			resource_ids_md5[md5str] = fullname
			json.dump(resource_ids_md5, open('resource_ids.json', 'w'))

def analyze_ids():
	print("下载resource_ids")
	resource_ids_content = get(resource_ids_url)

	print("解析resource_ids")
	resource_ids = eval(resource_ids_content)

	print("遍历resource_ids")
	for name in resource_ids:
		if name.endswith(".grd") and not name.startswith("<"):
			print("下载" + name)
			grd_content = get(name)
			if grd_content:
				analyze_grd(grd_content, os.path.dirname(name))

print("拉取分支记录")
r = requests.get(apiurl + resource_ids_url)
if r.status_code==200:
	history = json.loads(r.text)
	for info in reversed(history):
		tree = info["sha"]
		print("分支"+tree)
		if tree in complete_list:
			print("跳过分支")
		else:
			analyze_ids()
			complete_list.append(tree)
			json.dump(complete_list, open('complete.json', 'w'))

