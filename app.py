import streamlit as st
import chess
import random
import time
import math
import importlib
import streamlit_chess
importlib.reload(streamlit_chess)
from streamlit_chess import st_chess

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Neon Chess AI",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --neon-blue: #00f3ff;
    --neon-purple: #bc13fe;
    --neon-pink: #ff007f;
    --dark: #050510;
    --dark2: #090914;
    --dark3: #111122;
    --dark4: #1a1a35;
    --border: #2a2a4a;
    --text: #e2e2ff;
    --muted: #8888aa;
    --green: #00ffcc;
    --red: #ff3366;
}

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

.stApp { background-color: var(--dark); }

/* Header */
.chess-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.chess-header::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-blue), var(--neon-purple), transparent);
}
.chess-header h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(0, 243, 255, 0.3);
    margin: 0;
    line-height: 1;
}
.chess-header p {
    color: var(--neon-blue);
    font-size: 1rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 10px;
    text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
}

/* Status bar */
.status-bar {
    background: rgba(17, 17, 34, 0.7);
    border: 1px solid var(--neon-blue);
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.1rem;
    font-weight: 600;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
}
.status-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: var(--green);
    animation: pulse 1.5s infinite;
    box-shadow: 0 0 10px var(--green);
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
}

/* Info cards */
.info-card {
    background: rgba(17, 17, 34, 0.7);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
}
.info-card:hover {
    border-color: var(--neon-purple);
    box-shadow: 0 0 15px rgba(188, 19, 254, 0.2);
    transform: translateY(-2px);
}
.info-card h4 {
    font-family: 'Orbitron', sans-serif;
    color: var(--neon-blue);
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0 0 10px;
}
.info-card p {
    color: var(--text);
    font-size: 1.1rem;
    margin: 0;
}

/* Move history */
.move-history {
    background: rgba(17, 17, 34, 0.7);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    max-height: 250px;
    overflow-y: auto;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
}
.move-history::-webkit-scrollbar { width: 6px; }
.move-history::-webkit-scrollbar-thumb { background: var(--neon-purple); border-radius: 3px; }
.move-pair { display: flex; gap: 15px; margin-bottom: 6px; color: var(--text); }
.move-num { color: var(--neon-blue); min-width: 25px; font-weight: bold; }
.move-w { color: #fff; min-width: 65px; }
.move-b { color: var(--muted); }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--dark2) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0; width: 1px;
    background: linear-gradient(180deg, transparent, var(--neon-purple), transparent);
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--neon-blue) !important;
    font-family: 'Orbitron', sans-serif;
}

/* Buttons */
.stButton > button {
    background: transparent;
    color: var(--neon-blue);
    border: 1px solid var(--neon-blue);
    border-radius: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 10px 20px;
    transition: all 0.3s;
    width: 100%;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.1) inset;
}
.stButton > button:hover {
    background: var(--neon-blue);
    color: var(--dark);
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.4);
}
.stButton > button:active {
    transform: scale(0.98);
}

/* Select box */
.stSelectbox label {
    font-family: 'Orbitron', sans-serif;
    color: var(--neon-pink) !important;
}
.stSelectbox > div > div {
    background: var(--dark3);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 8px;
}

/* Metric */
.stMetric { background: rgba(17, 17, 34, 0.7); border-radius: 10px; padding: 12px; border: 1px solid var(--border); }
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif;
    color: var(--neon-purple);
}
[data-testid="stMetricLabel"] {
    color: var(--neon-blue) !important;
}

/* Board container */
.board-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    background: radial-gradient(circle, var(--dark3) 0%, var(--dark2) 100%);
    border: 2px solid var(--border);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 0 30px rgba(0,0,0,0.8);
    transition: all 0.3s;
}
.board-wrap:hover {
    border-color: var(--neon-purple);
    box-shadow: 0 0 40px rgba(188, 19, 254, 0.2);
}

/* Text input */
.stTextInput input {
    background: var(--dark3);
    border: 1px solid var(--border);
    color: var(--neon-blue);
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 1.2rem;
    font-weight: bold;
    text-align: center;
    letter-spacing: 2px;
}
.stTextInput input:focus {
    border-color: var(--neon-blue);
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.2);
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--dark3);
    border-radius: 8px;
    color: var(--neon-pink) !important;
    font-family: 'Orbitron', sans-serif;
}

hr { border-color: var(--border); opacity: 0.5; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
#  SESSION STATE INITIALIZATION
# ════════════════════════════════════════════════════════════════

def init_state():
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()
    if "move_history" not in st.session_state:
        st.session_state.move_history = []
    if "player_color" not in st.session_state:
        st.session_state.player_color = chess.WHITE
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "last_move" not in st.session_state:
        st.session_state.last_move = None
    if "eval_score" not in st.session_state:
        st.session_state.eval_score = 0
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "CYBER 🔵"
    if "wins" not in st.session_state:
        st.session_state.wins = 0
    if "losses" not in st.session_state:
        st.session_state.losses = 0
    if "draws" not in st.session_state:
        st.session_state.draws = 0

    # RL State
    if "rl_weights" not in st.session_state:
        st.session_state.rl_weights = {
            "pawn": 100.0,
            "knight": 320.0,
            "bishop": 330.0,
            "rook": 500.0,
            "queen": 900.0,
            "center": 15.0,
            "mobility": 5.0,
        }
    if "rl_training_history" not in st.session_state:
        st.session_state.rl_training_history = []
    if "episodes" not in st.session_state:
        st.session_state.episodes = 0
    if "selected_square" not in st.session_state:
        st.session_state.selected_square = None
    if "last_click_coords" not in st.session_state:
        st.session_state.last_click_coords = None

init_state()


# ════════════════════════════════════════════════════════════════
#  REINFORCEMENT LEARNING ENGINE (TD-LEARNING)
# ════════════════════════════════════════════════════════════════

class RLAgent:
    def __init__(self):
        self.weights = st.session_state.rl_weights
        
    def get_features(self, board):
        """Extract linear features for the value function approximator."""
        f = {k: 0.0 for k in self.weights.keys()}
        center = [chess.D4, chess.E4, chess.D5, chess.E5]
        
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece:
                sign = 1.0 if piece.color == chess.WHITE else -1.0
                pt = piece.piece_type
                if pt == chess.PAWN: f["pawn"] += sign
                elif pt == chess.KNIGHT: f["knight"] += sign
                elif pt == chess.BISHOP: f["bishop"] += sign
                elif pt == chess.ROOK: f["rook"] += sign
                elif pt == chess.QUEEN: f["queen"] += sign
                
                if sq in center:
                    f["center"] += sign
                    
        turn_sign = 1.0 if board.turn == chess.WHITE else -1.0
        f["mobility"] += turn_sign * board.legal_moves.count()
        return f

    def value(self, board):
        """Compute V(s) = sum(w_i * f_i)"""
        if board.is_checkmate():
            return -10000.0 if board.turn == chess.WHITE else 10000.0
        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0
        
        f = self.get_features(board)
        val = sum(self.weights[k] * f[k] for k in self.weights.keys())
        return val

    def train_self_play(self, num_games, alpha, epsilon, gamma):
        """Execute self-play batch using epsilon-greedy and TD(0) backward update."""
        prog = st.progress(0, text="Initializing self-play...")
        
        for i in range(num_games):
            prog.progress((i) / num_games, text=f"Simulating Game {i+1}/{num_games}...")
            board = chess.Board()
            states = [board.copy()]
            
            # Limit moves to prevent infinite loops in random play
            while not board.is_game_over() and len(states) < 100:
                if random.random() < epsilon:
                    # Exploration
                    move = random.choice(list(board.legal_moves))
                else:
                    # Exploitation: 1-step lookahead greedy
                    best_val = -math.inf if board.turn == chess.WHITE else math.inf
                    best_move = None
                    for m in board.legal_moves:
                        board.push(m)
                        val = self.value(board)
                        board.pop()
                        if board.turn == chess.WHITE:
                            if val > best_val: best_val, best_move = val, m
                        else:
                            if val < best_val: best_val, best_move = val, m
                    if best_move is None:
                        best_move = random.choice(list(board.legal_moves))
                    move = best_move
                
                board.push(move)
                states.append(board.copy())
            
            # End of game reward
            r = 0.0
            if board.is_checkmate():
                r = 10000.0 if board.turn == chess.BLACK else -10000.0
            
            # TD Update (backward pass)
            for t in range(len(states)-2, -1, -1):
                s = states[t]
                s_next = states[t+1]
                v_s = self.value(s)
                
                if t == len(states)-2:
                    v_next = r
                else:
                    v_next = self.value(s_next)
                    
                # Temporal Difference Error
                td_error = (gamma * v_next) - v_s
                if t == len(states)-2:
                    td_error = r - v_s
                
                # Clip error to prevent exploding gradients
                td_error = max(-5000.0, min(5000.0, td_error))
                
                f = self.get_features(s)
                for k in self.weights.keys():
                    self.weights[k] += alpha * td_error * f[k]
                    # Soft constraint to keep material weights positive
                    if k != "mobility":
                        self.weights[k] = max(0.1, self.weights[k])

            st.session_state.episodes += 1
            st.session_state.rl_training_history.append(r)
            
        prog.progress(1.0, text="Training complete.")
        time.sleep(0.5)
        prog.empty()

rl_agent = RLAgent()


def minimax(board, depth, alpha, beta, maximizing):
    """Alpha-Beta Minimax — Using true RL Value Function at leaves."""
    if depth == 0 or board.is_game_over():
        return rl_agent.value(board), None

    best_move = None
    if maximizing:
        best_val = -math.inf
        for move in order_moves(board):
            board.push(move)
            val, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        best_val = math.inf
        for move in order_moves(board):
            board.push(move)
            val, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, val)
            if beta <= alpha:
                break
        return best_val, best_move


def order_moves(board):
    """Move ordering: captures first, then checks, then quiet moves."""
    captures, checks, quiets = [], [], []
    for move in board.legal_moves:
        if board.is_capture(move):
            captures.append(move)
        elif board.gives_check(move):
            checks.append(move)
        else:
            quiets.append(move)
    return captures + checks + quiets


def get_ai_move(board, difficulty):
    depth_map = {"NOVICE 🟢": 1, "CYBER 🔵": 2, "NEURAL 🟣": 3, "QUANTUM 🔴": 4}
    depth = depth_map.get(difficulty, 2)
    maximizing = (board.turn == chess.WHITE)
    _, move = minimax(board, depth, -math.inf, math.inf, maximizing)
    if move is None:
        legal = list(board.legal_moves)
        move = random.choice(legal) if legal else None
    return move


# ════════════════════════════════════════════════════════════════
#  SIDEBAR — METHODOLOGY
# ════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ════════════════════════════════════════════════════════════════

st.markdown("""
<div class='chess-header'>
  <h1>NEON CHESS AI</h1>
  <p>TRUE RL · TD-LEARNING · SELF-PLAY · CYBER-AESTHETIC</p>
</div>
""", unsafe_allow_html=True)

board = st.session_state.board

# Layout
col_board, col_info = st.columns([3, 2], gap="large")

with col_board:
    # Status
    if board.is_checkmate():
        winner = "DARK" if board.turn == chess.WHITE else "LIGHT"
        st.markdown(f"<div class='status-bar' style='border-color:var(--red); color:var(--red);'><div class='status-dot' style='background:var(--red);'></div> CRITICAL HIT! <b>{winner}</b> WINS VIA CHECKMATE.</div>", unsafe_allow_html=True)
        if not st.session_state.game_over:
            st.session_state.game_over = True
            if winner == ("LIGHT" if st.session_state.player_color == chess.WHITE else "DARK"):
                st.session_state.wins += 1
            else:
                st.session_state.losses += 1
    elif board.is_stalemate():
        st.markdown("<div class='status-bar' style='border-color:var(--muted); color:var(--text);'><div class='status-dot' style='background:var(--muted);'></div> STALEMATE PROTOCOL ENGAGED.</div>", unsafe_allow_html=True)
        if not st.session_state.game_over:
            st.session_state.game_over = True
            st.session_state.draws += 1
    elif board.is_insufficient_material():
        st.markdown("<div class='status-bar' style='border-color:var(--muted); color:var(--text);'><div class='status-dot' style='background:var(--muted);'></div> INSUFFICIENT MATERIAL FOR DOMINANCE.</div>", unsafe_allow_html=True)
        if not st.session_state.game_over:
            st.session_state.game_over = True
            st.session_state.draws += 1
    elif board.is_check():
        st.markdown("<div class='status-bar' style='border-color:var(--neon-pink); color:var(--neon-pink);'><div class='status-dot' style='background:var(--neon-pink);'></div> WARNING: KING COMPROMISED. EVADE IMMEDIATELY.</div>", unsafe_allow_html=True)
    else:
        if board.turn == st.session_state.player_color:
            st.markdown("<div class='status-bar'><div class='status-dot'></div> USER INPUT REQUIRED. AWAITING COMMAND...</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-bar' style='border-color:var(--neon-purple); color:var(--neon-purple);'><div class='status-dot' style='background:var(--neon-purple);'></div> AI PROCESSING NEURAL PATHWAYS...</div>", unsafe_allow_html=True)

    # Board SVG and Click Handling
    board_flipped = (st.session_state.player_color == chess.BLACK)
    
    # Calculate legal moves for frontend highlight
    legal_moves_dict = {}
    if board.turn == st.session_state.player_color:
        for m in board.legal_moves:
            src = chess.square_name(m.from_square)
            dst = chess.square_name(m.to_square)
            if src not in legal_moves_dict:
                legal_moves_dict[src] = []
            legal_moves_dict[src].append(dst)

    st.markdown("<div class='board-wrap'>", unsafe_allow_html=True)
    move_val = st_chess(board.fen(), legal_moves=legal_moves_dict, board_flipped=board_flipped, key="cyber_chess_board")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.game_over and board.turn == st.session_state.player_color:
        if move_val is not None:
            # Check if this is a new move by comparing timestamp
            if "last_move_timestamp" not in st.session_state:
                st.session_state.last_move_timestamp = 0
            
            current_timestamp = move_val.get("timestamp", 0)
            if current_timestamp > st.session_state.last_move_timestamp:
                st.session_state.last_move_timestamp = current_timestamp
                
                source = move_val.get("source")
                target = move_val.get("target")
                
                # Convert chessboard.js format (e.g., "e2") to python-chess format
                if source and target:
                    try:
                        move = chess.Move.from_uci(source + target)
                        # Handle promotion
                        piece = board.piece_at(chess.parse_square(source))
                        if piece and piece.piece_type == chess.PAWN:
                            if target[1] == '8' or target[1] == '1':
                                move = chess.Move.from_uci(source + target + 'q')
                        
                        if move in board.legal_moves:
                            board.push(move)
                            st.session_state.last_move = move
                            st.session_state.move_history.append(move)
                            st.session_state.eval_score = rl_agent.value(board)
                            st.rerun()
                        else:
                            st.error("❌ ILLEGAL MOVE SEQUENCE DETECTED.")
                    except:
                        pass

        if st.button("💡 REQUEST AI ASSIST", use_container_width=True):
            hint_move = get_ai_move(board, "CYBER 🔵")
            if hint_move:
                st.info(f"OPTIMAL VECTOR: **{hint_move.uci()}**")

    # AI turn
    if not st.session_state.game_over and board.turn != st.session_state.player_color:
        with st.spinner("🧠 Quantum Cores Online..."):
            time.sleep(0.4)
            ai_move = get_ai_move(board, st.session_state.difficulty)
            if ai_move:
                board.push(ai_move)
                st.session_state.last_move = ai_move
                st.session_state.move_history.append(ai_move)
                st.session_state.eval_score = rl_agent.value(board)
        st.rerun()


with col_info:

    tab_dash, tab_train, tab_sys = st.tabs(["📊 DASHBOARD", "🧬 RL TRAINING", "⚙️ SYSTEM CORE"])

    with tab_sys:
        st.markdown("### 🎛️ PROTOCOLS")
        difficulty = st.selectbox(
            "AI CAPABILITY",
            ["NOVICE 🟢", "CYBER 🔵", "NEURAL 🟣", "QUANTUM 🔴"],
            index=1,
        )
        st.session_state.difficulty = difficulty

        player_side = st.selectbox("FACTION ALLIANCE", ["LIGHT ⬜", "DARK ⬛"])
        st.session_state.player_color = chess.WHITE if "LIGHT" in player_side else chess.BLACK

        if st.button("⚡ INITIALIZE NEW MATCH"):
            st.session_state.board = chess.Board()
            st.session_state.move_history = []
            st.session_state.game_over = False
            st.session_state.last_move = None
            st.session_state.eval_score = rl_agent.value(st.session_state.board)
            st.rerun()

    with tab_train:
        st.markdown("### 🧬 RL TRAINING FACILITY")
        with st.expander("CONFIGURE HYPERPARAMETERS", expanded=True):
            train_games = st.slider("EPISODES BATCH", 1, 20, 5)
            train_alpha = st.slider("LEARNING RATE (α)", 0.0001, 0.0100, 0.0010, format="%.4f")
            train_eps = st.slider("EXPLORATION (ε)", 0.0, 1.0, 0.2)
            train_gamma = st.slider("DISCOUNT (γ)", 0.5, 1.0, 0.95)
            
            if st.button("🔥 EXECUTE SELF-PLAY BATCH", use_container_width=True):
                rl_agent.train_self_play(train_games, train_alpha, train_eps, train_gamma)
                st.rerun()
                
        st.markdown("### 🧠 NEURAL DB")
        with st.expander("📡 TRUE RL ARCHITECTURE", expanded=True):
            st.markdown('''**Reinforcement Learning (RL)** implemented via **Linear TD-Learning**.
- **State ($S$)**: Extracted as a feature vector $\\vec{f}(S)$ of material and mobility.
- **Value Function ($V$)**: $V(S) = \\vec{w} \cdot \\vec{f}(S)$.
- **Learning**: Weights $\\vec{w}$ are dynamically updated via TD(0) after episodes based on reward signals (+10k win, -10k loss).''')

        with st.expander("🔄 EXPLORATION vs EXPLOITATION", expanded=True):
            st.markdown('''Uses an **$\\epsilon$-greedy policy** during self-play.
- With probability $\\epsilon$, the agent picks a random vector to discover new strategies.
- With probability $1-\\epsilon$, the agent exploits its current value weights.''')

    with tab_dash:
        st.markdown("### 📊 TELEMETRY")

        # Eval bar
        score = st.session_state.eval_score
        score_display = f"+{score/100:.1f}" if score > 0 else f"{score/100:.1f}"
        color_label = "LIGHT" if score > 0 else ("DARK" if score < 0 else "EQUILIBRIUM")
        adv_color = "var(--green)" if score > 0 else ("var(--neon-pink)" if score < 0 else "var(--muted)")

        st.markdown(f"""
<div class='info-card'>
  <h4>⚖️ DOMINANCE RATIO</h4>
  <p style='font-family:"Orbitron", sans-serif; font-size:1.8rem; font-weight:700; color:{adv_color}; text-shadow: 0 0 10px {adv_color};'>{score_display}</p>
  <p style='color:var(--muted); font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;'>{color_label} ADVANTAGE</p>
</div>
""", unsafe_allow_html=True)

    # RL Metrics
    st.markdown("### 🧬 NEURAL WEIGHTS")
    st.bar_chart(st.session_state.rl_weights)
    
    # Training history
    if st.session_state.episodes > 0:
        st.markdown(f"<p style='color:var(--muted); font-size:0.8rem;'>TRAINING EPISODES: {st.session_state.episodes}</p>", unsafe_allow_html=True)
        # Smooth the rewards for the chart
        if len(st.session_state.rl_training_history) > 0:
            st.line_chart(st.session_state.rl_training_history)

    # Move history
    st.markdown("### 📜 EXECUTION LOG")
    history = st.session_state.move_history
    if history:
        board_temp = chess.Board()
        moves_san = []
        for m in history:
            try:
                san = board_temp.san(m)
                moves_san.append(san)
                board_temp.push(m)
            except Exception:
                moves_san.append(m.uci())

        history_html = "<div class='move-history'>"
        for i in range(0, len(moves_san), 2):
            white_m = moves_san[i]
            black_m = moves_san[i+1] if i+1 < len(moves_san) else "..."
            history_html += f"""<div class='move-pair'>
                <span class='move-num'>{(i//2 + 1):02d}</span>
                <span class='move-w'>{white_m}</span>
                <span class='move-b'>{black_m}</span>
            </div>"""
        history_html += "</div>"
        st.markdown(history_html, unsafe_allow_html=True)
    else:
        st.markdown("<div class='move-history' style='color:var(--muted); text-align:center; font-style:italic; padding-top:20px;'>Awaiting first execution...</div>", unsafe_allow_html=True)
