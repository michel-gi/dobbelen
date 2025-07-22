# Dobbelen Project

A collection of Python tools for simulating dice rolls and analyzing the resulting probability distributions. This project features several graphical and console-based applications built with `tkinter`, `matplotlib`, and `numpy`.

## Features

This project consists of several standalone applications:

### GUI Applications

* **`dobbelsteen_simulatie`**: The main application for running various dice roll simulations and visualizing the outcomes. It includes an icon and version information.
* **`vergelijk_verdelingen`**:  A tool to visually compare different probability distributions generated from simulations.
* **`plot_eindpunt_kansen`**:  An application to plot the probabilities of final outcomes in multi-step simulations.

### Console Applications

* **`tekstdb_bewerk`**: A command-line tool for managing the text-based database (`database.py`) used by the applications.
* **`tekstdb_tester`**: A utility to test the integrity and functionality of the text database.

## Getting Started

The easiest way to use these tools is to download the pre-built executables for your operating system from the project's GitHub Releases page.

1. Go to the [**Releases**](https://github.com/[your-github-username]/[your-repo-name]/releases) page of this repository.
2. Find the latest release.
3. Under the **Assets** section, download the file corresponding to your operating system (Windows, macOS, or Linux) and the script you want to use.

### Running the Applications

* **Windows**: Download the `.exe` file and double-click it to run.
* **macOS / Linux**: Download the executable file. You may need to make it executable before running it from your terminal:

    ```bash

    # Example for the main simulation on Linux
    chmod +x ./dobbelsteen_simulatie-linux
    ./dobbelsteen_simulatie-linux
    ```

## Building from Source

If you prefer to build the applications yourself, you can do so by following these steps.

### Prerequisites

* Python 3.12
* Git

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/[your-github-username]/[your-repo-name].git
    cd dobbelen
    ```

2. **Set up a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Build with PyInstaller:**
    The project uses PyInstaller to create the executables. The build process is defined in the GitHub Actions workflow at `.github/workflows/build.yml`.

    To build a specific script, you can run one of the following commands:

    ```bash
    # For a GUI application like dobbelsteen_simulatie
    pyinstaller --onefile --windowed --hidden-import PIL._tkinter_finder dobbelsteen_simulatie.py

    # For a console application like tekstdb_bewerk
    pyinstaller --onefile --console tekstdb_bewerk.py
    ```

    The resulting executable will be located in the `dist/` directory.

## Continuous Integration

This project uses GitHub Actions for Continuous Integration and Continuous Deployment (CI/CD). On every push to the `main` branch, the following automated process is triggered:

1. Jobs are initiated for Windows, macOS, and Linux environments.
2. All Python dependencies from `requirements.txt` are installed.
3. PyInstaller builds executables for all five scripts on each operating system.
4. The built executables are uploaded as artifacts.
5. A new GitHub Release is automatically created and tagged with the current timestamp, attaching all the cross-platform executables as downloadable assets.
