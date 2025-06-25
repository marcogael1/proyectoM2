from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

model = joblib.load('decision_tree_model.pkl')
scaler = joblib.load('scaler.pkl')

cols_to_scale = ['Age', 'Weight', 'Height', 'Neck', 'Chest', 'Abdomen',
                 'Hip', 'Thigh', 'Knee', 'Ankle', 'Biceps', 'Forearm', 'Wrist']

selected_features = ['Density', 'Age', 'Weight', 'Chest', 'Abdomen', 'Biceps']

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    row = {col: data.get(col, 0) for col in cols_to_scale}
    scaled_values = scaler.transform([list(row.values())])[0]

    input_data = {
        'Density': data['Density'],
        'Age': scaled_values[cols_to_scale.index('Age')],
        'Weight': scaled_values[cols_to_scale.index('Weight')],
        'Chest': scaled_values[cols_to_scale.index('Chest')],
        'Abdomen': scaled_values[cols_to_scale.index('Abdomen')],
        'Biceps': scaled_values[cols_to_scale.index('Biceps')]
    }

    input_array = np.array([input_data[feat] for feat in selected_features]).reshape(1, -1)
    prediction = model.predict(input_array)
    return jsonify({'prediction': float(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
