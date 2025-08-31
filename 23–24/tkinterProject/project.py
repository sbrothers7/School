from tkinter import *
from tkinter import messagebox, scrolledtext, ttk
import os, io, contextlib

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fout = open(os.path.join(__location__, 'userdata.txt'), "a+")
userdata = open(os.path.join(__location__, 'userdata.txt'), "r+")

window = Tk()
window.geometry("1200x701")
window.title("Adventure Game")
center(window)
window.withdraw()
window.iconphoto(True, PhotoImage(file=__location__ + "/logo.png"))

userconfirm = False
user = ""
users = userdata.readlines()
userIndex = 0
stage = 0
tutorialstage = 0

def countdown(count):
    seconds = count % 60
    string = ""
    if seconds < 10: 
        string += "0"
    string += str(seconds)
    timer['text'] = str(count // 60) + ":" + string
    if count > 0:
        window.after(1000, lambda: countdown(count - 1))

def updateStage(n):
    users = open(os.path.join(__location__, 'userdata.txt'), "r").readlines()
    
    fmodify = open(os.path.join(__location__, 'userdata.txt'), "w")
    for i in range(len(users)):
        data = list(users[i].split())
        if i == userIndex: fmodify.write(data[0] + " " + data[1] + " " + str(n) + "\n")
        else: fmodify.write(users[i])
    fmodify.close()

def tutorial(redo=0): # tutorial
    global tutorialstage
    tutorial = Tk()
    tutorial.geometry("720x540")
    center(tutorial)
    tutorial.title("Tutorial")
    maxstep = 9
    
    def skip():
        tutorial.destroy()
        l1()
        
    def prev(a):
        # print(a)
        a -= 1
        if a < 1: a = 1
        global tutorialstage
        tutorialstage = a
        display(a)
    def cont(a): 
        # print(a)
        a += 1
        if a > maxstep and redo == 0: a = maxstep
        elif a > maxstep - 1 and redo == 1: a = maxstep - 1
        global tutorialstage
        tutorialstage = a
        display(a)
    
    # For finding out keypresses
    # def key_handler(event):
    #     print(event.char, event.keysym, event.keycode)
    # tutorial.bind("<Key>", key_handler)
    
    tutorial.bind("<Left>", lambda e: prev(tutorialstage))
    tutorial.bind("<Right>", lambda e: cont(tutorialstage))
    tutorial.bind("<backslash>", lambda e: skip())
    
    title = Label(tutorial, text="Tutorial", font=("Gothic A1", 20, "bold"))
    subtitle = Label(tutorial, text="", font=("Gothic A1", 15, "italic"))
    text = Label(tutorial, text="You may use the left and right arrow keys to navigate between the messages for this tutorial. If you would prefer to skip it, press the backslash key.", font=("Gothic A1", 18), wraplength=680, justify="center")
    startGame = Button(tutorial, text="start", font=("Gothic A1", 20, "bold"), foreground="green", command=lambda:skip())
    
    def display(a):
        subtitle["text"] = "page " + str(a)
        if a == 1: text.config(text="For each stage, there will be either a certain number of buttons or an entry box for you to submit an answer.")
        elif a == 2: text.config(text="There are time limits for each question and if you fail, the program will automatically close itself.")
        elif a == 3: text.config(text="Do not worry as your data will be saved in a seperate file accessed when logging in. You will be asked if you want to continue from when you closed the program / failed the challenge. To do so, input the correct username and password during the login.")
        elif a == 4: text.config(text="The given amount of time will differ from question to question, but there will be a timer at the top right of the page for each question.")
        elif a == 5: text.config(text="There are periods of time when you can pause the game. A prompt will appear asking if you want to take a break after each question. Until you press resume, the game will be paused.")
        elif a == 6: text.config(text="For questions, you will be asked to enter code. Unfortunately, only python code is available. If any other langauges are used, the code will not work.")
        elif a == 7: text.config(text="For inputs, use\n\nimport os\nfin = open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), \"testcase.txt\"), \"r\")\n\nTo read a line in the file, use\n\nfin.readline()\n\nTo read all lines, use\n\nfin.readlines()")
        elif a == 8: text.config(text="You may re-visit this page by pressing the escape key.")
        elif a == 9: 
            text.config(text="You may now proceed.")
            if redo != 1:
                tutorial.bind("<Return>", lambda e: skip())
                tutorial.after(1000, lambda: startGame.place(relx=0.5, rely=0.8, anchor="center"))
    
    title.place(relx=0.5, rely=0.1, anchor="center")
    subtitle.place(relx=0.5, rely=0.2, anchor="center")
    text.place(relx=0.5, rely=0.5, anchor="center")
    tutorial.mainloop()

def start(): # the starting phase
    def destroyWindow(): 
        loginwindow.destroy()
        tutorial()
        
    def recover(recover=True):
        print(userIndex)
        fread = open(os.path.join(__location__, 'userdata.txt'), "r").readlines()
        
        data = fread[userIndex].split()
        print(data)
        if len(data) == 2:
            fappend = open(os.path.join(__location__, 'userdata.txt'), "a")
            fappend.write(" 1")
            fappend.close()
            data.append(str(1))
        
        loginwindow.withdraw()
        window.deiconify()
        s = int(data[2].strip())
        if not recover: s = -1
        if s == -1: l1()
        elif s == 1: l1()
        elif s == 2: l2()
        
    def finishLogin(a): # after login process, final configurations for the user
        title.place_forget()
        usernameLabel.place_forget()
        confirmName.place_forget()
        usernameEntry.place_forget()
        passwordLabel.place_forget()
        confirmPassword.place_forget()
        passwordEntry.place_forget()
        logintypeLabel.place_forget()
        if a == 0: 
            success.config(text="successful login!")
            def query():
                if messagebox.askyesno(title="Info", message="Are you willing to recover your game progress?", icon="question"): recover()
                else:
                    if messagebox.askyesno(title="Quit?", message="Do you want to close the program?", icon="question"): 
                        loginwindow.destroy()
                        window.destroy()
                    else: 
                        loginwindow.withdraw()
                        if messagebox.askyesno(title="Login?", message="Log in with a different account?", icon="question"): start()
                        else: recover(False)
            window.after(1000, query)
                        
        else: 
            success.config(text="successful account creation!")
            global userIndex
            userIndex = len(users)
            def query():
                if messagebox.askyesno(title="Info", message="This program will test one's coding abilities and the difficulty will increase as one progresses through the levels. Do you wish to continue?", icon="info"):
                    loginwindow.after(1000, destroyWindow) # move on to the tutorial
                else: # quit the program
                    loginwindow.withdraw()
                    window.destroy()
                    exit()
            window.after(1000, query)
        success.place(relx=0.5, rely=0.5, anchor="center")
        
        
        
    def devSkip(): # skipping the login stage because it's annoying
        # if usernameEntry.get() == "sbrothers7":
            loginwindow.destroy()
            l1()
    
    def checkName(event=None):
        global user
        username = usernameEntry.get()
        if " " in username: 
            messagebox.showerror(title="Error", message="Usernames cannot contain spaces!", icon="error")
            return -1
        elif (1 < len(username) and 11 > len(username)):
            # retrieve user data from file
            user = username
            global userdata, users, userIndex
            found = False
            for i in range(len(users)):
                data = list(map(str, users[i].split()))
                print(data)
                if user == data[0]: 
                    found = True
                    userIndex = i
                    title.config(text="Greetings, " + user + ".")
                    logintypeLabel.config(text="Logging in to a preexisting account...")
                    logintypeLabel.place(relx=0.5, rely=0.2, anchor="center")
                    print("found user data") 
                    loginwindow.bind("<Return>", lambda e: checkPassword(0))
                    confirmPassword.config(command=lambda: checkPassword(0))
                    break
                    
            if not found: # if user does not exist, add to file
                logintypeLabel.config(text="Creating a new account...")
                logintypeLabel.place(relx=0.5, rely=0.2, anchor="center")
                fout.write(user) 
                passwordLabel.config(text="Create password:")
                fout.close()
                loginwindow.bind("<Return>", lambda e: checkPassword(1))
                confirmPassword.config(command=lambda: checkPassword(1))
            
            passwordLabel.place(relx=0.5, rely=0.5, anchor="e")
            passwordEntry.place(relx=0.5, rely=0.5, anchor="w")
            confirmPassword.place(relx=0.5, rely=0.7, anchor="center")
            passwordEntry.focus()
            confirmName.place_forget()
                
        else:
            messagebox.showerror(title="Error", message="Username must be 2 ~ 10 characters", icon="error")
            
    def checkPassword(a):
        fout = open(os.path.join(__location__, 'userdata.txt'), "a+")
        password = passwordEntry.get()
        if a == 1: # creating a password
            if len(password) < 4:
                if password == "": messagebox.showerror(title="Error", message="Your password cannot be empty!", icon="error")
                else: 
                    if messagebox.askyesno(title="Warning", message="Your password is a bit short. Preferrably, it should be over 4 characters. Do you still wish to continue?", icon="warning"):
                        fout.write(" " + password + "\n")
                        fout.close()
                        finishLogin(1)
                    else: print("retry")
            elif " " in password: messagebox.showerror(title="Error", message="Passwords cannot contain spaces!", icon="error")
            else:
                fout.write(" " + password + "\n")
                fout.close()
                finishLogin(1)
        else:
            data = users[userIndex].split()
            if len(data) < 2: # corrupted file
                messagebox.showerror(title="Error", message="There has been a potential corruption in the data file. The program has deleted part of the user's data that has been corrupted. It is likely that the user quit the process before account registration was complete. Please login again.", icon="error")
                fmodify = open(os.path.join(__location__, 'userdata.txt'), "w")
                for i in range(len(users)):
                    if i == userIndex: continue
                    else: fmodify.write(users[i])
                fmodify.close()
                loginwindow.destroy()
                window.destroy()
                return -1
            if password != data[1]: # wrong password
                messagebox.showerror(title="Error", message="Wrong Password!", icon="error")
                print("wrong password")
            else:
                finishLogin(0)
    
    loginwindow = Tk()
    loginwindow.bind("<Return>", lambda e: checkName())
    # loginwindow.bind("<grave>", lambda e: devSkip())
    loginwindow.geometry("400x300")
    center(loginwindow)
    loginwindow.title("Login")
    title = Label(loginwindow, text="Greetings, fellow user.", font=("Gothic A1", 25, "bold"))
    logintypeLabel = Label(loginwindow, text="", font=("Gothic A1", 12, "italic"))
    usernameLabel = Label(loginwindow, text="Enter username:", font=("Gothic A1", 16))
    confirmName = Button(loginwindow, text="confirm", font=("Gothic A1", 12), command=checkName)
    usernameEntry = Entry(loginwindow, width=15)
    passwordLabel = Label(loginwindow, text="Enter password:", font=("Gothic A1", 16))
    confirmPassword = Button(loginwindow, text="confirm", font=("Gothic A1", 12))
    passwordEntry = Entry(loginwindow, width=15, show="*")
    success = Label(loginwindow, text="", font=("Gothic A1", 20, "bold"))
    # add not looking for this?
    
    title.place(relx=0.5, rely=0.1, anchor="center")
    usernameLabel.place(relx=0.5, rely=0.4, anchor="e")
    usernameEntry.place(relx=0.5, rely=0.4, anchor="w")
    usernameEntry.focus()
    confirmName.place(relx=0.5, rely=0.6, anchor="center")
    loginwindow.mainloop()
    
def keywidgets(stage):
    timer.pack(anchor="center")
    desc.pack(side="top", pady=20, anchor="center")
    subdesc.pack(anchor="w", pady=10)
    ex.pack(anchor="w", pady=10)
    textinputlabel.pack(anchor="w", pady=20)
    textinput.pack(pady=10)
    submit.config(command=lambda: checkAnswer(stage))
    submit.pack(pady=10)

def l2():
    window.deiconify()
    countdown(600)
    
    desc.config(text="Exceptional Grading Process")
    subdesc.config(text="The Maths Department has to input a number grade (1~7) based on a student's performance on the test. However, they are too lazy to check every student's score. Help them by coding a program that will automatically find out the number grade corresponding to the student's score on the test based on the grade boundaries (7: 80~100, 6: 65~79, 5: 50~64, 4: 40~49, 3: 30~39, 2: 20~29, 1: 0~19) for N students.\n\nInput format: 1 line containing an integer, N, the following N lines containing the score for each student\nOutput format: N lines each containing the attainments of the Nth student")
    ex.config(text="INPUT (file \"testcase.txt\"):\n5\n81\n77\n98\n60\n85\n\nOUTPUT (stdout):\n7\n6\n7\n5\n7")
    
    keywidgets(2)
    updateStage(2)

def l1(): # Q1
    window.deiconify()
    countdown(600)
    
    desc.config(text="Exceptional Login")
    subdesc.config(text="Leo is getting frustrated because of people entering capital letters in their usernames when creating accounts for his website. He wants to make all usernames lowercase if there are any characters that are in uppercase. Help him by coding a program that will convert any uppercase characters into lowercase. Additionally, he does not want any space characters in the usernames. If there are any space characters, replace them with underscores.\n\nInput format: one line of string will be given (maximum length 100 characters).\nOutput format: output one line of string")
    ex.config(text="INPUT (file \"testcase.txt\"):\ngOOfY uSeRnAME\n\nOUTPUT (stdout):\ngoofy_username")
    
    keywidgets(1)
    updateStage(1)
    
def checkAnswer(n):
    res = ""
    def output(): # getting terminal output
        captured_string = io.StringIO()
        with contextlib.redirect_stdout(captured_string):
            try:
                exec(textinput.get("1.0", END))
            except RuntimeError:
                return "r"
            except SyntaxError:
                return "s"
            except ArithmeticError:
                return "a"
            except:
                return "?"
            
        stdout = captured_string.getvalue()
        return stdout

    def result(): # display testcases
        tc = Tk()
        tc.title("Run Result")
        tc.geometry("600x120")
        center(tc)
        nextstage = Button(tc, text="Next Question", font=("Gothic A1", 10), fg="green")
        def gotonextstage():
            tc.destroy()
            exec("l" + str(n + 1) + "()")
            global first
            first = True
            window.geometry("1200x701")
            
        for i in range(len(ansres)):
            testcaselabel = Label(tc, text="Testcase " + str(i + 1) + ":", font=("Gothic A1", 15))
            symbol = Label(tc, text="", font=("Gothic A1", 40))
            if ansres[i] == 1: 
                testcaselabel.config(fg="green")
                symbol.config(text="✔", fg="green")
            else: 
                testcaselabel.config(fg="red")
                symbol.config(text=ansres[i], fg="red")
            testcaselabel.place(relx=(0.9*(i/len(ansres)) + 0.15), rely=0.1, anchor="center")
            symbol.place(relx=(0.9*(i/len(ansres)) + 0.15), rely=0.5, anchor="center")
            
        if ansres.count(1) == len(ansres): 
            nextstage.config(command=lambda:gotonextstage())
            nextstage.place(relx=0.5, rely=1.0, anchor="s")
        tc.mainloop()

    ansres = [] # keep track of correct and incorrect testcases
    def checktestcase(correctAns, input):
        testcase = open(os.path.join(__location__, "testcase.txt"), "w+")
        testcase.write(input)
        testcase.close()
        res = output()
        if res == correctAns: ansres.append(1)
        else: 
            if not res in "rsa?" or res == "": ansres.append("✘")
            else: ansres.append(res)
        
    if n == 1: # Q1 testcases
        checktestcase("goofyusername\n", "gOOfyuSeRnAME")
        checktestcase("goofy_username\n", "goofy username")
        checktestcase("goofy_username\n", "gOOfy uSeRnAME")
        checktestcase("hello_my_name_is_sbrothers7_\n", "hello my name is sbrothers7 ")
        checktestcase("__hi__\n", "  HI  ")
        checktestcase("jol_gee_teng\n", "Jol Gee Teng")
        # print(ansres)
        result()
        """
        print(fin.readline().lower().replace(" ", "_"))
        
        (answer)
        """
        
canvaswidth = 1200
first = True
intextinput = False

def resize():
    global canvaswidth
    canvaswidth = canvas.winfo_width()
    subdesc.config(wraplength=canvaswidth)
    ex.config(wraplength=canvaswidth)
    textinput.config(width=int(canvaswidth / 10 - 2))
    # print(canvaswidth)
# def addpaddingtocanvas(): canvas.pack_configure(padx=int(canvaswidth / 12))

def on_mousewheel(event):
    # print(intextinput)
    if not intextinput:
        global first
        if first:
            width = window.winfo_width()
            height = window.winfo_height()
            window.geometry("{}x{}".format(width, height - 1))
            first = False
        
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            # canvas.xview_scroll(scroll, "units")
            return
        else: canvas.yview_scroll(scroll, "units")

# scorollable window
canvas = Canvas(window, state="disabled", highlightthickness=0)
scroll = ttk.Scrollbar(window, command=canvas.yview)
frame = Frame(canvas)
canvas.config(yscrollcommand=scroll.set)
frame.pack(fill=BOTH, expand=True)
canvas.create_window(0, 0, window=frame, anchor="nw")
canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox(ALL)))
scroll.pack(side=RIGHT, fill=Y)
canvas.pack(fill=BOTH, expand=True, padx=75, pady=0)
canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e))
frame.bind("<Button-1>", lambda e: frame.focus_set())

# widgets on window
desc = Label(frame, text="", font=("Gothic A1", 30, "bold"))
subdesc = Label(frame, text="", font=("Gothic A1", 15), justify="left")
ex = Label(frame, text="", font=("Courier New", 16), justify="left")
textinputlabel = Label(frame, text="Write code below:", font=("Gothic A1", 18, "bold"), justify="left")

def ctrlEvent(event):
    if event.state == 4 and event.keysym == 'c':
        content = textinput.selection_get()
        window.clipboard_clear()
        window.clipboard_append(content)
        return 
    elif event.state == 4 and event.keysym == 'v':
        textinput.insert('end', window.selection_get(selection="CLIPBOARD"))
        return
    else: return
    
def entertextinput(): 
    global intextinput
    intextinput = True
def leavetextinput(): 
    global intextinput
    intextinput = False
    
textinput = scrolledtext.ScrolledText(frame, height=30, width=90, font=("Courier New", 16))
textinput.insert(INSERT, "import os\nfin = open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), \"testcase.txt\"), \"r\")\n")
textinput.config(undo=True)
textinput.bind("<Enter>", lambda e: entertextinput())
textinput.bind("<Leave>", lambda e: leavetextinput())

def autoclose(n):
    index = textinput.index(INSERT)
    y, x = map(int, index.split("."))
    string = "{}.{}".format(y, x + 1)
    if n == 1: textinput.insert(index, "'")
    elif n == 2: textinput.insert(index, "\"")
    elif n == 3: textinput.insert(string, ")")
    textinput.mark_set(INSERT, index)

textinput.bind("<'>", lambda e: autoclose(1))
textinput.bind("<\">", lambda e: autoclose(2))
textinput.bind("<(>", lambda e: autoclose(3))

timer = Label(window, text="", font=("Gothic A1", 20))
submit = Button(frame, text="Submit", font=("Gothic A1", 16, "bold"), fg="deep sky blue", highlightbackground="gray25", highlightthickness=1, bg="gray50")

window.bind("<Escape>", lambda e: tutorial(1))
window.bind("<Configure>", lambda e: resize())

stageImg = 0
# img = PhotoImage(file=str(stageImg) + ".jpg").place()
# imageCont = Label(window, image=img).place()

start()
fout.close()
