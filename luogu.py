import requests
import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json

header = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

_strongth =["入门难度", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"]

def creat_soup(str):
	return BeautifulSoup(requests.get(str, headers = header).text,'html.parser')

def get_pass_subject(url):
	tag = creat_soup(url).find("h2", text = "通过题目")
	res = set([])
	for x in tag.next_siblings:
		if(x.name == 'a'): res.add(x.string)
	return res

def get_subject_info(str):
#	print("colleting the info of", str)
	url = "https://www.luogu.org/problemnew/show/" + str
	soup = creat_soup(url)
	res = {"tag":[], "strong":""}

	try:
		class_contents = ['lg-tag', 'am-badge', 'am-radius', 'lg-bg-pink', 'am-hide']
		for x in soup.find_all('span'):
			if (x['class'] == class_contents):
				res["tag"].append(x.string)
		
		hard_tag = soup.find("strong", string = "难度")
		for x in hard_tag.parent.children:
			if(x != "\n"): res["strong"] = x.string
	except:
		print("Fail to get the info of", str, "!")
		res = None;
	
	return res
	
def get_user_info(url):
	subjects = get_pass_subject(url)
	s_info ={}
	t_info ={}
	for x in subjects:
		info = get_subject_info(x)
		if(info == None): continue
		str = info["strong"]
		if(s_info.get(str) == None): s_info[str] = 1
		else: s_info[str] += 1

		for str in info["tag"]:
			if(t_info.get(str) == None): t_info[str] = 1
			else: t_info[str] += 1	
	soup = creat_soup(url)
	name = soup.find("h1").string.split(' ')[1]
	return (name, s_info, t_info)

def draw(data):
	name = data[0]
	s_info = data[1]
	t_info = data[2]
	label = []
	data = []
	plt.rcParams['font.sans-serif']=['SimHei'] 
	plt.rcParams['axes.unicode_minus']=False

	for x in _strongth:
		if(s_info.get(x) != None):
			label.append(x)
			data.append(s_info[x])

	X = range(len(data))
	
	plt.title(name + "的做题记录（难度）")
	P1 = plt.bar(X, data, tick_label = label)

	for x, y in zip(X, data):
		plt.text(x, y - 1, '%d' % y, ha='center', va='center', fontsize=12)

	plt.savefig("strongth.png")
	plt.figure()

	label = []
	data = []
	p = 0
	for k, v in sorted(t_info.items(), key = lambda item:item[1], reverse = 1):
		if(p >= 8): break
		p += 1
		label.append(k)
		data.append(v)
	
	X = range(len(data))
	
	plt.title(name + "的做题记录（标签）")
	P2 = plt.bar(X, data, tick_label = label)

	for x, y in zip(X, data):
		plt.text(x, y - 1, '%d' % y, ha='center', va='center', fontsize=12)
	
	plt.savefig("tag.png")
	plt.close("all")

def printf(data, subjects):
	name = data[0]
	s_info = data[1]
	t_info = data[2]

	with open('data.txt', 'w') as f:
		f.write(name + '的做题记录:\n')
		f.write("您总共AC了" + "%d" % len(subjects) + "道题" + "\n")
		p = 0
		for x in subjects:
			if(p == 6):
				f.write('\n')
				p = 0
			f.write(x + ' ')
			p += 1;
		
		f.write('\n\n')
		f.write('按难度分类：\n')

		for x in _strongth:
			if(s_info.get(x) != None):
				f.write(x + ":" + "%d" % s_info[x] + "\n")
		
		f.write('\n')
		f.write("按标签分类：\n")

		for k, v in sorted(t_info.items(), key = lambda item:item[1], reverse = 1):
			f.write(k + ':' + "%d" % v + '\n')


with open("url.txt", "r") as f:
	url = f.read()
print(url)
res = get_user_info(url)
draw(res)
printf(res, get_pass_subject(url))
print("finish.")