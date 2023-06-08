import curses

def showmouseinfo(win: 'curses._CursesWindow', info: str):
    win.addstr(0,0,info)