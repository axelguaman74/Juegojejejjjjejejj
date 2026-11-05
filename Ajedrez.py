import streamlit as st
import chess
import chess.svg
import random

st.set_page_config(page_title="Juego de Ajedrez", layout="centered")

st.title("♟️ Mi Juego de Ajedrez")

# Inicializar el estado del tablero
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

board = st.session_state.board

# Renderizar el tablero en formato SVG visual
board_svg = chess.svg.board(board=board, size=400)
st.image(board_svg, use_container_width=True)

# Estado de la partida y turno
if board.is_game_over():
    st.error("¡El juego ha terminado!")
    st.write(f"Resultado final: {board.result()}")
else:
    turno = "Blancas" if board.turn == chess.WHITE else "Negras"
    st.info(f"Turno actual: **{turno}**")

# Entrada para el movimiento del jugador
st.markdown("### Realizar Movimiento")
st.write("Ingresa tu jugada en notación UCI (ejemplos: `e2e4`, `g1f3`, `e7e5`).")

col1, col2 = st.columns([3, 1])

with col1:
    move_input = st.text_input("Movimiento:", key="move_input", placeholder="e2e4")

with col2:
    submit_move = st.button("Mover")

if submit_move and move_input:
    try:
        move = chess.Move.from_uci(move_input.strip().lower())
        if move in board.legal_moves:
            board.push(move)
            st.rerun()
        else:
            st.warning("Movimiento no permitido según las reglas.")
    except ValueError:
        st.error("Formato inválido. Usa notación UCI de 4 caracteres (ej: e2e4).")

# Turno de la máquina (Negras)
if not board.is_game_over() and board.turn == chess.BLACK:
    st.markdown("---")
    if st.button("Hacer mover a la Computadora (Negras)"):
        legal_moves = list(board.legal_moves)
        if legal_moves:
            bot_move = random.choice(legal_moves)
            board.push(bot_move)
            st.rerun()

# Botón para reiniciar la partida
st.markdown("---")
if st.button("Reiniciar Partida"):
    st.session_state.board = chess.Board()
    st.rerun()
