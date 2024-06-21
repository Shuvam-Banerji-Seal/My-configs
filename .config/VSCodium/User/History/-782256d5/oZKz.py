import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to load and validate data from text file
def load_data(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(", ")
                row = {}
                for part in parts:
                    key, value = part.split(": ")
                    row[key] = float(value)
                data.append(row)
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
        raise
    except Exception as e:
        logging.error(f"Error loading data from '{file_path}': {e}")
        raise
    return pd.DataFrame(data)

# Function to preprocess the data
def preprocess_data(df):
    try:
        X = df[['k1', 'b']]
        y = df['MRR']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    except KeyError as e:
        logging.error(f"Missing column in dataset: {e}")
        raise
    except Exception as e:
        logging.error(f"Error preprocessing data: {e}")
        raise
    return X_scaled, y, scaler

# Function to train the model
def train_model(X, y):
    try:
        model = RandomForestRegressor(random_state=42)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
        grid_search.fit(X, y)
        logging.info(f"Best parameters: {grid_search.best_params_}")
        return grid_search.best_estimator_
    except Exception as e:
        logging.error(f"Error training model: {e}")
        raise

# Function to predict MRR given k1 and b
def predict_mrr(params, model, scaler):
    try:
        k1, b = params
        X_scaled = scaler.transform([[k1, b]])
        return -model.predict(X_scaled)[0]  # maximize MRR
    except Exception as e:
        logging.error(f"Error predicting MRR: {e}")
        raise

# Function to optimize parameters
def optimize_params(model, scaler, max_mrr):
    try:
        def objective(params):
            return predict_mrr(params, model, scaler)
        
        bounds = [(0.0, 5.0), (0.0, 1.0)]
        initial_guesses = [[0.5, 0.5], [1.0, 0.2], [0.8, 0.8]]
        results = []
        
        for initial_guess in initial_guesses:
            result = minimize(objective, initial_guess, bounds=bounds)
            results.append(result)
        
        best_result = max(results, key=lambda x: -x.fun)
        best_k1, best_b = best_result.x
        best_mrr = -best_result.fun
        
        if best_mrr >= max_mrr:
            return best_k1, best_b, best_mrr
        else:
            logging.warning("Could not find a better MRR than the maximum in the dataset.")
            return None, None, max_mrr
    except Exception as e:
        logging.error(f"Error optimizing parameters: {e}")
        raise

# Function to plot data and results
def plot_results(df, best_k1, best_b, best_mrr):
    try:
        plt.figure(figsize=(12, 8))
        sns.scatterplot(data=df, x='k1', y='b', size='MRR', hue='MRR', palette='viridis', legend=None, sizes=(20, 200))
        if best_k1 is not None and best_b is not None:
            plt.scatter(best_k1, best_b, color='red', s=100, label=f'Optimal (k1={best_k1:.2f}, b={best_b:.2f}, MRR={best_mrr:.4f})')
        plt.xlabel('k1')
        plt.ylabel('b')
        plt.title('k1 and b vs. MRR')
        plt.legend()
        plt.show()
    except Exception as e:
        logging.error(f"Error plotting results: {e}")
        raise

# Function to save ordered results to file
def save_ordered_results(df):
    try:
        ordered_df = df.sort_values(by='MRR', ascending=False)
        ordered_df.to_csv('ordered_res.txt', index=False)
    except Exception as e:
        logging.error(f"Error saving ordered results: {e}")
        raise

# Main function to execute the workflow
def main(file_path):
    try:
        logging.info("Loading data...")
        df = load_data(file_path)
        logging.info("Data loaded successfully.")

        logging.info("Preprocessing data...")
        X, y, scaler = preprocess_data(df)
        logging.info("Data preprocessed successfully.")

        logging.info("Training model...")
        model = train_model(X, y)
        logging.info("Model trained successfully.")

        max_mrr = df['MRR'].max()
        logging.info(f"Maximum MRR in dataset: {max_mrr}")

        logging.info("Optimizing parameters...")
        best_k1, best_b, best_mrr = optimize_params(model, scaler, max_mrr)
        if best_k1 is not None and best_b is not None:
            logging.info(f"Best k1: {best_k1}")
            logging.info(f"Best b: {best_b}")
            logging.info(f"Predicted MRR: {best_mrr}")
        else:
            logging.info("No better parameters found.")

        logging.info("Plotting results...")
        plot_results(df, best_k1, best_b, best_mrr)
        logging.info("Plotting completed.")

        logging.info("Saving ordered results to file...")
        save_ordered_results(df)
        logging.info("Results saved to 'ordered_res.txt'.")
        print("The best k1 and b values are: ", best_k1, best_b)
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    file_path = "/home/shuvam/Information_Retrieval/reults_bm25/output/summary2.txt"  # Update with the correct file path
    main(file_path)
