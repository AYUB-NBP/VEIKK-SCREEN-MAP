from screeninfo import get_monitors

def main():
    definition()

def definition():
    stats = get_monitors()

    elems = str(stats[0]).split(',')
    #elems list of information items

    width =""
    height=""
    for _ in elems:
        if "width=" in _:
            for c in _:
                if c.isnumeric():
                    width = width + c
                else:
                    pass
        if "height=" in _:
            for c in _:
                if c.isnumeric():
                    height = height + c
                else:
                    pass
    return width, height
    #print(width+' '+ height)
   

if __name__ == "__main__":
    main()