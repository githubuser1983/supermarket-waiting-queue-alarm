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
  q <- opq(bbox = bb, timeout=30) %>%
        add_osm_feature(key = 'shop', value = 'supermarket') %>%
        add_osm_feature(key = 'addr:postcode', value = as.character(subset_plz$zipcode[i]))
  dat = osmdata_sf(q)
  dat2 = dat$osm_points
  dat2 = dat2[! is.na(dat2$addr.street),]
  dat2 = dat2[! is.na(dat2$addr.housenumber),]
  dat3 = dat$polygones
  dat3[! is.na(dat3$addr.street),]
  dat3[! is.na(dat3$addr.housenumber),]
  dat_filt = cbind(dat2$addr.postcode,dat2$name,dat2$addr.street,dat2$addr.housenumber, dat2$geometry,dat2$osm_id)
  write.csv2(dat_filt,append=T,col.names=F,row.names=F,file="test2.csv",na="NA")
  dat_filt = cbind(dat3$addr.postcode,dat3$name,dat3$addr.street,dat3$addr.housenumber, dat3$geometry,dat3$osm_id)
  write.csv2(dat_filt,append=T,col.names=F,row.names=F,file="test2.csv",na="NA")
}
