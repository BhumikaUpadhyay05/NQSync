from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from threading import Lock

app = Flask(__name__)

# Thread-safe storage for simulation results
simulation_results = {}
results_lock = Lock()

def safe_float(value, default):
    try:
        return float(value)
    except:
        return default
    
#cow protocol
def simulate_cow_qkd(distance_km,
                     fiber_type='underground',
                     mu=0.1,
                     pulse_rate=1e9,
                     det_eff=0.2,
                     dark_rate=100,
                     dead_time=20e-6,
                     error_correction_efficiency=0.9,
                     visibility=0.98,
                     num_pulses=100000):

    alpha = 0.20 if fiber_type == 'underground' else 0.30
    loss_dB = alpha * distance_km
    transmittance = 10 ** (-loss_dB / 10)

    # Decoy state parameters
    decoy_ratio = 0.3
    mu_signal = mu
    mu_decoy = mu * 0.1

    # distance-dependent QBER model
    min_qber = max(0.005, 0.005 + (0.02 * distance_km / 100))  # 0.5% to 2.5% from 0-100km
    effective_visibility = 1 - min_qber

    p_signal = mu_signal * transmittance * det_eff
    p_decoy = mu_decoy * transmittance * det_eff
    p_dark = dark_rate / pulse_rate

    alice_bits = np.random.randint(0, 2, num_pulses)
    alice_decisions = np.random.rand(num_pulses) < 0.5
    is_decoy = np.random.rand(num_pulses) < decoy_ratio

    bob_key, alice_key = [], []
    signal_detections = dark_counts = decoy_detections = 0
    required_errors = 0

    for i in range(num_pulses):
        detected = False
        current_p_signal = p_decoy if is_decoy[i] else p_signal
        
        if np.random.rand() < current_p_signal and alice_decisions[i]:
            detected = True
            if is_decoy[i]:
                decoy_detections += 1
                continue
            else:
                signal_detections += 1
                # Calculation for how many errors we should have by now
                target_errors = int(min_qber * signal_detections)
                
                # Force error if we're behind target
                if (required_errors < target_errors) or (signal_detections > 0 and required_errors == 0):
                    bit = 1 - alice_bits[i]
                    required_errors += 1
                else:
                    bit = alice_bits[i] if np.random.rand() < effective_visibility else 1 - alice_bits[i]
                
                alice_key.append(alice_bits[i])
                bob_key.append(bit)
        elif not detected and np.random.rand() < p_dark:
            detected = True
            dark_counts += 1
            alice_key.append(None)
            bob_key.append(np.random.randint(0, 2))

    comparable_positions = [i for i, val in enumerate(alice_key) if val is not None]
    num_comparable = len(comparable_positions)
    errors = sum(alice_key[i] != bob_key[i] for i in comparable_positions) if num_comparable > 0 else None
    QBER = max(min_qber, errors / num_comparable) if num_comparable > 0 else min_qber  # Enforcing minimum

    R_raw = pulse_rate * p_signal / (1 + pulse_rate * p_signal * dead_time)
    R_sifted = 0.5 * R_raw
    R_final = R_sifted * (1 - error_correction_efficiency * QBER)

    return {
        'distance_km': float(distance_km),
        'fiber_type': fiber_type,
        'loss_dB': float(loss_dB),
        'transmittance': float(transmittance),
        'p_signal': float(p_signal),
        'p_dark': float(p_dark),
        'detection_prob': float(p_signal + p_dark),
        'QBER': float(QBER),
        'bit_errors': int(errors) if errors is not None else None,
        'raw_rate_bps': float(R_raw),
        'sifted_key_rate': float(R_sifted),
        'final_rate_bps': float(R_final),
        'visibility': float(visibility),
        'key_match_ratio': float(1 - QBER) if num_comparable > 0 else 0.0,
        'num_detected': int(len(bob_key)),
        'num_signal_detections': int(signal_detections),
        'num_dark_counts': int(dark_counts),
        'num_comparable': int(num_comparable),
        'num_decoy_detections': int(decoy_detections),
        'protocol': 'cow'
    }

# DPS QKD simulation function
def simulate_dps_qkd(distance_km, fiber_type='underground',
                     mu=0.2, pulse_rate=1e9, det_eff=0.06,
                     dark_rate=800, dead_time=20e-6,
                     disclosure_rate=0.03125, compression_ratio=0.5,
                     visibility=0.98, num_pulses=10000000):

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
                total_error_prob = loss_dB*0.0085
                bit = ideal_bit if np.random.rand() > total_error_prob else 1 - ideal_bit
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

@app.route("/cow-form", methods=["GET"])
def cow_form():
    from_node = request.args.get('from')
    to_node = request.args.get('to')
    return render_template("cow_form.html", from_node=from_node, to_node=to_node)
@app.route("/save-cow-simulation", methods=["POST"])
def save_cow_simulation():
    try:
        data = request.get_json()
        from_node = data['from_node']
        to_node = data['to_node']

        with results_lock:
            if from_node in simulation_results and to_node in simulation_results[from_node]:
                return jsonify({'success': False, 'error': 'This connection is already configured.'})

        result = simulate_cow_qkd(
            distance_km=safe_float(data.get('distance_km'), 50),
            fiber_type=data.get('fiber_type', 'underground'),
            mu=safe_float(data.get('mu'), 0.1),
            pulse_rate=safe_float(data.get('pulse_rate'), 1e9),
            det_eff=safe_float(data.get('det_eff'), 0.2),
            dark_rate=safe_float(data.get('dark_rate'), 100),
            dead_time=safe_float(data.get('dead_time'), 20e-6),
            error_correction_efficiency=safe_float(data.get('error_correction_efficiency'), 0.9),
            visibility=safe_float(data.get('visibility'), 0.98)
        )

        with results_lock:
            simulation_results.setdefault(from_node, {})[to_node] = {
                'protocol': 'cow',
                'configured': True,
                'parameters': data,
                'result': result
            }

        return jsonify({'success': True, 'data': {
            'from_node': from_node,
            'to_node': to_node,
            'protocol': 'cow'
        }})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/remove-link", methods=["POST"])
def remove_link():
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
    try:
        with results_lock:
            simulation_results.clear()
        return jsonify({"success": True, "message": "All configurations cleared."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


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

        with results_lock:
            if from_node in simulation_results and to_node in simulation_results[from_node]:
                return jsonify({'success': False, 'error': 'This connection is already configured.'})

        result = simulate_dps_qkd(
            distance_km=safe_float(data.get('distance_km'), 50),
            fiber_type=data.get('fiber_type', 'underground'),
            mu=safe_float(data.get('mu'), 0.2),
            pulse_rate=safe_float(data.get('pulse_rate'), 1e9),
            det_eff=safe_float(data.get('det_eff'), 0.06),
            dark_rate=safe_float(data.get('dark_rate'), 800),
            dead_time=safe_float(data.get('dead_time'), 20e-6),
            disclosure_rate=safe_float(data.get('disclosure_rate'), 0.03125),
            compression_ratio=safe_float(data.get('compression_ratio'), 0.5),
            visibility=safe_float(data.get('visibility'), 0.98)
        )

        with results_lock:
            simulation_results.setdefault(from_node, {})[to_node] = {
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

@app.route("/get-results")
def get_results():
    return jsonify(simulation_results)

@app.route("/coming-soon")
def coming_soon():
    return render_template("coming_soon_landing.html")
@app.route("/results")
def results():
    with results_lock:
        return render_template("results.html", simulation_results=simulation_results)
@app.route("/documentation")
def documentation():
    return render_template("documentation.html")


if __name__ == "__main__":
    app.run(debug=True)
