#!/usr/bin/env python3
# encoding: utf-8

import curses
import json
import sys
import subprocess
import os
import signal

class AdbTools:

    name = "adb tools"

    # json config
    config = None
    log_path = None

    # color
    DEFAULT_COLOR = 1
    FG_RED_COLOR = 2
    FG_GREEN_COLOR = 3
    current_usb_status = DEFAULT_COLOR

    # board info
    INPUT_COLS = 3
    INPUT_LINE = 2
    INPUT_INFO = 4
    INPUT_COLS_CHAR = "-"
    INPUT_PREFIX = "logtools # "
    LEFT_START_COL = 1
    TOP_START_ROW = 2
    RIGHT_END_COL = 1
    BOTTOM_END_ROW= 1
    RIGHT_LEFT_SCALE = 3

    # keyboard code
    KEY_BOARD_ENTER = 10
    KEY_BOARD_ESC = 27
    KEY_BOARD_BACKSPACE = 127
    KEY_BOARD_UP = 259
    KEY_BOARD_DOWN = 258
    KEY_BOARD_LEFT = 260
    KEY_BOARD_RIGHT = 261

    # row and col
    maxRows = 80
    maxCols = 20

    # screen
    mainScreen = None
    leftScreen = None
    rightScreen = None
    progressBar = None
    inputScreen = None

    # input string
    input_str = ""

    # screen index
    tab_screen_index = 0
    left_cmd_index = 0
    left_cmd_index_top = 0
    components = None
    current_process = None

    def __init__(self, argv):
        config_path = argv["config"]
        self.log_path = argv["log"]

        # get config
        self.config = json.loads(self.GetJsonFromFile(config_path))

        # curses
        self.mainScreen = curses.initscr()
        self.mainScreen.border(0)
        curses.noecho()
        curses.cbreak()
        self.mainScreen.keypad(1)
        self.maxRows = curses.LINES
        self.maxCols = curses.COLS

        self.mainScreen.addstr(1, self.LEFT_START_COL + ((self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL) // 2) - (len(self.name) // 2), self.name)
        self.mainScreen.refresh()

        # color
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        self.current_usb_status = self.FG_RED_COLOR
    
        # Define windows to be used for bar charts
        # curses.newwin(height, width, begin_y, begin_x)
        self.leftScreen = curses.newwin(
                self.maxRows - self.TOP_START_ROW - self.INPUT_COLS - self.BOTTOM_END_ROW, 
                (self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL) // self.RIGHT_LEFT_SCALE * 1, 
                self.TOP_START_ROW,
                self.LEFT_START_COL
            ) 
        self.leftScreen.clear()
        self.leftScreen.border(0)

        # curses.newwin(height, width, begin_y, begin_x)
        self.rightScreen = curses.newwin(
                self.maxRows - self.TOP_START_ROW - self.INPUT_COLS - self.BOTTOM_END_ROW, 
                (self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL) - (self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL) // self.RIGHT_LEFT_SCALE * 1, 
                self.TOP_START_ROW,
                self.maxCols - self.maxCols // self.RIGHT_LEFT_SCALE * 2 - self.RIGHT_END_COL
            )
        self.rightScreen.clear()
        self.rightScreen.border(0)

        # curses.newwin(height, width, begin_y, begin_x)
        self.inputScreen = curses.newwin(
                self.INPUT_COLS, 
                self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL,
                self.maxRows - self.INPUT_COLS - self.BOTTOM_END_ROW,
                self.LEFT_START_COL
            )
        self.inputScreen.clear()
        self.inputScreen.border(0)

        self.componet_show()
        self.tab_screen_border()

        # input prefix
        rows, cols = self.inputScreen.getmaxyx()
        self.inputScreen.addstr(rows - self.INPUT_LINE, self.LEFT_START_COL, self.INPUT_PREFIX)

        self.leftScreen.refresh()
        self.rightScreen.refresh()
        self.inputScreen.refresh()


    def do_cmd(self, **param):
        cmd = param["cmd"]

        cmd_found = False
        cmd_error = False
        result = None
        component = None
        self.rightScreen.clear()
        self.rightScreen.border(0)
        rows, cols = self.rightScreen.getmaxyx()

        if cmd.isnumeric():
            cmd_index = int(cmd)
            if cmd_index < len(self.config["components"]) and cmd_index >= 0:
                component = self.config["components"][cmd_index]
                cmd = component["name"]
                cmd_found = True
        else:
            for component in self.config["components"]:
                name = component["name"]
                if name == cmd:
                    cmd_found = True
                    break

        output = []
        current_shell = ""
        if cmd_found:
            if component != None:
                for shell in component["shell"]:
                    if rows > 3:
                        self.rightScreen.addstr(1, self.LEFT_START_COL, "waiting '" + shell + "' end....")
                        self.rightScreen.refresh()

                    self.current_process = subprocess.Popen(
                            shell.split(" "),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8'
                        )
                    while True:
                        realtime_output = self.current_process.stdout.readline()
                        if realtime_output == '' and self.current_process.poll() is not None:
                            break

                        if realtime_output:
                            output.append(realtime_output.strip())
                          
                            line_index = 2
                            for line in output:
                                self.rightScreen.addstr(line_index, self.LEFT_START_COL, line)

                                line_index += 1
                                if line_index > (rows - 2):
                                    break

                            self.rightScreen.refresh()

                    if self.current_process.returncode != 0:
                        current_shell = shell
                        cmd_error = True
                        break

                if cmd_error:
                    output.append("error shell: '" + current_shell + "' in cmd: " + cmd)

        if not cmd_error:
            if not cmd_found:
                output.append("info: can't find this cmd: " + cmd)
            else:
                output.append("cmd: " + cmd + " Success")

        self.rightScreen.clear()
        i = 0
        with open(self.log_path, "a") as log_file:
            if len(output) <= (rows - 2):
                for line in output:
                    self.rightScreen.addstr(i + 1, self.LEFT_START_COL, "%02d " % i + line)
                    log_file.write(line + "\n")

                    i += 1
            else:
                for line in reversed(output):
                    self.rightScreen.addstr(rows - i - 1, self.LEFT_START_COL, "%02d " % (rows - i) + line)
                    log_file.write(line + "\n")

                    i += 1
                    if i > (rows - 2):
                        break
        
        self.rightScreen.border(0)
        self.rightScreen.refresh()
    
    def tab_screen_border(self):
        if self.tab_screen_index == 0:
            self.leftScreen.attron(curses.color_pair(self.FG_GREEN_COLOR))
            self.leftScreen.border(0)
            self.leftScreen.refresh()
            self.leftScreen.attroff(curses.color_pair(self.FG_GREEN_COLOR))

            self.rightScreen.attron(curses.color_pair(self.DEFAULT_COLOR))
            self.rightScreen.border(0)
            self.rightScreen.refresh()
            self.rightScreen.attroff(curses.color_pair(self.DEFAULT_COLOR))
        else:
            self.leftScreen.attron(curses.color_pair(self.DEFAULT_COLOR))
            self.leftScreen.border(0)
            self.leftScreen.refresh()
            self.leftScreen.attroff(curses.color_pair(self.DEFAULT_COLOR))

            self.rightScreen.attron(curses.color_pair(self.FG_GREEN_COLOR))
            self.rightScreen.border(0)
            self.rightScreen.refresh()
            self.rightScreen.attroff(curses.color_pair(self.FG_GREEN_COLOR))

    def componet_show(self):
        # init component
        COMPONENT_START_LINE = 1
        row_index = 0
        component_index = 0
        align_size = 0
        self.components = []
        rows, cols = self.leftScreen.getmaxyx()
        for component in self.config["components"]:
            name = component["name"]
            self.components.append(name)

            if len(name) > align_size:
                align_size = len(name)

        self.leftScreen.clear()

        # 数组内容少，或者索引目前小于rows数量时
        if ((rows - 2) >= len(self.config["components"]) or (self.left_cmd_index < (rows - 2))):
            for name in self.components[:rows - 2]:
                name = name + " " * (align_size - len(name))
                col_offset = self.LEFT_START_COL + ((cols - self.LEFT_START_COL - self.RIGHT_END_COL) // 2) - ((len(name) + len('%02d ' % (0))) // 2)
                if row_index == self.left_cmd_index:
                    self.leftScreen.addstr(COMPONENT_START_LINE + row_index, col_offset, '%02d ' % (component_index) + name, curses.color_pair(self.FG_GREEN_COLOR))
                else:
                    self.leftScreen.addstr(COMPONENT_START_LINE + row_index, col_offset, '%02d ' % (component_index) + name)

                row_index += 1
                component_index += 1

                if row_index >= rows:
                    break
        else:
            # 数组前闭后开，所以要整体+1
            component_index = self.left_cmd_index - (rows - 2) + 1
            components_tmp = self.components[self.left_cmd_index - (rows - 2) + 1:self.left_cmd_index + 1]

            for name in components_tmp:
                name = name + " " * (align_size - len(name))
                col_offset = self.LEFT_START_COL + ((cols - self.LEFT_START_COL - self.RIGHT_END_COL) // 2) - ((len(name) + len('%02d ' % (0))) // 2)
                if name.strip() == components_tmp[-1]:
                    self.leftScreen.addstr(COMPONENT_START_LINE + row_index, col_offset, '%02d ' % (component_index) + name, curses.color_pair(self.FG_GREEN_COLOR))
                else:
                    self.leftScreen.addstr(COMPONENT_START_LINE + row_index, col_offset, '%02d ' % (component_index) + name)

                row_index += 1
                component_index += 1
        
        self.leftScreen.refresh()
        self.rightScreen.refresh()
    
    def terminal_process(self):
        self.current_process.terminate()

    def main(self):
        while True:
            ch = self.mainScreen.getch()
            if ch == curses.KEY_RESIZE:
                self.mainScreen.clear()
                self.maxRows, self.maxCols = self.mainScreen.getmaxyx()
                self.mainScreen.border(0)
                self.mainScreen.addstr(1, self.LEFT_START_COL + ((self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL) // 2) - (len(self.name) // 2), self.name)
                
                rows = self.maxRows - self.TOP_START_ROW - self.INPUT_COLS - self.BOTTOM_END_ROW
                cols = (self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL) // self.RIGHT_LEFT_SCALE * 1
                self.leftScreen.clear()
                self.leftScreen.resize(rows, cols)
                self.leftScreen.border(0)

                rows = self.maxRows - self.TOP_START_ROW - self.INPUT_COLS - self.BOTTOM_END_ROW
                content_cols = self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL
                cols = content_cols - (content_cols) // self.RIGHT_LEFT_SCALE
                self.rightScreen.clear()
                self.rightScreen.resize(rows, cols)
                self.rightScreen.mvwin(
                        self.TOP_START_ROW,
                        self.maxCols - self.maxCols // self.RIGHT_LEFT_SCALE * 2 - self.RIGHT_END_COL
                    )
                self.rightScreen.border(0)

                rows = self.INPUT_COLS 
                cols = self.maxCols - self.LEFT_START_COL - self.RIGHT_END_COL
                self.inputScreen.clear()
                self.inputScreen.resize(rows, cols)
                self.inputScreen.mvwin(
                        self.maxRows - self.INPUT_COLS - self.BOTTOM_END_ROW,
                        self.LEFT_START_COL
                    )
                self.inputScreen.border(0)

                self.componet_show()
                
                # input prefix
                rows, cols = self.inputScreen.getmaxyx()
                self.inputScreen.addstr(rows - self.INPUT_LINE, self.LEFT_START_COL, self.INPUT_PREFIX, curses.color_pair(self.current_usb_status))
                self.inputScreen.addstr(rows - self.INPUT_LINE, self.LEFT_START_COL + len(self.INPUT_PREFIX), self.input_str)

                self.mainScreen.refresh()
                self.leftScreen.refresh()
                self.rightScreen.refresh()
                self.inputScreen.refresh()

                self.tab_screen_border()

            elif ch == self.KEY_BOARD_ESC:
                break
            elif ch == self.KEY_BOARD_ENTER:
                self.inputScreen.addstr(1, self.LEFT_START_COL + len(self.INPUT_PREFIX), " " * len(self.input_str))

                # exit program
                if self.input_str.strip() in ["exit", "quit"]:
                    break

                # do_cmd({"cmd": input_str})
                if len(self.input_str) > 0:
                    self.do_cmd(screen = self.rightScreen,cmd=self.input_str)
                else:
                    self.do_cmd(screen = self.rightScreen,cmd=self.components[self.left_cmd_index])

                self.input_str = ""
            elif ch == self.KEY_BOARD_BACKSPACE:
                self.inputScreen.addstr(1, self.LEFT_START_COL + len(self.INPUT_PREFIX) + len(self.input_str) - 1, " ")
                self.input_str = self.input_str[:-1]
            elif ch == ord("\t"):
                if self.tab_screen_index == 0:
                    self.tab_screen_index = 1
                else:
                    self.tab_screen_index = 1

                self.tab_screen_border()
            elif (ch >= ord("A") and ch <= ord("z")) or (ch >= ord("0") and (ch <= ord("9"))):
                self.input_str += chr(ch)
            elif ch == self.KEY_BOARD_UP:
                self.left_cmd_index -= 1
                if self.left_cmd_index < 0:
                    self.left_cmd_index = 0
                self.componet_show()
                self.tab_screen_border()
            elif ch == self.KEY_BOARD_DOWN:
                self.left_cmd_index += 1
                if self.left_cmd_index >= len(self.components):
                    self.left_cmd_index = len(self.components) - 1
                self.componet_show()
                self.tab_screen_border()
            else : 
                self.rightScreen.addstr(1, self.LEFT_START_COL, str(ch))
                self.rightScreen.refresh()
                pass

            self.inputScreen.addstr(1, self.LEFT_START_COL, self.INPUT_PREFIX + self.input_str)
            self.inputScreen.refresh()

        curses.endwin()

    # 1. How to parse json file with c-style comments?
    #   https://stackoverflow.com/questions/29959191/how-to-parse-json-file-with-c-style-comments
    def GetJsonFromFile(self, filePath):
        contents = ""

        fh = open(filePath, encoding="utf-8")
        for line in fh:
            cleanedLine = line.split("//", 1)[0]
            if len(cleanedLine) > 0 and line.endswith("\n") and "\n" not in cleanedLine:
                cleanedLine += "\n"
            contents += cleanedLine
        fh.close

        while "/*" in contents:
            preComment, postComment = contents.split("/*", 1)
            contents = preComment + postComment.split("*/", 1)[1]

        return contents

adbtools = None
def handler(signum, frame):
    adbtools.terminal_process()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)

    # config path
    json_file_path = ""
    log_file_path = os.path.dirname(__file__) + "/log.txt"
    if len(sys.argv) != 2:
        json_file_path = "tools/adbtools.json"
    else:
        json_file_path = sys.argv[1]

    adbtools = AdbTools({"config": json_file_path, "log": log_file_path})
    adbtools.main()
