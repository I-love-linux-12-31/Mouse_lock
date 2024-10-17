import Xlib.display
import Xlib.X
import Xlib.XK
import subprocess


def get_display_info() -> dict:
    """
    Returns dict - <display name>: {<display info>}
    Example:
        {
            "DP-1": {
                'name': 'DP-1',
                'width': 800,
                'height': 450,
                'x': 0,
                'y': 0,
                "primary": True,
            },
        }
    """

    xrandr_output = subprocess.check_output(['xrandr', '--query']).decode('utf-8')
    # Output for my system with 3 displays and 2 video cards:
    """
Screen 0: minimum 320 x 200, current 5120 x 1348, maximum 16384 x 16384
DP-4 connected 1600x1200+3520+148 (normal left inverted right x axis y axis) 408mm x 306mm
   1600x1200     60.00*+
   ...    
DP-5 connected primary 1920x1200+1600+0 (normal left inverted right x axis y axis) 518mm x 324mm
   1920x1200     59.95*+ 
   ...
HDMI-2 connected 1600x900+0+0 (normal left inverted right x axis y axis) 443mm x 249mm
   1600x900      60.00*+  59.94    59.95    59.82  
   ...
HDMI-3 disconnected (normal left inverted right x axis y axis)
DVI-D-1 disconnected (normal left inverted right x axis y axis)
DP-1-1 disconnected (normal left inverted right x axis y axis)
DP-1-2 disconnected (normal left inverted right x axis y axis)
DP-1-3 disconnected (normal left inverted right x axis y axis)
HDMI-1-1 disconnected (normal left inverted right x axis y axis)
    """

    lines = xrandr_output.split('\n')
    displays_info = dict()
    for line in lines[1:]:
        if line and line[0] not in (' ', '\t') and "disconnected" not in line:
            primary = False
            if 'primary' in line:
                primary = True
                line = line.replace('primary', ' ')

            parts = line.split()
            # print(parts)
            name = parts[0]
            resolution = parts[2].split('+')[0]
            position = parts[2].split('+')[1:]
            width, height = map(int, resolution.split('x'))
            x, y = map(int, position)
            info = {
                'name': name,
                'width': width,
                'height': height,
                'x': x,
                'y': y,
                "primary": primary
            }
            displays_info[name] = info
    return displays_info


def get_primary_monitor_info():
    for display_info in get_display_info().values():
        if display_info["primary"]:
            return display_info
    return None


display = Xlib.display.Display()
screen = display.screen()
root = screen.root

current_display = get_primary_monitor_info()

shift_x = current_display['x']
shift_y = current_display['y']
selected_display_width = current_display['width']
selected_display_height = current_display['height']

center_x = shift_x + selected_display_width // 2
center_y = shift_y + selected_display_height // 2

restrict_border_collisions = False



def is_mouse_on_target_display():
    pointer = root.query_pointer()
    if restrict_border_collisions:
        delta = 64
        if current_display["primary"]:
            delta = 16
        return (shift_x + delta <= pointer.root_x < shift_x + selected_display_width - delta and
                shift_y + delta <= pointer.root_y < shift_y + selected_display_height - delta)
    return (shift_x <= pointer.root_x < shift_x + selected_display_width and
            shift_y <= pointer.root_y < shift_y + selected_display_height)


def move_mouse_to_center():
    """
    Changes mouse position to center of selected area
    """
    root.warp_pointer(center_x, center_y)
    display.sync()


def select_display(display_name):
    """
    Updates global variables with new screen info.
    """
    global selected_display_width, selected_display_height, shift_x, shift_y, center_x, center_y, current_display

    displays = get_display_info()
    info = displays.get(display_name, None)
    if info is None:
        print(f"Error: No info about display {display_name}")
        return False
    current_display = info
    shift_x = current_display['x']
    shift_y = current_display['y']
    selected_display_width = current_display['width']
    selected_display_height = current_display['height']

    center_x = shift_x + selected_display_width // 2
    center_y = shift_y + selected_display_height // 2

    print(f"Selected display: {current_display['name']}")
    print(f"Resolution: {selected_display_width}x{selected_display_height}")
    print(f"Position: ({shift_x}, {shift_y})")
    print(f"Center point: ({center_x}, {center_y})")
    return True

def work_func():
    if not is_mouse_on_target_display():
        move_mouse_to_center()

def on_exit():
    display.close()
