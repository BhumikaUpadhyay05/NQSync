# Installation Guide

This guide provides step-by-step instructions for installing and setting up the NQSync QKD Simulation Platform on your system.

## System Requirements

### Minimum Requirements

- **Operating System:** Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python:** 3.9 or higher supported by Flask

### Recommended Requirements

- **Operating System:** Windows 11, macOS 12+, or Ubuntu 20.04+
- **Python:** 3.10 or higher

## Prerequisites

### Python Installation

1. **Download Python:** [https://www.python.org](https://www.python.org)
2. **Install Python:** Run the installer and check “Add Python to PATH”
3. **Verify Installation:** Run this in your terminal/command prompt :
   ```bash
   python --version
   pip --version
   ```

### Git Installation

1. **Download Git:** [https://git-scm.com](https://git-scm.com)
2. **Install Git:** Use default settings during installation
3. **Verify Installation:** Run this in your terminal/command prompt :
   ```bash
   git --version
   ```

## Installation Methods

### Method 1: Clone from Repository (Recommended)

**1. Clone the Repository:**

```bash
git clone https://github.com/BhumikaUpadhyay05/NQSync.git
cd NQSync
```

**2. (Optional) Create and Activate Virtual Environment:**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. Install Python Dependencies:**

```bash
pip install -r requirements.txt
```

**4. Launch the Application:**

```bash
python app.py
```

You will be directed to the **NQSync homepage** in your default browser.

### Method 2: Download ZIP Archive

1. **Download ZIP:** Navigate to the GitHub repository, click "Code" → "Download ZIP".
2. **Extract:** Unzip to your desired location.
3. Follow steps 2-4 from Method 1.

## Platform-Specific Instructions

### Windows

```bash
# Open Command Prompt or PowerShell as Administrator
# Then follow Method 1
```

### macOS

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python
brew install git

# Then follow Method 1
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3 python3-pip python3-venv
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install git

# Then follow Method 1
```

You are now ready to simulate a quantum network!
[Quick Start Guide](Getting-Started.md) – Learn how to run your first simulation
