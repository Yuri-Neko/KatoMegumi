import json
import urllib
import requests as r
from bs4 import BeautifulSoup
baseURL = "https://komikindo.id/"

def index(request):
    response = r.get(baseURL)
    
    resolve = json.dumps({
        'status': 'success',
        'message': 'Welcome to Komikindo API',
        'statusCode': response.status_code,
    })
    
    return json.dumps(resolve)

def home(request):
    response = r.get(baseURL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    obj["menu"] = []
    mangas_menu = soup.find(id="menu-second-menu").find_all("li")
    for manga in mangas_menu:
        name = manga.find("a").text
        link = {
            'url': manga.find("a").get("href"),
            'endpoint': manga.find("a").get("href").replace(baseURL, "")
        }
        
        obj["menu"].append({ 'name': name, 'link': link })
        
    obj["body"] = {}
    mangas_menu = soup.find_all("section", {"class": "whites"})
    for manga in mangas_menu:
        if (manga.find(id="informasi")):
            continue
        
        popular = manga.find_all("div", {"class": "mangapopuler"})
        if (len(popular) > 0):
            obj["body"]["popular"] = []
            mangas = manga.find("div", {"class": "mangapopuler"}).find_all("div", {"class": "animepost"})
            for m in mangas:
                name = m.find("a", itemprop="url").get("title")
                thumb = m.find("img").get("src").split("?")[0]
                link = {
                    'url': m.find("a", itemprop="url").get("href"),
                    'endpoint': m.find("a", itemprop="url").get("href").replace(baseURL, "")
                }
                last_upload = m.find("span", {"class": "datech"}).text
                last_chapter = {
                    'name': m.find("div", {"class": "lsch"}).find("a").text,
                    'url': m.find("div", {"class": "lsch"}).find("a").get("href"),
                    'endpoint': m.find("div", {"class": "lsch"}).find("a").get("href").replace(baseURL, "")
                }
                obj["body"]["popular"].append({ 'name': name, 'thumb': thumb, 'link': link, 'last_upload': last_upload, 'last_chapter': last_chapter })
            continue
            
        latest = manga.find_all("div", {"class": "latestupdate-v2"})
        if (len(latest) > 0):
            obj["body"]["latest"] = []
            mangas = manga.find_all("div", {"class": "animepost"})
            for m in mangas:
                name = m.find("a", itemprop="url").get("title")
                thumb = m.find("img").get("src").split("?")[0]
                link = {
                    'url': m.find("a", itemprop="url").get("href"),
                    'endpoint': m.find("a", itemprop="url").get("href").replace(baseURL, "")
                }
                obj["body"]["latest"].append({ 'name': name, 'thumb': thumb, 'link': link })
            continue

    return json.dumps(obj)

def daftar_komik(request, page):
    response = r.get(baseURL + 'daftar-komik/page/' + str(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        
        name = manga.find("a", itemprop="url").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a", itemprop="url").get("href"),
            'endpoint': manga.find("a", itemprop="url").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            endpoint = url.replace(baseURL, "")
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })

    return json.dumps(obj)

def komik_terbaru(request, page):
    response = r.get(baseURL + 'komik-terbaru/page/' + str(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        
        name = manga.find("a", itemprop="url").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a", itemprop="url").get("href"),
            'endpoint': manga.find("a", itemprop="url").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            endpoint = url.replace(baseURL, "")
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })

    return json.dumps(obj)

def komik(request, type, page):
    response = None
    if (type == "manga"):
        response = r.get(baseURL + 'manga/page/' + str(page))
    elif (type == "manhua"):
        response = r.get(baseURL + 'manhua/page/' + str(page))
    elif (type == "manhwa"):
        response = r.get(baseURL + 'manhwa/page/' + str(page))
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        name = manga.find("a").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a").get("href"),
            'endpoint': manga.find("a").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            endpoint = url.replace(baseURL, "")
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })

    return json.dumps(obj)
    
def komik_detail(request, endpoint):
    response = r.get(baseURL + endpoint)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    manga = soup.find(class_="postbody")
    obj["name"] = manga.find(class_="entry-title").text.replace("Komik ","")
    obj["alters"] = manga.find(class_="spe").find_all("span")[0].text.split(": ")[1].split(", ")
    obj["status"] = manga.find(class_="spe").find_all("span")[1].text.split(": ")[1]
    obj["author"] = manga.find(class_="spe").find_all("span")[2].text.split(": ")[1]
    obj["illustator"] = manga.find(class_="spe").find_all("span")[3].text.split(": ")[1]
    obj["grafis"] = manga.find(class_="spe").find_all("span")[4].text.split(": ")[1]
    obj["tema"] = manga.find(class_="spe").find_all("span")[5].text.split(": ")[1]
    obj["konten"] = manga.find(class_="spe").find_all("span")[6].text.split(": ")[1]
    obj["type"] = manga.find(class_="spe").find_all("span")[7].text.split(": ")[1]
    obj["score"] = manga.find(itemprop="ratingValue").text
    
    obj["genres"] = []
    genres = manga.find(class_="genre-info").find_all("a")
    for genre in genres:
        name = genre.get("title")
        link = {
            'url': genre.get("href"),
            'endpoint': genre.get("href").replace(baseURL, "")
        }
        obj["genres"].append({ 'name': name, 'link': link })  
    
    obj["synopsis"] = manga.find(itemprop="description").text.split("\n")[1]
    
    obj["chapters"] = []
    chapters = manga.find(id="chapter_list").find_all(class_="lchx")
    for chapter in chapters:
        name = chapter.find("a").text
        link = {
            'url': chapter.find("a").get("href"),
            'endpoint': chapter.find("a").get("href").replace(baseURL, "")
        }
        obj["chapters"].append({ 'name': name, 'link': link })
        
    
    return json.dumps(obj)

def search(request, query):
    response = r.get(baseURL + '?' + urllib.parse.urlencode({'s': query}))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        name = manga.find("a").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a").get("href"),
            'endpoint': manga.find("a").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            endpoint = url.replace(baseURL, "")
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })
    
    return json.dumps(obj)

def chapter(request, endpoint):
    response = r.get(baseURL + endpoint)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    manga = soup.find("head")
    chapter_link = manga.find("link", {"type": "application/json"}).get("href")
    
    reschap = r.get(chapter_link)
    res = json.loads(reschap.text)
    obj["title"] = res["title"]["rendered"]
    
    soupp = BeautifulSoup(res["content"]["rendered"], 'html.parser')
    obj["images"] = []
    imgs = soupp.find_all("img")
    for img in imgs:
        obj["images"].append(img.get("src"))
        
    return json.dumps(obj)