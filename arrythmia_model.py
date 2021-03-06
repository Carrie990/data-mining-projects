# 1. define problem
# arrythmia data is downloaded from UCI, and has a size of 452 * 280, 279 features and 1 lable. for the label, 1 represents normal, and 2-16 represent others.
# purpose: we name class 1 as positive and class 2-16 as negative, aiming to create a model which can classify the samples accurately。

import pandas as pd
import numpy as np

# 2. data cleaning
# load data
arrythmia=pd.read_csv('/Users/carrie/data/arrythmia.csv', sep=',',header=None) # 452*280
## 2-1. filling missing data
### print some rows to check abnormal data and replace them, such as "?","","NaN"
print(arrythmia.iloc[0:3])
arrythmia = arrythmia.replace('?', np.NaN) 
### data format 
arrythmia.dtypes
arrythmia = arrythmia.convert_objects(convert_numeric=True) # convert object to numeric
### use mean to fill missing value
arrythmia = arrythmia.fillna(arrythmia.mean())
# test code: print(arrythmia.iloc[0])

## 2-2. filter abnormal 
### according to the description, check the distrbution of some row, such as height
import matplotlib.pyplot as plt
height = arrythmia[2]
plt.figure()
height.plot()
plt.show()

### from the figure, we see some people's height is over 250cm, use height_mean to fill the abnormal data
h_mean = height.mean()
# test code: print(h_mean)
for i in range(0,len(height)):
    if height[i] > 250:
        height[i] = h_mean
height.plot()
plt.show()

## 2-3. split data into features and label
arrythmia_feature = arrythmia.values[:, :arrythmia.shape[1]-1]
arrythmia_label = arrythmia.values[:, arrythmia.shape[1]-1]

# test code: print(arrythmia_feature.shape)
# test code: print(arrythmia_label.shape)

for i in range(len(arrythmia_label)):
    if arrythmia_label[i] > 1:
        arrythmia_label[i] = 0
# print(arrythmia_label)

# 3.dimension reduction (as we can see, arrythmia is a small sample with high dimensions, with is hard to make predict model)
## 3-1. Unsupervised dimensionality reduction  
### use PCA to reduce dimension
from sklearn.decomposition import PCA
pca = PCA(n_components=60)
arrythmia_train_reduced = pca.fit_transform(arrythmia_feature)
print(arrythmia_train_reduced.shape)

# 4. build prediction model
# split data into train_data and test_data,select 80% of data as training data
arrythmia_train_feature,arrythmia_test_feature,arrythmia_train_label,arrythmia_test_label = train_test_split(arrythmia_train_reduced,arrythmia_label,test_size=0.2)

## 4-1. use LogisticRegression
from sklearn import linear_model
reg = linear_model.LogisticRegression(C=0.01)
reg.fit(arrythmia_train_feature, arrythmia_train_label)
# predicting
reg.predict(arrythmia_test_feature)

# 5. model evaluation
## accuracy
reg.score(arrythmia_test_feature, arrythmia_test_label)
## precision
from sklearn.metrics import average_precision_score
average_precision = average_precision_score(arrythmia_test_label, arrythmia_predict_label)
## recall
from sklearn.metrics import recall_score
recall_score(arrythmia_test_label, arrythmia_predict_label) 
## f1 score/F-measure
from sklearn.metrics import f1_score
f1_score(arrythmia_test_label, arrythmia_predict_label)
## G-mean/G-measure

## ROC curve
from sklearn import metrics
print(arrythmia_test_label)
print(arrythmia_predict_label)
fpr, tpr, thresholds = metrics.roc_curve(arrythmia_test_label, arrythmia_predict_label, pos_label=1)
plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
