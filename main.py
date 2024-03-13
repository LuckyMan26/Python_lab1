from MusicStore import Album,Artist,MusicStore,Genre


if __name__ == '__main__':
    music_store = MusicStore()
    album1 = Album("Name1", 1, 5)
    album2 = Album("Name2", 2, 6)
    album3 = Album("Name3", 3, 7)
    album4 = Album("Name4", 4, 8)
    album5 = Album("Name5", 5, 9)
    try:
        music_store.addAlbum(album1)
        music_store.addAlbum(album2)
        music_store.addAlbum(album3)
        music_store.addAlbum(album4)
        music_store.addAlbum(album5)
    except Exception as e:
        print(e)
    artist1 = Artist("AC/DC", 1, [album1, album2], Genre.ROCK)
    artist2 = Artist("2Pac", 2, [album3, album4], Genre.RAP)
    artist3 = Artist("Lady Gaga", 3, [album5], Genre.POP)
    try:
        music_store.addArtist(artist1)
        music_store.addArtist(artist2)
        music_store.addArtist(artist3)
    except Exception as e:
        print(e)
    print("IS VALID ", music_store.checkIsValid("music_store.xml"))
    music_store.save_to_xml("music_store.xml")
    music_store_2 = MusicStore()
    music_store_2.load_from_xml("music_store.xml")
    music_store_2.save_to_xml("music_store_2.xml")



