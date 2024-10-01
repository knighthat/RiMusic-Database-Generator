import sqlite3



class Database: 
    '''
    To add onther table, add a method before the last method (execute) and follow this pattern
    def $tableName$_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute($command$)

    :param tableName:
        Is the name of the table.
        Should use underscore '_' as the replacement to spaces
        And in all lowercase.
    :param command:
        Is the SQL command
    '''

    def album_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `Album` (
                `id` TEXT NOT NULL, 
                `title` TEXT, 
                `thumbnailUrl` TEXT, 
                `year` TEXT, 
                `authorsText` TEXT, 
                `shareUrl` TEXT, 
                `timestamp` INTEGER, 
                `bookmarkedAt` INTEGER, 
                PRIMARY KEY(`id`)
            );
        ''')

    def android_metadata_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE android_metadata (locale TEXT);
        ''')

    def artist_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `Artist` (
                `id` TEXT NOT NULL, 
                `name` TEXT, 
                `thumbnailUrl` TEXT, 
                `timestamp` INTEGER, 
                `bookmarkedAt` INTEGER,
                PRIMARY KEY(`id`)
            );
        ''')

    def playlist_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `Playlist` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                `name` TEXT NOT NULL, 
                `browseId` TEXT
            );
        ''')

    def queue_media_item_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `QueuedMediaItem` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                `mediaItem` BLOB NOT NULL, 
                `position` INTEGER
            );
        ''')

    def room_master_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE room_master_table (
                id INTEGER PRIMARY KEY,
                identity_hash TEXT
            );
        ''')

    def search_quert_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `SearchQuery` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                `query` TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE UNIQUE INDEX `index_SearchQuery_query` ON `SearchQuery` (`query`);
        ''')

    def song_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `Song` (
                `id` TEXT NOT NULL, 
                `title` TEXT NOT NULL, 
                `artistsText` TEXT, 
                `durationText` TEXT, 
                `thumbnailUrl` TEXT, 
                `likedAt` INTEGER, 
                `totalPlayTimeMs` INTEGER NOT NULL, 
                PRIMARY KEY(`id`)
            );
        ''')

    def event_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `Event` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                `songId` TEXT NOT NULL, 
                `timestamp` INTEGER NOT NULL, 
                `playTime` INTEGER NOT NULL, 
                FOREIGN KEY(`songId`) REFERENCES `Song`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE 
            );
        ''')

        cursor.execute('''
            CREATE INDEX `index_Event_songId` ON `Event` (`songId`);
        ''')

    def format_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `Format` (
                `songId` TEXT NOT NULL, 
                `itag` INTEGER, 
                `mimeType` TEXT, 
                `bitrate` INTEGER, 
                `contentLength` INTEGER, 
                `lastModified` INTEGER, 
                `loudnessDb` REAL, PRIMARY KEY(`songId`), 
                FOREIGN KEY(`songId`) REFERENCES `Song`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE 
            );
        ''')

    def lyrics_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `Lyrics` (
                `songId` TEXT NOT NULL, 
                `fixed` TEXT, 
                `synced` TEXT, 
                PRIMARY KEY(`songId`), 
                FOREIGN KEY(`songId`) REFERENCES `Song`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE 
            );
        ''')

    def song_album_map_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `SongAlbumMap` (
                `songId` TEXT NOT NULL, 
                `albumId` TEXT NOT NULL, 
                `position` INTEGER, 
                PRIMARY KEY(`songId`, `albumId`), 
                FOREIGN KEY(`songId`) REFERENCES `Song`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE , 
                FOREIGN KEY(`albumId`) REFERENCES `Album`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE 
            );
        ''')

        cursor.execute('''
            CREATE INDEX `index_SongAlbumMap_songId` ON `SongAlbumMap` (`songId`);
        ''')

        cursor.execute('''
            CREATE INDEX `index_SongAlbumMap_albumId` ON `SongAlbumMap` (`albumId`);
        ''')

    def song_artist_map_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `SongArtistMap` (
                `songId` TEXT NOT NULL, 
                `artistId` TEXT NOT NULL, 
                PRIMARY KEY(`songId`, `artistId`), 
                FOREIGN KEY(`songId`) REFERENCES `Song`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE , 
                FOREIGN KEY(`artistId`) REFERENCES `Artist`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE 
            );
        ''')

        cursor.execute('''
            CREATE INDEX `index_SongArtistMap_songId` ON `SongArtistMap` (`songId`);
        ''')

        cursor.execute('''
            CREATE INDEX `index_SongArtistMap_artistId` ON `SongArtistMap` (`artistId`);
        ''')

    def song_playlist_map_table(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE `SongPlaylistMap` (
                `songId` TEXT NOT NULL, 
                `playlistId` INTEGER NOT NULL, 
                `position` INTEGER NOT NULL, 
                PRIMARY KEY(`songId`, `playlistId`), 
                FOREIGN KEY(`songId`) REFERENCES `Song`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE , 
                FOREIGN KEY(`playlistId`) REFERENCES `Playlist`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE 
            );
        ''')

        cursor.execute('''
            CREATE INDEX `index_SongPlaylistMap_songId` ON `SongPlaylistMap` (`songId`);
        ''')

        cursor.execute('''
            CREATE INDEX `index_SongPlaylistMap_playlistId` ON `SongPlaylistMap` (`playlistId`);
        ''')

    def execute(self, cursor: sqlite3.Cursor) -> None:

        for method_name in dir(self):
            if 'execute' == method_name:
                continue

            method = getattr(self, method_name)

            if not callable(method):
                continue

            try:
                method(cursor)
            except TypeError :
                pass


def main(database_path: str = 'RiMusic.db') -> None:
    connection = sqlite3.Connection(database_path)
    cursor: sqlite3.Cursor = connection.cursor()

    datbase: Database = Database()
    datbase.execute(cursor)

    connection.commit()
    connection.close()