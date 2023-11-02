
import rpy2.robjects as robjects
f = open('/home/liyunkai/code/data/beta/GSE20242_beta.csv', 'r')
answer = f.readline()
print(answer)
robjects.r.source('/home/liyunkai/code/R/01/Horvath.R')
# run R test function
RTestFunction = robjects.r.Horvath('D:/backend/data/beta/GSE20242_beta.csv', 0.5)

