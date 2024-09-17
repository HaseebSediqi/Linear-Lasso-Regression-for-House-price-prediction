# -*- coding: utf-8 -*-
"""LinearRegression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XiYJtFQTm8Uo7I1cGk6o6Nr9zRSRiqas

Importing Libraries
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.linear_model import LinearRegression, Lasso,LassoCV
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns

data=pd.read_csv("HousingData.csv") # loading datat

"""Data Exploration"""

data.head()

data.shape

data.isnull().sum()

null_columns = data.columns[data.isnull().any()]
data[null_columns].isnull().sum()

"""Handling Missing Values"""

medians = data.median()

data_cleaned = data.fillna(data.median()) #assiging median of each col to na values

data_cleaned.head(9)

data_cleaned.isnull().sum()

"""Seperating  features X ( Predictors ) and Target variable Y"""

X = data_cleaned.drop('MEDV', axis = 1) # axis = 1 shows opertion perform on columns
Y = data_cleaned['MEDV']

"""Spliting data into Training and Testing Sets"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, Y_train)

"""Bigger the Magnititude of Ceoficient, bigger is the influence of that feature in prediction. Intercept is the value of response variable when all other features are zero."""

print("Model Coefficients: ", model.coef_)
print("Model Intercept: ", model.intercept_)

"""Visualize the importance of each feature. We can see NOX ( the higher the value of Nitrogen in envrionemnt, has biggest negative impact in pricing of house ) also RM and CHAS played role in the price"""

features = X.columns
importances = model.coef_
plt.figure(figsize=(10,6))
plt.barh(features,importances)
plt.xlabel("Coeficient values")
plt.title("Feature Importance")
plt.show()

"""R2 indicates 65% of variance are explained by the features. While MSE indicate 24.9%, indicating the percntage of error. The Higher R2 value and lower MSE value, indicates better model fit. Our model performs moderately well."""

Y_pred = model.predict(X_test)
mse = mean_squared_error(Y_test,Y_pred)
r2 = r2_score(Y_test,Y_pred)
print("Mean Squared Error: ",mse)
print("R2 : ",r2)

"""Visualizing Actual vs Predicted value by model. If blue dots are closely align to red line, indicates better model fit. we see some of data points are far away but most of them are align on or closer to the line"""

plt.figure(figsize=(10,6))
plt.scatter(Y_test,Y_pred,color='blue')
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], color='red')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.grid(True)
plt.show()

"""Each blue point represents a prediction from the model, with the x-axis showing the predicted value and the y-axis showing the corresponding residual (error).
Residual= Yactual− Ypredicted
​
"""

plt.figure(figsize=(10,6))
residuals = Y_test -  Y_pred
plt.scatter(Y_pred,residuals,color = "blue")
plt.hlines(y=0, xmin=Y_pred.min(), xmax=Y_pred.max(), colors='red')
plt.xlabel("Predicted Value")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.grid(True)
plt.show()

"""Lets fit another model and consider onl the most important features to see if model improves"""

X2 = data_cleaned[['RM','NOX','CHAS','LSTAT','DIS','PTRATIO','RAD']]
Y2 = data_cleaned['MEDV']

X2_train,X2_test,Y2_train,Y2_test = train_test_split(X2,Y2,test_size=0.2, random_state=42)

model2 = LinearRegression()
model2.fit(X2_train,Y2_train)

print("Coeficients: ",model2.coef_)
print("Intercept: ",model2.intercept_)

"""New Model with lesser feature did not improve our model as we got approximately same values for MSE and R2 as we had in previous model"""

Y2_pred = model2.predict(X2_test)
mse2 = mean_squared_error(Y2_test,Y2_pred)
r22 = r2_score(Y2_test,Y2_pred)
print("MSE : ", mse2)
print("R2:,",r22)

"""We can try Lasso Regression with a penalty value of alpha ( Tuning regularization parameter). we keep trying different values for alpha till we get a value that does not improve model futher"""

lasso_model = Lasso(alpha = 0.001)
lasso_model.fit(X_train,Y_train)

Y_lasso_pred = lasso_model.predict(X_test)

mse_lasso = mean_squared_error(Y_test,Y_lasso_pred)
r2_lasso = r2_score(Y_test,Y_lasso_pred)
print("Mean Squared Error: ", mse_lasso)
print("R2: ",r2_lasso)

"""Rather then manually trying different Alpha values, we can use cross validation to chose the optimal value for Alpha"""

alphas = np.logspace(-3,1,50)

lasso_cv_model = LassoCV(alphas=alphas, cv=5)
lasso_cv_model.fit(X_train,Y_train)

best_alpha_cv = lasso_cv_model.alpha_
print("Best Value for alpha: ", best_alpha_cv)

"""We can see even, Lasso model did not improve the result. But overall the reuslt and performance is average. One way to improve, would be trying a bigger data set or using non linear models like Decision Tree or Random Forest"""

Y_pred_lasso_cv = lasso_cv_model.predict(X_test)
mse_lasso_cv = mean_squared_error(Y_test,Y_pred_lasso_cv)
r2_lasso_cv =  r2_score(Y_test,Y_pred_lasso_cv)
print("Means square error: ", mse_lasso_cv)
print("R squared: ",r2_lasso_cv)