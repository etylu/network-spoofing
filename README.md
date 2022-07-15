# Spoof Media Control Access (MAC) Address
This directory enables the user to disguise their device's MAC address. To successfully utilize this service, Python3 must be installed within the Linux OS. To check which version of Python has come preinstalled with the OS run the following command (upgrade as you see fit):

```
$ python --version
```

After upgrading your version of Python, its time to setup the Python virtual environment by running the following commands:

```
$ python3 -m venv env
$ env/bin/pip3 install -r requirements.txt
```

The above commands may vary per your preferred aliases. But essentially, you will need to initialize a virtual environment named `env` and and install the Python libraries `python-contracts` in said environment.

Within the terminal run the following command to activate the service:

```
$ python3 core.py {the name of your interface} -r
```

The `-r` indicates that a randomized MAC address is desired.
