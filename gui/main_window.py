import dearpygui.dearpygui as dpg
from utils.card_utils import parse_board_string
from gui import card_panel
from gui.equity_matrix_panel import draw_equity_matrix
from engine.equity_matrix import generate_equity_matrix

def on_run_solver():
    try:
        board = dpg.get_value("board_input")
        villain_hand = dpg.get_value("villain_hand_input")
        parsed_board = parse_board_string(board)
        parse_board_string(villain_hand)  # validate villain hand as 4-char

        dpg.set_value("equity_text", f"Parsed board: {parsed_board}")

        # Generate equity matrix (169 hands vs villain_hand on board)
        matrix = generate_equity_matrix(villain_hand, board)
        draw_equity_matrix(matrix)

    except ValueError as e:
        dpg.set_value("equity_text", f"[Error] {e}")

def resize_plot_callback(sender, app_data):
    width = dpg.get_viewport_client_width()
    height = dpg.get_viewport_client_height()
    dpg.set_item_pos("main_window", [0, 0])
    dpg.set_item_width("main_window", width)
    dpg.set_item_height("main_window", height)
    dpg.set_item_width("equity_matrix_panel", width - 40)

def run_gui():
    dpg.create_context()
    dpg.create_viewport(title="Poker Solver", width=1200, height=800)

    card_panel.create_themes()

    # When 3 cards are picked from the card panel
    def on_flop_selected(flop_str):
        dpg.set_value("board_input", flop_str)
        on_run_solver()

    card_panel.on_flop_selected = on_flop_selected
    card_panel.draw_card_picker_modal()

    dpg.set_viewport_resize_callback(resize_plot_callback)

    with dpg.window(label="Poker Solver", tag="main_window"):
        dpg.add_input_int(label="Stack Size", default_value=100, tag="stack_input")
        dpg.add_input_int(label="Pot Size", default_value=3, tag="pot_input")

        dpg.add_input_text(label="Board (e.g. AhKsTc)", default_value="", tag="board_input")
        dpg.add_button(label="Pick Flop Cards", callback=lambda: dpg.configure_item("card_picker_window", show=True))

        dpg.add_input_text(label="Villain Hand (e.g. KdJd)", default_value="", tag="villain_hand_input")

        dpg.add_button(label="Run Solver", callback=on_run_solver)
        dpg.add_spacer(height=10)
        dpg.add_text("", tag="equity_text")

        # Equity Matrix Panel (replaces equity_plot)
        with dpg.child_window(tag="equity_matrix_panel", width=-1, height=500):
            pass

    dpg.setup_dearpygui()
    dpg.show_viewport()
    resize_plot_callback(None, None)
    dpg.start_dearpygui()
    dpg.destroy_context()
