import dearpygui.dearpygui as dpg

# --- Public Globals ---
selected_cards = []
highlighted_theme = None
default_theme = None

# --- External Callbacks (set externally) ---
on_flop_selected = None

# --- Theme Setup ---
def create_themes():
    global highlighted_theme, default_theme

    with dpg.theme() as highlighted_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 180, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 200, 255), category=dpg.mvThemeCat_Core)

    with dpg.theme() as default_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 50, 50), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 70, 70), category=dpg.mvThemeCat_Core)

# --- Card Panel UI ---
def draw_card_picker_modal():
    with dpg.window(label="Pick Flop Cards", modal=True, show=False, no_close=True,
                    tag="card_picker_window", width=420, height=460):
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=340)
            dpg.add_button(label="❌", width=40, height=20, callback=cancel_card_picker)

        dpg.add_text("Click 3 cards to set flop:")

        with dpg.group(horizontal=True):
            for suit in ['c', 'd', 'h', 's']:
                with dpg.child_window(width=90, height=350):
                    for rank in '23456789TJQKA':
                        card = rank + suit
                        add_card_button(card)

        dpg.add_button(label="Clear Selection", callback=clear_selected_cards)

# --- Card Buttons ---
def add_card_button(card):
    tag = f"card_{card}"
    dpg.add_button(label=card, width=80, tag=tag, callback=lambda: select_card(card))
    dpg.bind_item_theme(tag, default_theme)

def select_card(card):
    global selected_cards

    card_tag = f"card_{card}"

    if card in selected_cards:
        selected_cards.remove(card)
        dpg.bind_item_theme(card_tag, default_theme)
        return

    if len(selected_cards) >= 3:
        return

    selected_cards.append(card)
    dpg.bind_item_theme(card_tag, highlighted_theme)

    if len(selected_cards) == 3:
        flop_str = ''.join(selected_cards)
        if on_flop_selected:
            on_flop_selected(flop_str)
        dpg.configure_item("card_picker_window", show=False)
        clear_selected_cards()

# --- Reset/Clear ---
def clear_selected_cards():
    global selected_cards
    for card in selected_cards:
        dpg.bind_item_theme(f"card_{card}", default_theme)
    selected_cards = []

def cancel_card_picker():
    clear_selected_cards()
    dpg.configure_item("card_picker_window", show=False)
    dpg.set_value("board_input", "")
    dpg.set_value("equity_text", "")
