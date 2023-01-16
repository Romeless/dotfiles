from qtile_extras import widget
from qtile_extras.widget import decorations
from qtile_extras.widget.decorations import BorderDecoration
from core.widgets import *
from utils import color, config
from utils.settings import two_monitors

widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=14,
    padding=2,
    background=color['bg'],
    decorations=[
        BorderDecoration(
            colour=color['bg'],
            border_width=[5, 0, 4, 0],
            )
        ]
)
extension_defaults = widget_defaults.copy()


def create_bar(extra_bar = False):
    """Create top bar, defined as function to allow duplication in other monitors"""
    return bar.Bar(
        [
            # w_sys_icon,
            w_sys_icon,    
            # w_current_layout,
            # Workspaces
            *gen_groupbox(),

            # Left spacer
            # gen_spacer(),
            separator(),
            
            *w_mpd,

            # Window name
            # w_window_name_icon,
            # w_window_name,

            separator(),
            # crash!! 
            # *w_dunst(),

            # Right spacer
            gen_spacer(),
            
            # w_window_name_icon,
            # w_window_name,

            # gen_spacer(),

            # hidden systray
            *((w_systray,) if not extra_bar else ()),
            separator(),
            
            # hidden widgets TODO
            # w_box,
            # separator(),
            # separator_sm(),

            # WM layout indicator
            # *gen_current_layout(),

            # Battery
            *w_battery,
            separator(),

            *w_brightness,
            separator(),

            # Sound
            # w_volume_icon,
            # separator_sm(),
            *w_volume,
            separator(),

            # Clock
            *w_gen_clock,
            separator(),

            # Power button
            w_power,
        ],
        32,
        # margin=[0, 0, 30, 0],
        border_width=[0,0,2,0],
        border_color=color['blue'],
    )


main_screen_bar = create_bar()
secondary_screen_bar = bar.Gap(2)
if two_monitors:
    secondary_screen_bar = create_bar(True)

