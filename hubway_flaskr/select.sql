select stations.name,"dock-" || docks.id as dock, "bike-" || bikes.id as bike
   from stations, docks, bikes   where docks.station = stations.name   and bikes.dock = docks.id   order by stations.name, dock;

select
    stations.name
    ,docks.id as dock
    ,bikes.id as bike
from
    stations
    ,docks
    ,bikes
where
    docks.station = stations.name
and
    bikes.dock = docks.id
order by
    stations.name,
    docks.station
;
----select 
----    t1.name,
----    "dock-" || t2.id as dock,
----    t2.station,
----    "bike-" || t3.id as bike----,
----    ----"dock-" || t3.dock as "in dock",
----    ----t3.sponsor
----from
----    stations t1,
----    docks t2,
----    bikes t3
----where
----    t2.station = t1.name
--------and
----    ----t3.dock = t2.id
--------group by
----    ----t1.name,
----    ----t2.id,
----    ----t3.id
----order by
----    t1.name,
----    t2.id,
----    t3.id
----;
----    
