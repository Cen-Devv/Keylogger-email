import cx_Freeze
import sys

base=None
if (sys.platform=="win32"):
    base="Win32GUI"
executables = [cx_Freeze.Executable('main.py', base=base)]

cx_Freeze.setup(
    name="main",
    options={'build_exe': {'packages':['pynput','re','smtplib','email.mime.multipart',
    'email.mime.text','email.mime.base','email','schedule','time'],}},

    executables = executables
    
)
