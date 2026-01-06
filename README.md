## Delve: Procedural Cave Pathfinding
Delve is a Python-based procedural simulation that addresses the limitations of static game environments. By leveraging Perlin Noise, the project generates infinite, non-repeating cave terrains, providing a unique navigational challenge in every session.

Built as a "Gold Miner" themed maze game, the player (a gold square) must navigate through complex, algorithmically generated caverns to reach the exit (a green square).

## 🚀 Features
Infinite Procedural Generation: Uses Perlin Noise algorithms to create organic, cave-like structures that never repeat.

Dynamic Pathfinding: Challenges players to find routes through winding mazes and narrow tunnels.

Leaderboard System: Integrated SQLite database to track performance, including:

Level Number

Map Seed (for replayability)

Completion Time

Real-time Visualization: Powered by Pygame for smooth rendering of the terrain and player movement.

## 🛠️ Tech Stack
Language: Python 3.x

Graphics: Pygame

Math/Noise: Perlin Noise algorithm for terrain generation

Database: SQLite3 for persistent local storage of high scores

## ⚙️ Installation
Clone the repository:

Bash

git clone https://github.com/iamdanielvarghese/Delve.git
cd Delve
Install dependencies: Ensure you have Python installed, then run:

Bash

pip install pygame
## 🎮 How to Play
Run the main script to start the simulation:

Bash

python main.py

Objective: Navigate the gold square to the green exit.

Controls: Use the Arrow Keys or WASD to move through the cave.

Goal: Complete the levels as fast as possible to secure a spot on the leaderboard.

## 🏗️ Future Roadmap
[ ] Implement A* Pathfinding visualization to compare human vs. AI performance.

[ ] Add different biomes and environmental hazards.

[ ] Launch a full fledged game

[] Implement a "Fog of War" system where the player can only see tiles within a certain radius, increasing the difficulty and emphasizing exploration.



## Authors
- [Daniel Varghese] (https://github.com/iamdanielvarghese)
- [Adil Muhammed N] (https://github.com/aadillllll)
- [Al Fayaz Hayder]
- [Adithyan]
