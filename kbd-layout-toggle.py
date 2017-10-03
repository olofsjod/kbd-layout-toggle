import subprocess

def getCurrentKbdLayout():
    s = subprocess.run(["setxkbmap", "-query"], stdout=subprocess.PIPE)
    output_str = s.stdout.decode("utf-8")
    output_arr = output_str.split("\n")

    return output_arr[2].split(":     ")[1]

def changeKbdLayout(layout):
    s = subprocess.run(["setxkbmap", layout], stdout=subprocess.PIPE)
    

def main():
    currentLayout = getCurrentKbdLayout()

    if currentLayout == "se":
        changeKbdLayout("se-svorak-custom")
    else:
        changeKbdLayout("se")

    print(getCurrentKbdLayout())

    

main()
