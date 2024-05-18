# import numpy as np
from math import gamma
import pandas as pd

from imblearn.over_sampling import SMOTE
from collections import Counter

from sklearn.model_selection import train_test_split

# from tensorflow.keras.utils import to_categorical

from sklearn.svm import SVC

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
import seaborn as sns

import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

data = pd.read_excel("Project_Dataset/ECA_dataset.xlsx")
print(data.head(5))
print(data.columns)

print(data.isnull().sum())

data.drop(data.columns[[3, 4]], axis=1, inplace=True)
print(data.head(5))
print(data.columns)

data['Target Type'] = data['Target Type'].replace("Light Armour", 1)
data['Target Type'] = data['Target Type'].replace("Heavy Armour", 2)
data['Target Type'] = data['Target Type'].replace("Troops in Open Field", 3)
data['Target Type'] = data['Target Type'].replace("Troops in Bunkers", 4)
data['Target Type'] = data['Target Type'].replace("Parked Aircraft", 5)

data['Damage Level'] = data['Damage Level'].replace("Low", 0)
data['Damage Level'] = data['Damage Level'].replace("Moderate", 1)
data['Damage Level'] = data['Damage Level'].replace("Heavy", 2)

print(data.head(5))

data.to_excel("Project_Dataset/Preprocessed_ECA_dataset.xlsx", index=False)

# READ PREPROCESSED DATA
data = pd.read_excel("Project_Dataset/Preprocessed_ECA_dataset.xlsx")
print(data.head(5))

# Target_type = ['Light Armour', 'Heavy Armour',
#                'Troops- In Open', 'Troops- In Bunker', 'Parked Aircraft']

# DATASET VISUALIZATION
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x=data['Range(m)'], y=data['Target Type'])
plt.title("Visualization")
plt.xlabel("Range")
plt.ylabel("Target Type")
plt.show()


# DATA DIVISION (for train test split)
y = data['Damage Level']
x = data.drop(['Damage Level'], axis=1)

print(y)
print(x)

# TRAIN - TEST SPLITTING
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

print(x_test)
print(y_test)


# DATA BALANCING USING SMOTE
counter = Counter(y_train)
print("__________________BEFORE::::::", counter)

smt = SMOTE()

x_train_sm, y_train_sm = smt.fit_resample(x_train, y_train)

counter = Counter(y_train_sm)
print("___________________AFTER:::::::", counter)


print("x_train_sm shape:", x_train_sm.shape)
print("y_train_sm shape:", y_train_sm.shape)

# y_train = to_categorical(y_train_sm, 3)
# y_test = to_categorical(y_test, 3)
# print("after categorical")
# print(y_train.shape)
# print(y_test.shape)

# # SVM MODEL CREATION
# svm = SVC(kernel='poly', degree=3, gamma='scale')
# # svm.fit(x_train, y_train)
# svm.fit(x_train_sm, y_train_sm)

# prediction = svm.predict(x_test)

# Model Creation-Pipeline(Standardization & KNN)
scaler = StandardScaler()
# svm = SVC(kernel='poly', degree=3, gamma='scale')
svm = SVC()
# pipe_svm = Pipeline([('scaler', StandardScaler()),
#                     ('svm', SVC(kernel='poly', degree=3, gamma='scale'))])
pipe_svm = Pipeline([('scaler', StandardScaler()),
                    ('svm', SVC())])
pipe_svm.fit(x_train_sm, y_train_sm)

prediction = pipe_svm.predict(x_test)

# calculate accuracy =(TP+TN)/total
acc = accuracy_score(y_test, prediction)
print(f"The accuracy score for SVM is :{round(acc,3)*100}%")

# confusion matrix
cm = confusion_matrix(y_test, prediction)
print("Confusion Matrix is :\n", cm)


# plotting confusion matrix
conf_matrix = pd.DataFrame(data=cm,
                           columns=['Low', 'Moderate', 'High'],
                           index=['Low', 'Moderate', 'High'])
plt.figure(figsize=(10, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d',
            cmap="Greens", linecolor="Blue", linewidths=1.5)
plt.show()


# model saving
filename = "pipeline_svm_model.sav"
joblib.dump(pipe_svm, filename)
