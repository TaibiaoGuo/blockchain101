# !/usr/bin python3
# encoding:utf-8
'''
 @Time     :2020/10/22 2:01 AM
 @Author   :TaibiaoGuo
 @FileName :cliClient
 @Github   :https://github.com/TaibiaoGuo
 @Describe : cliClient 实现了命令行客户端的交互逻辑
'''
import locale
import os
import subprocess
import sys
import textwrap
import traceback
from datetime import time

import dialog

from p2pChat import ClientFactory

# Global parameters
params = {}

tw = textwrap.TextWrapper(width=78, break_long_words=False,
                          break_on_hyphens=True)
from textwrap import dedent

try:
    from textwrap import indent
except ImportError:
    try:
        callable  # Normally, should be __builtins__.callable
    except NameError:
        # Python 3.1 doesn't have the 'callable' builtin function. Let's
        # provide ours.
        def callable(f):
            return hasattr(f, '__call__')


    def indent(text, prefix, predicate=None):
        l = []

        for line in text.splitlines(True):
            if (callable(predicate) and predicate(line)) \
                    or (not callable(predicate) and predicate) \
                    or (predicate is None and line.strip()):
                line = prefix + line
            l.append(line)

        return ''.join(l)


class CLIClient(ClientFactory):
    """
    CLIClient 实现了命令行交互的客户端抽象工厂
    """

    def new_client(self, server_ip, server_port):
        pass

    def ping(self):
        pass

    def message_handle(self):
        pass


class ChatDialog:
    """
    Dialog库的简单封装，实现了p2pChat所需要的基本UI组件
    """

    def __init__(self, Dialog_instance):
        self.dlg = Dialog_instance

    def clear_screen(self):
        program = "clear"

        try:
            p = subprocess.Popen([program], shell=False, stdout=None,
                                 stderr=None, close_fds=True)
            retcode = p.wait()
        except os.error as e:
            self.msgbox("Unable to execute program '%s': %s." % (program,
                                                                 e.strerror),
                        title="Error")
            return False

        if retcode > 0:
            msg = "Program %s returned exit status %d." % (program, retcode)
        elif retcode < 0:
            msg = "Program %s was terminated by signal %d." % (program, -retcode)
        else:
            return True

        self.msgbox(msg)
        return False

    def check_exit_request(self, code, ignore_Cancel=False):
        if code == self.CANCEL and ignore_Cancel:
            return True

        if code in (self.CANCEL, self.ESC):
            button_name = {self.CANCEL: "Cancel",
                           self.ESC: "Escape"}
            msg = "You pressed {0} in the last dialog box. Do you want " \
                  "to exit this demo?".format(button_name[code])
            if self.dlg.yesno(msg) == self.OK:
                sys.exit(0)
            else:
                return False
        else:
            return True
    
    def widget_loop(self, method):
        def wrapper(*args, **kwargs):
            while True:
                res = method(*args, **kwargs)
                if hasattr(method, "retval_is_code") \
                        and getattr(method, "retval_is_code"):
                    code = res
                else:
                    code = res[0]
                if self.check_exit_request(code):
                    break
            return res

        return wrapper

    def __getattr__(self, name):
        obj = getattr(self.dlg, name)
        if hasattr(obj, "is_widget") and getattr(obj, "is_widget"):
            return self.widget_loop(obj)
        else:
            return obj

    def _Yesno(self, *args, **kwargs):
        """Convenience wrapper around dialog.Dialog.yesno().

        Return the same exit code as would return
        dialog.Dialog.yesno(), except for ESC which is handled as in
        the rest of the demo, i.e. make it spawn the "confirm quit"
        dialog.

        """
        # self.yesno() automatically spawns the "confirm quit" dialog if ESC or
        # the "No" button is pressed, because of self.__getattr__(). Therefore,
        # we have to use self.dlg.yesno() here and call
        # self.check_exit_request() manually.
        while True:
            code = self.dlg.yesno(*args, **kwargs)
            # If code == self.CANCEL, it means the "No" button was chosen;
            # don't interpret this as a wish to quit the program!
            if self.check_exit_request(code, ignore_Cancel=True):
                break

        return code

    def Yesno(self, *args, **kwargs):
        """Convenience wrapper around dialog.Dialog.yesno().

        Return True if "Yes" was chosen, False if "No" was chosen,
        and handle ESC as in the rest of the demo, i.e. make it spawn
        the "confirm quit" dialog.

        """
        return self._Yesno(*args, **kwargs) == self.dlg.OK

    def Yesnohelp(self, *args, **kwargs):
        """Convenience wrapper around dialog.Dialog.yesno().

        Return "yes", "no", "extra" or "help" depending on the button
        that was pressed to close the dialog. ESC is handled as in
        the rest of the demo, i.e. it spawns the "confirm quit"
        dialog.

        """
        kwargs["help_button"] = True
        code = self._Yesno(*args, **kwargs)
        d = {self.dlg.OK: "yes",
             self.dlg.CANCEL: "no",
             self.dlg.EXTRA: "extra",
             self.dlg.HELP: "help"}

        return d[code]


class PersonalInfo:
    def __init__(self):
        # 姓名
        self.name = ""
        # 昵称
        self.nick_name = ""
        # 打招呼内容
        self.hi_message = ""

    def new_personal_info(self):
        return PersonalInfo

    def set_personal_info(self, fields):
        self.name = fields[0]
        self.nick_name = fields[1]
        self.hi_message = fields[3]
        
    def get_name(self):
        return self.name
    def get_nick_name(self):
        return self.nick_name
    def get_hi_message(self):
        return self.hi_message

user_personal_info = PersonalInfo().new_personal_info()

class MyUI:
    def __init__(self):
        # The MyDialog instance 'd' could be passed via the constructor and
        # stored here as a class or instance attribute. However, for the sake
        # of readability, we'll simply use a module-level attribute ("global")
        # (d.msgbox(...) versus self.d.msgbox(...), etc.).
        global d
        # If you want to use Xdialog (pathnames are also OK for the 'dialog'
        # argument), you can use:
        #   dialog.Dialog(dialog="Xdialog", compat="Xdialog")
        self.Dialog_instance = dialog.Dialog(dialog="dialog")
        # See the module docstring at the top of the file to understand the
        # purpose of MyDialog.
        d = ChatDialog(self.Dialog_instance)
        backtitle = "孤独星球"
        d.set_background_title(backtitle)
        # These variables take the background title into account
        self.max_lines, self.max_cols = d.maxsize(backtitle=backtitle)
        # Warn if the terminal is smaller than this size
        self.min_rows, self.min_cols = 24, 80
        self.term_rows, self.term_cols, self.backend_version = \
            self.get_term_size_and_backend_version()

    def get_term_size_and_backend_version(self):
        # Avoid running '<backend> --print-version' every time we need the
        # version
        backend_version = d.cached_backend_version
        if not backend_version:
            print(tw.fill(
                "Unable to retrieve the version of the dialog-like backend. "
                "Not running cdialog?") + "\nPress Enter to continue.",
                  file=sys.stderr)
            input()

        term_rows, term_cols = d.maxsize(use_persistent_args=False)
        if term_rows < self.min_rows or term_cols < self.min_cols:
            print(tw.fill(dedent("""\
             Your terminal has less than {0} rows or less than {1} columns;
             you may experience problems with the demo. You have been warned."""
                                 .format(self.min_rows, self.min_cols)))
                  + "\nPress Enter to continue.")
            input()

        return (term_rows, term_cols, backend_version)

    def progressboxoid(self, widget, func_name, text, **kwargs):
        # 没有对 os.error 异常做处理
        read_fd, write_fd = os.pipe()

        child_pid = os.fork()
        if child_pid == 0:
            try:
                # We are in the child process. We MUST NOT raise any exception.
                # No need for this one in the child process
                os.close(read_fd)

                # Python file objects are easier to use than file descriptors.
                # For a start, you don't have to check the number of bytes
                # actually written every time...
                # "buffering = 1" means wfile is going to be line-buffered
                with os.fdopen(write_fd, mode="w", buffering=1) as wfile:
                    for line in text.split('\n'):
                        wfile.write(line + '\n')
                        time.sleep(0.02 if params["fast_mode"] else 1.2)

                os._exit(0)
            except:
                os._exit(127)

        # We are in the father process. No need for write_fd anymore.
        os.close(write_fd)
        # Call d.progressbox() if widget == "progressbox"
        #      d.programbox() if widget == "programbox"
        # etc.
        getattr(d, widget)(
            fd=read_fd,
            title="{0} example with a file descriptor".format(widget),
            **kwargs)

        # Now that the progressbox is over (second child process, running the
        # dialog-like program), we can wait() for the first child process.
        # Otherwise, we could have a deadlock in case the pipe gets full, since
        # dialog wouldn't be reading it.
        exit_info = os.waitpid(child_pid, 0)[1]
        if os.WIFEXITED(exit_info):
            exit_code = os.WEXITSTATUS(exit_info)
        elif os.WIFSIGNALED(exit_info):
            d.msgbox("%s(): first child process terminated by signal %d" %
                     (func_name, os.WTERMSIG(exit_info)))
        else:
            assert False, "How the hell did we manage to get here?"

        if exit_code != 0:
            d.msgbox("%s(): first child process ended with exit status %d"
                     % (func_name, exit_code))

    def run(self):
            self.main_logic()

    def main_logic(self):
        """
        UI部分的主逻辑
        UI组件会在被调用时在终端渲染出界面
        """
        # 1、启动贴片
        self.introduction_info_box()
        # 2、用户输入个人信息
        self.personal_info_input_box()


    def introduction_info_box(self):
        func_name = "Soul APP"
        text = """\
这个时代不浪漫到什么程度了呢？

深情的人，都被叫做舔狗；
忧郁糟心的人，被称为矫情。

放弃挣扎和绝望了，也只会自嘲地说一句：

“就让我丧着吧。”




你突然好像就对所有事物都失去兴趣了，
曾经想去做的事不想做了，
曾经拼命想吸引别人注意，现在却丧失了表达的欲望。

看见月亮就只是月亮，听见雨声就只是雨声。
对自己好的人，一眼就看穿他背后的目的；

不再轻易相信任何人任何话，
手机从不离身，
独自吃外卖的次数
比和朋友约着出去吃的次数多了太多。

不再轻易地吐露自己的心声，
变得独立，变得不喜欢麻烦任何人，

你其实并不是不浪漫，但大多时候已经懒得去浪漫了。
相比起自由自在，你觉得任何一种关系都会束缚自己。



当然最主要的，还是知音难寻。
所以身边的人都变得无足轻重起来。

但，其实你依然很浪漫；
像春风一样，自由而浪漫着。

你知道，其实有些人，
我们已经见过这辈子的最后一面了。

只是当时我们并没有发觉。
你表现得不喜欢任何事物，
是因为你很少得到过想要的。

人和人之间想要保持长久舒适的关系，
靠的是共性和吸引，
而不是压迫、捆绑、奉承，
和一味地付出以及道德捆绑式的自我感动。
你还是有忧郁的时候，
只不过你把那些话发在了漂流瓶里，不会有任何人知道。

你看山中有月亮，便会枕着月亮睡觉；
你听见了下雨，就听见了温柔的歌。

Soul APP 这个现实的世界里，
依然让我们浪漫的社交软件。

* 匿名广场树洞：让你无顾虑地表达自己；
* 灵魂匹配：找到与你契合的灵魂；

这世上所有的浪漫，都是因为你愿意为他浪费。
浪费时间，浪费精力，浪费爱...
但如果我不能浪费在喜欢的人身上，
那我宁愿把它浪费在自己身上。
做一阵春风，拥抱我，或者让我永远自由浪漫。

Soul APP 跟随灵魂找到你
找到契合的灵魂 找到真实的自己
"""

        return self.progressboxoid("progressbox", func_name, text)

    def personal_info_input_box(self):
        elements = [
            ("姓名", 1, 1, "李佳仪", 1, 20, 4, 10),
            ("聊天室昵称", 2, 1, "人间", 2, 20, 15, 30),
            ("打招呼宣言", 3, 1, "世界上美好的东西不太多，立秋傍晚从河对岸吹来的风", 3, 20, 15, 40)]

        code, fields = d.form("请输入你的基本信息。遇到新朋友会自动发送打招呼信息。",
                              elements, width=77)
        # 将用户信息填入全局变量 user_personal_info
        user_personal_info.set_personal_info(fields)
        return fields
    def welcome_tutorial_box(self):
        text = """\

"""





if __name__ == "__main__":
    """This demo shows the main features of pythondialog."""
    locale.setlocale(locale.LC_ALL, '')

    try:
        app = MyUI()
        app.run()
    except dialog.error as exc_instance:
        # The error that causes a PythonDialogErrorBeforeExecInChildProcess to
        # be raised happens in the child process used to run the dialog-like
        # program, and the corresponding traceback is printed right away from
        # that child process when the error is encountered. Therefore, don't
        # print a second, not very useful traceback for this kind of exception.
        if not isinstance(exc_instance,
                          dialog.PythonDialogErrorBeforeExecInChildProcess):
            print(traceback.format_exc(), file=sys.stderr)

        print("Error (see above for a traceback):\n\n{0}".format(
            exc_instance), file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

