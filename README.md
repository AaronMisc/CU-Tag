# Leveldotpy Game

Leveldotpy is a local multiplayer game, where you can play tag on one computer (but two keyboards are recommended for many players.)

## Features
- **Menu**: Menu with Start Game, Settings, Instructions, Credits, and Quit.
- **Game**: Tag other players, and be tagged for the least time to win. A very fun game.
- **Good performance**: Optimised, FPS around 100-300 for low-end PCs. Deltatime movement.
- **Customizable Settings**: Modify the game in settings.
- **Instructions**: How to use the program and play the game. Debug functions.

## Dependencies
The following Python libraries and modules are required to run the game:
- `pygame`
- `pygame_gui`
- `pytmx`
- `tabulate`
- `sys` (built-in)
- `math` (built-in)
- `os.path` (built-in)
- `random` (built-in)

## Starting Program
### Prerequisites
- Python 3.x (recommended: 3.12.0)
- If you have a version before 3.4, install pip

### Windows
Open Microsoft Powershell
To update pip:
`python.exe -m pip install --upgrade pip`

To install libraries
`pip install pygame pygame_gui pytmx tabulate`

### Apple (MacOS)
Open Terminal
To update pip:
`pip3 install --upgrade pip`

To install libraries:
`pip3 install pygame pygame_gui pytmx pytimer tabulate`

### Debugging
If there are errors, try using the community edition of pygame.
For windows:
1. `pip uninstall pygame`
2. `pip install pygame-ce`

## Usage
Use buttons to navigate.

### Game States
1. **Menu**: Default start state.
2. **Game**: The actual gameplay. Click start to start the game.
3. **Game Stats**: View player statistics post-game.
4. **Settings**: Adjust game options.
5. **Instructions**: Learn how to play.
6. **Credits**: View acknowledgments.

### Keyboard Shortcuts
- **F1**: Toggle Player List
- **F2**: Toggle Label Player Names
- **F3**: Toggle FPS Display
- **F4**: Toggle Player Keybinds
- **F5**: Toggle Player Tag Times
- **F11**: Switch Fullscreen Mode
- **ESC**: Return to Menu
- **DELETE**: Reset game (in-game only, after 5 presses).

## License
This project is licensed under the Apache-2.0 License. [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Acknowledgements
### Project
- **Name**: AaronMisc  
- **Title**: Leveldotpy  
- **Version**: Alpha 1.0  
- **Repository**: [GitHub - Leveldotpy](https://github.com/AaronMisc/Leveldotpy/)  
- **Published on**: 08/03/2025  

### Language and Libraries
- [Pygame](https://www.pygame.org/): A set of Python modules designed for writing video games.
- [Pygame GUI](https://pygame-gui.readthedocs.io/): A GUI toolkit for use with `pygame`.
- [Pytmx](https://github.com/bitcraft/pytmx): A simple library for reading Tiled Map Editor files.
- [Tabulate](https://pypi.org/project/tabulate/): Coverting lists to tables in Python.

### **Resources Used**
- **Fonts**: *Consolas* by Luc(as) de Groot.
- **Images**: Created using Pixilart ([Pixilart Website](https://www.pixilart.com)).
- **Level Editor**: Tiled ([Tiled Map Editor](https://www.mapeditor.org)).

### Special Thanks
**ClearCode - Platformer Tutorial**. Basics of a platformer in Pygame.
- [YouTube - Platformer Tutorial Video](https://www.youtube.com/watch?v=WViyCAa6yLI)
- [ClearCode's Chanel](https://www.youtube.com/@ClearCode)
