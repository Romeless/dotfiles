from libqtile import bar, qtile, lazy
import subprocess

from qtile_extras import widget
from qtile_extras.widget import decorations
from qtile_extras.widget.decorations import RectDecoration

from utils.settings import workspace_names, with_battery, with_wlan
from utils import color, config

import os

home = os.path.expanduser('~')

group_box_settings = {
    "padding": 4,
    "borderwidth": 4,
    "active": color['fg'],
    "inactive": color['gray'],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": color['black'],
    "block_highlight_text_color": color['red'],
    "highlight_method": "block",
    "this_current_screen_border": color['black'],
    "this_screen_border": color['fg'],
    "other_current_screen_border": color['black'],
    "other_screen_border": color['black'],
    "foreground": color['fg'],
    "background": color['black'],
    "urgent_border": color['red'],
}

# functions for callbacks
def open_launcher():
    qtile.cmd_spawn('rofi -show drun -theme ~/.config/rofi/launcher.rasi')

def open_pavu():
    qtile.cmd_spawn('pavucontrol')

def open_powermenu():
    qtile.cmd_spawn('' + home + '/.local/bin/power')

def open_batterymenu():
    qtile.cmd_spawn('' + home + '/.local/bin/battery_profile')

def open_calendar():
    qtile.cmd_spawn('' + home + '/.local/bin/toggle_cal')

def dunst():
    return subprocess.check_output(["./.config/qtile/scripts/dunst.sh"]).decode("utf-8").strip()

def toggle_dunst():
    qtile.cmd_spawn("./.config/qtile/scripts/dunst.sh --toggle")

def toggle_notif_center():
    qtile.cmd_spawn("./.config/qtile/scripts/dunst.sh --notif-center")

def parse_window_name(text):
    '''Simplifies the names of a few windows, to be displayed in the bar'''
    target_names = [
        'Mozilla Firefox',
        'Visual Studio Code',
        'Discord',
    ]
    try:
        return next(filter(lambda name: name in text, target_names), text)
    except TypeError:
        return text


# separator
def separator_lg():
    return widget.Sep(
            foreground=color['bg'],
            padding=8,
            linewidth=3,
    )

def separator():
    return widget.Sep(
        # foreground=color['white'],
        foreground=color['bg'],
        padding=4,
        linewidth=3,
    )


def separator_sm():
    return widget.Sep(
        # foreground=color['white'],
        foreground=color['bg'],
        padding=1,
        linewidth=1,
        size_percent=55,
    )


# widget decorations
base_decor = {
    'colour': color['black'],
    'filled': True,
    'padding_y': 4,
    'line_width': 0,
}


def _left_decor(color: str, padding_x=None, padding_y=4):
    return [
        RectDecoration(
            colour=color,
            radius=[4, 0, 0, 4],
            filled=True,
            padding_x=padding_x,
            padding_y=padding_y,
        )
    ]


def _right_decor():
    return [
        RectDecoration(
            colour=color['black'],
            radius=[0, 4, 4, 0],
            filled=True,
            padding_y=4,
            padding_x=0,
        )
    ]


# hollow knight icon
w_hk = widget.Image(
    background=color['fg'],
    margin_x=14,
    margin_y=3,
    mouse_callbacks={'Button1': open_launcher},
    filename='~/.config/qtile/icons/hkskull.png',
)

# left icon
w_sys_icon = widget.TextBox(
    # text=' ',
    # text=' ',
    # text='ﮊ',
    # text='',
    # text='',
    # text='',
    # text='',
    text = '',
    font='Font Awesome 6 Free Solid',
    fontsize=20,
    # foreground='#000000',
    foreground=color['blue'],
    background=color['bg'],
    padding=16,
    mouse_callbacks={'Button1': open_launcher},
)


# workspace groups
def gen_groupbox():
    return (
        w_oval_open,
        widget.GroupBox(
            font='Font Awesome 6 Free Solid',
            visible_groups=workspace_names,
            **group_box_settings,
        ),
        w_oval_close,
    )

w_oval_open = widget.TextBox(
    text="",
    foreground=color['black'],
    background=color['bg'],
    fontsize=18,
    padding=0,
)

w_oval_close = widget.TextBox(
    text="",
    foreground=color['black'],
    background=color['bg'],
    fontsize=18,
    padding=0,
)

# spacers
def gen_spacer():
    return widget.Spacer()

def w_dunst():
    return (
        w_oval_open,
        widget.GenPollText(
            func=dunst,
            update_interval=1,
            foreground=color['maroon'],
            background=color['black'],
            padding=8,
            mouse_callbacks={
                "Button1": toggle_dunst,
                "Button3": toggle_notif_center,
            },
        ),
        w_oval_close,
    )

# window name
w_window_name_icon = widget.TextBox(
    text=' ',
    foreground='#ffffff',
    background=color['bg'],
    font='Font Awesome 6 Free Solid',
)

w_window_name = widget.WindowName(
    foreground='#ffffff',
    width=bar.CALCULATED,
    empty_group_string='Desktop',
    max_chars=35,
    parse_text=parse_window_name,
)

# systray
w_systray = widget.Systray(
    icon_size=20,
    background=color['bg'],
    padding=5,
)

# current layout
w_current_layout = widget.CurrentLayoutIcon(
    custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons/")],
    foreground=color['gray'],
    # background=color['black'],
    # padding=-4,
    scale=0.6,
)

w_mpd = (
    w_oval_open,
    widget.Mpd2(
        status_format='{play_status} ',
        foreground=color["fg"],
        background=color["black"],
        font="Font Awesome 6 Free Solid",
        fontsize=12,
        no_connection="",
        idle_format="",
    ),
    widget.Mpd2(
        status_format='{artist}/{title}',
        foreground=color["fg"],
        background=color["black"],
        fontsize=12,
        max_chars=20,
        no_connection="No connection",
        idle_format="MPD IDLE"
    ),
    widget.Mpd2(
        status_format='[{repeat}{random}{single}{consume}{updating_db}]',
        foreground=color["fg"],
        background=color["black"],
        fontsize=12,
        no_connection="",
        idle_format="",
    ),
    w_oval_close,
)

# brightness
w_brightness = (
    (
        w_oval_open,
        widget.Backlight(
            format=' ',
            foreground=color['yellow'],
            background=color['black'],
            backlight_name='intel_backlight',
            show_short_text=False,
            fontsize=18,
        ),
        widget.Backlight(
            format='{percent:2.0%}',
            backlight_name='intel_backlight',
            show_short_text=False,
            foreground=color['yellow'],
            background=color['black'],
        ),
        w_oval_close,
    )
)

# battery
w_battery = (
    w_oval_open,
    widget.Battery(
        format='{char} ',
        charge_char='',
        discharge_char='',
        full_char='',
        unknown_char='',
        empty_char='',
        show_short_text=False,
        foreground=color['pink'],
        background=color['black'],
        fontsize=18,
        mouse_callbacks={'Button1': open_batterymenu},
    ),
    widget.Battery(
        format='{percent:2.0%}',
        show_short_text=False,
        foreground=color['pink'],
        background=color['black'],
        mouse_callbacks={'Button1': open_batterymenu},
    ),
    w_oval_close,
    # if with_battery
    # else ()
)

# volume
w_volume = (
    w_oval_open,
    widget.TextBox(
        text='墳 ',
        foreground=color['green'],
        background=color['black'],
        fontsize=20,
        font='Font  Awesome 6 Free Solid',
    ),
    widget.PulseVolume(
        foreground=color['green'],
        background=color['black'],
        limit_max_volume='True',
        mouse_callbacks={'Button3': open_pavu},
    ),

    w_oval_close,
)

# internet
w_wlan = (
    (
        widget.Wlan(
            format='󰖩',
            foreground=color['dark'],
            disconnected_message='󰖪',
            fontsize=16,
            interface='wlo1',
            update_interval=5,
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn('' + home + '/.local/bin/nmgui'),
                # 'Button3': lambda: qtile.cmd_spawn(myTerm + ' -e nmtui'),
            },
            padding=4,
            decorations=_left_decor(color['maroon']),
        ),
        separator_sm(),
        widget.Wlan(
            format='{percent:2.0%}',
            disconnected_message=' ',
            interface='wlo1',
            update_interval=5,
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn('' + home + '/.local/bin/nmgui'),
                # 'Button3': lambda: qtile.cmd_spawn(myTerm + ' -e nmtui'),
            },
            decorations=_right_decor(),
        ),
        separator(),
    )
    if with_wlan
    else ()
)

# time, calendar
w_gen_clock = (
    w_oval_open,
    widget.TextBox(
        text=' ',
        font='Font Awesome 6 Free Solid',
        fontsize=20,
        foreground=color['blue'],
        background=color['black'],
        mouse_callbacks={'Button1': open_calendar},
    ),
    widget.Clock(
        format='%b %d, %H:%M',
        foreground=color['blue'],
        background=color['black'],
        mouse_callbacks={'Button1': open_calendar},
    ),
    w_oval_close,
)

# power menu
w_power = widget.TextBox(
    text='⏻',
    foreground=color['red'],
    font='Font Awesome 6 Free Solid',
    fontsize=18,
    padding=16,
    mouse_callbacks={'Button1': open_powermenu},
)

w_test = widget.WidgetBox(
    close_button_location='right',
    fontsize=24,
    font='JetBrainsMono Nerd Font',
    text_open=' ',
    text_closed=' ',
    widgets=[w_systray],
    decorations=_left_decor(color['maroon']),
)

# widget box
w_box = widget.WidgetBox(
    close_button_location='right',
    fontsize=24,
    text_closed='',
    text_open='',
    widgets=[
        widget.CPU(
        
        ),
        widget.DF(
        
        ),    # free disk space
        widget.Memory(
        
        ),
        # widget.Net(
        
        # ),
        # TODO uptime, CPU, temp, diskfree, memory
    ],
)
