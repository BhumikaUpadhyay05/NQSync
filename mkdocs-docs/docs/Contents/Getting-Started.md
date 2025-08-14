Now that the [installation](Installation-Guide.md) is complete, you are ready to run your first simulation!  
This section will guide you through building your network on the canvas, assigning QKD protocols, configuring links, and running simulations effortlessly.

## Working with the Canvas

### Using the Canvas and Toolbar

**1. Launch the Simulator**  
 Click the **“Launch Simulator”** button from the main menu or landing page. This opens the interactive canvas interface.

   <p align="center">
     <img src="/docs/assets/launchsim.png" alt="Launch Simulator" width="400">
   </p>

**2. Explore the Toolbar**  
 Once the canvas loads, you will see several key tools on the top toolbar:

   <p align="center">
     <img src="/docs/assets/toolbar.png" alt="Toolbar Options" width="300">
   </p>

&nbsp;&nbsp;&nbsp;&nbsp;- **Add Nodes**: Create devices (systems or ports) on the canvas. These nodes can be connected with links and configured with QKD protocols.<br>
&nbsp;&nbsp;&nbsp;&nbsp;- **Simulate Network**: Run the simulation once you have designed and congigured your network topology. Results such as QBER and key rate will be displayed.<br>
&nbsp;&nbsp;&nbsp;&nbsp;- **Reset**: Clear the canvas to start designing a new network from scratch.<br>

### Configure Nodes and Create Links

<div style="float: right; width: 300px; margin-left: 20px;">
  <img src="/docs/assets/nodeconfig.png" alt="Configuration Panel" width="300">
</div>

Double-click a node to open its configuration panel and establish connections:

- **Node Name**: Custom name for the selected device.
- **From**: Automatically filled with the selected source node.
- **To**: Select the destination node to form a link.
- **Protocol**: Choose a QKD protocol — **DPS QKD** or **CoW QKD**.
- **Cancel**: Close the panel without saving changes.
- **Delete Node**: Remove the node (only if no links are connected).
- **Configure**: Submit parameters and create the link.

<div style="clear: both;"></div>

### Configure Protocol Parameters

When you click **Configure**, you will be directed to one of the following forms depending on the selected protocol — either **DPS QKD** or **CoW QKD**. These forms are pre-filled with default values, which you can modify as needed.

<div style="display: flex; justify-content: space-around; gap: 20px; margin-top: 10px; margin-bottom: 10px;">
  <img src="/docs/assets/DPSform.png" alt="DPS QKD Form" width="300">
  <img src="/docs/assets/COWform.png" alt="CoW QKD Form" width="300">
</div>

Once you click **Save Configuration**, you will return to the canvas where a colored link will appear between your selected systems:

- <span style="color:#00bcd4; font-weight:bold;">Blue</span> for **DPS QKD**
- <span style="color:#ffb300; font-weight:bold;">Yellow</span> **CoW QKD**

You can then click **Simulate Network** to view performance metrics and results.

To delete a link, **left + right click simultaneously** on it and confirm when prompted.

  <p align="center">
     <img src="/docs/assets/delete.png" alt="delete link" width="400">
   </p>
## Running Simulation

After configuring all desired links:

1. Click **Simulate Network**.
2. The system will run backend simulations based on your parameters.
3. A results page will display key metrics like:<br>
   &nbsp;&nbsp;&nbsp;&nbsp; - Quantum Bit Error Rate (QBER)
   &nbsp;&nbsp;&nbsp;&nbsp; - Final key rate

## Available Protocol Parameters

### Common Parameters (for both DPS & CoW)

| Parameter     | Description                                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `distance_km` | Distance between two nodes (in kilometers) over which quantum key distribution is performed.                                                            |
| `fiber_type`  | Type of optical fiber used in the channel. Can be "underground" or "aerial", affecting signal loss.                                                     |
| `mu`          | Mean photons per pulse . Represents the average number of photons sent by Alice per pulse.(0.2 for DPS, 0.1 for CoW by default).                        |
| `pulse_rate`  | Pulse repetition rate (in Hz) at which photons are sent by Alice.                                                                                       |
| `det_eff`     | Detector efficiency. Probability (between 0 and 1) that a photon is successfully detected.                                                              |
| `dark_rate`   | Dark count rate of the detector (counts per second). Represents false clicks due to noise or thermal effects.                                           |
| `dead_time`   | Dead time of the detector (in seconds). It is the interval after each detection during which the detector is inactive and cannot record further events. |
| `visibility`  | Interference visibility, indicating the quality of phase coherence. Values closer to 1 imply ideal interference and lower error rates.                  |
| `num_pulses`  | Number of photon pulses sent by Alice during the simulation. Affects how statistically stable the results are.                                          |

---

### DPS QKD-Specific Parameters

| Parameter           | Description                                                                                                             |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `disclosure_rate`   | The fraction of the raw key disclosed for QBER estimation. Higher values improve accuracy but reduce usable key length. |
| `compression_ratio` | The factor with which the key is shortened during privacy amplification to remove leaked information.                   |

---

### CoW QKD-Specific Parameters

| Parameter                     | Description                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `error_correction_efficiency` | Efficiency of the error correction algorithm used in post-processing. Typically between 0.9 and 1. Higher values preserve more of the key. |

---

> You are now ready to simulate a quantum network! Continue to explore different protocols and settings to understand how quantum communication behaves under varied conditions.
