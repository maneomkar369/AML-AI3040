# Methodology: True RL Neon Chess AI

## 1. Project Overview
This project completely transitions from static heuristic-based chess (Minimax) to a **True Reinforcement Learning (RL)** architecture. The AI uses self-play and Temporal Difference (TD-Learning) to iteratively learn the value of chess positions based on its own experience.

## 2. RL Architecture

### 2.1 State Representation & Features
The agent evaluates the board using a **Linear Value Function Approximator**: $V(S) = \vec{w} \cdot \vec{f}(S)$.
The feature vector $\vec{f}(S)$ includes:
- Material counts (Pawns, Knights, Bishops, Rooks, Queens)
- Center control
- Mobility (legal move count)

### 2.2 Temporal Difference Learning (TD-0)
Instead of relying on deep tree searches, the agent updates its weights $\vec{w}$ dynamically at the end of each episode using the TD-Learning update rule.
- **Reward Signal**: $+10,000$ for a win, $-10,000$ for a loss.
- **Update Process**: The agent traverses its experience replay buffer, propagating the final reward backward to adjust the weights of states that led to the outcome.

### 2.3 Exploration vs. Exploitation
During self-play training batches, the agent utilizes an **$\epsilon$-greedy policy**:
- With probability $\epsilon$, it makes a random move to discover new board states and strategies.
- With probability $1 - \epsilon$, it exploits its current weight vectors to play the best known move.

## 3. UI/UX & Web Architecture
- **Interactive Component**: Replaced static Streamlit SVG rendering with a custom React/JS bridging component (`chessboardjs`). This eliminates UI flickering and enables native drag-and-drop mechanics.
- **Telemetry Dashboard**: Integrated real-time Streamlit charts (`st.bar_chart`, `st.line_chart`) to visualize the neural weight evolution and win-rate during self-play.
- **Cyberpunk Aesthetic**: Complete CSS injection to redesign the interface with custom Google fonts, neon gradients, and responsive tabbed navigation.
