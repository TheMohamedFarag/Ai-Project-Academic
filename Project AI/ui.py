import tkinter as tk
from tkinter import messagebox
import math, random
from solver import solve

class App:
    BG,DARK,GOLD,DIM,TEXT = "#070712","#0f0f20","#e6b800","#7c3aed","#e2e8f0"

    def __init__(self, root):
        self.root=root; self.root.title("♛ N-Queens"); self.root.configure(bg=self.BG)
        self.root.resizable(False,False); self.sols=[]; self.idx=0; self.glows=[]; self.t=0
        self._ui(); self._stars(); self._tick()

    def _btn(self, p, t, c, **k):
        return tk.Button(p,text=t,command=c,relief="flat",cursor="hand2",padx=14,pady=6,
                         bg=k.pop("bg",self.DARK),fg=k.pop("fg",self.TEXT),font=("Georgia",k.pop("fs",10),"bold"),**k)

    def _ui(self):
        self.root.geometry("700x980")
        self.bg=tk.Canvas(self.root,width=700,height=980,bg=self.BG,highlightthickness=0); self.bg.place(x=0,y=0)
        [self.bg.create_oval(350-i*18,490-i*18,350+i*18,490+i*18,fill="#{:02x}{:02x}{:02x}".format(int(60*(i/18)*.4),int(10*(i/18)*.4),int(120*(i/18)*.4)),outline="") for i in range(18,0,-1)]
        tk.Label(self.root,text="♛  N-QUEENS  SOLVER  ♛",font=("Georgia",18,"bold"),bg=self.BG,fg=self.GOLD).pack(pady=(18,0))
        tk.Frame(self.root,bg=self.GOLD,height=1).pack(fill="x",padx=60,pady=6)
        row=tk.Frame(self.root,bg=self.BG); row.pack(pady=8)
        tk.Label(row,text="N =",font=("Georgia",13),bg=self.BG,fg=self.TEXT).pack(side="left")
        self.n_var=tk.IntVar(value=1)
        sp=tk.Spinbox(row,from_=1,to=10,textvariable=self.n_var,width=3,font=("Georgia",14,"bold"),
                      bg=self.DARK,fg=self.GOLD,buttonbackground=self.DARK,relief="flat",justify="center",insertbackground=self.GOLD,command=self._validate)
        sp.pack(side="left",padx=10); [sp.bind(e,lambda _:self._validate()) for e in ("<FocusOut>","<Return>")]
        self._btn(row,"✦ SOLVE ✦",self._solve,bg=self.GOLD,fg="#07070f",fs=12).pack(side="left",padx=6)
        self.info=tk.StringVar(value="Choose N (1–10) and press SOLVE")
        tk.Label(self.root,textvariable=self.info,font=("Georgia",11,"italic"),bg=self.BG,fg=self.DIM).pack(pady=4)
        self.cv=tk.Canvas(self.root,width=580,height=580,bg=self.BG,highlightthickness=0); self.cv.pack(pady=4)
        nav=tk.Frame(self.root,bg=self.BG); nav.pack(pady=4)
        self._btn(nav,"◀ PREV",self.prev).pack(side="left",padx=8)
        self.nav_var=tk.StringVar()
        tk.Label(nav,textvariable=self.nav_var,font=("Georgia",11,"bold"),bg=self.BG,fg=self.GOLD,width=10).pack(side="left")
        self._btn(nav,"NEXT ▶",self.next).pack(side="left",padx=8)
        tk.Frame(self.root,bg=self.GOLD,height=1).pack(fill="x",padx=60,pady=8)
        tk.Label(self.root,text="ALL SOLUTIONS",font=("Georgia",10,"bold"),bg=self.BG,fg="#4a4a6a").pack()
        outer=tk.Frame(self.root,bg=self.BG); outer.pack(fill="both",expand=True,padx=10,pady=4)
        self.scv=tk.Canvas(outer,bg=self.BG,highlightthickness=0,height=220)
        sb=tk.Scrollbar(outer,orient="horizontal",command=self.scv.xview)
        self.scv.configure(xscrollcommand=sb.set); sb.pack(side="bottom",fill="x"); self.scv.pack(fill="both",expand=True)
        self.mf=tk.Frame(self.scv,bg=self.BG); self.scv.create_window((0,0),window=self.mf,anchor="nw")
        self.mf.bind("<Configure>",lambda e:self.scv.configure(scrollregion=self.scv.bbox("all")))

    def _stars(self):
        self.star_ids=[(self.bg.create_oval(x:=random.randint(0,700),y:=random.randint(0,980),x+random.uniform(.8,2.5),y+random.uniform(.8,2.5),fill="#{:02x}{:02x}{:02x}".format(b:=random.randint(80,220),b,b),outline=""),random.uniform(0,6.28),random.uniform(.02,.07),b) for _ in range(110)]

    def _validate(self):
        try: v=int(self.n_var.get()); self.n_var.set(max(1,min(10,v))) or (v>10 and messagebox.showwarning("Limit","Max N=10"))
        except: self.n_var.set(6)

    def _tick(self):
        self.t+=1
        [self.bg.itemconfig(s,fill="#{:02x}{:02x}{:02x}".format(*(3*[int(b*(0.3+0.7*(0.5+0.5*math.sin(ph+self.t*sp))))]))) for s,ph,sp,b in self.star_ids]
        [( self.cv.coords(o,cx-rr,cy-rr,cx+rr,cy+rr), self.cv.itemconfig(o,outline=self.GOLD+format(int(80+(0.5+0.5*math.sin(self.t*.12))*120),"02x")) ) for o,cx,cy,r in self.glows for rr in [r+(0.5+0.5*math.sin(self.t*.12))*5]]
        self.root.after(40,self._tick)

    def _solve(self):
        self._validate(); n=self.n_var.get(); self.sols=solve(n); self.idx=0; self.glows.clear()
        if not self.sols: messagebox.showinfo("N-Queens",f"No solution for N={n}"); return
        self._draw(animate=True); self._mini(n)

    def _cell_color(self, is_queen, is_light):
        return ("#2a1a00" if is_light else "#1a0f00") if is_queen else ("#1c1c38" if is_light else "#10102a")

    def _draw(self, animate=False):
        self.cv.delete("all"); self.glows.clear()
        sol=self.sols[self.idx]; n=len(sol); cs=520//n; mg=30
        [self.cv.create_rectangle(mg-g,mg-g,mg+520+g,mg+520+g,outline="#{:02x}{:02x}{:02x}".format(int(0xe6*g/6*.4),int(0xb8*g/6*.4),0)) for g in range(6,0,-1)]
        qs=[(x1:=mg+c*cs,y1:=mg+r*cs) for r in range(n) for c in range(n)
            if [self.cv.create_rectangle(x1:=mg+c*cs,y1:=mg+r*cs,x1+cs,y1+cs,fill=self._cell_color(sol[r]==c,(r+c)%2==0),outline="#20203a",width=1)] and sol[r]==c]
        [self.cv.create_text(mg+i*cs+cs//2,mg+532,text="ABCDEFGHIJ"[i],font=("Georgia",8),fill="#4a4a6a") or
         self.cv.create_text(mg-12,mg+i*cs+cs//2,text=str(n-i),font=("Georgia",8),fill="#4a4a6a") for i in range(n)]
        def place(qi):
            if qi>=len(qs): return
            cx,cy=qs[qi][0]+cs//2,qs[qi][1]+cs//2; rr=cs*.38
            self.glows.append((self.cv.create_oval(cx-rr,cy-rr,cx+rr,cy+rr,outline=self.GOLD,width=2,fill=""),cx,cy,rr))
            self.cv.create_text(cx,cy,text="♛",font=("Georgia",max(12,int(cs*.55)),"bold"),fill=self.GOLD)
            if animate: self.root.after(120*(qi+1),lambda q=qi+1:place(q))
        self.root.after(80,lambda:place(0)) if animate else [place(i) for i in range(len(qs))]
        total=len(self.sols)
        self.info.set(f"✦  {total} solution{'s'if total>1 else''} for N={n}  ✦"); self.nav_var.set(f"{self.idx+1} / {total}")

    

    def next(self):
        if self.sols: self.idx=(self.idx+1)%len(self.sols); self._draw(); self._mini(self.n_var.get())
    def prev(self):
        if self.sols: self.idx=(self.idx-1)%len(self.sols); self._draw(); self._mini(self.n_var.get())

if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()