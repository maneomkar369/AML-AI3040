import streamlit.components.v1 as components
import os

_component_func = components.declare_component(
    "streamlit_chess",
    path=os.path.join(os.path.dirname(__file__), "frontend")
)

def st_chess(fen, legal_moves=None, board_flipped=False, key=None):
    if legal_moves is None:
        legal_moves = {}
    return _component_func(fen=fen, legal_moves=legal_moves, board_flipped=board_flipped, key=key, default=None)
