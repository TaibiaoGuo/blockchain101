# !/usr/bin python3
# encoding:utf-8
'''
 @Time     :2020/10/22 2:01 AM
 @Author   :TaibiaoGuo
 @FileName :cliClient
 @Github   :https://github.com/TaibiaoGuo
 @Describe : cliClient 实现了命令行客户端的交互逻辑
'''
import os
import subprocess

import dialog

from p2pChat import ClientFactory


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

    def personal_info_input_box(self):
        elements = [
            ("Size (cm)", 1, 1, "175", 1, 20, 4, 3),
            ("Weight (kg)", 2, 1, "85", 2, 20, 4, 3),
            ("City", 3, 1, "Groboule-les-Bains", 3, 20, 15, 25),
            ("State", 4, 1, "Some Lost Place", 4, 20, 15, 25),
            ("Country", 5, 1, "Nowhereland", 5, 20, 15, 20),
            ("My", 6, 1, "I hereby declare that, upon leaving this "
                         "world, all", 6, 20, 0, 0),
            ("Very", 7, 1, "my fortune shall be transferred to Florent "
                           "Rougon's", 7, 20, 0, 0),
            ("Last", 8, 1, "bank account number 000 4237 4587 32454/78 at "
                           "Banque", 8, 20, 0, 0),
            ("Will", 9, 1, "Cantonale Vaudoise, Lausanne, Switzerland.",
             9, 20, 0, 0)]

        code, fields = d.form("Please fill in some personal information:",
                              elements, width=77)
        return fields


class MyUI:
    def __init__(self):
        # The MyDialog instance 'd' could be passed via the constructor and
        # stored here as a class or instance attribute. However, for the sake
        # of readability, we'll simply use a module-level attribute ("global")
        # (d.msgbox(...) versus self.d.msgbox(...), etc.).
        global d
        self.Dialog_instance = dialog.Dialog(dialog="dialog")
        d = MyUI(self.Dialog_instance)
        backtitle = "点对点聊天"
        d.set_background_title(backtitle)
        # These variables take the background title into account
        self.max_lines, self.max_cols = d.maxsize(backtitle=backtitle)
        self.demo_context = self.setup_debug()
        # Warn if the terminal is smaller than this size
        self.min_rows, self.min_cols = 24, 80
        self.term_rows, self.term_cols, self.backend_version = \
            self.get_term_size_and_backend_version()

    def personal_info_input_box(self):
        elements = [
            ("姓名", 1, 1, "张三", 1, 20, 4, 10),
            ("聊天室昵称", 2, 1, "张三丰", 2, 20, 15, 30),
            ("打招呼宣言", 3, 1, "嗨，我是张三丰", 3, 20, 15, 40)]

        code, fields = d.form("请输入你的基本信息。遇到新朋友会自动发送打招呼信息。",
                              elements, width=77)
        return fields


if __name__ == "__main__":
    app = MyUI()
    app.personal_info_input_box()
