
drop table if exists stations;
drop table if exists bikes;
drop table if exists docks;
drop table if exists trips;
drop table if exists rides;
drop table if exists plans;

create table stations(
    id integer primary key autoincrement,
    name text 
);
insert into stations values (1, "TraderJoes");
insert into stations values (2, "Harvard");
insert into stations values (3, "Central");
insert into stations values (4, "Kendall");

create table docks (
    id integer primary key autoincrement,
    station int not null,
    is_alive integer
);

--  three docks at TJ's
insert into docks values (NULL, 1, 1);
insert into docks values (NULL, 1, 1);
insert into docks values (NULL, 1, 1);

--  three docks at Harvard
insert into docks values (NULL, 2, 1);
insert into docks values (NULL, 2, 1);
insert into docks values (NULL, 2, 1);

--  three docks at Central
insert into docks values (NULL, 3, 1);
insert into docks values (NULL, 3, 1);
insert into docks values (NULL, 3, 1);

--  three docks at Kendall
insert into docks values (NULL, 4, 1);
insert into docks values (NULL, 4, 1);
insert into docks values (NULL, 4, 1);

create table bikes (
    id integer primary key autoincrement,
    dock integer NULL,
    sponsor text NULL,
    is_alive integer
);

--  one bike in transit
insert into bikes values (NULL, NULL,"wtorcaso", 1);

--  three bikes in the first three docs,
--  whatever station that happens to be
insert into bikes values (NULL, 1,"GnuBio", 1);
insert into bikes values (NULL, 2,"GnuBio", 1);
insert into bikes values (NULL, 3,"GnuBio", 1);

--  one bike at Harvard
insert into bikes values (NULL, 4, "HarvardUniversity", 1);

--  one bike at Central's
insert into bikes values (NULL, 7, "CityOfCambridge", 1);

--  one bike at Kendall
insert into bikes values (NULL, 10,"MIT", 1);

create table rides (
    id integer primary key autoincrement,
    event text,   --  departed, rejected, arrived
    bike_id integer,
    station_from integer,
    station_to integer,
    event_time datetime
);

create table plans (
    id integer primary key autoincrement,
    station_from text,
    station_to text
);

