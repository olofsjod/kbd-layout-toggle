"""kbd-layout-toggle.py
written by Olof Sjödin <me@olofsjodin.se>

The purpose of this program is to change between QWERTY and DVORAK painlessly
in a tiled window manager.

"""

import subprocess
import argparse

def getXKBmapQuery():
    s = subprocess.run(["setxkbmap", "-query"], stdout=subprocess.PIPE)
    output_str = s.stdout.decode("utf-8")
    output_arr = output_str.split("\n")
    output_arr = output_arr[:-1]

    ret = {}
    for line in output_arr:
        temp = line.replace(" ", "") #remove spaces
        temp = temp.split(":")
        key = temp[0]
        val = temp[1]
        
        ret[key] = val

    return ret

def printCurrentKbdLayout():
    q = getXKBmapQuery()
    
    ret = ""
    if "layout" in q:
        ret += q["layout"]

    if "variant" in q:
        ret += "/" + q["variant"]
    else:
        ret += "/qwerty"

    print(ret)


def changeKbdLayout(k):
    msg = "Changed layout to " + str(k)

    parameters = []

    if "layout" in k:
        parameters.extend(["-layout", k["layout"]])
    if "variant" in k:
        parameters.extend(["-variant", k["variant"]])

    cmd = ["setxkbmap"]
    cmd.extend(parameters)
    
    subprocess.run(["notify-send", msg], stdout=subprocess.PIPE)
    subprocess.run(cmd, stdout=subprocess.PIPE)

def isDvorak():
    q = getXKBmapQuery()
    if "variant" in q:
        if q["variant"] == "dvorak":
            return True
    return False

def toggleDvorak():
    is_dvorak = isDvorak()

    if is_dvorak:
        k = {"layout": "se", "variant" : ""}
        changeKbdLayout(k)
    else:
        k = {"layout": "se", "variant" : "dvorak"}
        changeKbdLayout(k)
        

def toggle(keyboard_layouts):
    cur_query = getXKBmapQuery()
    cur_layout_index = keyboard_layouts.index(cur_layout_str)

    next_layout_index = (cur_layout_index + 1) % len(keyboard_layouts)
    next_layout_str = keyboard_layouts[next_layout_index]
    
    changeKbdLayout(next_layout_str)
    

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--print-current-layout", "-p", help="print the current keyboard layout", action="store_true")
    parser.add_argument("--layout", "-l", help="change the keyboard layout to other layout", nargs=2, metavar=('LAYOUT_NAME', 'VARIANT'))
 
    parser.add_argument("--toggle", "-t", help="change the keyboard layout between se and se-svorak-custom", action="store_true")
    
    args = parser.parse_args()

    if args.print_current_layout:
        printCurrentKbdLayout()
    elif args.toggle:
        toggleDvorak()
    elif args.layout != None:
        new_layout = args.layout[0]
        new_variant = args.layout[1]
        l = {"layout" : new_layout, "variant" : new_variant}
        changeKbdLayout(l)

if __name__ == "__main__":
    main()
