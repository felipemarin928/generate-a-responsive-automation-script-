import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulator configuration
simulator_config = {
    "delay_range": [500, 2000],  # delay in milliseconds
    "error_rate": 0.2,  # error rate in percentage
    "max_iterations": 10
}

# Automation script templates
script_templates = {
    "login": {
        "steps": [
            {"action": "input", "target": "username", "value": "testuser"},
            {"action": "input", "target": "password", "value": "testpass"},
            {"action": "click", "target": "login_button"}
        ]
    },
    "logout": {
        "steps": [
            {"action": "click", "target": "logout_button"}
        ]
    }
}

@app.route('/generate_script', methods=['POST'])
def generate_script():
    data = request.get_json()
    script_type = data.get('script_type')
    if script_type not in script_templates:
        return jsonify({"error": "Invalid script type"}), 400

    script_template = script_templates[script_type]
    script_steps = script_template['steps']

    automation_script = []
    for step in script_steps:
        action = step['action']
        target = step['target']
        value = step.get('value')
        automation_script.append({"action": action, "target": target, "value": value})

    return jsonify({"script": automation_script})

@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.get_json()
    script = data.get('script')
    if not script:
        return jsonify({"error": "Invalid script"}), 400

    simulation_results = []
    for step in script:
        action = step['action']
        target = step['target']
        value = step.get('value')

        # Simulate delay
        delay = random.randint(simulator_config['delay_range'][0], simulator_config['delay_range'][1])
        time.sleep(delay / 1000)

        # Simulate error
        if random.random() < simulator_config['error_rate']:
            simulation_results.append({"step": step, "result": "error"})
        else:
            simulation_results.append({"step": step, "result": "success"})

    return jsonify({"results": simulation_results})

if __name__ == '__main__':
    app.run(debug=True)