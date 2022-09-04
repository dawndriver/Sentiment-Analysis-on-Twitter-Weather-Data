gc();
#setwd('~/Desktop/CS5344/src/R_src') # remember to change to your own path
setwd('~/Documents/workspace/Hadoop-Project/src/R_src'); #Tam's working directory

library(car)
library(plyr)
library(dplyr)
library(ggplot2)
library(lattice)
library(caret)
source('twoplot.R')

# define countries
country <- c("Canada")
# valid weather_type: "temp", "rain", "humid", "wind"
weather_type <- "temp"
# valid emo_weather: temp", "rain"
# empty string "" means treat all emo_weathers
emo_weather <- ""

##########################################################
# Reading weather data file
##########################################################
weather<-read.csv('weather_avg_new.csv',na.strings='NULL',stringsAsFactors=FALSE,header=TRUE);
weather$time <- as.Date(weather$time, "%d-%m-%Y")
#summary(weather)
#head(weather)
# weather[weather$location == "Canada",]
# test<-weather %>%
#   group_by(location) %>%
#   summarize(count = n());
# 
# test[(test$count!=12 & test$count!=13) & test$count < 3,];

# Assign missing value for temp as mean value
weather<-weather %>%
  group_by(location) %>%
  mutate(temp=ifelse(is.na(temp),mean(temp,na.rm=TRUE),temp));

# Assign missing value for wind as min value
weather<-weather%>%
  group_by(location)%>%
  mutate(wind=ifelse(is.na(wind),min(wind,na.rm=TRUE),wind));

# Assign missing value for rain as min value
weather<-weather%>%
  group_by(location)%>%
  mutate(rain=ifelse(is.na(rain),min(rain,na.rm=TRUE),rain));

# Assign missing value for humid as min value
weather<-weather%>%
  group_by(location)%>%
  mutate(humid=ifelse(is.na(humid),min(humid,na.rm=TRUE),humid));

# If there is still NA value, means that only one entry for that location and time
# So ignore that entry
weather<-weather[!is.na(weather$temp) & !is.na(weather$wind) & !is.na(weather$rain) & !is.na(weather$humid),]
# Detect outlier based on 2 standard deviation
weather<-weather %>%
  group_by(location) %>%
  mutate(rain=ifelse(rain > 600, 1.47, rain));

##########################################################
# Reading emotion data file
##########################################################
emo<-read.csv('emotion_new.csv', na.strings = 'NULL', stringsAsFactors=FALSE)
#summary(emo)
#show(emo)
emo$time <- as.Date(emo$time, "%d-%m-%Y")
emo$value[emo$emotion=="positive"] <- as.numeric(1)
emo$value[emo$emotion=="negative"] <- as.numeric(-1)
emo$value[emo$emotion=="neutral"] <- 0

#######################################
# Take the sum of emo, filtered by location and grouped by location and time
#######################################
weather <- weather %>%
  filter(location %in% country) %>%
  group_by(time) %>%
  summarize(temp=mean(temp),wind=mean(wind),rain=mean(rain),humid=mean(humid));

weather <- weather[c("time",weather_type)]
colnames(weather) <- c("time", "total")

if (emo_weather=="") {
  emo <- emo %>%
    filter(location %in% country) %>%
    group_by(time) %>%
    summarize(total=sum(value));
} else {
  emo <- emo %>%
    filter(location %in% country) %>%
    group_by(time,cat) %>%
    summarize(total=sum(value));
    emo <- emo[emo$cat==emo_weather,]
}

########################################
## Plot
########################################
twoplot(weather, emo, c(weather_type), country);
