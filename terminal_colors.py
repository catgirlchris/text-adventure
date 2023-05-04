
import curses
import curses.textpad
import time

def main(stdscr:'curses._CursesWindow'):
    CP_BLANK = 256
    if curses.has_colors():
        curses.use_default_colors()

        for c in range(curses.COLORS):
            curses.init_pair(c, 0, c)

        curses.init_pair(CP_BLANK, 0, 0)

    curses.curs_set(0)

    stdscr.insstr(0,0, f'COLORS: {curses.COLORS}')
    stdscr.insstr(1,0, f'COLOR PAIRS: {curses.COLOR_PAIRS}, DEFAULT_PAIR: {curses.color_content(0)}')

    
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
    #colorpad.border()
    # title
    stdscr.addstr(beg[0]-2,beg[1]+3,
                  'COLORCILLOS DISPONIBLES', curses.color_pair(0))

    stdscr.refresh()
    colorpad_refresh()
    
    # debug pause
    stdscr.getch()

    #curses.textpad.rectangle(colorpad, beg[0],beg[1]-2, beg[0]+2,beg[1]+2)
    colorpad_refresh()

    draw_highlight_rect = lambda: curses.textpad.rectangle(
                                    colorpad,
                                    beg[0]+offset*2,beg[1]-3,
                                    beg[0]+2+offset*2,beg[1]+1)

    erase_highlight_rect = lambda: curses.textpad.rectangle(
                                    colorpad,
                                    beg[0]+offset*2-2,beg[1]-3,
                                    beg[0]+2+offset*2-2,beg[1]+1)

    highlightpad = curses.newpad(3,10)
    highlightpad.border()
    highlightpad.overlay(colorpad, 0,0, 3,0, 5,9)
    colorpad_refresh()
    stdscr.getch()
    #highlightpad.clear()
    highlightpad.erase()
    colorpad_refresh()
    stdscr.getch()
    #colorpad.erase()
    #draw_colors(colorpad, color_structure)
    #colorpad.border()
    #colorpad_refresh()
    #stdscr.getch()

    colorpad.scrollok(True)
    end = True
    # Scrolling loop
    while(end):
        # erase last rectangle
        #colorpad.attron(curses.color_pair(0))
        #erase_highlight_rect()
        #colorpad.attroff(curses.color_pair(0))

        colorpad.attron(curses.color_pair(1))
        #draw_highlight_rect()
        colorpad.attroff(curses.color_pair(1))

        colorpad_refresh()

        key :str = stdscr.getch()
        if (key == curses.KEY_DOWN):
            #colorpad.scroll(1)
            offset = min(offset+1, len(color_structure)+size[0])
        elif (key == curses.KEY_UP):
            #colorpad.scroll(-1)
            offset = max(offset-1, 0)
        elif (key == curses.KEY_RIGHT):
            color_structure[offset] += 1
            color_structure[offset+1] -= 1
            draw_colors(colorpad, color_structure)
        elif (key == curses.KEY_LEFT):
            color_structure[offset] -= 1
            color_structure[offset-1] += 1
            draw_colors(colorpad, color_structure)

        # KEY TO EXIT
        elif (key == curses.KEY_ENTER):
            end = False
        
        # draw new rectangle
        #curses.textpad.rectangle(colorpad, beg[0]+offset*2,beg[1]-2, beg[0]+2+offset*2,beg[1]+2)

        # draw colorpad
        colorpad_refresh()
        time.sleep(0.0167)
    


if __name__ == '__main__':
    curses.wrapper(main)