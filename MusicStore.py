import xml
from enum import Enum
from typing import List
import xml.dom.minidom as minidom

import lxml
from lxml.etree import XMLSchema
class Genre(Enum):
    ROCK = 1
    RAP = 2
    POP = 3
    Classical = 4

    def __str__(self):
        return self.name


class ElementNotFoundException(Exception):
    def __str__(self):
        return "Element not found"




class Album(object):
    def __init__(self, name: str, id: int, numberOfSongs: int):
        self.id = id
        self.name = name
        self.numberOfSongs = numberOfSongs


class Artist(object):
    def __init__(self, name: str, id: int, albums: List[Album], genre: Genre):
        self.id = id
        self.name = name
        self.albums = albums
        self.genre = genre

    def hasAlbum(self, album_: Album) -> bool:
        for album in self.albums:
            if album == album_:
                return True
        return False

    def removeAlbum(self, album: Album):
        self.albums.remove(album)

class MusicStore(object):
    def __init__(self):
        self.artists = []
        self.albums = []

    def getArtistId(self, id):
        res = None
        for artist in self.artists:
            if artist.id == id:
                res = artist
                return res

        if res is None:
            raise ElementNotFoundException

    def getAlbumId(self, id):
        res = None

        for album in self.albums:
            if album.id == id:
                res = album
                return res
        if res is None:
            raise ElementNotFoundException

    def addArtist(self, artist: Artist):
        id = artist.id
        for a in self.artists:
            if id == a.id:
                raise ElementNotFoundException
        self.artists.append(artist)

    def addAlbum(self, alb: Album):
        id = alb.id
        for a in self.albums:
            if id == a.id:
                raise ElementNotFoundException

        self.albums.append(alb)

    def getAlbumInd(self, ind: int):
        result = None
        try:
            result = self.albums[ind]
        except IndexError:
            print('Index ' + str(ind) + " > " + str(len(self.albums)))
        finally:
            return result

    def getArtistsInd(self, ind: int):
        result = None
        try:
            result = self.artists[ind]
        except IndexError:
            print('Index ' + str(ind) + " > " + str(len(self.artists)))
        finally:
            return result

    def countAlbums(self):
        return len(self.albums)

    def countArtists(self):
        return len(self.artists)

    def deleteAlbum(self, id):
        try:
            album = self.getAlbumId(id)
        except Exception as e:
            print(e)
        self.albums.remove(album)
        for artist in self.artists:
            if artist.hasAlbum(album):
                 artist.removeAlbum(album)


    def deleteArtist(self, id):
        try:
            artist = self.getArtistId(id)
        except Exception as e:
            print(e)
            self.artists.remove(artist)
            list_of_albums = artist.albums
            for album in self.albums:
                if album in list_of_albums:
                    self.albums.remove(album)

    def save_to_xml(self, filename):
        doc = minidom.Document()
        musicstore_elem = doc.createElement("MusicStore")
        doc.appendChild(musicstore_elem)

        for artist in self.artists:
            artist_elem = doc.createElement("Artist")
            artist_elem.setAttribute("id", str(artist.id))
            artist_elem.setAttribute("name", artist.name)
            artist_elem.setAttribute("genre", str(artist.genre))
            musicstore_elem.appendChild(artist_elem)

            for album in artist.albums:
                album_elem = doc.createElement("Album")
                album_elem.setAttribute("id", str(album.id))
                album_elem.setAttribute("name", album.name)
                album_elem.setAttribute("numberOfSongs", str(album.numberOfSongs))
                artist_elem.appendChild(album_elem)

        with open(filename, "w") as file:
            file.write(doc.toprettyxml(indent="  "))

    def load_from_xml(self, filename):
        doc = xml.dom.minidom.parse(filename)
        musicstore_elem = doc.documentElement

        artist_nodes = musicstore_elem.getElementsByTagName("Artist")
        for artist_node in artist_nodes:
            artist_id = artist_node.getAttribute("id")
            name = artist_node.getAttribute("name")
            genre = artist_node.getAttribute("genre")

            artist = Artist(id=artist_id, name=name, genre=genre, albums=[])
            self.artists.append(artist)

            album_nodes = artist_node.getElementsByTagName("Album")
            for album_node in album_nodes:
                album_id = album_node.getAttribute("id")
                album_name = album_node.getAttribute("name")
                number_of_songs = album_node.getAttribute("numberOfSongs")

                album = Album(id = album_id, name = album_name, numberOfSongs=number_of_songs)
                artist.albums.append(album)

    @staticmethod
    def checkIsValid(filename) -> bool:

        xml_validator = lxml.etree.XMLSchema(lxml.etree.parse("schema.xsd"))

        xml_file = lxml.etree.parse(filename)
        is_valid = xml_validator.validate(xml_file)
        return is_valid
