from flask import Flask, render_template, request
import pickle
import numpy as np

# Setup Flask application
app = Flask(__name__)

# Load the trained model from the pickle file
def load_model():
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

# Function to make predictions
def prediction(lst):
    model = load_model()
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    pred_value = None  # Initialize predicted value
    if request.method == 'POST':
        try:
            # Extract form inputs
            ram = request.form.get('ram', type=int)
            weight = request.form.get('weight', type=float)
            company = request.form.get('company')
            typename = request.form.get('typename')
            opsys = request.form.get('opsys')
            cpu = request.form.get('cpuname')
            gpu = request.form.get('gpuname')
            touchscreen = request.form.getlist('touchscreen')  # Checkbox inputs
            ips = request.form.getlist('ips')  # Checkbox inputs

            # Build the feature list
            feature_list = [
                ram,
                weight,
                len(touchscreen),
                len(ips)
            ]

            # Categorical feature lists
            company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
            typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
            opsys_list = ['linux', 'mac', 'other', 'windows']
            cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
            gpu_list = ['amd', 'intel', 'nvidia']

            # Helper function to encode categorical data
            def encode_categorical(lst, value):
                for item in lst:
                    feature_list.append(1 if item == value else 0)

            # Encode each categorical input
            encode_categorical(company_list, company)
            encode_categorical(typename_list, typename)
            encode_categorical(opsys_list, opsys)
            encode_categorical(cpu_list, cpu)
            encode_categorical(gpu_list, gpu)

            # Predict and scale the value
            pred_value = prediction(feature_list)
            pred_value = round(pred_value[0] * 221, 2)

        except Exception as e:
            print(f"Error processing input: {e}")
            pred_value = "Error: Please check your input values."

    # Render the template with the predicted value
    return render_template('index.html', pred_value=pred_value)

if __name__ == '__main__':
    app.run(debug=True)
