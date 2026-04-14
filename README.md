An advanced, production-grade implementation of the classic Snake Game in Python. Instead of just manual controls, this project features an **Autonomous AI Agent** powered by the **A* (A-Star) Pathfinding Algorithm**.

This project demonstrates the practical application of Artificial Intelligence and pathfinding algorithms in real-time environments.

## ✨ Key Features

* **Dual Play Modes:**
  * **Manual Control:** Play the classic game using Arrow Keys.
  * **AI Auto-Pilot:** Press `A` to hand over the controls to the AI. Watch the snake autonomously calculate the shortest path to the food!
* **A* Pathfinding:** The AI uses the A* search algorithm combined with the *Manhattan Distance* heuristic to find the most optimal route.
* **Dynamic Obstacle Avoidance:** The algorithm intelligently treats the screen boundaries and the snake's own growing body as impassable obstacles, recalculating the path on every single frame.
* **Clean & Modern Code:** Built using Python `dataclasses`, explicit type hinting, and a logical, modular architecture.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Library:** Pygame (for rendering and the game engine)
* **Algorithms:** A* Search, Manhattan Distance Heuristic
* **Data Structures:** Priority Queues (`heapq`)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/khanwarda/AI-Snake-Game-AStar.git
   cd AI-Snake-Game-AStar
2. **Install the required dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
3. **Run the game:**
   ```bash
   python snake.py
## 🎮 How to Play / Controls

* **Arrow Keys (Up, Down, Left, Right):** Move the snake manually.
* **Key `A`:** Toggle AI Auto-Pilot ON or OFF. (The snake turns **Blue** when AI is active).
* **Key `SPACE`:** Restart the game after Game Over.
* **Key `ESC`:** Quit the application.

## 🧠 How the AI Logic Works

The core of this autonomous agent is the `AStarAI` class:

* **Grid as a Graph:** The game window is treated as a grid where each block is a node.
* **Heuristic Evaluation:** It calculates the distance from the snake's head to the food using *Manhattan Distance*.
* **Cost Calculation:** Using a priority queue (`heapq`), it constantly evaluates the lowest-cost path while avoiding coordinates occupied by the snake's body (`snake_body[:-1]`).
* **Fallback Mechanism:** If the snake gets trapped and no valid path to the food exists, the AI defaults to the first available safe move to prolong survival.

## 🖼️ Gameplay Showcase

### 🕹️ Manual Mode (Score: 14)
<img width="1075" height="690" alt="Screenshot 2026-04-14 214653" src="https://github.com/user-attachments/assets/234406b2-18ee-4d5e-9919-34d3e3090774" />


### 🤖 AI Auto-Pilot (Optimal Pathfinding)
<img width="1152" height="675" alt="Screenshot 2026-04-14 214619" src="https://github.com/user-attachments/assets/280cb109-a0ca-4dcc-b3ac-36321f8ea1dd" />



### 💀 Game Over & Collision
<img width="1160" height="707" alt="Screenshot 2026-04-14 214529" src="https://github.com/user-attachments/assets/f7ed3283-2423-4f07-b9ef-0fa12d8a8398" />


---
**Developed by:** Warda Khan  
*Tech Trainer & Applied AI Enthusiast*
