# School Project: Basic Ransomware Simulation

**Please Note:** This code is intended for educational purposes only and shouldn't be used in malicious ways. Misuse can be illegal and unethical.

## Project Overview

This project consists of three Python scripts that work together to simulate the behavior of real-life ransomware:

1. **noaransomware.py:** This is the main ransomware code. It contains functions to find and encrypt files using a key generated from the `cryptography.fernet` Python module. Before encryption, the script establishes a connection with the middleman server to retrieve the LAN IP of the target device to set up the backdoor (more on the backdoor later).

2. **decrypt.py:** This file contains the code to decrypt files that have been encrypted by the ransomware. The script retrieves the encryption key from "thekey.key" and applies it to the encrypted files, restoring them to their original form.

3. **middleserver.py:** This script acts as the middleman server, responsible for relaying information between the ransomware and the outside world, adding a layer of obfuscation to the ransomware's activities. This script manages connections for two different sessions: setting the local IP for the `notaransomware.py` scipt to give a reverse shell to (password protected) and providing the said IP to our ransomware. That is to say that the middleman script will allow a connection from the attackers machine in order for said machine to advertise its lcoal IP and another session for the ransomware to fetch said LAN IP. It does not have to be a local IP though, any IP will work but LAN is more secure.

## Why a backdoor and why a middleman?

We have the backdoor, or reverse shell, in order for the attacker to examine the target in order to find the best files in which to hold ransom. Once the attacker has found the files to encrypt, he executes a command within the reverse shell (running within the `notaransomware.py` script) which will finalise the attack.
We have the middle man because the attackers IP might change but the middleman servers IP can stay constant.

## !! Word of warning !!

USE THIS PROJECT AT YOUR OWN RISK, THE PROJECT IS DESIGNED TO BE AS REAL TO REAL LIFE RANSOMWARE ATTACK AS IT CAN BE SO YOUR DATA IS YOUR RESPONISBILITY.
I **ONLY** RECCOMEND RUNNING THESE SCRIPTS INSIDE A VIRTUAL MACHINE!!!

**NO ONE BUT YOU IS RESPONSIBLE FOR YOUR ACTIONS!**

## How To Run

To correctly execute these programs, you will need Python3 and the `cryptography` package installed on your system. If the `cryptography` package isn't already installed, you can add it using pip:

```bash
pip install cryptography
```

Next, to run the program:

1. Launch the middleman server with the command `python3 middleserver.py`.

You will see the server spring to life, printing basic messages to let you know whats going on.

2. On the attack machine, make sure you have netcat installed and run `ncat -lvnp 35038`. This will instruct netcat to listen `-l` verbosely `-v` idk `-n` and `-p` specifies the port.

You will use this netcat session once the ransomware opens a backdoor for us.

4. On your victim computer, run the ransomware with the command `python noaransomware.py`.

The script immideiately try connecting to the middleman server, if it fails to connect, it will retry and retry again.
Once it has connected to the middleman server, it will ask the middleman server for the attackers ip.
Once recieved the attackers IP, the ransomware script will open a backdoor to the attacker.

The attacker can then go on looking for some juicy files within the system to encrypt (your job).
Once you found your juicy files, run `:attack` inside the backdoor (again, the netcat seesion).

4. If you want to decrypt files, run `python decrypt.py`

Ensure the scripts run on machines within the same network.

Remember to be responsible when running these scripts! Do not attempt to run the ransomware on any computer to which you do not have explicit permission.

## Understanding the Code

Take the time to go through the Python scripts and understand how they work together. This can be very beneficial in improving your understanding of real-world cyber threats and how to protect yourself (or a network you manage) from them.

Ransomware is an unfortunate reality of the modern world, and understanding how it works is an important part of any cybersecurity education. This project is a simplified example of a real-world ransomware attack, but the concepts here – secure keys, file encryption, network communication – are directly applicable to advanced threats. Be sure to read and understand the comments in the code, as they are there to help you understand what's happening!

## Contributing

This being a school project, collaboration is welcomed! If you have any ideas on how to improve the simulation or the readability of the code, don't hesitate to make changes and submit a pull request.
