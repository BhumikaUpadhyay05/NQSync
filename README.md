# NQSync - Quantum Network Simulator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**NQSync** is an interactive web-based quantum network simulation platform that enables users to visually simulate Quantum Key Distribution (QKD) protocols through an intuitive drag-and-drop interface.

##  Overview

NQSync makes quantum communication accessible by providing a user-friendly GUI for simulating two popular QKD protocols:
- **Coherent One-Way (COW) QKD**
- **Differential Phase Shift (DPS) QKD**

Instead of complex command-line tools requiring deep technical knowledge, NQSync offers real-time visualization of quantum network behaviors, making it an ideal educational and research tool.

##  Features

-  **Visual Network Builder**: Drag-and-drop canvas interface for creating quantum networks
-  **Dual Protocol Support**: Simulate both COW and DPS-QKD protocols
-  **Real-time Analytics**: Live visualization of key rates, QBER, and detection statistics
-  **Configurable Parameters**: Adjust transmission distance, fiber type, detector characteristics, and more
-  **Interactive Graphs**: Dynamic plots showing performance metrics vs. distance
-  **Web-based**: No installation required - runs entirely in the browser

##  Quick Start

### Prerequisites

```bash
Python 3.8+
Flask
NumPy
Matplotlib (for result visualization)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/BhumikaUpadhyay05/NQSync.git
cd NQSync

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The simulator will be available at `http://localhost:5000`

##  Usage

### 1. COW Protocol Simulation

```python
# Navigate to COW protocol form
# Configure parameters:
- Distance: 50-100 km
- Fiber type: Underground (0.2 dB/km) or Aerial (0.3 dB/km)
- Average photons per pulse (μ): 0.1-1.0
- Pulse rate: 100 MHz - 1 GHz
- Detector efficiency: 0-100%
```

### 2. DPS Protocol Simulation

```python
# Navigate to DPS protocol form
# Configure parameters:
- Distance: 50-120 km
- Phase modulation: 0 or π
- Disclosure rate: Fraction of bits for error checking
- Compression ratio: Privacy amplification factor
```

### 3. Network Topology

- Use the canvas interface to place quantum nodes
- Draw fiber connections between nodes
- Configure protocol parameters for each link
- View real-time simulation results

## 🔧 Key Parameters

### Common Parameters (Both Protocols)

| Parameter | Description | Range |
|-----------|-------------|-------|
| `distance` | Fiber channel length (km) | 50-100 km |
| `fiber_type` | Cable installation type | underground/aerial |
| `mu` | Average photons per pulse | 0.1-1.0 |
| `pulse_rate` | Laser repetition rate (Hz) | 100 MHz - 1 GHz |
| `det_eff` | Detector efficiency (%) | 0-100 |
| `dark_rate` | Dark count rate (Hz) | 0-1000 |
| `dead_time` | Detector recovery time (s) | 1e-9 - 1e-6 |
| `visibility` | Interference visibility | 0.90-0.99 |

### COW-Specific Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `error_correction_efficiency` | Error correction factor | 1.16 |
| `decoy_ratio` | Fraction of decoy states | 0.30 |
| `mu_signal` | Signal state intensity | 0.5 |
| `mu_decoy` | Decoy state intensity | 0.05 |

### DPS-Specific Parameters

| Parameter | Description | Range |
|-----------|-------------|-------|
| `disclosure_rate` | Bits revealed for error checking | 0.1-0.3 |
| `compression_ratio` | Privacy amplification factor | 0.5-0.9 |

##  Output Metrics

The simulator provides:
- **Key Rate (bps)**: Secure key generation rate
- **QBER (%)**: Quantum Bit Error Rate
- **Raw Detection Rate**: Initial photon detection statistics
- **Sifted Rate**: Post-processing key rate
- **Final Secure Rate**: After error correction and privacy amplification



##  Scientific Background

### COW Protocol
Encodes bits using pairs of empty and non-empty pulses. Security derives from coherence between sequential pulses.

**Key Rate Formula:**
```
R_final = R_sifted × (1 - error_correction_efficiency × QBER)
```

### DPS Protocol
Encodes information in phase differences between consecutive pulses using random phase modulation (0 or π).

**Key Rate Formula:**
```
R_final = R_sifted × (1 - disclosure_rate) × (1 - compression_ratio)
```

##  Contributors

- **Bhumika Upadhyay** - IISER Bhopal 
- **Aini Rizvi** - VIT Bhopal University 
- **Siddhant Jawalker** - NSFU Bhopal

**Supervised by:** Dr. Ankur Raina, QUCIS Lab, IISER Bhopal

##  References

1. Brazaola-Vicario et al. "High-Fidelity Coherent-One-Way QKD Simulation Framework for 6G Networks" (2025)
2. Malpani, Kumar, Pathak. "Implementation of coherent one way protocol for quantum key distribution up to 145 km" (2024)
3. Kumar et al. "Experimental implementation of distributed phase reference quantum key distribution protocols" (2023)
4. Chatterjee et al. "qkdSim: An experimenter's simulation toolkit for QKD" (2019)

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

Special thanks to Dr. Ankur Raina for guidance throughout this project, and to the QUCIS Lab at IISER Bhopal for providing the research foundation.

## 📧 Contact

For questions or collaboration opportunities:
- GitHub Issues: [Create an issue](https://github.com/BhumikaUpadhyay05/NQSync/issues)
- Email: [Contact maintainers through GitHub]

---

**Project Duration:** May 2025 - July 2025  
**Institution:** Indian Institute of Science Education and Research, Bhopal
