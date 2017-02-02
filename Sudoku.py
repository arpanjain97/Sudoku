from Tkinter import *
import math,pickle,random,tkMessageBox,tkSimpleDialog
class Sudoku:
    #class dealing with solving of sudoku
    def __init__(self,sud_l='400000805030000000000700000020000060000080400000010000000603070500200000104000000'):
        #Initialises the sudoku and prepares squares
        self.sudoku=list(sud_l)
        alpha='ABCDEFGHI'
        digit='123456789'
        self.sqr=self.cross(alpha,digit)
        self.units=([self.cross(alpha,col) for col in digit]+
               [self.cross(row,digit) for row in alpha]+
               [self.cross(rb,cb) for rb in ['ABC','DEF','GHI'] for cb in ['123','456','789']])
    def cross(self,A,B):
        #cross product of two sequences
        return [a+b for a in A for b in B]
    def peer(self,item):
        #generates list of peers
        temp=[p for p in self.units if item in p]
        peer=set()
        for a in temp:
            peer.update(a)
        peer.remove(item)
        return list(peer)
    def parse(self):
        #generate blank sudoku and place possible values
        self.sudoku=['123456789' if w=='0' else w  for w in self.sudoku]
        self.values=dict(zip(self.sqr,self.sudoku))
        for i in self.sqr:
            if len(self.values[i])==1:
                if not all(self.eliminate(self.values,self.values[i],s) for s in self.peer(i)):
                    return False
        return self.values
    def assign(self,values,d,b):
    # if a box has multi-possibility yet has the only occurence of a digit in a unit(row,column,box)
        rem=values[b].replace(d,'')
        if all(self.eliminate(values,d,b) for d in rem):
            return values
        else:
            return False
    def eliminate(self,values,d,b):
    #removes single possibilty boxes from peers(simplification of grid)
        if d not in values[b]:
            return values
        values[b]=values[b].replace(d,'')
        if len(values[b])==0:
        #contradiction: No possible Value
            return False
        if len(values[b])==1:
        #removal of only possibility from peers
            d2=values[b]
            if not all(self.eliminate(values,d2,b2) for b2 in self.peer(b)):
                return False
        for u in self.units:
        # assign propagation
            davail=[s for s in u if d in values[s]]
            if len(davail)==0:
                return False
            elif len(davail)==1:
                if not self.assign(values,d,davail[0]):
                    return False
        return values
    def some(self,seq):
        #return some possible value
        for e in seq:
            if e:
                return e
        return False
    def search(self,val):
        #depth search approach
        if val is False:
            return False
        if all(len(val[s])==1 for s in self.sqr):
            return val
        n,s=min((len(val[s]),s) for s in self.sqr if len(val[s])>1)
        return self.some(self.search(self.assign(val.copy(),d,s)) for d in val[s])
    def solve(self):
        #initiates depth search and changes result back in string format
        ans=self.search(self.parse())
        tmp=''
        for s in self.sqr:
            tmp+=ans[s]
        return tmp
    def check(self):
        #checks entered sudoku
        if any(i=='0' for i in self.sudoku):
            return False
        chksud=self.parse()
        for i in self.sqr:
            if not all(self.eliminate(chksud,chksud[i],s) for s in self.peer(i)):
                return False
        return True
class Timer_app():
    '''class for timer widget implementation'''
    def __init__(self,window):
        self.win=window
        self.box=Label(self.win,text="00:00",font=(basefont,60,basestyle),bg=theme_color2,fg='white',relief="flat")
        self.box.place(x=950,y=265)
        self.count=-1
    def start(self):
        #start timer
        self.count+=1
        disp=str(self.count/600)+str((self.count%600)/60)+":"+str((self.count%600%60)/10)+str(self.count%600%60%10)
        self.box.config(text=disp)
        self.chk=self.win.after(1000,self.start)
    def stop(self):
        #stop timer
        if self.count>-1:
            self.win.after_cancel(self.chk)
    def reset(self):
        #reset timer
        self.stop()
        self.count=-1
        self.box.config(text='00:00')
    def get(self):
        # returns current time
        return self.count
    def adj(self,val):
        #sets time
        self.count=val
        self.start()
class Grid():
    '''class dealing with sudoku grid as shown on screen'''
    def __init__(self,root,y_pos=50,x_pos=100):
        #creates blank grid
        self.grid_items=[[0 for row in range(9)] for col in range(9)]
        for row in range(9):
            x_pos=100
            for col in range(9):
                self.grid_items[row][col]=Entry(root,font=('Comic Sans Ms',30,'bold'),fg="red",width=2,disabledforeground="black",borderwidth=5,justify='center',relief='flat')
                self.grid_items[row][col].bind('<FocusOut>',self.__valid)
                if col==3 or col==6:
                    x_pos+=10
                self.grid_items[row][col].place(x=65*col+x_pos,y=70*row+y_pos)
            if row==2 or row==5:
                y_pos+=10
    def __valid(self,event):
        #checks validity of entered values
            d=event.widget.get()
            if len(d)>1 or d not in ['','1','2','3','4','5','6','7','8','9']:
                tkMessageBox.showwarning("Invalid Input","Enter a value between 1 and 9")
                event.widget.delete(0,END)
    def show(self,seq,disp='que'):
        #shows the sudoku string as grid on screen
        for row in range(9):
            for col in range(9):
                if seq[9*row+col]!='0':
                    self.grid_items[row][col].insert(0,seq[9*row+col])
                    if disp=='que':
                        self.grid_items[row][col].config(state='disabled')
    def clrscr(self):
        #to make grid blank
        for row in range(9):
            for col in range(9):
                self.grid_items[row][col].config(state='normal')
                self.grid_items[row][col].delete(0,END)
    def state(self):
        #returns current state
        state=''
        for row in range(9):
            for col in range(9):
                bstate=self.grid_items[row][col].get()
                if bstate:
                    state+=bstate
                else:
                    state+='0'
        return state
class Load():
    #Creates a loading connector
    def __init__(self):
        self.content=list()
    def load_dir(self):
        #loads from question directory
        fil=open(r'data\sudoku.db','rb')
        suds=fil.readlines()
        chosen=random.choice(suds)
        fil.close()
        return chosen
    def load_sav(self,username):
        #loads from user saves
        try:
            fil=self.fil_open(r'data\user_'+username+'.sav')
            obj=pickle.load(fil)
            fil.close()
            return obj
        except IOError:
            pass
    def fil_open(self,loc):
        try:
            fil=open(loc,'rb')
            return fil
        except IOError:
            tkMessageBox.showwarning("Open Directory","Unable to open Directory location: "+loc+".\nEither it doesnt exist or is corrupt.")
            raise 
class Save():
    #create a saving object and save it in data directory
    def __init__(self):
        self.savlist=list()
    def list_enum(self,ques,ans,state,timer):
        self.savlist=[ques,ans,state,timer]
    def save_act(self,username,ques,ans,state,timer):
        self.list_enum(ques,ans,state,timer)
        fil=open(r'data\user_'+username+'.sav','wb')
        pickle.dump(self.savlist,fil)
        fil.close()
        fil=open(r'data\users.db','ab')
        fil.write(username+'\n')
        fil.close()
class Loading:
    #creates a circle rotating load screen
    def __init__(self,root,width,height,x=350,y=320):
        self.w=width
        self.h=height
        self.circ=[a for a in range(1,7)]
        self.can=Canvas(root,width=width,height=height)
        self.can.config(bg='dodgerblue3')
        self.can.place(x=x,y=y)
        self.circles()
    def circ_stk(self):
        tmp=self.circ.pop(0)
        self.circ+=[tmp]
    def circles(self):
        #creates animation circles
        rad=self.h/10
        for i in range(6):
            pos_x=int((self.w/3)*math.cos((math.pi/3)*i))+(self.w/2)
            pos_y=int((self.h/3)*math.sin((math.pi/3)*i))+(self.h/2)
            self.can.create_oval(pos_x-rad,pos_y-rad,pos_x+rad,pos_y+rad,fill='black',outline='dodgerblue3',tags=i+1)
    def animate(self,delay=150):
        #animates the circle movement
        self.circ_stk()
        self.can.itemconfig(self.circ[0],fill='white')
        self.can.itemconfig(self.circ[5],fill='grey80')
        self.can.itemconfig(self.circ[4],fill='grey70')
        self.can.itemconfig(self.circ[3],fill='grey60')
        self.can.itemconfig(self.circ[2],fill='grey50')
        self.can.itemconfig(self.circ[1],fill='dodgerblue3')
        self.fps=root.after(delay,self.animate)
    def destroy(self):
        #removes loadscreen
        root.after_cancel(self.fps)
        self.can.destroy()
class Controller(Sudoku,Grid):
    '''class for creating GUI aspect of the programme'''
    def __init__(self,root):
        #creates main window of programme and its menu
        self.root=root
        self.load_conn=Load()
        self.save_conn=Save()
        self.lvl_map={1:8,2:4,3:2}
        root.after(2,self.add_widgets)
        self.Window()
    def Window(self):
        #formats window and loads images
        root.wm_title("SUDOKU")
        root.state("zoomed")
        self.root.wm_iconbitmap(r'img\icon.ico')
        self.back=PhotoImage(file=base_img)
        self.canv=Canvas(self.root,height=766,width=1366)
        self.canv.place(x=0,y=0)
        self.canv.create_image(0,0,image=self.back,anchor='nw')
        self.menubar=Menu(self.root)
        self.root.config(menu=self.menubar)
        self.title=PhotoImage(file=r'img\title.gif')
        self.canv.create_image(750,65,image=self.title,anchor='nw')
    def add_widgets(self):
        #adds the required widgets to window
        self.grid=Grid(self.root)
        self.timer=Timer_app(self.root)
        Button(self.root,text='SUBMIT',relief='flat',font=(basefont,30,basestyle),fg='white',bg=theme_color2,command=self.check).place(x=975,y=450)
        filemenu=Menu(self.menubar,tearoff=0)
        filemenu.add_command(label="New",command=self.new)
        filemenu.add_command(label="Restart",command=self.restart)
        filemenu.add_command(label="Load",command=self.loader)
        filemenu.add_command(label="Save",command=self.save)
        filemenu.add_command(label="Solution",command=self.solv)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=self.s_exit)
        self.menubar.add_cascade(label="MENU",menu=filemenu)
        self.menubar.add_command(label="Fullscreen",command=self.fullscreen)
        self.menubar.add_command(label=" View Help",command=self.help_d)
        self.root.bind('<F5>',self.help_d)
        self.root.bind('<Escape>',self.s_exit)
    def s_exit(self,event=None):
        #safe exit func
        if not tkMessageBox.askyesno("Exit","Do you want to quit without saving ?"):
            return None
        self.root.destroy()
    def fullscreen(self):
        #fullscreen func
        root.wm_attributes("-fullscreen",True)
    def help_d(self,event=None):
        #shows help document
        try:
            doc=self.load_conn.fil_open(r"data\helpdoc.dat")
            master=Toplevel()
            master.wm_iconbitmap(r'img\icon.ico')
            scrollbar = Scrollbar(master)
            scrollbar.pack(side=RIGHT, fill=Y)
            text = Text(master,wrap=WORD ,yscrollcommand=scrollbar.set)
            text.tag_config('h1',foreground='red',font='courier 10 bold')
            text.tag_config('h2',foreground='blue',font='courier 10 bold')
            text.tag_config('h3',font='courier 12 bold')
            text.tag_config('t1',font='courier 20 bold',underline=1)
            text.insert(END,doc.read())
            text.tag_add('t1',1.0,2.0)
            doc.seek(0,0)
            copy=doc.readlines()
            for i in copy:
                t=0
                ind=copy.index(i)+1
                if i[0]=='*':
                    t='h1'
                elif i[0]=='#':
                    t='h2'
                elif 'Arpan' in i:
                    t='h3'
                if t:
                    text.tag_add(t,float(ind),float(ind+1))
            text.config(state='disabled')
            text.pack()
            doc.close()
            scrollbar.config(command=text.yview)
        except IOError:
            pass
    def new(self):
        #create level select menu
        self.grid.clrscr()
        self.timer.reset()
        fontu=(basefont,30,basestyle)
        self.lvl = IntVar()
        self.master=Toplevel(bg=theme_color)
        self.master.wm_iconbitmap(r'img\icon.ico')
        Radiobutton(self.master, text="Easy   ",fg='green',bg=theme_color,offrelief='flat',variable=self.lvl,indicatoron=0,font=fontu,value=1,command=self.create).pack(anchor=W)
        Radiobutton(self.master, text="Medium",fg='yellow',bg=theme_color,offrelief='flat',variable=self.lvl,indicatoron=0,font=fontu,value=2,command=self.create).pack(anchor=W)
        Radiobutton(self.master, text="Hard   ",fg='red3',bg=theme_color,offrelief='flat',variable=self.lvl,indicatoron=0,font=fontu,value=3,command=self.create).pack(anchor=W)
    def create(self):
        #adjusts sudoku as per level and display
        hint_no=self.lvl_map[self.lvl.get()]
        self.master.destroy()
        self.ldscreen=Loading(self.root,100,100,x=325,y=300)
        self.ldscreen.animate()
        sudoku=self.load_conn.load_dir()
        sud_obj=Sudoku(sudoku)
        ans=list(sud_obj.solve())
        sudoku=list(sudoku)
        if ans:
            while hint_no>0:
                ind=random.randint(0,80)
                if sudoku[ind]!=ans[ind]:
                    sudoku[ind]=ans[ind]
                    hint_no-=1
        self.ques=''.join(sudoku)
        self.ans=''.join(ans)
        self.grid.show(sudoku)
        self.timer.start()
        self.ldscreen.destroy()
    def loader(self):
       #creates menu to load sudoku from user saved sudokus
       try:
           fil=self.load_conn.fil_open(r"data\users.db")
           self.load_win=Toplevel()
           self.load_win.config(bg='dodgerblue')
           self.load_opt=Listbox(self.load_win,height=0,width=10,relief='flat',font=(basefont,30,basestyle),bg=theme_color,fg='white')
           self.load_opt.pack()
           self.saved=fil.readlines()
           for i in self.saved:
               self.load_opt.insert(END,i)
           Button(self.load_win,bg=theme_color,relief='flat',text="LOAD",font=(basefont,30,basestyle),command=self.load,fg='purple4').pack()
           fil.close()
       except:
            pass
    def load(self):
        #restores the state of game
        selno=int(self.load_opt.curselection()[0])
        self.load_win.destroy()
        data=self.load_conn.load_sav(self.saved[selno][:-1])
        self.ques=data[0]
        self.ans=data[1]
        self.grid.clrscr()
        self.grid.show(self.ques)
        self.grid.show(data[2],'ans')
        self.timer.stop()
        self.timer.adj(data[3])
    def save(self):
        #saving func
        state=self.grid.state()
        nam=tkSimpleDialog.askstring("Save Game","Entry name",initialvalue="< BLANK >")
        self.save_conn.save_act(nam,self.ques,self.ans,state,self.timer.get())
    def restart(self):
        #func to restart loaded sudoku
        self.grid.clrscr()
        self.grid.show(self.ques)
        self.timer.reset()
        self.timer.start()
    def solv(self):
        #func to show solution
        self.timer.stop()
        self.grid.clrscr()
        self.grid.show(self.ques)
        self.grid.show(self.ans,'ans')
    def check(self):
        #func to check the submitted answers
        self.timer.stop()
        scr=self.grid.state()
        sud=Sudoku(scr)
        if sud.check():
            tkMessageBox.showwarning("Correct","Answer is correct")
        else:
            tkMessageBox.showwarning("Incorrect","Answer is either incorrect or incomplete")
            self.timer.start()
###MAIN###
basefont="Comic Sans Ms"
basestyle='bold'
theme_color='dodgerblue'
theme_color2='grey70'
base_img=r'img\back.gif'
root=Tk()
Main_obj=Controller(root)
root.mainloop()
