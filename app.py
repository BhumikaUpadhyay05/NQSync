from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
from threading import Lock

app = Flask(__name__)

# Store simulation configurations and results
simulation_configs = {}
simulation_results = {}
results_lock = Lock()

def simulate_dps_qkd(distance_km, fiber_type='underground',
                     mu=0.2, pulse_rate=1e9, det_eff=0.06,
                     dark_rate=800, dead_time=20e-6,
                     disclosure_rate=0.03125, compression_ratio=0.5,
                     visibility=0.98, num_pulses=1000000):

    alpha = 0.20 if fiber_type == 'underground' else 0.30
    loss_dB = alpha * distance_km
    transmittance = 10 ** (-loss_dB / 10)

    p_signal = mu * transmittance * det_eff
    p_dark = dark_rate / pulse_rate
    detection_prob = p_signal + p_dark

    alice_bits = np.random.randint(0, 2, num_pulses)
    alice_phases = np.pi * alice_bits
    photon_presence = np.random.rand(num_pulses) < mu

    bob_key = []
    alice_key = []
    dark_counts = 0
    signal_detections = 0

    for i in range(1, num_pulses):
        detected = False
        bit = None
        is_signal = False

        if photon_presence[i] and photon_presence[i - 1]:
            if np.random.rand() < transmittance * det_eff:
                detected = True
                is_signal = True
                signal_detections += 1
                phase_diff = (alice_phases[i] - alice_phases[i - 1]) % (2*np.pi)
                ideal_bit = 0 if np.isclose(phase_diff, 0) else 1
                bit = ideal_bit if np.random.rand() < visibility else 1 - ideal_bit
                alice_key.append(ideal_bit)

        if not detected and np.random.rand() < p_dark:
            detected = True
            dark_counts += 1
            bit = np.random.randint(0, 2)
            alice_key.append(None)

        if detected:
            bob_key.append(bit)

    comparable_positions = [i for i, val in enumerate(alice_key) if val is not None]
    num_comparable = len(comparable_positions)

    if num_comparable == 0:
        QBER = 0.5
        errors = None
    else:
        errors = sum(alice_key[i] != bob_key[i] for i in comparable_positions)
        QBER = errors / num_comparable

    R_raw = pulse_rate * detection_prob / (1 + pulse_rate * detection_prob * dead_time)
    R_sifted = 0.5 * R_raw
    R_final = R_sifted * (1 - disclosure_rate) * (1 - compression_ratio)

    return {
        'distance_km': distance_km,
        'fiber_type': fiber_type,
        'transmittance': transmittance,
        'loss_dB': loss_dB,
        'p_signal': p_signal,
        'QBER': QBER,
        'bit_errors': errors,
        'raw_rate_bps': R_raw,
        'sifted_key_rate': R_sifted,
        'final_rate_bps': R_final,
        'detection_prob': detection_prob,
        'visibility': visibility,
        'key_match_ratio': 1 - QBER if num_comparable > 0 else 0,
        'len_alice_key': len(alice_key),
        'len_bob_key': len(bob_key),
        'num_detected': len(bob_key),
        'num_signal_detections': signal_detections,
        'num_dark_counts': dark_counts,
        'num_comparable': num_comparable
    }

@app.route("/")
def home():
    return render_template("main_index.html")

@app.route("/select-protocol")
def select_protocol():
    return render_template("protocol_select.html")

@app.route("/canvas")
def canvas():
    return render_template("canvas.html")

@app.route("/simulator-form", methods=["GET"])
def simulator_form():
    from_node = request.args.get('from')
    to_node = request.args.get('to')
    return render_template("simulator_form.html", from_node=from_node, to_node=to_node)

@app.route("/save-simulation", methods=["POST"])
@app.route("/save-simulation", methods=["POST"])
def save_simulation():
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
        
        # Prevent duplicate configuration
        if from_node in simulation_results and to_node in simulation_results[from_node]:
            return jsonify({'success': False, 'error': 'This connection is already configured.'})

        # Convert safe floats
        def safe_float(value, default):
            try:
                return float(value)
            except:
                return default

        distance_km = safe_float(data.get('distance_km'), 50)
        fiber_type = data.get('fiber_type', 'underground')
        mu = safe_float(data.get('mu'), 0.2)
        pulse_rate = safe_float(data.get('pulse_rate'), 1e9)
        det_eff = safe_float(data.get('det_eff'), 0.06)
        dark_rate = safe_float(data.get('dark_rate'), 800)
        dead_time = safe_float(data.get('dead_time'), 20e-6)
        disclosure_rate = safe_float(data.get('disclosure_rate'), 0.03125)
        compression_ratio = safe_float(data.get('compression_ratio'), 0.5)
        visibility = safe_float(data.get('visibility'), 0.98)

        result = simulate_dps_qkd(
            distance_km, fiber_type, mu, pulse_rate, det_eff,
            dark_rate, dead_time, disclosure_rate, compression_ratio, visibility
        )

        with results_lock:
            if from_node not in simulation_results:
                simulation_results[from_node] = {}
            simulation_results[from_node][to_node] = {
                'protocol': 'dps',
                'configured': True,
                'parameters': data,
                'result': result
            }

        return jsonify({'success': True, 'data': {
            'from_node': from_node,
            'to_node': to_node,
            'protocol': 'dps'
        }})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

        data = request.get_json()
        
        from_node = data.get('from_node')
        to_node = data.get('to_node')
        distance_km = safe_float(data.get('distance_km'), 50)
        fiber_type = data.get('fiber_type', 'underground')
        mu = safe_float(data.get('mu'), 0.2)
        pulse_rate = safe_float(data.get('pulse_rate'), 1e9)
        det_eff = safe_float(data.get('det_eff'), 0.06)
        dark_rate = safe_float(data.get('dark_rate'), 800)
        dead_time = safe_float(data.get('dead_time'), 20e-6)
        disclosure_rate = safe_float(data.get('disclosure_rate'), 0.03125)
        compression_ratio = safe_float(data.get('compression_ratio'), 0.5)
        visibility = safe_float(data.get('visibility'), 0.98)

        result = simulate_dps_qkd(
            distance_km, fiber_type, mu, pulse_rate, det_eff,
            dark_rate, dead_time, disclosure_rate, compression_ratio, visibility
        )

        # Store the result
        with results_lock:
            if from_node not in simulation_results:
                simulation_results[from_node] = {}
            simulation_results[from_node][to_node] = {
                'protocol': 'dps',
                'configured': True,
                'result': result
            }

        return jsonify({'success': True, 'result': result})

@app.route("/get-results")
def get_results():
    return jsonify(simulation_results)

@app.route("/combined-results")
def combined_results():
    # Process all results and prepare for display
    combined = []
    for from_node, connections in simulation_results.items():
        for to_node, config in connections.items():
            if config['configured']:
                combined.append({
                    'from': from_node,
                    'to': to_node,
                    'protocol': config['protocol'],
                    'result': config['result']
                })
    return render_template("combined_results.html", results=combined)

@app.route("/coming-soon")
def coming_soon():
    return render_template("coming_soon_landing.html")

if __name__ == "__main__":
    app.run(debug=True)