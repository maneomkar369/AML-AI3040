# Neon Chess AI: True Reinforcement Learning

A fully interactive, high-performance Chess AI built using True Reinforcement Learning (TD-Learning) and a responsive, cyberpunk-themed UI.

## 🚀 Features
- **True Reinforcement Learning**: The agent uses Temporal Difference (TD-0) learning to update its neural weights dynamically.
- **Self-Play Training**: Train the agent in real-time right from the browser. Watch its weight vectors evolve via live telemetry.
- **Interactive Cyberpunk UI**: Drag-and-drop gameplay, glowing neon highlights, smooth piece animations, and live dashboard metrics.
- **Dynamic Suggestions**: Hover over any piece to see valid moves highlighted in real-time.

## 🖥️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🎮 How to Play
- **Gameplay**: Drag and drop pieces on the board to move.
- **Training**: Open the `🧬 RL TRAINING` tab to configure hyperparameters (Epsilon, Alpha, Gamma) and run a Self-Play Batch to make the AI smarter.
- **Analytics**: Watch the `📊 DASHBOARD` tab to see real-time shifts in the agent's dominance ratio and neural weights.
