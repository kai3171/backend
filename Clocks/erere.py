
import rpy2.robjects as robjects

robjects.r.source('../R/01/Horvath.R')
# run R test function
RTestFunction = robjects.r.Horvath('../data/beta/GSE20242_beta.csv', 0.5)
