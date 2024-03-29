import json
import os
import sys
import curses
import unicodedata
import logging
import _thread
import time
from queue import Queue

from anpp.ShellCMD import Shell

class CmdWindow:

    def __init__(self, config: dict):
        logFormat = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(format=logFormat, level=logging.DEBUG, filename=os.path.expanduser('~') + "/.anpp/run.log", filemode='a')
        self.log = logging.getLogger()
        self.log.debug("Cmd Window start init")

        self.logBuffer = []

        # self.cmdSets            = config["cmdSets"]
        self.cmdSets            = config
        self.currentCmdSets     = self.cmdSets
        self.currentFocusCmdSet = self.currentCmdSets[list(self.currentCmdSets.keys())[0]]
        self.cmdSetsIndent      = []

        self.shCmd = None
        self.shCmdStatus = None
        self.needFreshInfo = True
        self.needFreshStatus = True
        self.queue = Queue()
        self.shell = Shell(self.queue)
        self.activeScroll = False
        self.activeScrollIndex = 0

        # keyboard code
        KEY_BOARD_ENTER = 10
        KEY_BOARD_ESC = 27
        KEY_BOARD_Search = 47

        KEY_BOARD_UP    = curses.KEY_UP
        KEY_BOARD_DOWN  = curses.KEY_DOWN
        KEY_BOARD_LEFT  = curses.KEY_LEFT
        KEY_BOARD_RIGHT = curses.KEY_RIGHT
        if sys.platform.startswith('win32'):
            KEY_BOARD_UP    = 450
            KEY_BOARD_DOWN  = 456
            KEY_BOARD_LEFT  = 452
            KEY_BOARD_RIGHT = 454
        elif sys.platform.startswith('darwin'):
            pass

        # 初始化一个窗口
        self.mainScreen = curses.initscr()
        # 绘制边框
        # self.mainScreen.border(0)
        # 使用curses通常要关闭屏幕回显，目的是读取字符仅在适当的环境下输出
        curses.noecho()
        # 应用程序一般是立即响应的，即不需要按回车就立即回应的，这种模式叫cbreak模式，相反的常用的模式是缓冲输入模式
        curses.cbreak()
        # 终端经常返回特殊键作为一个多字节的转义序列，比如光标键，或者导航键比如Page UP和Home键。
        # curses可以针对这些序列做一次处理，比如curses.KEY_LEFT返回一个特殊的值。要完成这些工作，必须开启键盘模式。
        self.mainScreen.keypad(1)
        # 不显示光标
        curses.curs_set(0) 

        # color
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        self.DEFAULT_COLOR = 1
        self.FG_GREEN_COLOR = 2

        # 获取当前行列信息
        self.maxRows = curses.LINES
        self.maxCols = curses.COLS
        MIN_ROWS = 24
        MIN_COLS = 80
        if (self.maxRows < MIN_ROWS or self.maxCols < MIN_COLS):
            curses.endwin()
            print("terminal rows must more than " + str(MIN_ROWS))
            print("terminal cols must more than " + str(MIN_COLS))
            exit(0)

        # 当前选择的目标程序
        index = 0
        # 终端可显示的程序列表第一个程序，因为存在列表显示不全，只能显示部分程序列表的问题
        topIndex = 0
        # Search模式
        inSearchMode = False
        # 输入字符串
        inputString = ""

        # Define windows to be used for bar charts
        # curses.newwin(height, width, begin_y, begin_x)
        self.selectScreen = curses.newwin(
                ((self.maxRows - 3) // 3 * 2),                      # 上下边框 + 内容
                self.maxCols,                                       # 左右边框 + 左右空列
                0,                                                  # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
                0                                                   # 主屏左边框 + 左空列
            )

        # Define windows to be used for bar charts
        # curses.newwin(height, width, begin_y, begin_x)
        self.infoScreen = curses.newwin(
                ((self.maxRows - 3) - ((self.maxRows - 3) // 3 * 2)),   # 上下边框 + 内容
                self.maxCols,                                           # 左右边框 + 左右空列
                ((self.maxRows - 3) // 3 * 2),                          # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
                0                                                       # 主屏左边框 + 左空列
            )

        # Define windows to be used for bar charts
        # curses.newwin(height, width, begin_y, begin_x)
        self.statusScreen = curses.newwin(
                3,                                              # 上下边框 + 内容
                self.maxCols,                                   # 左右边框 + 左右空列
                self.maxRows - 3,                               # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
                0                                               # 主屏左边框 + 左空列
            )

        self.selectScreen.border(0)
        self.infoScreen.border(0)
        self.statusScreen.border(0)

        self.drawList(self.selectScreen, list(self.currentCmdSets.keys()), topIndex, index)

        self.mainScreen.refresh()
        self.selectScreen.refresh()
        self.infoScreen.refresh()
        self.statusScreen.refresh()

        _thread.start_new_thread(self.infoRefresh, ("info refresh",))
        _thread.start_new_thread(self.runShellCmd, ("shell cmd",))

        while True:
            # 等待按键事件
            ch = self.mainScreen.getch()

            self.log.debug("key %d" % (ch))

            if self.activeScroll:
                if ch == KEY_BOARD_UP or ch == ord('k'):
                    self.activeScrollIndex -= 1
                elif ch == KEY_BOARD_DOWN or ch == ord('j'):
                    self.activeScrollIndex += 1
                elif ch == ord('s'):
                    if self.activeScroll:
                        self.activeScroll = False
                else:
                    pass

                self.needFreshInfo = True

                continue

            if ch == curses.KEY_RESIZE:
                self.mainScreen.clear()
                self.maxRows, self.maxCols = self.mainScreen.getmaxyx()

                if (self.maxRows < MIN_ROWS or self.maxCols < MIN_COLS):
                    curses.endwin()
                    print("terminal rows must more than " + str(MIN_ROWS))
                    print("terminal cols must more than " + str(MIN_COLS))
                    exit(0)
                
                # Define windows to be used for bar charts
                # curses.newwin(height, width, begin_y, begin_x)
                self.selectScreen = curses.newwin(
                        ((self.maxRows - 3) // 3 * 2),                      # 上下边框 + 内容
                        self.maxCols,                                       # 左右边框 + 左右空列
                        0,                                                  # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
                        0                                                   # 主屏左边框 + 左空列
                    )

                # Define windows to be used for bar charts
                # curses.newwin(height, width, begin_y, begin_x)
                self.infoScreen = curses.newwin(
                        ((self.maxRows - 3) - ((self.maxRows - 3) // 3 * 2)),       # 上下边框 + 内容
                        self.maxCols,                                               # 左右边框 + 左右空列
                        ((self.maxRows - 3) // 3 * 2),                              # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
                        0                                                           # 主屏左边框 + 左空列
                    )

                # Define windows to be used for bar charts
                # curses.newwin(height, width, begin_y, begin_x)
                self.statusScreen = curses.newwin(
                        3,                                              # 上下边框 + 内容
                        self.maxCols,                                   # 左右边框 + 左右空列
                        self.maxRows - 3,                               # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
                        0                                               # 主屏左边框 + 左空列
                    )

                self.selectScreen.border(0)

                self.drawList(self.selectScreen, list(self.getCurrentCmdSetsList()), topIndex, index)

                self.mainScreen.refresh()
                self.selectScreen.refresh()
                self.needFreshInfo = True
                self.needFreshStatus = True

                inputString = ""

                continue

            # 退出按键
            elif ch == KEY_BOARD_ESC or ch == ord('q'):
                index = -1
                break
            elif ch == ord('s'):
                if not self.activeScroll:
                    self.activeScroll = True
                    self.activeScrollIndex = 0
                    self.needFreshInfo = True
            elif ch == ord('c'):
                if self.shell != None:
                    self.shell.terminate()

                    self.logBuffer.append("terminate: " + self.shCmd)

                continue
            elif ch == KEY_BOARD_UP or ch == ord('k'):
                self.log.debug("key up")

                index -= 1
                if index <= 0:
                    index = 0

                # 处理上边缘
                if topIndex == (index + 1):
                    topIndex -= 1

                self.selectScreen.clear()
                self.selectScreen.border(0)

                self.drawList(self.selectScreen, self.getCurrentCmdSetsList(), topIndex, index)

                self.selectScreen.refresh()
            elif ch == KEY_BOARD_DOWN or ch == ord('j'):
                self.log.debug("key down")

                index += 1
                if index >= len(self.getCurrentCmdSetsList()):
                    index = len(self.getCurrentCmdSetsList()) - 1
                else:
                    # 处理下边缘
                    # 上下两个边框占用2行
                    if (topIndex + (self.maxRows - 2)) == index :
                        topIndex += 1

                self.selectScreen.clear()
                self.selectScreen.border(0)

                self.drawList(self.selectScreen, self.getCurrentCmdSetsList(), topIndex, index)

                self.selectScreen.refresh()
            elif ch == KEY_BOARD_LEFT or ch == ord('h'):
                self.log.debug(self.cmdSetsIndent)
                if len(self.cmdSetsIndent) == 0:
                    continue

                self.currentCmdSets = self.cmdSets
                self.cmdSetsIndent = self.cmdSetsIndent[0:-1]
                for item in self.cmdSetsIndent:
                    self.currentCmdSets = self.currentCmdSets[item]
                
                topIndex = 0
                index = 0

                self.selectScreen.clear()
                self.selectScreen.border(0)

                self.drawList(self.selectScreen, self.getCurrentCmdSetsList(), topIndex, index)

                self.selectScreen.refresh()
            elif ch == KEY_BOARD_ENTER or ch == KEY_BOARD_RIGHT or ch == ord('l'):
                self.log.debug("enter")
                listTarget = None
                if isinstance(self.currentCmdSets, list) :
                    listTarget = self.getCurrentCmdSetsList()

                    if self.shCmd == None:
                        self.shCmd = listTarget[index]
                        self.shCmdStatus = "prepare"

                        self.logBuffer.append(self.shCmd)
                    else:
                        self.logBuffer.append(self.shCmd + "is running")

                else:
                    key = list(self.currentCmdSets.keys())[index]
                    if isinstance(self.currentCmdSets[key], str):
                        self.logBuffer.append(key + ": " + self.currentCmdSets[key])
                    else:
                        self.cmdSetsIndent.append(key)
                        self.currentCmdSets = self.currentCmdSets[key]

                        topIndex = 0
                        index = 0

                    listTarget = self.getCurrentCmdSetsList()

                self.selectScreen.clear()
                self.selectScreen.border(0)

                self.drawList(self.selectScreen, listTarget, topIndex, index)

                self.selectScreen.refresh()

                self.needFreshInfo = True
                self.needFreshStatus = True
            elif ch == KEY_BOARD_Search:
                # /字符表示进入检索，参考vim
                inputString += "/"


                # 开启光标显示
                curses.curs_set(1) 

            else:
                pass

        # 退出curses环境
        curses.endwin()
    
    def infoRefresh(self, name):
        self.log.debug(name)

        while True:

            if self.needFreshInfo or (not self.queue.empty()):
                if self.queue.qsize() > 0:
                    self.logBuffer.append(self.queue.get())

                self.infoScreen.clear()
                if self.activeScroll:
                    self.infoScreen.attron(curses.color_pair(self.FG_GREEN_COLOR))
                self.infoScreen.border(0)
                if self.activeScroll:
                    self.infoScreen.attroff(curses.color_pair(self.FG_GREEN_COLOR))
                self.drawInfo(self.infoScreen)
                self.infoScreen.refresh()

                self.needFreshInfo = False

            if self.needFreshStatus:
                self.statusScreen.clear()
                self.statusScreen.border(0)
                self.drawStatus(self.statusScreen)
                self.statusScreen.refresh()

                self.needFreshStatus = False

            time.sleep(0.1)

    def runShellCmd(self, name):
        self.log.debug(name)

        while True:

            if self.shCmd != None:
                self.shCmdStatus = "running"
                self.needFreshStatus = True

                ret = self.shell.start(self.shCmd)
                self.log.debug(ret)
                # self.logBuffer.append(ret["output"])

                self.shCmdStatus = "stop"
                self.shCmd = None
                self.needFreshInfo = True
                self.needFreshStatus = True

            time.sleep(0.1)

    def getCurrentCmdSetsList(self):
        if isinstance(self.currentCmdSets, list):
            if isinstance(self.currentCmdSets[0], str):
                return self.currentCmdSets
            else:
                targetList = []
                for item in self.currentCmdSets:
                    targetList.append(item["cmd"])

                return targetList
        else:
            return list(self.currentCmdSets.keys())

    def _strWidth(self, chs):

        chLength = 0
        for ch in chs:
            if (unicodedata.east_asian_width(ch) in ('F','W','A')):
                chLength += 2
            else:
                chLength += 1

        return chLength

    def drawList(self, window: curses.window, listData, topIndex, index):
        row  = 1
        self.maxRows, self.maxCols = window.getmaxyx()
        listDataMaxLen = 0

        for item in listData:
            if len(item) > listDataMaxLen:
                listDataMaxLen = len(item)

        # 上下两个边框占用2行
        if (self.maxRows - 2) > len(listData):
            for item in listData:
                # 行从1开始绘图，index是从0开始算的
                if ((row - 1) == index):
                    window.addstr(row, self.maxCols // 2 - listDataMaxLen // 2, item, curses.color_pair(curses.COLOR_GREEN))
                else:
                    window.addstr(row, self.maxCols // 2 - listDataMaxLen // 2, item)

                row += 1
        else:
            # 上下两个边框占用2行
            for item in listData[topIndex:topIndex + (self.maxRows - 2)]:
                # 行从1开始绘图，index是从0开始算的
                if (row - 1) == (index - topIndex):
                    window.addstr(row, self.maxCols // 2 - listDataMaxLen // 2, item, curses.color_pair(curses.COLOR_GREEN))
                else:
                    window.addstr(row, self.maxCols // 2 - listDataMaxLen // 2, item)

                row += 1

    def drawInfo(self, window: curses.window):
        maxRows, maxCols = window.getmaxyx()

        if self.activeScrollIndex > 0:
            self.activeScrollIndex = 0
        elif self.activeScrollIndex < (0 - (len(self.logBuffer) - (maxRows - 2))):
            self.activeScrollIndex = (0 - (len(self.logBuffer) - (maxRows - 2)))
        else:
            pass

        for row in range(maxRows - 2):
            if len(self.logBuffer) == 0:
                break

            if row >= len(self.logBuffer):
                break

            if (maxRows - 2) > len(self.logBuffer):
                window.addstr(row + 1, 1, self.logBuffer[row])
            else:
                offset = len(self.logBuffer) - (maxRows - 2) + row
                offset += self.activeScrollIndex
                window.addstr(row + 1, 1, self.logBuffer[offset])

    def drawStatus(self, window: curses.window):
        if self.shCmd == None:
            statusString = " " * (self.maxCols - 2)
            window.addstr(1, 1, statusString)
        else:
            statusString = (self.shCmd + " is " + self.shCmdStatus)[0:(self.maxCols - 2)]
            window.addstr(1, 1, statusString)

if __name__ == "__main__" :
    configFile = open(os.path.expanduser('~') + "/.anpp/ACmdSets.json")
    config = json.load(configFile)
    cmdWindow = CmdWindow(config)
