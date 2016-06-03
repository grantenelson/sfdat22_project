import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score

# Load final data frame
with open('/Users/grantnelson/desktop/data_science/sfdat22_project/final_df.txt','rb') as f:
	final_df = pickle.load(f)

y = final_df['author']
X = final_df.iloc[:,4:31]

# # Find best parameters for n_estimators and max_features
# accuracy_scores = []
# for feature in range(1, len(X.columns) +1):
# 	rf = RandomForestClassifier(n_estimators = 150, max_features = feature, random_state = 222)
# 	scores = cross_val_score(rf, X, y, cv = 10, scoring = 'accuracy')
# 	accuracy_scores.append(scores.mean())

# print accuracy_scores

# accuracy_scores = []
# for estimators in range(150,300,10):
# 	rf = RandomForestClassifier(n_estimators = estimators, max_features = 6, random_state = 222)
# 	scores = cross_val_score(rf, X, y, cv = 10, scoring = 'accuracy')
# 	accuracy_scores.append(scores.mean())

# print accuracy_scores

# Fit a tree with best parameters
rf = RandomForestClassifier(n_estimators = 150, max_features = 6, oob_score = True, random_state = 222)
rf.fit(X, y)

print 'OOB score:', rf.oob_score_
print 0.92481203007518797

print pd.DataFrame({'feature':X.columns, 'importance':rf.feature_importances_}).sort('importance', ascending = False)

X_important = rf.transform(X, threshold = 'mean')
rf = RandomForestClassifier(n_estimators = 150, max_features = 6, oob_score = True, random_state = 222)
scores = cross_val_score(rf, X_important, y, cv = 10, scoring = 'accuracy')

print 'Accuracy: ', scores.mean()
print 0.88489842219895998
