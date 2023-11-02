library(GEOquery)
# ���߶�ȡGEO����
dd <- getGEO('GSE20236', destdir = './', AnnotGPL=F, getGPL = F)
# ��ȡBetaֵ(��ʹ��GEO���صĻ���оƬ���м׻�������ʱ)
beta <- exprs(dd[[1]])
#��ȡ�ٴ�����
pheno <- pData(dd[[1]])



#��ȡ����GEO����
setwd('E:/cecilia/���ݼ�')
dd <- getGEO("GSE53740", filename="GSE53740_series_matrix.txt.gz", destdir = '', AnnotGPL=F, getGPL = F)

# ��ȡBetaֵ(��ʹ��GEO���صĻ���оƬ���м׻�������ʱ)
beta <- exprs(dd)
#��ȡ�ٴ�����
pheno <- pData(dd)
#pheno$`age:ch1` = as.numeric(sub(" years", '', pheno$`age:ch1`))
pheno$`age (y):ch1` = as.numeric(pheno$`age (y):ch1`)
path = "C:/Users/DELL/OneDrive/������_crr_personal/��24ƪԴ����/CorticalClock-master/PredCorticalAge/"
setwd(path)
source('CorticalClock.R')
starttime <- proc.time()
CorticalClock(beta,pheno,'C:/Users/DELL/OneDrive/������_crr_personal/��24ƪԴ����/CorticalClock-master/PredCorticalAge/','geo_accession','age (y):ch1')
runningtime <- proc.time()-starttime
print(runningtime)



####�ٴ�������������ֿ�
dd <- getGEO('GSE72775', destdir = './', AnnotGPL=F, getGPL = F)
#��ȡ�ٴ�����
pheno <- pData(dd[[1]])
pheno$`age:ch1` = as.numeric(pheno$`age:ch1`)
###��ȡ�������####
library(csv)
#���ص���csv�ļ�
data <- "E:/cecilia/���ݼ�/GSE72775_datBetaNormalized.csv"
beta <- read.csv(data,row.names=1)
colnames(beta) <- pheno$geo_accession
path = "C:/Users/DELL/OneDrive/������_crr_personal/��24ƪԴ����/CorticalClock-master/PredCorticalAge/"
setwd(path)
source('CorticalClock.R')
starttime <- proc.time()
CorticalClock(beta,pheno,'C:/Users/DELL/OneDrive/������_crr_personal/��24ƪԴ����/CorticalClock-master/PredCorticalAge/','geo_accession','age:ch1')
runningtime <- proc.time()-starttime
print(runningtime)
