# School Project: Basic Ransomware Simulation

**Please Note:** This code is intended for educational purposes only and shouldn't be used in malicious ways. Misuse can be illegal and unethical.

## Project Overview

This project consists of three Python scripts that work together to simulate the behavior of real-life ransomware:

1. **noaransomware.py:** This is the main ransomware code. It contains functions to find and encrypt files using a key generated from the `cryptography.fernet` Python module. Before encryption, the script establishes a connection with the middleman server to retrieve the LAN IP of the target device to set up the backdoor.

2. **decrypt.py:** This file contains the code to decrypt files that have been encrypted by the ransomware. The script retrieves the encryption key from "thekey.key" and applies it to the encrypted files, restoring them to their original form.

3. **middleserver.py:** This script acts as the middleman server, responsible for relaying information between the ransomware and the outside world, adding a layer of obfuscation to the ransomware's activities. This script manages connections for two different purposes: setting the target IP for the ransomware (password protected) and providing the said IP to our ransomware.

## How To Run

To correctly execute these programs, you will need Python and the `cryptography` package installed on your system. If the `cryptography` package isn't already installed, you can add it using pip:

```bash
pip install cryptography
```

Next, to run the program:

1. Launch the middleman server with the command `python middleserver.py`
2. On a separate terminal (or computer), run the ransomware with the command `python noaransomware.py`
3. If you want to decrypt files, run `python decrypt.py`

Ensure the scripts run on machines within the same network.

Remember to be responsible when running these scripts! Do not attempt to run the ransomware on any computer to which you do not have explicit permission.

## Understanding the Code

Take the time to go through the Python scripts and understand how they work together. This can be very beneficial in improving your understanding of real-world cyber threats and how to protect yourself (or a network you manage) from them.

Ransomware is an unfortunate reality of the modern world, and understanding how it works is an important part of any cybersecurity education. This project is a simplified example of a real-world ransomware attack, but the concepts here – secure keys, file encryption, network communication – are directly applicable to advanced threats. Be sure to read and understand the comments in the code, as they are there to help you understand what's happening!

## Contributing

This being a school project, collaboration is welcomed! If you have any ideas on how to improve the simulation or the readability of the code, don't hesitate to make changes and submit a pull request.