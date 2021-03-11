from tkinter import ttk, font, messagebox
from generate_mac import generate_mac
import os, sys, re, signal
import pyperclip as pc
from tkinter import *
import webbrowser
import time
import threading








def resource_path(location):
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    spriteFolderPath = os.path.join(CurrentPath,location)
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath+"/"
Assets_path = resource_path('Assets')
file_path = Assets_path+'vendors'

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 31
        y = y + cy + self.widget.winfo_rooty() +5
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,background="#ffffe0", relief=SOLID, borderwidth=1,font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        x = (widget['state'])
        if x == "disabled":
            return
            #toolTip.showtip("Button Will Enable After First\nSuccessful MAC Address Change")
        else:
            toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def shoW_Toast():
    ToastWin = Toplevel()
    def destroy_toast ():
        time.sleep(5)
        ToastWin.destroy()
    ToastWin.wm_overrideredirect(1)
    #ToastWin.wm_geometry
    w = 350
    h = 41
    ws = ToastWin.winfo_screenwidth()
    hs = ToastWin.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/5) - (h/2)  #change hs/2 to hs/4 to left window up
    ToastWin.geometry('%dx%d+%d+%d' % (w, h, x, y))
    label = Label(ToastWin,text="    MAC Address Copied To Clipboard     ",highlightthickness=4,highlightbackground="blue", justify=CENTER,background="white", relief=SOLID, borderwidth=2,font=("Comic Sans MS", "15", "normal"))
    label.pack(ipadx=1)
    t1 = threading.Thread(target=destroy_toast)
    t1.start()

mainwindow = Tk()


def fixed_map(option):
    return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]


style = ttk.Style(mainwindow)
style.theme_use("winnative")
style.configure("Treeview.Heading",font=("arial",12, "bold"))
style.configure("Treeview",font=("arial",12),rowheight=25)
style.map('Treeview', foreground=fixed_map('foreground'),background=fixed_map('background'))





background_Col = "#dce5ff"
ButtonBack_Col = "#d7ffff"
ButtonBack_Col_active = "#b5ffff"
entry_box_var = StringVar(mainwindow)
entry_box_var2 = StringVar(mainwindow)
Company_var = StringVar(mainwindow)
entry_box_var2.set("Enter MAC Prefix (eg. 00:06:8C)")
entry_box_var.set("Click On Genarate MAC")
OP_var = IntVar(mainwindow)
Check_Box1=IntVar(mainwindow)
Check_Box2=IntVar(mainwindow)
Check_Box1.set(0)
Check_Box2.set(0)

clip_b_path = PhotoImage(file = Assets_path+ "Clipboard.png")
#git_b_photoimage = clip_b_path.subsample(1, 1)

print('*'*100)
print(file_path)
print('*'*100)
company_names = generate_mac.list_vendors(file_path)        #Problem OccursIn This Line
company_names = sorted(company_names)
company_names.insert(0,"Not Selected")

co = company_names


def main_MAC_Gen_Fun(com):
    if com == "ran":
        mac = generate_mac.total_random()
        entry_box_var.set(mac)
        return
    if com == "ran-half":
        try:
            mac = generate_mac.vid_provided(entry_box_var2.get())
            entry_box_var.set(mac)
            return
        except:
            messagebox.showwarning("Error!","Please Input Valid\nPrefix !!")
            return


def mainscreen():
    global Glb, Glb2, e_mac2, old_mac_V
    mainwindow.config(bg=background_Col)

    for i in mainwindow.winfo_children():
        i.destroy()

    TOPFRAME = Frame(mainwindow,bg=background_Col)
    TOPFRAME.pack(side=TOP)

    Label(TOPFRAME,text="MAC ID Genarator",font=("URW Bookman L",13,"bold"),bg=background_Col,fg="#4b4b6d").pack()
    #Label(TOPFRAME,text="    ",bg=background_Col).pack(side=LEFT)


    OP_Frame = Frame(mainwindow,bg=background_Col)
    Label(OP_Frame,text=" ",font=("URW Bookman L",2),bg=background_Col).pack(side=TOP)
    OP_Frame.pack(side=TOP)
    Button_Frame1 = Frame(mainwindow,bg=background_Col)
    Button_Frame1.pack(side=TOP)

    BodyFrame = Frame(mainwindow,bg=background_Col)
    BodyFrame.pack(side=TOP)

    BodyFrame2 = Frame(mainwindow,bg=background_Col)
    BodyFrame2.pack(side=TOP)


    def OP_select_fun():
        global e_mac2
        if OP_var.get() == 0:
            messagebox.showwarning("Error!","Please Select A\nOPtion First")
        elif OP_var.get() == 1:
            Select_B.config(text="Selected",state=DISABLED)
            R1.config(state=DISABLED)
            R2.config(state=DISABLED)
            Reset_B.config(state=NORMAL)
            Label(BodyFrame,text="\n\n",font=("C059",2,"bold"),bg=background_Col).pack()
            Label(BodyFrame,text="Randomly Genareted MAC Address",font=("C059",12,"bold"),bg=background_Col).pack()
            Label(BodyFrame,text=" ",font=("C059",1,"bold"),bg=background_Col).pack()
            e_mac2 = Entry(BodyFrame,state=DISABLED,width=36,justify=CENTER,font=("Century Schoolbook L",14,"italic"),textvariable=entry_box_var)
            e_mac2.config(disabledforeground="black",disabledbackground="white")
            e_mac2.config(highlightbackground="blue", highlightcolor="blue",highlightthickness=1)
            e_mac2.pack()
            Label(BodyFrame,text="\n",font=("C059",1,"bold"),bg=background_Col).pack()
            def b1_Fun ():
                b1.config(text="Re-Genarate MAC")
                cpy_B.config(state=NORMAL,cursor='hand2')
                main_MAC_Gen_Fun("ran")
            b1 = Button(BodyFrame,command=b1_Fun,activebackground=ButtonBack_Col_active,fg="darkorchid4",bg = ButtonBack_Col,text="Genarate MAC",font=("P052",12,"bold"))
            b1.pack()
            def copy_text():
                text1 = entry_box_var.get()
                pc.copy(text1)
                shoW_Toast()

            cpy_B = Button(BodyFrame,image=clip_b_path,relief=FLAT,state=DISABLED,command=copy_text)
            cpy_B.place(x=375,y=53)
            CreateToolTip(cpy_B, text = "Copy MAC Address To\nClipboard")
            Label(BodyFrame,text=" ",font=("C059",1,"bold"),bg=background_Col).pack()


        elif OP_var.get() == 2:
            Select_B.config(text="Selected",state=DISABLED)
            R1.config(state=DISABLED)
            R2.config(state=DISABLED)
            Reset_B.config(state=NORMAL)
            for i in BodyFrame.winfo_children():
                i.destroy()

            def CH_Selected (e):
                global Glb, Glb2, e_mac2
                if e == 1:
                    if Check_Box1.get() == 1:
                        Ch_B2.config(state=DISABLED)
                        Check_Box2.set(0)
                        for i in BodyFrame2.winfo_children():
                            i.destroy()
                    Label(BodyFrame2,text=" ",font=("C059",3,"bold"),bg=background_Col).pack()
                    e_mac2 = Entry(BodyFrame2,textvariable=entry_box_var2,width=36,justify=CENTER,font=("Century Schoolbook L",12,"bold","italic"))
                    e_mac2.config(disabledforeground="black",disabledbackground="white")
                    e_mac2.config(highlightbackground="blue", highlightcolor="blue",highlightthickness=1)
                    e_mac2.pack()

                    Label(BodyFrame2,text=" ",font=("C059",3,"bold"),bg=background_Col).pack()
                    e_mac3 = Entry(BodyFrame2,textvariable=entry_box_var,state=DISABLED,width=36,justify=CENTER,font=("Century Schoolbook L",12,"bold","italic"))
                    e_mac3.config(disabledforeground="black",disabledbackground="white")
                    e_mac3.config(highlightbackground="blue", highlightcolor="blue",highlightthickness=1)
                    e_mac3.pack()

                    def Mac_Gen():
                        x = entry_box_var2.get()
                        regex = re.compile(':')
                        if (regex.search(x) != None) and x!="Enter MAC Prefix (eg. 00:06:8C)":
                            Glb.config(text="Re-Genarate")
                            Glb2.config(state=NORMAL)
                            main_MAC_Gen_Fun("ran-half")
                        else:
                            messagebox.showwarning("Error!","Please Input Valid\nPrefix !!")

                    def MAc_Clear():
                        Glb.config(text="Genarate")
                        Glb2.config(state=DISABLED)
                        entry_box_var2.set("Enter MAC Prefix (eg. 00:06:8C)")
                        entry_box_var.set("Click On Genarate MAC")
                        e_mac3.focus_set()

                    #Label(BodyFrame2,text=" ",font=("C059",3,"bold")).pack()
                    Glb = Button(BodyFrame2,command=Mac_Gen,activebackground=ButtonBack_Col_active,fg="darkorchid4",bg = ButtonBack_Col,text="Genarate Mac",font=("P052",12,"bold"))
                    Glb.pack(side=LEFT,anchor=W)
                    Glb2 = Button(BodyFrame2,command=MAc_Clear,activebackground=ButtonBack_Col_active,fg="darkorchid4",bg = ButtonBack_Col,text="Clear",state=DISABLED,font=("P052",12,"bold"))
                    Glb2.pack(side=RIGHT,anchor=E)
                    Label(BodyFrame2,text="\n\n\n",font=("C059",10,"bold"),bg=background_Col).pack(side=BOTTOM)
                    def on_e_mac2_click(e):
                        if entry_box_var2.get()=="Enter MAC Prefix (eg. 00:06:8C)":
                            e_mac2.delete(0, "end")
                            e_mac2.insert(0, '')
                    '''def on_e_mac2_focusout(e):
                        if entry_box_var2.get() == "":
                            entry_box_var2.set("Enter MAC Prefix (eg. 00:06:8C)")'''

                    e_mac2.bind('<FocusIn>', on_e_mac2_click)
                    #e_mac2.bind('<FocusOut>', on_e_mac2_focusout)

                    if Check_Box1.get() == 0:
                        Ch_B2.config(state=NORMAL)
                        Check_Box2.set(0)
                        entry_box_var2.set("Enter MAC Prefix (eg. 00:06:8C)")
                        entry_box_var.set("Click On Genarate MAC")
                        for i in BodyFrame2.winfo_children():
                            i.destroy()

                elif e == 2:
                    if Check_Box2.get() == 1:
                        Ch_B1.config(state=DISABLED)
                        Check_Box1.set(0)
                        for i in BodyFrame2.winfo_children():
                            i.destroy()
                        Label(BodyFrame2,text="\n",font=("C059",2,"bold"),bg=background_Col).pack()
                        combo = ttk.Combobox(BodyFrame2,textvariable=Company_var,state='readonly',values=co,width=16,justify=CENTER,font=("Bitstream Vera Serif",12,"italic"))
                        combo.pack()
                        combo.current(0)
                        Label(BodyFrame2,text="\n",font=("C059",4,"bold"),bg=background_Col).pack()
                        Button(BodyFrame2,fg="darkorchid4",text="Genarate",activebackground=ButtonBack_Col_active,bg = ButtonBack_Col,font=("P052",12,"bold")).pack()
                        Label(BodyFrame2,text="\n",font=("C059",5,"bold"),bg=background_Col).pack()

                    if Check_Box2.get() == 0:
                        Ch_B1.config(state=NORMAL)
                        Check_Box1.set(0)
                        for i in BodyFrame2.winfo_children():
                            i.destroy()
            Label(BodyFrame,text=" ",font=("C059",3,"bold"),bg=background_Col).pack()
            Ch_B1 = Checkbutton(BodyFrame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,font=("Cantarell",11,"bold"),command=lambda:CH_Selected(1),text="Genarate MAC With Specific Prefix",variable=Check_Box1,onvalue=1,offvalue=0)
            Ch_B1.pack()
            Ch_B2 = Checkbutton(BodyFrame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,font=("Cantarell",11,"bold"),command=lambda:CH_Selected(2),text="Genarate MAC With Specific Vendor Byte",variable=Check_Box2,onvalue=1,offvalue=0)
            Ch_B2.pack()






    def OP_Reset_fun ():
        Select_B.config(text="Select",state=NORMAL)
        Reset_B.config(state=DISABLED)
        OP_var.set(0)
        R1.config(state=NORMAL)
        R2.config(state=NORMAL)
        for i in BodyFrame.winfo_children():
            i.destroy()
        for i in BodyFrame2.winfo_children():
            i.destroy()
        Check_Box1.set(0)
        Check_Box2.set(0)
        entry_box_var.set("Click On Genarate MAC")


    R1 = Radiobutton(OP_Frame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,text="Randomly Generate MAC Address",font=("Quicksand Light",12,"bold"),padx = 20,variable=OP_var,value=1)
    R1.pack(side=LEFT)
    R2 = Radiobutton(OP_Frame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,text="Generate MAC Address Manually",font=("Quicksand Light",12,"bold"),padx = 20,variable=OP_var,value=2)
    R2.pack(side=RIGHT)
    Select_B = Button(Button_Frame1,text="Select",fg="darkorchid4",font=("Courier 10 Pitch",11,"bold"),activebackground=ButtonBack_Col_active,bg = ButtonBack_Col,command=OP_select_fun)
    Label(Button_Frame1,text="\n",font=("URW Bookman L",1),bg=background_Col).pack(side=TOP)
    Select_B.pack(side=LEFT)
    Label(Button_Frame1,text=" "*55,bg=background_Col).pack(side=LEFT)
    Reset_B = Button(Button_Frame1,fg="darkorchid4",font=("Courier 10 Pitch",11,"bold"),activebackground=ButtonBack_Col_active,bg = ButtonBack_Col,text="Reset",state=DISABLED,command=OP_Reset_fun)
    Reset_B.pack(side=RIGHT)


if __name__ == '__main__':
    mainscreen()
    mainwindow.mainloop()