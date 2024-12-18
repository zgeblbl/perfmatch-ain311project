from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import load

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Load the pre-trained logistic regression model
loaded_model = load("svm_model_team.joblib")

player_df_dropped_row = pd.read_parquet('parquet_data/player_df_missing_handled.parquet')
X_player = player_df_dropped_row[['S', 'Kills', 'Errors', 'Total Attacks', 'Hit Pct', 'Assists', 
                                  'SErr', 'Digs', 'Block Assists', 'PTS', 'name']]
names = X_player['name']
numeric_df = X_player.drop(columns=['name'])

# MinMaxScaler ile normalizasyon
scaler = StandardScaler()
numeric_columns = numeric_df.columns
normalized_data = scaler.fit_transform(numeric_df)
normalized_df = pd.DataFrame(normalized_data, columns=numeric_columns)
normalized_df['name'] = X_player['name'].values
averaged_df = normalized_df.groupby('name').mean(numeric_only=True).reset_index()


# Prediction function
def test_model(selected_players):
    # Filter the selected players
    filtered_df = averaged_df[averaged_df["name"].isin(selected_players)]
    
    if filtered_df.empty:
        return "Error: No valid players found in the dataset."

    # Calculate the average features
    averages = filtered_df.mean(numeric_only=True)

    # Prepare the data for prediction
    averages_df = pd.DataFrame([averages])
    averages_array = averages_df.to_numpy()

    # Make a prediction
    new_prediction = loaded_model.predict(averages_array)
    return new_prediction[0]

# Route to handle the prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()  # Get JSON data from frontend
        selected_players = data.get("filteredPlayers", [])
        print(selected_players)
        
        filtered_df = averaged_df[averaged_df['name'].isin(selected_players)]
        averages = filtered_df.mean(numeric_only=True)
        
        averages_df = pd.DataFrame([averages])
        averages_df = averages_df.to_numpy()
        
        prediction = loaded_model.predict(averages_df)
        prediction_result = int(prediction[0])
        print({'success': True, 'prediction': prediction_result})
        return jsonify({'success': True, 'prediction': prediction_result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
if __name__ == "__main__":
    app.run(debug=True)