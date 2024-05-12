import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import pandas as pd



class ML():
    def __init__(self):
        self.target_columns = ['Overall Utilization', 'Total Packet Variation', 'Input Packet Variation', 'Output Packet Variation', 'Average Error Percentage', 'Input Error Percentage', 'Output Error Percentage', 'Total Discards', 'Input Discards', 'Output Discards']  # List of potential target columns
   

    def start_ml(self, ml_choice, df):
        
        self.ml_choice = ml_choice
        self.df = df
        df.drop(columns=['timestamp'], inplace=True)
        X_train, X_test, y_train, y_test = self.split_train_and_test(df)
        
        if ml_choice == "Linear Regression":
            self.model = self.train_linear_regression(X_train, y_train)
            self.rmse, self.mae = self.evaluate_model_metrics(self.model, X_test, y_test)
            self.print_metrics("Linear Regression", self.rmse, self.mae)
        elif ml_choice == "Random Forest":
            self.model = self.train_random_forest(X_train, y_train)
            self.rmse, self.mae = self.evaluate_model_metrics(self.model, X_test, y_test)
            self.print_metrics("Random Forest", self.rmse, self.mae)
        else:
            self.model = self.train_support_vector_machine(X_train, y_train)
            self.rmse, self.mae = self.evaluate_svm_model_metrics(self.model, X_test, y_test)
            self.print_svm_metrics(self.rmse, self.mae)

        return self.model, self.rmse, self.mae

    def get_target_var(self):
        return self.present_target_columns

    def split_train_and_test(self, df):
        
        self.present_target_columns = [col for col in self.target_columns if col in df.columns]
        print("Present target columns:", self.present_target_columns)
        
        if not self.present_target_columns:
            raise ValueError("None of the target columns are present in the DataFrame.")

        target_variables = df[self.present_target_columns]
        X = df.drop(columns=self.present_target_columns)
        X_train, X_test, y_train, y_test = train_test_split(X, target_variables, test_size=0.2, shuffle=False)
        X_test.reset_index(drop=True, inplace=True)
        y_test.reset_index(drop=True, inplace=True)
        print("Training set shape:", X_train.shape)
        print("Testing set shape:", X_test.shape)

        return X_train, X_test, y_train, y_test

    def get_present_columns(self):
        return self.present_target_columns
    
    def train_linear_regression(self, X_train, y_train):
        lrmodel = LinearRegression()
        lrmodel.fit(X_train, y_train)

        return lrmodel

    def train_random_forest(self, X_train, y_train):

        rfmodel = RandomForestRegressor()
        rfmodel.fit(X_train, y_train)

        return rfmodel

    def train_support_vector_machine(self, X_train, y_train):
        svm_models = {}
        
        for target_column in y_train.columns:

            svm_model = SVR()     
            svm_model.fit(X_train, y_train[target_column])    
            svm_models[target_column] = svm_model

        return svm_models
    
    def get_model(self):
        try:
            return self.model
        except AttributeError:
            print("Please train a model before saving.")


    def evaluate_model_metrics(self, model, X_test, y_test):
        
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred, multioutput='raw_values'))
        mae = mean_absolute_error(y_test, y_pred, multioutput='raw_values')
        rmse_dict = {target: value for target, value in zip(y_test.columns, rmse)}
        mae_dict = {target: value for target, value in zip(y_test.columns, mae)}
        self.plot_metrics(rmse_dict, mae_dict, 'Random Forest')
        self.plot_metrics_scatter_per_variable(y_test, y_pred, 'Random Forest')
        
        return rmse_dict, mae_dict

    def evaluate_svm_model_metrics(self, svm_models, X_test, y_test):
        svm_rmse = {}
        svm_mae = {}
        
        for target_column, svm_model in svm_models.items():
           
            y_pred = svm_model.predict(X_test)
            svm_rmse[target_column] = np.sqrt(mean_squared_error(y_test[target_column], y_pred))
            svm_mae[target_column] = mean_absolute_error(y_test[target_column], y_pred)
            self.plot_metrics(svm_rmse, svm_mae, 'SVM')


        
        return svm_rmse, svm_mae

    def print_metrics(self, model_name, rmse, mae):
        print(f"{model_name} RMSE for each target variable:")
        for target, value in rmse.items():
            print(f"{target}: {value}")
        
        print(f"\n{model_name} MAE for each target variable:")
        for target, value in mae.items():
            print(f"{target}: {value}")
        
        print("\n")

    def print_svm_metrics(self, rmse, mae):
        print("Support Vector Machine RMSE for each target variable:")
        for target, value in rmse.items():
            print(f"{target}: {value}")


        
        print("\nSupport Vector Machine MAE for each target variable:")
        for target, value in mae.items():
            print(f"{target}: {value}")
        
        print("\n")

