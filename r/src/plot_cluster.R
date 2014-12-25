# load library
library('ggplot2')
library('dplyr')

# distance from imperial residence
get_distance = function(lon, lat) {
  lon_distance = abs(139.7521-lon)*91159.16112
  lat_distance = abs(35.6825-lat)*111263.283
  sqrt(lon_distance**2+lat_distance**2)/1000
}
# separate by comma and return developer listed first
main_developer = function(dev_list) {
  l = strsplit(as.character(dev_list), ',')
  v = c()
  for (i in 1:length(l)) {
    v = c(v, unlist(l[[i]])[1])
  }
  v
}

# load data
mantions = read.delim('../python/data/mansion_poem_tokyo.tsv',
                      header=F,
                      sep='\t')
clusters = read.delim('../python/out/words/label.txt',
                      header=F,
                      sep='\t')

# merge and create column
colnames(mantions) = c('no', 'name', 'lon', 'lat',
                       'min_price', 'max_price', 'price',
                       'min_space', 'max_space', 'developer',
                       'created', 'title', 'description')
colnames(clusters) = c('cluster_id')
data = cbind(mantions, clusters)
data$distance = get_distance(data$lon, data$lat)
data$developer = main_developer(data$developer)

# summarize
data %>% 
  group_by(cluster_id) %>% 
  summarize(n=n(),
            price.mean=mean(price),
            distance.mean=mean(distance))
data %>% 
  group_by(cluster_id, developer) %>% 
  summarize(n=n()) %>%
  filter(n>2)



# plot sample
p = ggplot(data, aes(distance, price))
p = p+geom_point(aes(colour=factor(cluster_id)), size=2)
p = p+theme_bw(base_family = "HiraKakuProN-W3")
p = p+theme(axis.text.x=element_text(size=5),
            axis.title.x=element_text(size=7),
            axis.text.y=element_text(size=5),
            axis.title.y=element_text(size=7),
            legend.text=element_text(size=5),
            legend.title=element_text(size=7))
p = p+labs(x='皇居からの距離 [km]',
           y='坪単価 [万円/坪]',
           colour='クラスタID')
plot(p)
ggsave(file="out/cluster_map.png",
       plot=p, dpi=300, width=4, height=3)
