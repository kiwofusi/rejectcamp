# -*- coding: utf-8 -*-

def initializeUserDict(count=1):
	user_dict={}
	for p1 in get_hot()[0:count]:
		for p2 in get_urlposts(p1['url'])[0:80]:
			user = p2['user']
			user_dict[user]={}
	return user_dict



def initializeTagDict(user_dict):
	tag_dict={}
	for user in user_dict:
		for url in get_userposts(user):
			tag_dict[url['url']]={}
	return tag_dict

		

def fillItems(user_dict):
	all_items={}
	for user in user_dict:
		for i in range(3):
			try:
				posts=get_userposts(user)
				break
			except:
				print "Failed user " + user + ", retrying"
				time.sleep(4)
		for post in posts:
			url = post['url']
			user_dict[user][url] = 1.0
			all_items[url] = 1

	for ratings in user_dict.values():
		for item in all_items:
			if item not in ratings:
				ratings[item] = 0.0


def fillTags(tag_dict):
	all_tags={}
	try:
		for url in tag_dict:
			tags = get_itemtags(url)
			for tag in tags:
				tag_dict[url][tag] = 1.0
				all_tags[tag] = 1
	except TypeError:
		pass

	for ratings in tag_dict.values():
		for tag in all_tags:
			if tag not in ratings:
				ratings[tag] = 0.0
	




import feedparser


def get_hot():
	d = feedparser.parse("http://b.hatena.ne.jp/hotentry?mode=rss")
	items = []

	for e in d.entries[0:1]:
		try:
			tags = []
			for t in e.tags:
				tags.append(t['term'])
		except AttributeError:
			tags = ''

		items.append({'url':e.link, 'title':e.title, 'tag':tags})


	return items
	
	

import simplejson
import urllib
def get_urlposts(url):
	url = 'http://b.hatena.ne.jp/entry/json/?url=' + url
	lines = urllib.urlopen(url)
	for line in lines:
		line = line.strip(')')
		line = line.strip('(')
	json = simplejson.loads(line)

	bkm = {}
	users = []

	try:
		users = []
		for u in json['bookmarks']:
			users.append({'user':u['user']})
	except AttributeError:
		users = ''
	
	
	return users


def get_userposts(user):
	url = 'http://b.hatena.ne.jp/' + user + '/atomfeed'
	page = 0
	items = []
	while(page < 3):
		d = feedparser.parse(url + "?of=" + str(page*30))
		for e in d.entries:
			try:
				tags = []
				for t in e.tags:
					tags.append(t['term'])
			except AttributeError:
				tags = ''
			items.append({'url':e.links[0].href, 'title':e.title, 'tag':tags})
		page += 1
	return items


def get_itemtags(url):
	url = 'http://b.hatena.ne.jp/entry/json/?url=' + url
	lines = urllib.urlopen(url)
	for line in lines:
		line = line.strip(')')
		line = line.strip('(')
	json = simplejson.loads(line)
	tags = []
	try:
		for u in json['bookmarks']:
			tags.extend(u['tags'])
	except AttributeError,TypeError:
		tags = ''


	
	
	return tags