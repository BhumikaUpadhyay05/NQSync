## What is NQSync?

**NQSync** is a **web-based network simulator** made for analysing **quantum networks**. Inspired by tools like ns-3, it enables users to build and simulate network topologies through an intuitive **canvas interface**.

Made for a researcher, student, or developer, NQSync offers a platform to design and analyze networks enhanced with **Quantum Key Distribution (QKD)** protocols such as **DPS** and **CoW**—giving insights into performance variations based on distance, link type, and protocol parameters.

Built for **education and research**, NQSync mimics real-world network behavior in software, enabling experimentation with **QKD** protocols such as **DPS** and **CoW**

## Key Features

- **Visual Topology Builder**  
  It helps user Create and configure networks by dragging multiple nodes and connecting them with links in a canvas.

- **QKD protocols**  
  Simulate QKD protocols such as **DPS (Differential Phase Shift)** and **CoW (Coherent One-Way)** for secure key exchange.

- **Result Metrics**  
  Run simulations and analyse performance metrics like **QBER**, **final key rate**, and **signal transmittance** for multiple nodes.

- **Customizable Parameters**  
  Adjust physical and protocol-level parameters (fiber length, efficiency, dark counts, etc.) for each link.

- **Educational & Research Focused**  
  Ideal for experimenting with network topologies, or exploring hybrid communication systems.

## What is Quantum Key Distribution?

**Quantum Key Distribution (QKD)** is a secure communication method that uses quantum mechanics to enable two parties to generate a shared, secret random key known only to them. This key can then be used to encrypt and decrypt messages. The fundamental advantage of QKD is its ability to detect any attempt at eavesdropping. Quantum Key Distribution (QKD) leverages the fundamental principles of quantum mechanics to enable cryptographic systems with **unconditional security**, guaranteed by the laws of physics.

## What is Coherent One-Way (CoW) Protocol?

- The CoW QKD protocol was introduced to enhance robustness against photon-number splitting attacks.
- Alice uses a laser source to send a sequence of time-separated optical pulses through an optical fiber.
- Logical bits are encoded as:<br>
  &nbsp;&nbsp;&nbsp;&nbsp; - Bit '0': signal pulse followed by an empty time slot.<br>
  &nbsp;&nbsp;&nbsp;&nbsp; - Bit '1': empty time slot followed by a signal pulse.
- Occasionally, Alice sends decoy sequences with two consecutive pulses to detect eavesdropping.
- Bob receives the pulses and uses a beam splitter to split incoming signals into two paths.
- One path is sent directly to a detector for time-of-arrival analysis, which reveals the key bit.
- The other path enters an interferometer to check for coherence between adjacent pulses.
- If coherence is maintained, it indicates the transmission is secure and eavesdropping is unlikely.
- By analyzing both arrival time and interference visibility, Bob can detect disturbances caused by potential attackers.

## What is Differential Phase Shift (DPS) QKD Protocol?

- The DPS QKD protocol was proposed in 2002 by Inoue et al.
- Alice creates a weak coherent pulse (WCP) — dim laser pulses each carrying very few photons (on average 0.2).
- She randomly changes the phase of each pulse to either 0 or π using a phase modulator.
- She sends these modulated pulses to Bob using an optical fiber.
- Bob passes the received pulses to a 1-bit delay Mach–Zehnder interferometer.
- This device compares the phase of two back-to-back pulses by making them interfere with each other.
- The outputs of the Mach–Zehnder interferometer are measured either by single photon detectors (SPDs) or superconducting nanowire single photon detectors (SNSPDs).
- Depending on which detector clicks, Bob can figure out the phase difference between the two pulses — this carries the key information.
- Bob tells Alice the exact times when one of his detectors clicked (but not which detector).
- Alice checks the two pulses she sent at those times:
  - If the phase difference was **0**, they both write down bit **0**.
  - If the phase difference was **π**, they both write down bit **1**.

## Result

They now share a secret key known only to them, which can be used to encrypt messages securely.

## Post-Processing of Raw Keys

After generating the raw key using **CoW** or **DPS QKD**, post-processing is essential to correct errors and ensure security.  
This process involves three main steps:

### 1. Parameter Estimation

- A small portion of the raw key is publicly disclosed to estimate the **Quantum Bit Error Rate (QBER)**.
- The fraction of the raw key used for this estimation is called the **disclose rate (DR)**.
- Parameter estimation helps detect the presence of an eavesdropper (Eve) and assess transmission errors.
- Ideally, DR is **50%**, but this significantly reduces the final key rate. In practice, a DR of **3–10%** is often sufficient.

### 2. Error Correction

- Based on the measured QBER, the sender and receiver apply error-correction protocols (e.g., **LDPC codes**) to remove discrepancies and align their keys.

### 3. Privacy Amplification

- To eliminate any partial information Eve might have obtained, the key is shortened.
- The shortening factor is called the **compression ratio (CR)**.
- This step ensures strong secrecy by producing the final secure key.
