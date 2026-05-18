# Methodology: True Reinforcement Learning in Chess AI

## 1. Executive Summary & Architectural Paradigm
This document outlines the theoretical foundation and engineering implementation of the **Neon Chess AI**. The project represents a paradigm shift from traditional heuristic chess engines—which rely on static evaluation tables and deep minimax search trees—to an adaptive agent powered by **True Reinforcement Learning (RL)**. 

By employing a **Linear Value Function Approximator**, Temporal Difference ($TD-0$) learning, an experience replay buffer, and a custom asynchronous frontend component bridge, the system achieves both real-time strategic adaptability and zero-latency visual responsiveness.

---

## 2. Theoretical Reinforcement Learning Framework

### 2.1 State Representation & Feature Extraction ($S \rightarrow \vec{f}(S)$)
In classical Deep RL (e.g., AlphaZero), board states are fed into deep convolutional neural networks. To maintain high-speed inference and real-time training within a web browser environment, our AI utilizes a **Linear Value Function Approximator**.

For any given board state $S$, the environment extracts a normalized feature vector $\vec{f}(S) \in \mathbb{R}^n$:
$$\vec{f}(S) = \begin{bmatrix} f_{\text{material}} \\ f_{\text{center}} \\ f_{\text{mobility}} \\ \vdots \end{bmatrix}$$

1. **Material Balance ($f_{\text{material}}$)**: The differential sum of piece values on the board. Standard FIDE relative values are assigned: Pawns ($1.0$), Knights ($3.0$), Bishops ($3.2$), Rooks ($5.0$), and Queens ($9.0$).
2. **Center Dominance ($f_{\text{center}}$)**: A calculated score measuring piece occupancy and direct attacks on the central matrix (`d4, d5, e4, e5`).
3. **Dynamic Mobility ($f_{\text{mobility}}$)**: The branching factor (number of legal moves available) for the active color minus the branching factor of the opponent.

The estimated value of any board state $V(S)$ is computed as the dot product of the feature vector $\vec{f}(S)$ and the agent's learned weight vector $\vec{w}$:
$$V(S) = \vec{w} \cdot \vec{f}(S) = \sum_{i=1}^{n} w_i f_i(S)$$

### 2.2 Temporal Difference ($TD-0$) Weight Optimization
Unlike minimax engines that evaluate positions statically, the `RLAgent` learns dynamically after every match. At the end of an episode, an objective terminal reward $R_T$ is issued:
- **Victory**: $+10,000$
- **Defeat**: $-10,000$
- **Equilibrium (Draw/Stalemate)**: $0$

During gameplay or simulated self-play, all encountered feature vectors and transition states are stored in an **Experience Replay Buffer**. When the episode terminates, the terminal reward is propagated backward through time using the $TD(0)$ learning rule:

$$\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$$
$$\vec{w} \leftarrow \vec{w} + \alpha \cdot \delta_t \cdot \vec{f}(S_t)$$

Where:
- **$\alpha$ (Learning Rate)**: Dictates the step size of weight adjustments per episode.
- **$\gamma$ (Discount Factor)**: Determines the importance of future rewards compared to immediate rewards.
- **$\delta_t$ (TD Error)**: The difference between the estimated state value and the actual observed outcome.

### 2.3 Exploration vs. Exploitation ($\epsilon$-Greedy Policy)
To ensure the AI does not get stuck in suboptimal strategic loops during self-play training, it employs an **$\epsilon$-greedy exploration policy**:
- **Exploration ($\text{Probability } \epsilon$)**: The agent ignores current weights and selects a completely random legal move to discover unexplored positions and tactical variations.
- **Exploitation ($\text{Probability } 1-\epsilon$)**: The agent evaluates all valid successor states using $V(S) = \vec{w} \cdot \vec{f}(S)$ and selects the move with the maximum expected return.

---

## 3. Asynchronous Web & UI Architecture

Building a responsive chess game inside Streamlit presents a fundamental engineering hurdle: standard Streamlit widgets trigger full server-side script reruns on every interaction, causing severe UI flickering and drag-and-drop input lag.

```
+-------------------------------------------------------------------+
|                        STREAMLIT WEB SERVER                       |
|                                                                   |
|   +-----------------------+           +-----------------------+   |
|   |    Python Backend     |           |   React / JS Iframe   |   |
|   |    (app.py / chess)   |           |    (chessboard.js)    |   |
|   +-----------------------+           +-----------------------+   |
|               ^                                   ^               |
|               |        1. JSON: FEN & Legal Moves |               |
|               +-----------------------------------+               |
|               |                                                   |
|               |        2. PostMessage: User Move & Timestamp      |
|               +---------------------------------------------------+
+-------------------------------------------------------------------+
```

### 3.1 Custom Frontend Bridge (`streamlit_chess`)
To bypass server latency, we encapsulated the visual board inside an isolated HTML/JavaScript iframe utilizing `chessboardjs` and jQuery.
1. **Uninterrupted Rendering**: The Python backend passes the current board state (in FEN notation) and a dictionary of legal moves down to the JS iframe during initialization.
2. **Client-Side Physics**: Dragging, sliding animations, and dropping pieces are handled entirely by browser DOM events. The board does not unmount or blink when pieces move.
3. **Atomic Move Reporting**: When a move is completed, JS generates a timestamped payload (`{source: 'e2', target: 'e4', timestamp: 1716000000}`) and posts it back to Python. The backend validates the move against FIDE rules and updates the session state.

### 3.2 Dynamic Visual Move Suggestions
To elevate user experience, the system provides real-time tactical feedback:
- The Python backend precomputes all legal move destinations for every active piece.
- This mapping (`{'e2': ['e3', 'e4'], 'g1': ['f3', 'h3']}`) is sent to the JS client.
- When the user hovers over or clicks a piece, JS intercepts the event and instantly applies glowing neon CSS styles (`.highlight-legal`) to valid target squares, disappearing instantly upon drop or mouse-out.

---

## 4. Telemetry & Real-Time Monitoring
The interface is designed around a cyberpunk aesthetic ("Cyber Neon") and provides deep analytical visibility into the AI's cognitive state:
- **Dominance Ratio Gauge**: Uses dynamic gradient text to show the exact mathematical advantage computed by the value function.
- **Neural Weight Bar Chart**: Live visualization of $\vec{w}$. As the AI trains via self-play, users can observe weights for concepts like "Center Control" or "Knight Mobility" spike or drop in real-time.
- **Execution Log**: Formats move history into clean Standard Algebraic Notation (SAN) pairs.

---

## 5. Conclusion
The Neon Chess AI effectively demonstrates how complex Reinforcement Learning models and high-performance asynchronous web components can be seamlessly merged. By combining $TD(0)$ weight updates with browser-native drag-and-drop mechanics, the project delivers an exceptionally smooth, intelligent, and visually striking chess experience.
