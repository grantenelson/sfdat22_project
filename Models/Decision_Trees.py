import pickle
import pandas as pd
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.tree import DecisionTreeClassifier
from nltk import ConfusionMatrix
from sklearn import metrics

# Load final data frame
with open('/Users/grantnelson/desktop/data_science/sfdat22_project/final_df.txt','rb') as f:
	final_df = pickle.load(f)


# Create dummy variables of author column in order to predict probability of
# each author separately
y = pd.get_dummies(final_df['author'])
X = final_df.iloc[:,4:31]

# Instantiate dataframe to hold predicted probabilities for each text block
predicted_probs = pd.DataFrame()

# Define folds for cross-validation
kf = KFold(len(final_df), n_folds = 10, shuffle = True, random_state = 222)

# Loop through folds
for train_index, test_index in kf:
	X_train, X_test = X.iloc[train_index], X.iloc[test_index]
	# Define train/test split on entire df of response dummies, but train and
	# predict on each author separately
	y_train, y_test = y.iloc[train_index], y.iloc[test_index]
	for author in y:
		dtree = DecisionTreeClassifier(max_depth = 8, random_state = 222)
		dtree.fit(X_train, y_train[author])
		# Take probability of author = 1 for each obs in test set and attach to Y_test
		pos_preds = [i[1] for i in dtree.predict_proba(X_test)]
		col_name = author + '_prob'
		# Append predictions for that author to y_test to retain original index
		y_test[col_name] = pos_preds
	# Append predicted probabilities for each author to common dataframe
	probs = y_test[['Faulkner_prob','Hemingway_prob','Fitzgerald_prob','Steinbeck_prob']]
	predicted_probs = predicted_probs.append(probs)

# Assign prediction to highest probability author for each block
predicted_probs['prediction'] = predicted_probs.idxmax(axis = 1)
predicted_probs['prediction'] = predicted_probs.prediction.map(lambda x: x[:-5])

# Create df of dimensions from final_df (author, work, block)
dimensions = final_df[['author','work','block','text']]

# Merge predicted probabilities into dimensions
prediction_df = dimensions.merge(predicted_probs, how = 'left', left_index = True, right_index = True)

### METRICS

print 'Overall accuracy: ', metrics.accuracy_score(prediction_df['author'], prediction_df['prediction'])
print '\n'

# Make confusion matrix and calculate sensitivity/specificity for each author
performance_data = {}
for author in ['Faulkner','Fitzgerald','Hemingway','Steinbeck']:
	actual = np.where(prediction_df['author'] == author, 1, 0)
	pred = np.where(prediction_df['prediction'] == author, 1, 0)
	prob = prediction_df[author + '_prob']
	performance_data[author] = (actual, pred, prob)

for key, value in performance_data.iteritems():
		conf_mat = metrics.confusion_matrix(value[0],value[1])
		true_neg = conf_mat[0,0]
		false_pos = conf_mat[0,1]
		false_neg = conf_mat[1,0]
		true_pos = conf_mat[1,1]
		print key + ':'
		print conf_mat
		print 'Accuracy: ', metrics.accuracy_score(value[0],value[1])
		print 'Sensitivity: ', true_pos / float(true_pos + false_neg)
		print 'Specificity: ', true_neg / float(true_neg + false_pos)
		print 'ROC/AUC Score:', metrics.roc_auc_score(value[0],value[2])
		print '\n'
		print prediction_df[prediction_df['author'] == key][['Faulkner_prob','Fitzgerald_prob','Hemingway_prob','Steinbeck_prob']].mean()
		print '\n'
		dtree = DecisionTreeClassifier(max_depth = 8, random_state = 222)
		dtree.fit(X, y[key])
		print pd.DataFrame({'feature':X.columns, 'importance':dtree.feature_importances_}).sort('importance', ascending = False).head()






