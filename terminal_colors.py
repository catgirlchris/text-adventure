
import curses
import curses.textpad
import time

def main(stdscr:'curses._CursesWindow'):
    CP_BLANK = curses.COLORS
    if curses.has_colors():
        curses.use_default_colors()

        for c in range(curses.COLORS):
            curses.init_pair(c, 0, c)

        curses.init_pair(CP_BLANK, curses.COLOR_BLACK, curses.COLOR_BLACK)

    curses.curs_set(0)

    stdscr.insstr(0,0, f'COLORS: {curses.COLORS}')
    stdscr.insstr(1,0, f'COLOR PAIRS: {curses.COLOR_PAIRS}')

    
    columns = 100
    rows = 100
    
    stdscr.insstr(3,0, f'COLOR PANEL (y,x): {rows},{columns}')

    colorpad = curses.newpad(rows, columns)

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
                colorpad.addstr('   ', curses.color_pair(0))
                color += 1
            colorpad.addstr('\n\n', curses.color_pair(0))

    draw_colors(colorpad, color_structure)

    # colorpad info for pad.refresh()
    offset = 0
    beg = (5,2)
    size = [stdscr.getmaxyx()[0] - beg[0], stdscr.getmaxyx()[1]]

    stdscr.refresh()
    colorpad.refresh(offset,0,
                         beg[0],beg[1], 
                         beg[0]+size[0]-1, beg[1]+size[1])
    
    # debug pause
    stdscr.getch()

    #curses.textpad.rectangle(colorpad, beg[0],beg[1]-2, beg[0]+2,beg[1]+2)
    colorpad.refresh(offset,0,
                         beg[0],beg[1], 
                         beg[0]+size[0]-1, beg[1]+size[1])

    colorpad.scrollok(True)
    end = True
    # Scrolling loop
    while(end):
        # erase last rectangle
        colorpad.attron(curses.color_pair(CP_BLANK))
        curses.textpad.rectangle(colorpad, beg[0]+offset*2,beg[1]-2, beg[0]+2+offset*2,beg[1]+2)
        colorpad.attroff(curses.color_pair(CP_BLANK))
        colorpad.refresh(offset,0,
                         beg[0],beg[1], 
                         beg[0]+size[0]-1, beg[1]+size[1])

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
        colorpad.refresh(offset,0,
                         beg[0],beg[1], 
                         beg[0]+size[0]-1, beg[1]+size[1])
        time.sleep(0.0167)
    


if __name__ == '__main__':
    curses.wrapper(main)