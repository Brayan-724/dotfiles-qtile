# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, extension, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "kitty" # guess_terminal()

spacer = widget.TextBox(" ")
white = {
    "default": "CFCFEA",
    "pure": "ffffff",
}
primary = {
    "default": "902296",
    "light": "58428A",
    "dark": "3D2E60",
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Qminimize
    Key([mod, "shift"], "m", lazy.spawn('Qminimize -u'), desc="Minimize window"), # - u to show the rofi menu
    Key([mod], "m", lazy.spawn("Qminimize -m")), # -m to minimize

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit s;ides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Toggle between keyboard layouts
    Key([mod], "e", lazy.widget["keyboardlayout"].next_keyboard(), 
        desc="Toggle between keyboard layouts"),
    #Key([mod, "shift"], ".", lazy.run_extension(extension.WindowList()))
]

groups = [Group(i, label="•") for i in "123456789"]

for i in groups:
    #group = Group(i)
    group = i

    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], group.name, lazy.group[group.name].toscreen(),
            desc="Switch to group {}".format(group.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], group.name, lazy.window.togroup(group.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(group.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, "control"], group.name, lazy.window.togroup(group.name),
             desc="move focused window to group {}".format(group.name)),
    ])

layouts = [
    layout.Columns(
        border_focus="#ff0000",
        border_normal="#000000",
        border_width=1,
        margin=[5, 7, 5, 7]
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(border_width=1, border_focus="#00ff00"),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=10,
    padding=3,
    foreground=white["default"],
)
extension_defaults = widget_defaults.copy()

def app_btn(text, cmd, fontsize, foreground):
    def mouse_callback_app_btn():
        qtile.cmd_spawn(cmd)
    
    return widget.TextBox(
        text=text,
        padding=6,
        fontsize=fontsize,
        foreground=foreground,
        mouse_callbacks={
            "Button1": mouse_callback_app_btn
        }
    )

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentScreen(
                    active_text="•",
                    inactive_text="•",
                    fontsize=14
                ),
                widget.CurrentLayoutIcon(scale=0.5, padding=0),
                widget.GroupBox(
                    borderwidth=2,
                    highlight_method="line",
                    highlight_color=["000000.0", "000000.0"],
                    block_highlight_text_color=primary["default"],
                    this_current_screen_border=primary["light"],
                    this_screen_border=primary["dark"],
                    other_current_screen_border=primary["light"],
                    other_screen_border=primary["dark"],
                    hide_unused=False,
                    active="701A74",
                    inactive="352853",
                    fontsize=12,
                    spacing=2,
                    rounded=False,
                    disable_drag=True
                ),
                widget.Prompt(
                    prompt=" ",
                    fontsize=12,
                ),
                spacer,
                widget.WidgetBox(
                    widgets=[
                        widget.CPUGraph(
                            border_color=primary["default"],
                            graph_color=primary["default"],
                            fill_color=primary["dark"],
                        ),
                        widget.MemoryGraph(
                            border_color=primary["default"],
                            graph_color=primary["default"],
                            fill_color=primary["dark"],
                        ),
                        widget.TextBox(
                            text="Net",
                            fontsize=12,
                            foreground=primary["default"],
                        ),
                        widget.TextBox(
                            text="",
                            foreground="50D3C2",
                            padding=0,
                        ),
                        widget.NetGraph(
                            bandwidth_type="down",
                            border_color=primary["default"],
                            graph_color=primary["default"],
                            fill_color=primary["dark"],
                        ),
                        widget.TextBox(
                            text="",
                            foreground="D350A2",
                            padding=0,
                        ),
                        widget.NetGraph(
                            bandwidth_type="up",
                            border_color=primary["default"],
                            graph_color=primary["default"],
                            fill_color=primary["dark"],
                        ),
                    ],
                    text_open="📈",
                    text_closed="📉",
                    background="67855703",
                    fontsize=14,
                    margin=[0, 0, 2, 0],
                ),
                widget.Spacer(),
                widget.Notify(
                    audiofile="/home/apika/Downloads/mixkit-sci-fi-click-900.wav",
                ),
                widget.Spacer(),
                widget.TextBox(
                    text="",
                    fontsize=14,
                ),
                widget.Pomodoro(
                    length_pomodori=30,
                    length_short_break=5,
                    length_long_break=15,
                ),
                widget.KeyboardLayout(
                    configured_keyboards=["us", "es"],
                    foreground=primary["default"],
                ),
                widget.Wlan(interface="wlp13s0b1", format="WIFI: {essid}"),
                widget.Sep(),
                widget.Volume(emoji=True, channel="Capture"),
                widget.Sep(),
                widget.Clock(format='%d %m', fontsize=13),
                widget.Clock(format="%y"),
                widget.Sep(),
                widget.Clock(format='%H %M', fontsize=13),
                widget.Clock(format="%S"),
            ],
            24,
            margin=2,
            background="160003.2",
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                app_btn(
                    text="",
                    cmd=terminal,
                    fontsize=18,
                    foreground="99BB88"
                ),
                app_btn(
                    text="",
                    cmd="opera",
                    fontsize=18,
                    foreground="FF1B2D"
                ),
                app_btn(
                    text="ﭮ",
                    cmd="discord",
                    fontsize=18,
                    foreground="7289DA"
                )
            ],
            24,
            margin=2,
            background="160003.2",
        ),
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    #Click([mod], "Button2", lazy.window.bring_to_front())
    Click([mod], "Button2", lazy.window.toggle_floating())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

autostart = [
    "picom --vsync --shadow --inactive-opacity 0.95 &",
    "feh --bg-fill /home/apika/wallpapers/w2.jpg"
    #"xset led named 'Scroll Lock'"
]

for x in autostart:
    os.system(x)

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
