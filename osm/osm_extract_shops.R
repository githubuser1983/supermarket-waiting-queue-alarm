require(osmdata)
require(sf)
require(tidyverse)
require(ggmap)

plz = read.csv2("/Users/jade/Downloads/ww-german-postal-codes.csv")
subset_plz  = head(plz, n=5250)

bb = c(3.955,45.368,15.337,55.268)


#one query per zipcode
header = c("osm_id","name","postcode","street","housenumber","geometry")
write.table(header,col.names=F,row.names=F,file="test2.csv")
for (i in 1:nrow(subset_plz)){
  print(i)
  q <- opq(bbox = bb) %>%
        add_osm_feature(key = 'shop', value = 'supermarket') %>%
        add_osm_feature(key = 'addr:postcode', value = as.character(subset_plz$zipcode[i]))
  dat = osmdata_sf(q)
  dat2 = dat$osm_points
  dat3 = dat$polygones
  dat_filt = cbind(dat2$addr.postcode,dat2$name,dat2$addr.street,dat2$addr.housenumber, dat2$geometry,dat2$osm_id)
  write.table(dat_filt,append=T,col.names=F,row.names=F,file="test2.csv",sep=";")
  dat_filt = cbind(dat3$addr.postcode,dat3$name,dat3$addr.street,dat3$addr.housenumber, dat3$geometry,dat3$osm_id)
  write.table(dat_filt,append=T,col.names=F,row.names=F,file="test2.csv",sep=";")
}

#clean data in cmdline, osm data has many duplicates and uncomplete entries
#grep '^[0-9]' test2.csv  | cut -f 1,2,3,4 -d ";" | sort | uniq
