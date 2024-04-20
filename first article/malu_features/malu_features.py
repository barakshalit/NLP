import pandas as pd
import re
import glob
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import seaborn as sns



# Get a list of all CSV files. the csv fiels contains the features extracted by malu. 
file_paths_old = glob.glob('old/*.csv')
file_paths_new = glob.glob('new/*.csv')

# Initialize old
dataframes_old = []
names_list_old = []
author_list_old = []

# Initialize new
dataframes_new = []
names_list_new = []
author_list_new = []

# Iterate through each file path, read the CSV file, and append the DataFrame to the list
for file_path in file_paths_old:
    dataframes_old.append(pd.read_csv(file_path))
    
for file_path in file_paths_new:
    dataframes_new.append(pd.read_csv(file_path))

# Extract the author and title from the file path - old
for file_path in file_paths_old:
    parts = file_path.split("-")
    author = parts[0]
    author = author[4:]
    author_list_old.append(author)
    name = parts[1]
    name = name[:-4]
    names_list_old.append(name)

# Extract the author and title from the file path - new
for file_path in file_paths_new:
    parts = file_path.split("-")
    author = parts[0]
    author = author[4:]
    author_list_new.append(author)
    name = parts[1]
    name = name[:-4]
    names_list_new.append(name)


big_list_old = []
big_list_new = []  

old_data = dataframes_old[0].iloc[2].name
new_data = dataframes_new[0].iloc[2].name   
 

# Extract the values from the DataFrame - old
for i in range(len(dataframes_old)):
    old_data = dataframes_old[i]
      
    value_list = []
    len_values = len(old_data.iloc[2].name) - 1
    #print(len_values)
    for j in range(len_values):
        value_str = old_data.iloc[2].name[j+1]
        value_list.append(float(value_str))
    big_list_old.append(value_list)

# Extract the values from the DataFrame - new
for i in range(len(dataframes_new)):
    new_data = dataframes_new[i]
      
    value_list = []
    len_values = len(new_data.iloc[2].name) - 1
    #print(len_values)
    for j in range(len_values):
        value_str = new_data.iloc[2].name[j+1]
        value_list.append(float(value_str))
    big_list_new.append(value_list)

col_name_old = []
col_name_new = []

# Extract the column names from the DataFrame - old
len_names = len(dataframes_old[0].iloc[0].name) -1
for t in range(len_names):
        name = dataframes_old[0].iloc[0].name[t+1]
        col_name_old.append(name)

# Extract the column names from the DataFrame - new
len_names = len(dataframes_new[0].iloc[0].name) -1
for t in range(len_names):
        name = dataframes_new[0].iloc[0].name[t+1]
        col_name_new.append(name)

# Create a DataFrame - old
df_old = pd.DataFrame(big_list_old,columns = col_name_old)
df_old.insert(0, 'Author', author_list_old)
df_old.insert(1, 'Title', names_list_old)


# Create a DataFrame - new
df_new = pd.DataFrame(big_list_new,columns = col_name_new)
df_new.insert(0, 'Author', author_list_new)
df_new.insert(1, 'Title', names_list_new)

# append label - old
sum_rows_old = len(df_old)
value_old = []
for i in range (sum_rows_old): 
    value_old.append(-1)
df_old['label'] = value_old

# append label - new
sum_rows_new = len(df_new)
value_new = []
for i in range (sum_rows_new): 
    value_new.append(1)
df_new['label'] = value_new

# Prepare data
# removing the first two cols - Author and Title
old_data = df_old.iloc[:, 2:]
new_data = df_new.iloc[:, 2:]

#last col has the label 
X_old = old_data.iloc[:, :-1]
y_old = old_data.iloc[:, -1]

X_new = new_data.iloc[:, :-1]
y_new = new_data.iloc[:, -1]


# Combine data
X = pd.concat([X_old, X_new])
y = pd.concat([y_old, y_new])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train logistic regression model
model_LogisticRegression = LogisticRegression(max_iter=1000)
model_LogisticRegression.fit(X_train, y_train)

model_svm_liblinear = LinearSVC()
model_svm_liblinear.fit(X_train, y_train)

model_svm_libsvm = SVC()
model_svm_libsvm.fit(X_train, y_train)

# Make predictions
y_pred_LogisticRegression = model_LogisticRegression.predict(X_test)
y_pred_svm_liblinear = model_svm_liblinear.predict(X_test)
y_pred_svm_libsvm = model_svm_libsvm.predict(X_test)


# Evaluate model LogisticRegression
accuracy = accuracy_score(y_test, y_pred_LogisticRegression)
precision = precision_score(y_test, y_pred_LogisticRegression)
recall = recall_score(y_test, y_pred_LogisticRegression)
f1 = f1_score(y_test, y_pred_LogisticRegression)
conf_matrix = confusion_matrix(y_test, y_pred_LogisticRegression)

print("LogisticRegression model:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
print("Confusion Matrix:")
print(conf_matrix,"\n")


# Evaluate model svm_liblinear
accuracy = accuracy_score(y_test, y_pred_svm_liblinear)
precision = precision_score(y_test, y_pred_svm_liblinear)
recall = recall_score(y_test, y_pred_svm_liblinear)
f1 = f1_score(y_test, y_pred_svm_liblinear)
conf_matrix = confusion_matrix(y_test, y_pred_svm_liblinear)

print("svm_liblinear model:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
print("Confusion Matrix:")
print(conf_matrix,"\n")


# Evaluate model svm_libsvm
accuracy = accuracy_score(y_test, y_pred_svm_libsvm)
precision = precision_score(y_test, y_pred_svm_libsvm)
recall = recall_score(y_test, y_pred_svm_libsvm)
f1 = f1_score(y_test, y_pred_svm_libsvm)
conf_matrix = confusion_matrix(y_test, y_pred_svm_libsvm)

print("svm_libsvm model:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
print("Confusion Matrix:")
print(conf_matrix,"\n")



# prediction check
file_paths_check = glob.glob('prediction_check/*.csv')

# Initialize check
dataframes_check = []
names_list_check = []
author_list_check = []


for file_path in file_paths_check:
    dataframes_check.append(pd.read_csv(file_path))
    

# Extract the author and title from the file path - check
for file_path in file_paths_check:
    parts = file_path.split("-")
    author = parts[0]
    author = author[17:]
    author_list_check.append(author)
    name = parts[1]
    name = name[:-4]
    names_list_check.append(name)


big_list_check = []
check_data = dataframes_check[0].iloc[2].name 
 

# Extract the values from the DataFrame - check
for i in range(len(dataframes_check)):
    check_data = dataframes_check[i]
      
    value_list = []
    len_values = len(check_data.iloc[2].name) - 1
    #print(len_values)
    for j in range(len_values):
        value_str = check_data.iloc[2].name[j+1]
        value_list.append(float(value_str))
    big_list_check.append(value_list)



col_name_check = []


# Extract the column names from the DataFrame - check
len_names = len(dataframes_check[0].iloc[0].name) -1
for t in range(len_names):
        name = dataframes_check[0].iloc[0].name[t+1]
        col_name_check.append(name)


# Create a DataFrame - check
df_check = pd.DataFrame(big_list_check,columns = col_name_check)
df_check.insert(0, 'Author', author_list_check)
df_check.insert(1, 'Title', names_list_check)


new_data = df_check
song_name = new_data["Title"]
author_name = new_data["Author"]
data_sum = len (song_name)


new_data = new_data.iloc[:, 2:]


new_data_predictions_LogisticRegression = model_LogisticRegression.predict(new_data)
new_data_predictions_liblinear = model_svm_liblinear.predict(new_data)
new_data_predictions_svm_libsvm = model_svm_libsvm.predict(new_data)

for i in range(data_sum):
    if new_data_predictions_LogisticRegression[i] == 1:
        print(f"The song: {song_name[i]} of the author: {author_name[i]} in LogisticRegression predicts a new song")
    else:
        print(f"The song: {song_name[i]} of the author: {author_name[i]} in LogisticRegression predicts a old song")

for i in range(data_sum):
    if new_data_predictions_liblinear[i] == 1:
        print(f"The song: {song_name[i]} of the author: {author_name[i]} in svm_Liblinear predicts a new song")
    else:
        print(f"The song: {song_name[i]} of the author: {author_name[i]} in svm_Liblinear predicts a old song")

for i in range(data_sum):
    if new_data_predictions_svm_libsvm[i] == 1:
        print(f"The song: {song_name[i]} of the author: {author_name[i]} in svm_libsvm predicts a new song")
    else:
         print(f"The song: {song_name[i]} of the author: {author_name[i]} in svm_libsvm predicts a old song")




# plotting the data of malu and comapre it to the article
data = {
    'Features type': ['phraseology', 'punctuation', 'lexical usage', 'combined',"""National Institute for
Testing & Evaluation"""],
    'LogisticRegression': [0.67,0.72,0.78,0.78,0.94],
    'svm_liblinear': [0.56,0.78,0.89,0.78,0.83],
    'svm libsvm':[0.94,0.78,0.73,0.94,0.88]  
}

df = pd.DataFrame(data)
df_melted = pd.melt(df, id_vars='Features type', var_name='Classifier', value_name='Value')

# Create the bar plot
plt.figure(figsize=(10, 8))
sns.barplot(x='Features type', y='Value', hue='Classifier', data=df_melted)

plt.show()




