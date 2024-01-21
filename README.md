# Project Overview

This project serves as a dedicated server for the JustStone backdoor and STP (Stone Transfer Protocol). It is currently designed to operate as a standalone server, facilitating communication with the JustStone backdoor. Future plans include transforming it into a Command and Control (C&C) server. Subsequent to this transformation, a dedicated client is being developed to interact with the C&C server.

## Components:

- **JustStone Backdoor:** The server interacts with the JustStone backdoor, providing a platform for communication and control.

- **STP Protocol:** The Stone Transfer Protocol (STP) is employed for efficient and secure data exchange between the server and the backdoor.

## Future Development:

The project is in the process of transitioning into a C&C server, which will enable centralized control and management of multiple backdoors.

A dedicated client is currently under development to complement the transformed C&C server. This client will facilitate seamless interaction and control over the backdoors connected to the C&C server.

## Usage:

To run the server, you need three libraries: `secrets`, `datetime`, and `argparse`. Use the following pip commands to install each library:

```bash
pip install secrets
pip install datetime
pip install argparse
```

When running the server, you can use command-line arguments:

- `-a`: Please enter the IP address of the PC to be used as the server. The default value is localhost.
- `-p`: Please enter the port number the server will use. The default value is 6974.

Example usage:

```bash
python server.py -a <IP_ADDRESS> -p <PORT_NUMBER>
```

**Note:** Ensure to install the required libraries before running the server.

## How to Contribute:

Contributions to the project are welcome. If you wish to contribute, please check the [contributing guidelines](CONTRIBUTING.md) for more information. Your insights and enhancements are valuable to the project's development.

**Disclaimer:** This project is intended for educational purposes only. Usage for unauthorized or malicious activities is strictly prohibited.

# Version Information

**Requirements:**
This project requires Python version 3.11 or later. Please ensure that you have the correct Python version installed before running the server.

## How to Check Python Version:

You can check your Python version using the following command in the terminal or command prompt:

```bash
python --version
```

or

```bash
python -V
```

If your current Python version is below 3.11, please update to the latest version available on the official [Python website](https://www.python.org/downloads/).

## Note:

Ensure that the correct Python version is installed to guarantee compatibility and smooth execution of the server. If you encounter any issues related to Python version compatibility, updating to the specified version is recommended.

**Disclaimer:** The project's version requirements are designed to ensure optimal performance and functionality.
