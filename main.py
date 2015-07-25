from bs4 import BeautifulSoup
from requests import get
from json import dumps #only for prettiness

def grab_url(query):
	show = "%20".join(query.lower().split(" "))
	url = "http://www.imdb.com/find?s=all&q={}".format(show)
	return url

def grab_cast(soup, url, limit=5):
	actors = []
	partial = soup.find("td", {"class": "result_text"}).find("a")["href"]
	soup = BeautifulSoup(get("http://www.imdb.com{}".format(partial.replace('?', 'fullcredits?'))).text, 'html.parser')
	for tag in soup.find_all("span", {"class": "itemprop"}, limit=limit):
		actors.append(tag.text)
	print("\nActors: {}\n".format(actors))
	return actors 

def grab_recent_shows(soup, actor, limit=5):
	recents = []
	partial = soup.find("td", {"class": "result_text"}).find("a")["href"]
	soup = BeautifulSoup(get("http://www.imdb.com{}".format(partial)).text, 'html.parser')
	for tag in soup.find_all("div", {"class": "filmo-row"}, limit=limit):
		recents.append(tag.find("a").text)
	return recents

if __name__ == "__main__":
	output = {}

	show = input("Show Name: ")
	actorLimit = int(input("How many actors/actresses? "))
	showLimit = int(input("How many recent shows do you want? "))

	url = grab_url(show)
	soup = BeautifulSoup(get(url).text, 'html.parser')
	actors = grab_cast(soup, url, actorLimit)
	for actor in actors:
		print("{}: {}".format(actor, grab_url(actor)))
		soup = BeautifulSoup(get(grab_url(actor)).text, 'html.parser')
		recents = grab_recent_shows(soup, actor, showLimit)
		output[actor] = recents
	print(dumps(output, indent=4))
	#print("\n{}".format(output))