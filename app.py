from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from threading import Lock
from protocols import Protocol

app = Flask(__name__)

# Thread-safe storage for simulation results
# This dictionary will now store configurations and simulation results separately.
simulation_results = {}
results_lock = Lock()

def safe_float(value, default):
    """Safely convert a value to float, returning a default on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

@app.route("/cow-form", methods=["GET"])
def cow_form():
    """Renders the form for configuring a COW protocol link."""
    from_node = request.args.get('from')
    to_node = request.args.get('to')
    return render_template("cow_form.html", from_node=from_node, to_node=to_node)

@app.route("/save-cow-simulation", methods=["POST"])
def save_cow_simulation():
    """Saves the configuration for a COW link without running the simulation."""
    try:
        data = request.get_json()
        from_node = data['from_node']
        to_node = data['to_node']

        with results_lock:
            if from_node in simulation_results and to_node in simulation_results[from_node]:
                return jsonify({'success': False, 'error': 'This connection is already configured.'})

            # Store configuration data; simulation will be run later.
            simulation_results.setdefault(from_node, {})[to_node] = {
                'protocol': 'cow',
                'configured': True,
                'simulated': False,
                'parameters': data,
                'result': None
            }

        return jsonify({'success': True, 'data': {
            'from_node': from_node,
            'to_node': to_node,
            'protocol': 'cow'
        }})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/dps-form", methods=["GET"])
def simulator_form():
    """Renders the form for configuring a DPS protocol link."""
    from_node = request.args.get('from')
    to_node = request.args.get('to')
    return render_template("dps_form.html", from_node=from_node, to_node=to_node)

@app.route("/save-simulation", methods=["POST"])
def save_simulation():
    """Saves the configuration for a DPS link without running the simulation."""
    try:
        data = request.get_json()
        required_fields = ['from_node', 'to_node', 'distance_km', 'fiber_type', 
                           'mu', 'pulse_rate', 'det_eff', 'dark_rate',
                           'dead_time', 'disclosure_rate', 'compression_ratio',
                           'visibility']

        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'})

        from_node = data['from_node']
        to_node = data['to_node']

        with results_lock:
            if from_node in simulation_results and to_node in simulation_results[from_node]:
                return jsonify({'success': False, 'error': 'This connection is already configured.'})

            # Store configuration data; simulation will be run later.
            simulation_results.setdefault(from_node, {})[to_node] = {
                'protocol': 'dps',
                'configured': True,
                'simulated': False,
                'parameters': data,
                'result': None
            }

        return jsonify({'success': True, 'data': {
            'from_node': from_node,
            'to_node': to_node,
            'protocol': 'dps'
        }})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/simulate-network", methods=["POST"])
def simulate_network():
    """Runs the simulation for all configured links in the network."""
    try:
        with results_lock:
            # Iterate through all saved configurations and run the simulation
            for from_node, connections in simulation_results.items():
                for to_node, config in connections.items():
                    params = config['parameters']
                    protocol = config['protocol']
                    result = None

                    if protocol == 'dps':
                        result = Protocol.simulate_dps_qkd(
                            distance_km=safe_float(params.get('distance_km'), 50),
                            fiber_type=params.get('fiber_type', 'underground'),
                            mu=safe_float(params.get('mu'), 0.2),
                            pulse_rate=safe_float(params.get('pulse_rate'), 1e9),
                            det_eff=safe_float(params.get('det_eff'), 0.06),
                            dark_rate=safe_float(params.get('dark_rate'), 800),
                            dead_time=safe_float(params.get('dead_time'), 20e-6),
                            disclosure_rate=safe_float(params.get('disclosure_rate'), 0.03125),
                            compression_ratio=safe_float(params.get('compression_ratio'), 0.5),
                            visibility=safe_float(params.get('visibility'), 0.98)
                        )
                    elif protocol == 'cow':
                        result = Protocol.simulate_cow_qkd(
                            distance_km=safe_float(params.get('distance_km'), 50),
                            fiber_type=params.get('fiber_type', 'underground'),
                            mu=safe_float(params.get('mu'), 0.1),
                            pulse_rate=safe_float(params.get('pulse_rate'), 1e9),
                            det_eff=safe_float(params.get('det_eff'), 0.2),
                            dark_rate=safe_float(params.get('dark_rate'), 100),
                            dead_time=safe_float(params.get('dead_time'), 20e-6),
                            error_correction_efficiency=safe_float(params.get('error_correction_efficiency'), 0.9),
                            visibility=safe_float(params.get('visibility'), 0.98)
                        )
                    
                    # Update the record with the simulation result
                    if result is not None:
                        config['result'] = result
                        config['simulated'] = True

        return jsonify({'success': True, 'message': 'Network simulation complete.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/remove-link", methods=["POST"])
def remove_link():
    """Removes a configured link from the simulation."""
    try:
        data = request.get_json()
        from_node = data.get('from_node')
        to_node = data.get('to_node')

        with results_lock:
            if from_node in simulation_results and to_node in simulation_results[from_node]:
                del simulation_results[from_node][to_node]
                if not simulation_results[from_node]:
                    del simulation_results[from_node]
                return jsonify({'success': True})
            return jsonify({'success': False, 'error': 'Link not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/reset-all", methods=["POST"])
def reset_all():
    """Clears all configurations and simulation results."""
    try:
        with results_lock:
            simulation_results.clear()
        return jsonify({"success": True, "message": "All configurations cleared."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/")
def home():
    """Serves the main home page."""
    return render_template("main_index.html")

@app.route("/canvas")
def canvas():
    """Serves the network canvas page."""
    return render_template("canvas.html")

@app.route("/get-results")
def get_results():
    """Returns the current simulation results as JSON."""
    return jsonify(simulation_results)

@app.route("/coming-soon")
def coming_soon():
    """Serves a 'coming soon' page."""
    return render_template("coming_soon.html")

@app.route("/results")
def results():
    """Displays the final simulation results page."""
    with results_lock:
        return render_template("results.html", simulation_results=simulation_results)

@app.route("/documentation")
def documentation():
    """Serves the documentation page."""
    return render_template("documentation.html")

if __name__ == "__main__":
    app.run(debug=True)
