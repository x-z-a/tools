import wx
import wx.lib.agw.hyperlink as hl
import secrets
import string
import os

class PasswordGenerator(wx.Frame):
    def __init__(self):
        super().__init__(None, title="密钥生成工具", size=(500, 550))
        self.SetMinSize((500, 350))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 创建设置区域
        settings_box = wx.StaticBox(panel, label="设置选项")
        sbs = wx.StaticBoxSizer(settings_box, wx.VERTICAL)
        
        # 数字选项
        self.chk_digit = wx.CheckBox(panel, label="包含数字 (0-9)")
        self.chk_digit.SetValue(True)
        sbs.Add(self.chk_digit, 0, wx.ALL, 5)
        
        # 大写字母选项
        self.chk_upper = wx.CheckBox(panel, label="包含大写字母 (A-Z)")
        self.chk_upper.SetValue(True)
        sbs.Add(self.chk_upper, 0, wx.ALL, 5)
        
        # 小写字母选项
        self.chk_lower = wx.CheckBox(panel, label="包含小写字母 (a-z)")
        self.chk_lower.SetValue(True)
        sbs.Add(self.chk_lower, 0, wx.ALL, 5)
        
        # 位数设置
        hbox_length = wx.BoxSizer(wx.HORIZONTAL)
        st_length = wx.StaticText(panel, label="密钥位数:")
        hbox_length.Add(st_length, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.spin_length = wx.SpinCtrl(panel, min=4, max=128, initial=16)
        hbox_length.Add(self.spin_length, 0, wx.ALL, 5)
        sbs.Add(hbox_length, 0, wx.ALL, 5)
        
        vbox.Add(sbs, 0, wx.EXPAND|wx.ALL, 10)
        
        # 生成按钮
        self.btn_generate = wx.Button(panel, label="生成密钥")
        self.btn_generate.Bind(wx.EVT_BUTTON, self.on_generate)
        vbox.Add(self.btn_generate, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        # 结果显示
        result_box = wx.StaticBox(panel, label="生成的密钥")
        rbs = wx.StaticBoxSizer(result_box, wx.VERTICAL)
        
        self.txt_result = wx.TextCtrl(panel, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.txt_result.SetMinSize((-1, 100))
        rbs.Add(self.txt_result, 1, wx.EXPAND|wx.ALL, 5)
        
        # 操作按钮
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_copy = wx.Button(panel, label="复制密钥")
        self.btn_copy.Bind(wx.EVT_BUTTON, self.on_copy)
        self.btn_save = wx.Button(panel, label="保存到文件")
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        
        hbox_buttons.Add(self.btn_copy, 0, wx.RIGHT, 10)
        hbox_buttons.Add(self.btn_save, 0)
        rbs.Add(hbox_buttons, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        vbox.Add(rbs, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        # 状态栏
        self.status_bar = wx.StatusBar(panel)
        vbox.Add(self.status_bar, 0, wx.EXPAND)
        
        panel.SetSizer(vbox)
        self.Centre()
        
        # 初始禁用操作按钮
        self.btn_copy.Disable()
        self.btn_save.Disable()
        
        # 版权信息
        copyright = hl.HyperLinkCtrl(panel, -1, "© 2025 密钥生成工具", 
                                    URL="https://github.com/x-z-a/tools")
        vbox.Add(copyright, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)
        
        self.Show()

    def generate_password(self, length, use_digits, use_upper, use_lower):
        """生成安全的随机密钥"""
        characters = ""
        if use_digits:
            characters += string.digits
        if use_upper:
            characters += string.ascii_uppercase
        if use_lower:
            characters += string.ascii_lowercase
        
        if not characters:
            wx.MessageBox("请至少选择一种字符类型！", "错误", wx.OK | wx.ICON_ERROR)
            return ""
        
        # 使用secrets模块生成安全随机密钥
        return ''.join(secrets.choice(characters) for _ in range(length))

    def on_generate(self, event):
        """生成按钮事件处理"""
        length = self.spin_length.GetValue()
        use_digits = self.chk_digit.GetValue()
        use_upper = self.chk_upper.GetValue()
        use_lower = self.chk_lower.GetValue()
        
        password = self.generate_password(length, use_digits, use_upper, use_lower)
        
        if password:
            self.txt_result.SetValue(password)
            self.btn_copy.Enable()
            self.btn_save.Enable()
            self.status_bar.SetStatusText(f"成功生成 {length} 位密钥")

    def on_copy(self, event):
        """复制按钮事件处理"""
        if self.txt_result.GetValue():
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(self.txt_result.GetValue()))
                wx.TheClipboard.Close()
                self.status_bar.SetStatusText("密钥已复制到剪贴板")
            else:
                self.status_bar.SetStatusText("无法访问剪贴板")

    def on_save(self, event):
        """保存按钮事件处理"""
        password = self.txt_result.GetValue()
        if not password:
            return
            
        with wx.FileDialog(self, "保存密钥", wildcard="文本文件 (*.txt)|*.txt",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
                
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as f:
                    f.write(password)
                self.status_bar.SetStatusText(f"密钥已保存到: {pathname}")
            except IOError:
                wx.MessageBox(f"无法保存到文件: {pathname}", "错误", 
                             wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App()
    PasswordGenerator()
    app.MainLoop()