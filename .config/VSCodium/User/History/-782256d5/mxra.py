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

# Function to load data from text file
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                parts = line.strip().split(", ")
                row = {}
                for part in parts:
                    key, value = part.split(": ")
                    row[key] = float(value)
                data.append(row)
            except ValueError as e:
                logging.error(f"Error parsing line: {line} - {e}")
    return pd.DataFrame(data)

# Function to preprocess the data
def preprocess_data(df):
    X = df[['k1', 'b']]
    y = df['MRR']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler

# Function to train the model
def train_model(X, y):
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

# Function to predict MRR given k1 and b
def predict_mrr(params, model, scaler):
    k1, b = params
    X_scaled = scaler.transform([[k1, b]])
    return -model.predict(X_scaled)[0]

# Function to optimize parameters
def optimize_params(model, scaler, max_mrr):
    def objective(params):
        return predict_mrr(params, model, scaler)
    
    bounds = [(0.2, 1.3), (0.0, 1.0)]
    initial_guess = [0.5, 0.5]
    result = minimize(objective, initial_guess, bounds=bounds)
    
    if -result.fun >= max_mrr:
        best_k1, best_b = result.x
        best_mrr = -result.fun
        return best_k1, best_b, best_mrr
    else:
        logging.warning("Could not find a better MRR than the maximum in the dataset.")
        return None, None, max_mrr

# Function to plot data and results
def plot_results(df, best_k1, best_b, best_mrr):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='k1', y='b', size='MRR', hue='MRR', palette='viridis', legend=None, sizes=(20, 200))
    if best_k1 is not None and best_b is not None:
        plt.scatter(best_k1, best_b, color='red', s=100, label=f'Optimal (k1={best_k1:.2f}, b={best_b:.2f}, MRR={best_mrr:.4f})')
    plt.xlabel('k1')
    plt.ylabel('b')
    plt.title('k1 and b vs. MRR')
    plt.legend()
    plt.show()

# Main function to execute the workflow
def main(file_path):
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

if __name__ == "__main__":
    file_path = "/home/shuvam/Information_Retrieval/reults_bm25/output/summary.txt"  # Update this with the correct file path
    main(file_path)
