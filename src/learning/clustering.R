library(cluster)

# Chargement et épuration des données.
seal <- read.csv('constant.csv',sep='$',header=FALSE)
mydata <- seal[,2:length(seal)]
g <- length(mydata[,1])
mydata <- mydata[1:g-1,]




nbre_cluster <- 15
# Normalisation des données
for(i in 1:length(mydata))
    mydata[,i]=mydata[,i]/max(mydata[,i])
 mydata[,1]=mydata[,1]^(1/17)


#Clustering classique avec les k-means.
KMEANS <- kmeans(mydata, nbre_cluster)


plot(mydata[,1:2], col = KMEANS$cluster)
points(KMEANS$centers, col = 1:nbre_cluster, pch = 8)



mydata <-mydata[1:200,]
# Hierarchical clustering
#mydist <- dist(mydata)
#HCLUST <- hclust(mydist)
#plot(HCLUST)

# Agglomerative Nesting

#AGNES <- agnes(mydata, diss = FALSE, metric = "euclidean",stand = FALSE)

#print(AGNES)

# Dissimilarity Matrix

#DAISY<-daisy(mydata, metric = c("euclidean", "manhattan", "gower"),stand = FALSE, type = list())

# Divisive analysis clustering
#DIANA<-diana(mydata, diss=FALSE, metric = "euclidean", stand = FALSE)

# Fuzzy Analysis clustering

FANNY <- fanny(mydata, nbre_cluster, diss=FALSE, memb.exp = 1.2,metric = c("euclidean", "manhattan", "SqEuclidean"),stand = FALSE, iniMem.p = NULL, cluster.only = FALSE)

# Partionning around Medoids

PAM <-pam(mydata, nbre_cluster, FALSE, metric = "euclidean",medoids = NULL, stand = FALSE, cluster.only = FALSE)


