# J-Link Firmware Loader

This repository contains two versions of a Tkinter-based application for loading firmware onto an XMC4700-2048 microcontroller using a J-Link device. One version uses the `subprocess` module to interact with J-Link Commander, and the other uses the `pylink` library.

## Features

- Select firmware file via file dialog
- Load firmware onto XMC4700-2048 at 4000 kHz speed in SWD mode
- Display success or error messages in a message box

## Requirements

- Python 3.6+
- `tkinter` (usually included with Python)
- `pylink-square` (for the pylink version)
- `pyinstaller` (for building executables)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/jlink-firmware-loader.git
    cd jlink-firmware-loader
    ```

2. Install the required Python packages:
    ```sh
    pip install pylink-square
    pip install pyinstaller
    ```

## Usage

### Running the Application

You can run either version directly with Python:

- **Subprocess Version:**
    ```sh
    python subprocess_jlink_loader.py
    ```

- **Pylink Version:**
    ```sh
    python pylink_jlink_loader.py
    ```

### Building Executables

Batch files are provided to build standalone executables using `pyinstaller`:

- **Build Subprocess Version:**
    ```sh
    build_subprocess_jlink_loader.bat
    ```

- **Build Pylink Version:**
    ```sh
    build_pylink_jlink_loader.bat
    ```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PyLink](https://pypi.org/project/pylink-square/) - Python interface to J-Link.
- [PyInstaller](https://www.pyinstaller.org/) - Freezes Python applications into stand-alone executables.

