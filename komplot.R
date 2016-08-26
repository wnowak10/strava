#load csv
test <- read.csv("~/Desktop/test.csv", header=FALSE)
#load ggplot lib
library(ggplot2)
# create variable names
effortTime=test$V1
dateOfEffort=test$V2
#change dates from factor to character
dateOfEffort=as.character(dateOfEffort)
str(dateOfEffort)
#convert from character to R date object
dateOfEffort=as.Date(dateOfEffort,"%m/%d/%y")
# make plot using ggplot geom_line
ggplot(test, aes(dateOfEffort,effortTime))+geom_line(color='orange')+geom_point(color='dark orange')+ggtitle("Whirlwind Koms over Time")+
  labs(x="Date",y="Segment time")
