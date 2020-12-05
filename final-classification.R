#This piece of source code is part of FADCIL project from Visibilia
#More details about this project at: https://visibilia.net.br/fadcil
#Last updated: 10/08/2020



# Packages
library(h2o)
library(dplyr)
library(tidyverse)

# Import Data containing our meta-features
# we assume the data-to-train.csv file contains a set of features obtaines from ct-scans previously
# processed by our deep nets
base<-read.csv2("~/data-to-train.csv",sep=",")[,-1]
head(base)
base$label=as.factor(base$label)


###################################################################################################
##
# First, we will look for the best model which learn our meta-features

# START H2O CLUSTER ----
h2o.init()

# The training set (convert to an H2OFrame)
DB <- as.h2o(data.to.analyze3)

# Take a look at the training set
h2o.describe(DB)

# Spliting Data Set
split_h2o <- h2o.splitFrame(DB, c(0.8), seed = 1234)

train_set <- h2o.assign(split_h2o[[1]], "train" ) # 80%
test_set  <- h2o.assign(split_h2o[[2]], "test" )  # 20%

# Identify the predictor columns (remove response and ID column)
x <- setdiff(names(train_set), c("label"))

# H2O AutoML Training ----
# Execute an AutoML run for 100 models
aml <- h2o.automl(
  y = "label", 
  x = x, 
  training_frame = train_set,
  nfolds = 10,
  max_models = 100,
  seed = 1234)

aml@leaderboard

# Get leaderboard with 'extra_columns = 'ALL'
lb2 <- h2o.get_leaderboard(object = aml, extra_columns = 'ALL')
lb2

# Predict on hold-out test set
pred_conversion <- h2o.predict(object = aml, newdata = test_set)
#Confusion matrix on test data set
h2o.table(pred_conversion$predict, test_set$label)

# Get model ids for all models in the AutoML Leaderboard
model_ids <- as.data.frame(aml@leaderboard$model_id)[,1]
# Get the "All Models" Stacked Ensemble model
fit1 <- h2o.getModel(grep("XGBoost_grid__1_AutoML_20200807_191312_model_1", model_ids, value = TRUE)[1])

#compute performance
perf <- h2o.performance(fit1, test_set$label)
h2o.confusionMatrix(perf)
# h2o.accuracy(perf)
# h2o.tpr(perf)

h2o.varimp_plot(fit1)

#############################################################################
##
#Second, we save the adjusted model for it to be used at any time

model_path <- h2o.saveModel(object = fit1, path = getwd(), force = TRUE)
print(model_path)

# loadong saved model
saved_model <- h2o.loadModel(model_path)

# download the model built above to your local machine
my_local_model <- h2o.download_model(saved_model)



#############################################################################
##
# Third, using the adjusted model to classify the final test dataset

# upload the model that you just downloaded above to the H2O cluster
uploaded_model <- h2o.upload_model(my_local_model)


# Load the model from the validation file
new_observations <- h2o.importFile(path = '/data-to-analyze-fase3.csv',skipped_columns=c(1))
predictions  <- h2o.predict(object = fit1, DB)

h2o.exportFile(
  data=predictions[,c(1,3)],
  path="/classificacao-best-model-results.csv",
  force = FALSE,
  sep = ";",
  compression = NULL,
  parts = 1)

#h2o.shutdown()