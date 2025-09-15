from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Frontend HTML
frontend_html = """
<!DOCTYPE html>
<html>
<head>
    <title>BMI Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background: #f7f7f7; }
        h1 { color: #333; }
        input, button { padding: 8px; margin: 5px; }
        #result { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>⚖️ BMI Calculator</h1>

    <div>
        <input type="number" id="weight" placeholder="Weight (kg)" />
        <input type="number" id="height" placeholder="Height (cm)" />
        <button onclick="calculateBMI()">Calculate BMI</button>
    </div>

    <div id="result"></div>

    <script>
        async function calculateBMI() {
            let weight = document.getElementById('weight').value;
            let height = document.getElementById('height').value;
            if (!weight || !height) return alert("Enter both values!");

            let res = await fetch('/bmi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ weight: parseFloat(weight), height: parseFloat(height) })
            });
            let data = await res.json();
            document.getElementById('result').innerText = `Your BMI is ${data.bmi} (${data.category})`;
        }
    </script>
</body>
</html>
"""

# Route for frontend
@app.route('/')
def home():
    return render_template_string(frontend_html)

# BMI calculation route
@app.route('/bmi', methods=['POST'])
def bmi():
    data = request.json
    weight = data.get('weight')
    height = data.get('height') / 100  # convert cm to meters
    bmi_value = round(weight / (height ** 2), 2)

    # BMI category
    if bmi_value < 18.5:
        category = "Underweight"
    elif bmi_value < 25:
        category = "Normal weight"
    elif bmi_value < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return jsonify({"bmi": bmi_value, "category": category})

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
