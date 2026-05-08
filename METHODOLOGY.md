# Methodology: Chess RL AI

## 1. Project Overview
This project implements an intelligent Chess Engine integrated with a modern, interactive web interface. The core objective was to apply **Advanced Machine Learning** concepts—specifically Reinforcement Learning (RL) principles and tree-search optimization—to create a responsive and competitive AI.

## 2. Theoretical Framework

### 2.1 Reinforcement Learning (RL) Foundation
While deep RL agents (like AlphaZero) use Neural Networks, this project utilizes a **Classical RL-Adjacent Approach**:
- **State Space**: The $8 \times 8$ chessboard with $64$ squares, each potentially containing one of $12$ piece types.
- **Action Space**: All legal chess moves according to FIDE rules.
- **Reward Function**: 
  - Win: $+10,000$
  - Loss: $-10,000$
  - Draw: $0$
  - Intermediate rewards are calculated via the **Evaluation Function**.

### 2.2 Search Optimization: Minimax with Alpha-Beta Pruning
The agent uses the **Minimax algorithm** to explore future states. To handle the high branching factor of chess ($\approx 35$), **Alpha-Beta Pruning** is implemented.
- **Alpha ($\alpha$)**: The best value that the Maximizer (White) can currently guarantee.
- **Beta ($\beta$)**: The best value that the Minimizer (Black) can currently guarantee.
- **Pruning**: If at any point $\beta \leq \alpha$, the branch is discarded, significantly reducing the search space from $O(b^d)$ to $O(b^{d/2})$.

### 2.3 Heuristic Evaluation Function
The agent evaluates positions using a combination of **Material Value** and **Piece-Square Tables (PST)**:
- **Material Value**: Static values assigned to pieces (Pawn: 100, Knight: 320, etc.).
- **Positional Evaluation (PST)**: 64-value matrices that provide bonuses/penalties based on piece placement (e.g., Knights are rewarded for being central; Pawns for advancing).

## 3. Implementation Methodology

### 3.1 Software Architecture
- **Backend Logic**: Python's `chess` library for move validation and state management.
- **AI Engine**: Custom implementation of Minimax with iterative deepening and move ordering (Captures > Checks > Quiet moves).
- **Frontend**: Streamlit-based web interface.

### 3.2 UI/UX Design Evolution (Interactive Movement)
To achieve "Realistic Movement," the project transitioned from text-based UCI input to a **State-Driven Clickable Grid**:
1. **Grid Generation**: Dynamically rendering 64 buttons using Streamlit columns.
2. **State Machine**:
   - `Selection State`: Identifying the source square.
   - `Movement State`: Validating and executing the move to the target square.
3. **Visual Fidelity**: Using high-quality SVG assets (Lichess theme) and dynamic CSS injection for real-time feedback (Highlights, legal move dots).

## 4. Performance Analysis
The engine's performance scales with depth:
- **Depth 2**: Immediate responses ($\approx 50$ nodes), suitable for beginners.
- **Depth 4**: Strategic play ($\approx 1,500$ nodes), suitable for intermediate players.
The use of **Move Ordering** ensures that Alpha-Beta pruning is at its most efficient by searching the "best" branches first.

## 5. Conclusion
The resulting application demonstrates a successful synthesis of classical AI search techniques and modern web design, providing a high-fidelity environment for human-AI interaction in the context of Reinforcement Learning.
