import requests
from bs4 import BeautifulSoup

def Search():
    mode = "search"
    page = 1
    maxPage = 1000 
    searchName = input(" Search: ")
    category = ""
    name = f"?s={searchName}"
    ParsingTorrents(name, page, maxPage, category, mode)
 
def ShowNewTorrents():
    mode = "new"
    page =  1
    maxPage = 1000
    name = ""
    category = ""
    ParsingTorrents(name, page, maxPage, category, mode)

def Categories():
    mode = "categories"
    page = 1
    maxPage = 1000
    name = ""
    category = ShowCategoriesList()
    #print("You choise category:" , category)
    ParsingTorrents(name,page,maxPage,category,mode)

def ParsingTorrents(name, currentPage, maxPage, category, mode):
    if int(currentPage) < 0 or int(currentPage) > int(maxPage):
        print("Error number page go back...")
        CommandUser("deadlock", name, 1, maxPage, category, mode)
    link = f"https://mac-torrent-download.net/{category}/page/{currentPage}/{name}"
    requestsall = requests.get(link)
    soup = BeautifulSoup(requestsall.content, "html.parser")
    torrents_search = soup.find_all("a",{"rel":"bookmark"})
    print(link)
    pages = ""

    if mode == "search":
        searchResult = soup.find("h2").get_text()
        lastResult = searchResult.split()[5]
        if lastResult == "0":
            print(f" Search Results not found posts.")
        else:
            if int(lastResult) > 50:
                pages, maxPage = ParsingInformationForPagination(soup)

    elif mode == "new" or "categories":
        pages, maxPage = ParsingInformationForPagination(soup)

    #Выводим список торрентов
    PrintTorrentsList(torrents_search)
    #Выводим информацию о поиске 
    print("\n", pages)
    #Выводим список вспомогательных комманд
    PrintHelpCommandInTorrentList()
    #Считываем комманды юзера
    commandUser = input(" Command: ")
    CommandUser(commandUser, name, int(currentPage), maxPage, category,mode)
    #Парсим выбранный торрент
    ParsingTorrent(torrents_search, int(commandUser))
        
def ParsingInformationForPagination(soup):
    pages = soup.find("div",{"class":"pagination"}).next.get_text()
    maxPage = int(soup.find("div",{"class":"pagination"}).next.get_text().split()[3])
    return pages, maxPage

def ShowCategoriesList():
    link = "https://mac-torrent-download.net/"
    print(" Wait...")
    requestsall = requests.get(link)
    soup = BeautifulSoup(requestsall.content, "html.parser")
    categories = soup.find_all("li",{"class": "menu-item"}) 
    item_torrent = 1 

    for name in categories[:27]:
        name_category = name.text 
        print(f"{item_torrent}. {name_category}") 
        item_torrent += 1 
    
    choise_torrent = int(input("\n Choice number category:")) 
    link = categories[choise_torrent-1].next.get("href").split("/")
    category = f"{link[3]}/{link[4]}/{link[5]}" 
    return category

def CommandUser(commandUser, name, currentPage, maxPage, category,mode): 
    commandMenu = True
    while commandMenu:
        if commandUser == "n":
            ParsingTorrents(name, currentPage + 1, maxPage, category, mode)
        elif commandUser == "d":
            ParsingTorrents(name, currentPage - 1, maxPage, category, mode)
        elif commandUser[0] == "p":
            pageChoiceUser = commandUser.split()
            ParsingTorrents(name, int(pageChoiceUser[1]), maxPage, category, mode)
        elif commandUser == "deadlock":
            ParsingTorrents(name, currentPage, maxPage, category,mode)
        elif commandUser == "x":
            exit()
        else:
            break

def PrintTorrentsList(torrentsList):
    print(" Wait...")
    item_torrent = 1
    for linked in torrentsList:
        print(f" {item_torrent}. {linked.text}")
        item_torrent +=1

def PrintHelpCommandInTorrentList():
    #Справка по коммандам
    print("""
 Enter number to choice download Torrent
 n - next page
 p [number page] - go to page number
 d - Previos page
    """)
        
def ParsingTorrent(torrents_search, choice_torrent):
    print(" Wait....")
    
    #Парсинг выбранного торрента
    nextlink = torrents_search[choice_torrent - 1].get("href")
    print(" link-page:",nextlink)
    requestsUser = requests.get(nextlink)
    soup = BeautifulSoup(requestsUser.content, "html.parser")
    #Получаем информацию о торренте
    linkInfo_th = soup.find_all('th', {"class": "cell"})
    linkInfo_td = soup.find_all('td', {"class": "cell"})
    print(" img-link:", soup.find('img',{"itemprop":"image"}).get("src"))
    list = 0
    print(" ----------------------")
    while list <5:
        nameTorrent = linkInfo_th[list].get_text()
        infoTorrent = linkInfo_td[list].get_text()
        print(f" {nameTorrent}:{infoTorrent}")
        list = list + 1
    print(" ----------------------")

    #Получаем массив из двух объектов(в 1 будет Магнет ссылка, во втором ссылка на Торрент)
    arrayMagtenAndTorrent = soup.find_all('li', {"class": "btn-list"})
    linkMagnet = arrayMagtenAndTorrent[0].next.get("href")
    linkTorrent = arrayMagtenAndTorrent[1].next.get("href")

    #Дальше парсим магнет ссылку
    requestsMagnet = requests.get(linkMagnet)
    soupMagnet = BeautifulSoup(requestsMagnet.content, "html.parser")

    #Заодно парсим торрент ссылку
    requestsTorrent = requests.get(linkTorrent)
    soupTorrent = BeautifulSoup(requestsTorrent.content, "html.parser")

    #Ссылка на скачку магнет
    magnet = soupMagnet.find('p', {"id":"dlbtn"}).next.get("href")
    print(" Magnet link: ", magnet)

    #Ссылка на скачку торрент файла
    torrent = soupTorrent.find('p', {"id":"dlbtn"}).next.get("href")
    print(" Torrent link: ", torrent)
    pass


