A script made for quick changing of keybind sets for different players of the polish annual GTA 3D Trilogy 100% relay. Guaranteed to work on Windows, not tested on other systems (the `mouse` package only works with Windows and Linux with sudo). Allows for easy binding of keyboard and mouse keys (and the scroll wheel) to keyboard keys, rebinding *to* mouse was not needed and is therefore not supported right now.

# Prerequisites:
- [Python 3](https://www.python.org/downloads/)
- [keyboard](https://pypi.org/project/keyboard/)
- [mouse](https://pypi.org/project/mouse/)
- [pyyaml](https://pyyaml.org/)

# Installation

Download the files
- Clone the repo:
```
git clone https://github.com/PokerFacowaty/bindsbindsbinds
```
- ... or simply download `bindsbindsbinds.py` and `binds.yaml` and store them in the same directory

# Configuration
- Set up the keybind mapping(s) in binds.yaml using the provided 'defaults' set as reference. You can simply copy the entire set, paste it at the end of the file and change the name from 'defaults' if you wish to have multiple sets.

# Usage
```
python bindsbindsbinds.py
```

It will list all the keybind sets read from the yaml file and you can switch between them easily with Ctrl+Alt key combinations