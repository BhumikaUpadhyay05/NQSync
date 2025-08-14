## Project Layout

This section describes the overall directory layout and key files of the **NQSync QKD Simulation App** project.

    app.py                     # Main Flask application file.
    requiremnets.txt           # Python dependencies
    venv/                      # Virtual environment for the project (optional).

    static/                    # Frontend static assets.
        images/                # All images used in HTML and documentation.
        style.css              # Custom CSS for coming soon page.
        styles.css             # Custom CSS for the Home page of NQSync.
        styless.css            # Custom CSS for the canvas.


    templates/                 # HTML templates rendered by Flask.
        main_index.html        # Landing/home page of the app.
        canvas.html            # Interactive simulator canvas interface.
        dps_form.html          # Configuration form for DPS QKD protocol.
        cow_form.html          # Configuration form for CoW QKD protocol.
        results.html           # Displays simulation results
        coming_soon.html       # Placeholder for upcoming SDK simulation feature.


    mkdocs-docs/               # Documentation folder.
        mkdocs.yml             # MkDocs configuration file.
        docs/                  # All markdown pages and related assets.
            index.md           # Documentation homepage.
            Contents/          # Contains Other markdown pages like Introduction.md, Installation Guide.md etc.
            styles/            # Contains extra.css for styling
            assets/            # Contains the images used in the documentation

        venv/                  # Virtual environment for documentation (optional).

<br>

---

## System Architecture

This section explains the architectural components behind the **NQSync QKD Simulation Platform**.

---

### Backend

The backend is implemented using **Python (Flask)**, providing the core logic for QKD protocol simulations.

**Key Features:**

- RESTful API using `GET` and `POST` requests
- Theory-compliant simulation models for:<br>
  &nbsp;&nbsp;&nbsp;&nbsp;- **DPS-QKD** (Differential Phase Shift)<br>
  &nbsp;&nbsp;&nbsp;&nbsp;- **CoW-QKD** (Coherent One-Way)

**Main Functions:**

```python
def simulate_cow_qkd(distance_km, fiber_type='underground', mu=0.1, pulse_rate=1e9,
                     det_eff=0.2, dark_rate=100, dead_time=20e-6,
                     error_correction_efficiency=0.9, visibility=0.98, num_pulses=100000):
    ...

def simulate_dps_qkd(distance_km, fiber_type='underground', mu=0.2, pulse_rate=1e9,
                     det_eff=0.06, dark_rate=800, dead_time=20e-6,
                     disclosure_rate=0.03125, compression_ratio=0.5,
                     visibility=0.98, num_pulses=10000000):
    ...
```

### API Methods

The Flask backend exposes the following HTTP methods for client interaction:

- **GET** – Used for rendering pages and serving static files.
- **POST** – Used to handle form submissions and trigger QKD simulations based on user input.

### Web Frontend

The frontend is built using **HTML + CSS+ JavaScript** and provides an interactive and visual user interface.

- **Network Topology Builder**
  Drag-and-drop interface for visually creating QKD network topologies.

- **Protocol Configuration Modals**
  Interactive forms for assigning protocol and hardware parameters to each link.

- **Results**
  Displays simulation metrics (e.g., QBER, key rate) .

These files define the structure and flow of the **user interface** in the NQSync web app:

```plaintext
main_index.html     #  Landing/home page of the application.
canvas.html         #  Interactive simulator canvas for building networks.
dps_form.html       #  Configuration form for the DPS QKD protocol.
cow_form.html       #  Configuration form for the CoW QKD protocol.
results.html        #  Displays simulation results.
coming_soon.html    #  Placeholder for the upcoming SDK simulation module.

```
