# read in the data
setwd("C:/Users/David/workspace/concerts/")
boData <- read.csv('data/BoxOfficeData.csv', stringsAsFactors=F)

# do some formatting / transforming
boData$Date <- as.POSIXlt(boData$Date, format='%m/%d/%Y')

# fix discrepancies in Sold Out / Total Shows
bNoTS <- boData$TotalShows == 0
bSoldOutRatio <- boData$SoldRatio == 1
boData[bNoTS, "TotalShows"] <- as.integer(1)
boData[bNoTS & bSoldOutRatio, "SoldOutShows"] <- as.integer(1)
boData[bNoTS & !bSoldOutRatio, "SoldOutShows"] <- as.integer(0)

bGreaterSoldOut <- boData$SoldOutShows > boData$TotalShows
boData[bGreaterSoldOut, "SoldOutShows"] <- 
	as.integer(boData[bGreaterSoldOut, "TotalShows"] * boData[bGreaterSoldOut, "SoldRatio"])

boData[boData$TotalShows > 100, "TotalShows"] <- as.numeric(1)

# remove entries with zero for SoldRatio
boData <- boData[-which(boData$SoldRatio == 0),]

# remove entries with SoldRatio greater than one, after adjusting capacity for number of shows
bSuperSORatio <- boData$SoldRatio > 1
boData$Capacity[bSuperSORatio] <- boData$Capacity[bSuperSORatio] * boData$TotalShows[bSuperSORatio]
boData$SoldRatio <- boData$Sold / boData$Capacity
boData <- boData[-which(boData$SoldRatio > 1),]

stateLabels24 <- labels(summary(as.factor(boData$State), maxsum=25))[2:24]
stateSub <- boData[boData$State %in% stateLabels24,]
stateSub$State <- as.factor(stateSub$State)

headlinerLabels1000 <- labels(summary(as.factor(stateSub$Headliner), maxsum=1001))[1:1000]
stateHeadSub <- stateSub[stateSub$Headliner %in% headlinerLabels1000,]
stateHeadSub$Headliner <- as.factor(stateHeadSub$Headliner)
