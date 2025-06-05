import dearpygui.dearpygui as dpg

RANKS = 'AKQJT98765432'

def draw_equity_matrix(matrix_data):
    if dpg.does_item_exist("equity_matrix_panel"):
        dpg.delete_item("equity_matrix_panel", children_only=True)
    else:
        with dpg.child_window(tag="equity_matrix_panel", autosize_x=True, autosize_y=True):
            pass

    max_equity = max([v['equity'] for v in matrix_data.values()])

    with dpg.group(parent="equity_matrix_panel", horizontal=False):
        for i, r1 in enumerate(RANKS):
            with dpg.group(horizontal=True):
                for j, r2 in enumerate(RANKS):
                    if i < j:
                        label = f"{r1}{r2}s"
                    elif i > j:
                        label = f"{r2}{r1}o"
                    else:
                        label = f"{r1}{r1}"

                    equity_info = matrix_data.get(label, {'equity': 0, 'combos': 0})
                    eq = equity_info['equity']
                    combos = equity_info['combos']

                    # Simple blue-to-red heatmap
                    color_val = int(255 * (eq / max_equity)) if max_equity > 0 else 0
                    dpg.add_button(label=f"{label}\n{eq}%", width=50, height=50,
                                   callback=lambda l=label: print(f"Clicked {l}"),
                                   user_data=label,
                                   tag=f"eq_{label}")
                    dpg.set_item_theme(f"eq_{label}", create_cell_theme(color_val))

                    with dpg.tooltip(f"eq_{label}"):
                        dpg.add_text(f"{label}: {eq}% over {combos} combos")

def create_cell_theme(heat_value):
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255 - heat_value, heat_value, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255 - heat_value, heat_value, 120), category=dpg.mvThemeCat_Core)
    return theme_id
