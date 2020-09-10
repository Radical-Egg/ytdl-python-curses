import curses
import time


class cursesWindow:
    def printMainMenu(self, stdsrc):
        # clear screen
        stdsrc.clear()
        # get height and width of current terminal
        h, w = stdsrc.getmaxyx()

        # printing a menu centered, using enumerate to keep track of the position of the first row
        for index, row in enumerate(self.menuOptions):
            # getting center for menu
            x = w//2 - len(row)//2
            y = h//2 - len(self.menuOptions)//2 + index
            # highlighting selected row
            if index == self.current_row_index:
                stdsrc.attron(curses.color_pair(1)) # highlight on
                stdsrc.addstr(y, x, row) # init string
                stdsrc.attroff(curses.color_pair(1)) # highlight off
            else: # otherwise print menu as normal
                stdsrc.addstr(y, x, row) 
        
        stdsrc.refresh() # refresh screen
    def main(self, stdsrc):
        # turning blinking cursor off
        curses.curs_set(0)

        # making color pair
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.printMainMenu(stdsrc)

        while True:

            # getting character
            key = stdsrc.getch()

            # clears everything on current window
            stdsrc.clear()

            # getting key presses
            if key == curses.KEY_UP and self.current_row_index > 0:
                self.current_row_index -= 1
            elif key == curses.KEY_DOWN and self.current_row_index < len(self.menuOptions) - 1:
                self.current_row_index += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                stdsrc.clear()
                stdsrc.addstr(0, 0, "You pressed {}".format(self.menuOptions[self.current_row_index]))
                stdsrc.refresh()
                stdsrc.getch()

                if self.current_row_index == len(self.menuOptions) - 1:
                    break

            self.printMainMenu(stdsrc)
            
            stdsrc.refresh()


            time.sleep(3)
    def __init__(self, menuOptions):
        self.menuOptions = menuOptions
        self.current_row_index = 0

        


if __name__ == "__main__":

    mainMenu = ["Video", "Audio", "Audio/Video", "Exit"]
    mainMenu = cursesWindow(mainMenu)
    curses.wrapper(mainMenu.main)