### Distance & Loss

- **`Distance_km`** – Distance in kilometers between the sender (Alice) and receiver (Bob) in the fiber-optic network.

- **`Fiber_Type`** – Type of optical fiber used for transmission:  
  &nbsp;&nbsp;&nbsp;&nbsp;• **`Underground`** – Fiber lines laid below the surface, typically experience a loss of **0.2 dB/km**. These are more stable and less affected by environmental conditions.  
  &nbsp;&nbsp;&nbsp;&nbsp;• **`Aerial`** – Fiber lines suspended above ground (e.g., on poles), experience slightly higher attenuation at around **0.3 dB/km**, due to exposure to weather and physical disturbances.

- **`Channel_Loss_dB`** – Total optical power loss calculated as `α × distance`, where `α` is the attenuation coefficient based on fiber type.

- **`Transmittance`** – The ratio of power successfully transmitted through the fiber, computed as `T = 10^(-loss_dB / 10)`.

### Signal & Detection

- **`Signal_Probability_per_Pulse`** – Probability that a signal photon sent by Alice is successfully detected by Bob is:  
  `μ × T × η`, where:  
  `μ` = mean photon number  
  `T` = transmittance  
  `η` = detector efficiency

- **`Detection_Probability`** – Total probability that a pulse results in detection (including both signal and noise) is:<br>
  `P_signal + (dark_rate / pulse_rate)`

### Key Rate Calculations

- **`QBER`** –Quantum Bit Error Rate, the fraction of incorrect bits shared between Alice and Bob, given by:<br>
  `bit_errors / comparable_bits`.
- **`Bit_Errors`** – Number of mismatched bits between Alice and Bob during key comparison.
- **`Key_Match_Ratio`** – `1 - QBER`, percentage of matching bits.
- **`Raw_Key_Rate_bps`** – Initial bit rate of key generation based on detection probability, given by: <br>`R_raw = (pulse_rate × P_detect) / (1 + pulse_rate × P_detect × dead_time)`.
- **`Sifted_Key_Rate_bps`** – Rate of key bits retained after sifting.(~50% of raw key is usable.) given by: <br>`R_sifted = 0.5 × R_raw`
- **`Final_Key_Rate_bps`** – Final usable key rate after error correction:

  &nbsp;&nbsp;&nbsp;&nbsp;• **`DPS QKD`** –  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`R_final = R_sifted × (1 - disclosure_rate) × (1 - compression_ratio)`

  &nbsp;&nbsp;&nbsp;&nbsp;• **`CoW QKD`** –  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`R_final = R_sifted × (1 - error_correction_efficiency × QBER)`

### Bit & Detection Statistics

- **`Raw_Key_Length_Alice`** – Total number of bits Alice attempted to encode and transmit.
- **`Raw_Key_Length_Bob`** – Total number of bits detected and stored by Bob.
- **`Num_Detections`** – Total detections, including both signal-based and dark counts.
- **`Signal_based_Detections`** – Count of detections caused by actual signal photons.
- **`Dark_only_Detections`** – Detections that occurred due to detector noise or false positives (not actual signal).
- **`Comparable_Bits`** – Bits that are eligible for comparison between Alice and Bob to compute QBER.
- **`Visibility`** – Depicts interference quality. Affects how accurately Bob can infer Alice’s bit from phase differences.
