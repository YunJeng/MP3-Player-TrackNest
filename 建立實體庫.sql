-- Create Member Table
CREATE TABLE Member (
    MemberID INTEGER PRIMARY KEY auto_increment,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL,
    JoinDate DATE NOT NULL,
    Password TEXT NOT NULL,
    MemberType TEXT NOT NULL
);

-- Create Category Table
CREATE TABLE Category (
    CategoryID INTEGER PRIMARY KEY auto_increment,
    CategoryName TEXT NOT NULL
);

CREATE TABLE Artist (
    ArtistID INTEGER PRIMARY KEY auto_increment,
    ArtistName TEXT NOT NULL
);

CREATE TABLE Composer (
    ComposerID INTEGER PRIMARY KEY auto_increment,
    ComposerName TEXT NOT NULL
);

CREATE TABLE Album (
    AlbumID INTEGER PRIMARY KEY auto_increment,
    AlbumName TEXT NOT NULL
);

-- Create Song Table
CREATE TABLE Song (
    SongID INTEGER PRIMARY KEY auto_increment,
    Title TEXT,
    Duration TEXT,
    ReleaseDate DATE,
  	OurCode TEXT NOT NULL,
    ArtistID INTEGER,
    AlbumID INTEGER,
    CategoryID INTEGER,
    ComposerID INTEGER,
    FilePath char(255),
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID),
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (ComposerID) REFERENCES Composer(ComposerID)
);

-- Create Billboard Table
CREATE TABLE Billboard (
    BillboardID INTEGER PRIMARY KEY auto_increment,
    SongID INTEGER NOT NULL,
    Playtimes INTEGER NOT NULL,
    FOREIGN KEY (SongID) REFERENCES Song(SongID)
);

-- 	歌曲清單（不是播放清單）
CREATE TABLE PlayListSongs (
	PlayListSongsID INTEGER auto_increment,
    SongID INTEGER NOT NULL,
    MemberID INTEGER,
    PRIMARY KEY (PlayListSongsID),
    FOREIGN KEY (SongID) REFERENCES Song(SongID),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
);


-- select * from Album;
-- alter table Member modify column MemberType TEXT;
-- alter table Billboard modify column Playtimes INTEGER;
-- select * from song;
-- create database MP3;
use mp3;
-- drop database mp3;
-- update song set filepath='/Users/zhen/Desktop/VS studio/DatabaseManagement/music/a.mp3' where songid=1;
-- update song set filepath='/Users/zhen/Desktop/VS studio/DatabaseManagement/music/b.mp3' where songid=2;
