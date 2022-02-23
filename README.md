# Welcome to My Game Clones Repository

This repository contains clones of Pong, Breakout, and Tic-Tac-Toe that were made with python and pygame. The code is straight forward and non-modular. Feel free to fork and to learn some basics of making games with pygame and/or improve the code by refactoring or adding additional features.

# Requirements
To run the python scripts the following are required:
- python 3.9.7 or higher
- pygame 2.0.1 or higher

First download/fork the repo, than install the required packages by using pip and the provided _requirements.txt_:
```bash
pip install -r requirements.txt
```

Or by creating a new conda environment with _environment.yml_:
```
conda env create -f environment.yml
```

Once your environment is setup, activate it (if using conda):
```bash
conda activate pygames
```
__NOTE__: the default conda environment name is pygame. You can change this in _environment.yml_

Than navigate via the command line to the folder containing the game you wish to play (e.g. from the top level directory of the repository):

```bash
cd tictactoe
python tictactoe.py
```

__NOTE__: games will not load correct assets if run from the top level directory via
```bash
python ./pong/pong.py
```
You should run the game from its own directory

# ENJOY!!
