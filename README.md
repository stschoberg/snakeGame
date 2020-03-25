# snakeGame

This is a project to implement different AI solutions to solve the classic snake game. All of the AI implementations are my own however the game itself is built from a tutorial by techwithtim linked below.


[Here](https://medium.com/@stschoberg/playing-snake-with-ai-2ea68f0e914a) is some analysis of the algorithms


https://techwithtim.net/tutorials/game-development-with-python/snake-pygame/

## Installation

```bash
git clone https://github.com/stschoberg/snakeGame.git
```
## Usage

The game has various runmodes
1. keys - the user plays the game with the arrowkeys
2. random - the ai chooses a random path with no respect for the snack
3. shortest - the ai chooses the shortest path to the snack
4. better-shortest - the ai chooses the shortest path to the path but will avoid its own body
5. hamiltonian - guarenteed to win. takes a while

```bash
python3 playSnakeGame.py --option # where option is a mode listed above
```

