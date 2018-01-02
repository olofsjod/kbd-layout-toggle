import subprocess
import argparse

def getCurrentKbdLayout():
    s = subprocess.run(["setxkbmap", "-query"], stdout=subprocess.PIPE)
    output_str = s.stdout.decode("utf-8")
    output_arr = output_str.split("\n")

    return output_arr[2].split(":     ")[1]

def changeKbdLayout(layout):
    msg = "Changed layout to " + layout
    subprocess.run(["notify-send", msg], stdout=subprocess.PIPE)
    subprocess.run(["setxkbmap", layout], stdout=subprocess.PIPE)
    

def toggle(keyboard_layouts):
    cur_layout_str = getCurrentKbdLayout()
    cur_layout_index = keyboard_layouts.index(cur_layout_str)

    next_layout_index = (cur_layout_index + 1) % len(keyboard_layouts)
    next_layout_str = keyboard_layouts[next_layout_index]
    
    changeKbdLayout(next_layout_str)
    

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--print", help="print the current keyboard layout", action="store_true")
    parser.add_argument("--change-layout", help="change the keyboard layout to other layout", nargs=1)
    parser.add_argument("--toggle", help="change the keyboard layout between se and se-svorak-custom", action="store_true")
    
    args = parser.parse_args()

    if args.print:
        print(getCurrentKbdLayout())
    elif args.toggle:
        toggle(["se", "se-svorak-custom"])
    elif len(args.change_layout) > 0:
        new_layout = args.change_layout[0]
        changeKbdLayout(new_layout)

main()
