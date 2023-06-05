from playsound import playsound
import curses
import curses.textpad
import time
from pathlib import Path

from playsound import playsound

''' TODO CREDITS
sounds: Atelier Magicae '''

SCRIPT_DIR = Path(__file__).parent
PIXEL32 = SCRIPT_DIR / 'sfx' / 'Pixel_33.wav'

def main(stdscr:'curses._CursesWindow'):
    CP_BLANK = 256
    if curses.has_colors():
        curses.use_default_colors()

        for c in range(1, curses.COLOR_PAIRS-1):
            curses.init_pair(c, 0, c)

        #curses.init_pair(CP_BLANK, 0, 0)

    curses.curs_set(0)
    curses.mousemask(-1)

    stdscr.insstr(0,0, f'COLORS: {curses.COLORS}')
    #stdscr.insstr(1,0, f'COLOR PAIRS: {curses.COLOR_PAIRS}, DEFAULT_PAIR: {curses.color_content(0)}')

    
    columns = 100
    rows = 100
    
    stdscr.insstr(2,0, f'COLOR PANEL (y,x): {rows},{columns}')

    colorpad = curses.newpad(rows, columns)
    
    # colorpad info for pad.refresh()
    offset = 0
    beg = (5,3)
    size = [stdscr.getmaxyx()[0] - beg[0] -2*2, stdscr.getmaxyx()[1] - beg[1] -2 -1]

    colorpad_refresh = lambda: colorpad.refresh(offset,0,
                         beg[0],beg[1], 
                         beg[0]+size[0]+1, beg[1]+size[1])

    color = 0
    columns_used = 10
    color_structure = [6,6,5,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
                       6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
                       6,6,6]
    color_index = 0

    def draw_colors(colorpad:'curses._CursesWindow', color_structure:list[int]):
        # first line
        colorpad.addstr('\n', curses.color_pair(0))
        color = 0
        for e in color_structure:
            for i in range(0,e,1):
                colorpad.addstr(' {:0>3} '.format(color), curses.color_pair(0))
                colorpad.addstr('    ', curses.color_pair(color))
                colorpad.addstr('  ', curses.color_pair(0))
                color += 1
            colorpad.addstr('\n\n', curses.color_pair(0))

    draw_colors(colorpad, color_structure)

    # surrounding rectangle draw
    curses.textpad.rectangle(stdscr, beg[0]-2,beg[1]-2, beg[0]+size[0]+3, beg[1]+size[1]+1)

    # title
    stdscr.addstr(beg[0]-2,beg[1]+3,
                  'COLORCILLOS DISPONIBLES', curses.color_pair(0))

    stdscr.refresh()
    colorpad_refresh()
    
    # debug pause
    stdscr.getch()

    hlpad_pos = [3,0]
    hlpad_size = [3,10]
    highlightpad = curses.newpad(hlpad_size[0],hlpad_size[1])
    highlightpad.border()
    hl_overlay = lambda: highlightpad.overlay(colorpad, 0,0, 
                         hlpad_pos[0],hlpad_pos[1], 
                         hlpad_pos[0]+hlpad_size[0]-1,hlpad_pos[1]+hlpad_size[1]-1)

    hl_refresh = lambda: highlightpad.refresh(0,0, 
                         hlpad_pos[0],hlpad_pos[1], 
                         hlpad_pos[0]+hlpad_size[0]-1,hlpad_pos[1]+hlpad_size[1]-1)

    '''hl_overlay()
    colorpad_refresh()
    stdscr.getch()

    highlightpad.erase()
    colorpad.erase()
    draw_colors(colorpad, color_structure)
    colorpad_refresh()
    stdscr.getch()

    stdscr.getch()
    '''


    colorpad.scrollok(True)
    end = True

    # Scrolling loop
    while(end):
        event :str = stdscr.getch()
        if (event == curses.KEY_DOWN):
            colorpad.erase()
            hlpad_pos[0] = min(hlpad_pos[0]+2, len(color_structure)+size[0]*2)
            draw_colors(colorpad, color_structure)
            highlightpad.border()
            hl_overlay()
            offset = min(offset+2, len(color_structure)+size[0])
        elif (event == curses.KEY_UP):
            colorpad.erase()
            hlpad_pos[0] = max(hlpad_pos[0]-2, 0)
            draw_colors(colorpad, color_structure)
            highlightpad.border()
            hl_overlay()
            offset = max(offset-2, 0)
        elif (event == curses.KEY_RIGHT):
            color_structure[offset] += 1
            color_structure[offset+1] -= 1
            draw_colors(colorpad, color_structure)
        elif (event == curses.KEY_LEFT):
            color_structure[offset] -= 1
            color_structure[offset-1] += 1
            draw_colors(colorpad, color_structure)

        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            y, x = my - beg[0] + offset, mx-3
            if (bstate == curses.BUTTON1_CLICKED, colorpad.enclose(y, x)):
                #stdscr.addstr(y, x, stdscr.instr(my, mx, 5))
                playsound(str(PIXEL32), False)
                hlpad_pos[0],hlpad_pos[1] = y, x
                draw_colors(colorpad, color_structure)
                highlightpad.border()
                hl_overlay()

        # KEY TO EXIT
        elif ((event == curses.KEY_ENTER) | (event == ord('q'))):
            end = False

        # draw colorpad
        colorpad_refresh()
        time.sleep(0.0167)
    


if __name__ == '__main__':
    curses.wrapper(main)