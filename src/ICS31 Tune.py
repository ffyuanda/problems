from collections import namedtuple
import copy

Album = namedtuple('Album', 'id artist title year songs')
Song = namedtuple('Song', 'track title length play_count')

MUSIC = [
    Album("1", "Peter Gabriel", "Up", 2002,
        [Song(1, "Darkness", 411, 5),
         Song(2, "Growing Up", 453, 5)]),
    Album("2", "Simple Minds", "Once Upon a Time", 1985,
        [Song(1, "Once Upon a Time", 345, 9),
         Song(2, "All the Things She Said", 256, 10)]),
    Album("TRS", "The Rolling Stones", "Let It Bleed", 1969,
        [Song(1, "Gimme Shelter", 272, 3),
         Song(2, "Love In Vain", 259, 2),
         Song(3, "You Can't Always Get What You Want", 448, 10)])]


def get_song_input():
    """Function."""
    track = int(input('Enter the song\'s track:\n'))
    title = input('Enter the song\'s title:\n')
    length = int(input('Enter the song\'s length:\n'))
    play_count = int(input('Enter the song\'s play_count:\n'))

    return Song(track, title, length, play_count)


def get_album_input():
    """Function."""
    id_ = input('Enter the album\'s id:\n')
    artist = input('Enter the album\'s artist:\n')
    title = input('Enter the album\'s title:\n')
    year = int(input('Enter the album\'s year:\n'))
    album = Album(id_, artist, title, year, [])

    number_songs = int(input('Enter the number of songs in this album:\n'))
    assert type(number_songs) is int
    for i in range(number_songs):
        album.songs.append(get_song_input())

    return album


def add_album(albums: list):
    """Function."""
    albums.append(get_album_input())
    return albums


def remove_album(albums: list, id_: str):
    """Function."""
    assert type(albums) is list
    assert type(id_) is str

    for album in albums:
        if album.id == id_:
            albums.remove(album)
            return albums
    print('Album not found.')
    return albums


def favorite_song(albums, id_):
    """Function."""
    assert type(albums) is list
    assert type(id_) is str
    max_count = -1
    fav_song = None

    for album in albums:
        if album.id == id_:
            for song in album.songs:
                if song.play_count * song.length >= max_count:
                    fav_song = song
                    max_count = song.play_count * song.length

            return fav_song

    return 'Album not found.'


def unplayed_songs(albums, id_):
    """Function."""

    un_songs = list()

    for album in albums:
        if album.id == id_:
            for song in album.songs:
                if song.play_count == 0:
                    un_songs.append(song)

            return un_songs

    return 'Album not found.'


def favorite_album(albums):
    """Function."""
    max_count = -1
    fav_album = None

    for album in albums:
        total_play = 0
        for song in album.songs:
            total_play += song.play_count * song.length
        # print(total_play)
        if total_play >= max_count:
            max_count = total_play
            fav_album = album

    return fav_album


def unplayed_albums(albums):
    """A function."""
    no_albums = list()
    for album in albums:
        total_play = 0
        for song in album.songs:
            total_play += song.play_count
        if total_play == 0:
            no_albums.append(album)

    return no_albums


def print_menu():
    """Function."""
    print("""MUSIC COLLECTION MANAGER

add - Add a new album
del - Remove an album
fav_a - Print favorite album
fav_s - Print favorite song
not_a - Print not played albums
not_s - Print not played songs
exit - Exit the application\n""")
    music = copy.deepcopy(MUSIC)

    while True:
        try:
            op = input('Choose an option:\n')
        except EOFError:
            break
        if op == 'add':
            add_album(MUSIC)
        elif op == 'del':
            id_ = input('Enter the Album ID:\n')
            remove_album(MUSIC, id_)
        elif op == 'fav_a':
            if music == MUSIC:
                print(None)
            else:
                print(favorite_album(MUSIC))

        elif op == 'fav_s':
            id_ = input('Enter the Album ID:\n')
            print(favorite_song(MUSIC, id_))
        elif op == 'not_a':
            print(unplayed_albums(MUSIC))
        elif op == 'not_s':
            id_ = input('Enter the Album ID:\n')
            print(unplayed_songs(MUSIC, id_))
        elif op == 'exit':
            break
        else:
            continue
        print("""MUSIC COLLECTION MANAGER

add - Add a new album
del - Remove an album
fav_a - Print favorite album
fav_s - Print favorite song
not_a - Print not played albums
not_s - Print not played songs
exit - Exit the application\n""")


if __name__ == '__main__':
    print_menu()
    # print(favorite_album(MUSIC))
