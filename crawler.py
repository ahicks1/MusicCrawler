import requests
from bs4 import BeautifulSoup
from gmusicapi import Mobileclient

class Song:

    def __init__(self,name,artist):
        self.name = name
        self.artist = artist

class AppCrawler:

  def __init__(self,url):
    self.url = url
    self.songs = []
    return

  def query(self):
      self.get_song_from_url(self.url)
      return

  def get_song_from_url(self,link):
      page_text = requests.get(link)
      #print(page_text.text)
      soup = BeautifulSoup(page_text.text,'html.parser')
      songs = soup.find_all('div', class_='recently-played-song-title')
      for div in songs:
          sn = Song(div.get_text().strip(),div.next_sibling.next_sibling.get_text().strip())
          self.songs.append(sn)
        #print div.get_text().strip()

  def add_songs_to_library(self):
      api = Mobileclient()
      logged_in = api.login('legofan0329@gmail.com', '1944_D-d@y',Mobileclient.FROM_MAC_ADDRESS)

      playlist = api.create_playlist("JackFM #2", "This is what Jack is playing next")
      for sn in crawler.songs:
          print sn.name
          search_res = api.search(sn.name+" "+sn.artist, 10)
          songid = search_res["song_hits"][0]["track"]["storeId"]
          api.add_songs_to_playlist(playlist,songid)

crawler = AppCrawler("http://www.hellojack.com/recently-played/")
crawler.query()
crawler.add_songs_to_library()
