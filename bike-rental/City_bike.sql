drop database if exists city_bike;
CREATE database city_bike;
SET search_path TO city_bike;

DROP TABLE if exists bike_stations cascade ;
CREATE TABLE bike_Stations( 
ID bigint primary key,
Name varchar(50),
Longitude float,
Latitude float
);


DROP table if exists trips;
CREATE TABLE Trips (
ID bigserial PRIMARY KEY,
Duration INTERVAL,
Start_time timestamp,
End_time timestamp,
Start_Stn_id bigint REFERENCES bike_stations(ID),
End_Stn_id bigint REFERENCES bike_stations(ID),
Bike_id bigint,
User_type varchar(25),
Birth_year int,
Gender char(1)
);

DROP table if exists weather_station;
CREATE TABLE weather_station (
ID varchar(25) PRIMARY key,
names varchar(50) UNIQUE,
state char(2)
);

DROP table if exists weather_repts ;
CREATE TABLE weather_repts (
id bigserial primary key,
w_station varchar(25) REFERENCES weather_station(ID),
rep_date date,
avg_wind_spd float,
precipitation float,
snow float,
snow_depth float,
temp_avg int,
temp_max int,
temp_min int
);

------------------------------------ Views
create or replace  view vwbikes as (
select t.*, 
ss.name as start_name, ss.longitude as start_long, ss.latitude as start_lat,
es.name as end_name, es.longitude as end_long, es.latitude as end_lat,
wr.avg_wind_spd, wr.precipitation, wr.snow, wr.snow_depth, wr.temp_avg, wr.temp_max, wr.temp_min
from trips t 
join bike_stations ss on t.start_stn_id = ss.id
join bike_stations es on t.end_stn_id =es.id
join weather_repts wr on wr.rep_date = cast(t.start_time as date)
);

create or replace view vwdaily_biking as (
select cast(t.start_time as date) as day,
count(*)
from trips t
group by 1);

create or replace view vwstation_popularity as (

with starts as (
select start_stn_id, count(*) as s_cnt
from trips t1 
group by 1),
ends as (
select end_stn_id, count(*) as e_cnt
from trips t2
group by 1)
select bs.name, bs.longitude , bs.latitude,  
case when s.s_cnt is null then 0 else s.s_cnt end,
case when e.e_cnt is null then 0 else e.e_cnt end
from bike_stations bs 
left join starts as s on s.start_stn_id= bs.id
left join ends as e on e.end_stn_id = bs.id
order by 4 desc, 5 desc);


----------------------------Clustering
cluster bike_stations using bike_stations_pkey;
cluster trips using trips_pkey;
cluster weather_repts using weather_repts_pkey;
cluster weather_station using weather_station_pkey;
