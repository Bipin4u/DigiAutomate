from pywinauto.application import Application
import time

def automateATSC():
    app = Application(backend="uia").connect(path=r"C:Usersipin.kumarOneDrive - HCL Technologies LtdDesktopAtsc3XpressAtsc3Xpress.exe")
    main_dlg = app.window(title_re=".*Atsc3Xpress*")
    openfile = main_dlg.child_window(title="toolStrip1", auto_id="toolStrip1", control_type="ToolBar").child_window(title="Open", control_type="Button")
    openfile.click_input()  # Click the Open button
    time.sleep(3)
    try:
        # Handle the save prompt, if it appears
        smallwindow = main_dlg.child_window(title="Save", control_type="Window").child_window(title="No", auto_id="7", control_type="Button")
        smallwindow.click_input()
    except:
        pass
    app_file = Application().connect(title_re=".*Open")
    file_dlg = app_file.window(title_re=".*Open*")
    time.sleep(2)
    filev = file_dlg.child_window(title="&Open", class_name="Button")
    filev.click_input()  # Click the Open button
    time.sleep(2)