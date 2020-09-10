import curses
import re
from pytube import YouTube
import time
import progressbar


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

    # download functions
    def download(self, streamType, stdsrc, streamInfo):
        widgets = ['Loading: ', progressbar.AnimatedMarker()]
        bar = progressbar.ProgressBar(widgets=widgets).start()
        # clear screen
        stdsrc.clear()

        # get x and y of the current terminal
        h, w = stdsrc.getmaxyx()

        # info about video being downloaded
        

        # printing content in the center
        for index, row in enumerate(streamInfo):
            x = w//2 - len(row)//2
            y = h//2 - len(streamInfo)//2 + index

            stdsrc.addstr(y, x, row)
        
        # refresh screen
        stdsrc.refresh()

        # download with progress
        for i in bar(range(100)):
            if streamType == "audio/video":
                try:
                    self.yt.streams.filter(progressive=True).get_highest_resolution().download("./video/" + self.yt.title)
                except:
                    print("Unable to download audio/video for {}. Something went wrong.".format(self.yt.title))
            elif streamType == "audio_only":
                try:
                    self.yt.streams.get_audio_only().download("./audio_only/" + self.yt.title)
                except:
                    print("Unable to download audio_only for {}. Something went wrong".format(self.yt.title))
            time.sleep(0.02)

        
    def downloadPage(self, stdsrc):
        # clear screen
        stdsrc.clear()

        if self.current_row_index == 0:
            # downloading
            self.download("audio/video", stdsrc, streamInfo = ["You are downloading the video with audio for", self.yt.title, " "])
        elif self.current_row_index == 1:
            # downloading content
            self.download("audio_only", stdsrc, streamInfo = ["You are downloading the audio_only for", self.yt.title, " "])

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
                self.current_row_index -= 1 # making sure we cant go up past the top row
            elif key == curses.KEY_DOWN and self.current_row_index < len(self.menuOptions) - 1:
                self.current_row_index += 1 # making sure we cant go down past the bottom row
            elif key == curses.KEY_ENTER or key in [10, 13]: # checking for enter input
                # clear screen
                stdsrc.clear()

                # check to see if use wants to quit
                if self.current_row_index == len(self.menuOptions) - 1:
                    break
                else:
                    # else go to the download page
                    self.downloadPage(stdsrc)
                    stdsrc.refresh()

            self.printMainMenu(stdsrc)
            
            stdsrc.refresh()

    # making sure youtube link is provided
    def validateYouTubeLink(self):
        linkValidation = "^https://www.youtube.com/*" # regex pattern
        while True:
            self.ytLink = input("Enter Link: ") # enter link
            
            check = re.search(linkValidation, self.ytLink) # check for match

            # if theres a match break otherwise loop
            if check:
                break
            else:
                print("{} is not a YouTube link, not going to work.".format(self.ytLink))

    # init method
    def __init__(self):
        self.menuOptions = ["Audio and Video", "Audio_only", "Exit"]
        self.current_row_index = 0
        self.ytLink = None
        self.yt = None

        


if __name__ == "__main__":

    mainMenu = cursesWindow()
    mainMenu.validateYouTubeLink()
    mainMenu.yt = YouTube(mainMenu.ytLink)


    curses.wrapper(mainMenu.main)