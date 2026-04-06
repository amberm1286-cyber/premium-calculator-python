import tkinter as tk
import math

root = tk.Tk()
root.title("Premium Calculator")
root.geometry("360x650")
root.configure(bg="black")

memory = 0
is_degree = True

# -------- DISPLAY --------
entry = tk.Entry(root, font=("Arial", 24), bg="black", fg="white", bd=0, justify="right")
entry.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10, ipady=10)

history_box = tk.Text(root, height=4, bg="black", fg="gray", bd=0)
history_box.grid(row=1, column=0, columnspan=5, sticky="nsew")

# -------- SAFE EVAL --------
def safe_eval(expr):
    allowed = "0123456789+-*/(). "
    for c in expr:
        if c not in allowed:
            raise Exception("Invalid")
    return eval(expr)

# -------- BASIC --------
def click(val):
    current = entry.get()
    if val == ".":
        if "." in current.split()[-1]:
            return
    entry.insert(tk.END, val)

def clear():
    entry.delete(0, tk.END)

def backspace():
    entry.delete(len(entry.get())-1, tk.END)

def equal():
    try:
        expr = entry.get()
        result = safe_eval(expr)
        history_box.insert(tk.END, f"{expr} = {result}\n")
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# -------- MEMORY --------
def m_plus():
    global memory
    try:
        memory += float(entry.get())
    except:
        pass

def m_minus():
    global memory
    try:
        memory -= float(entry.get())
    except:
        pass

def m_recall():
    entry.delete(0, tk.END)
    entry.insert(0, memory)

def m_clear():
    global memory
    memory = 0

# -------- SAVE --------
def save_history():
    with open("history.txt", "w") as f:
        f.write(history_box.get("1.0", tk.END))

# -------- HISTORY TOGGLE --------
def toggle_history():
    if history_box.winfo_viewable():
        history_box.grid_remove()
    else:
        history_box.grid()

# -------- FUNCTIONS --------
def sin_func():
    val = float(entry.get())
    if is_degree:
        val = math.radians(val)
    res = math.sin(val)
    entry.delete(0, tk.END)
    entry.insert(0, round(res,6))
    history_box.insert(tk.END, f"sin = {res}\n")

def cos_func():
    val = float(entry.get())
    if is_degree:
        val = math.radians(val)
    res = math.cos(val)
    entry.delete(0, tk.END)
    entry.insert(0, round(res,6))
    history_box.insert(tk.END, f"cos = {res}\n")

def tan_func():
    val = float(entry.get())
    if is_degree:
        val = math.radians(val)
    res = math.tan(val)
    entry.delete(0, tk.END)
    entry.insert(0, round(res,6))
    history_box.insert(tk.END, f"tan = {res}\n")

def log_func():
    val = float(entry.get())
    res = math.log10(val)
    entry.delete(0, tk.END)
    entry.insert(0, res)

def ln_func():
    val = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, math.log(val))

def sqrt_func():
    val = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, math.sqrt(val))

def square_func():
    val = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, val**2)

def cube_func():
    val = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, val**3)

def cbrt_func():
    val = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, val**(1/3))

def power_func():
    click("**")

def percent_func():
    val = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, val/100)

def sign_func():
    val = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, -val)

def factorial_func():
    val = int(float(entry.get()))
    entry.delete(0, tk.END)
    entry.insert(0, math.factorial(val))

def toggle_mode():
    global is_degree
    is_degree = not is_degree
    mode_btn.config(text="DEG" if is_degree else "RAD")

# -------- BUTTON STYLE --------
def create_button(text, cmd, row, col, bg="#333"):
    btn = tk.Button(root, text=text, command=cmd, bg=bg, fg="white",
                    font=("Arial", 12), bd=0)

    btn.bind("<Enter>", lambda e: btn.config(bg="#555"))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

# -------- TOP ROW --------
mode_btn = tk.Button(root, text="DEG", command=toggle_mode)
mode_btn.grid(row=2, column=0)

create_button("⌫", backspace, 2,1)
create_button("AC", clear, 2,2)
create_button("HIS", toggle_history, 2,3)
create_button("SAVE", save_history, 2,4)

# -------- MEMORY ROW --------
create_button("MC", m_clear, 3,0)
create_button("M+", m_plus, 3,1)
create_button("M-", m_minus, 3,2)
create_button("MR", m_recall, 3,3)
create_button("=", equal, 3,4, "#ff9500")

# -------- NUMBERS --------
buttons = [
("7",4,0),("8",4,1),("9",4,2),("/",4,3),
("4",5,0),("5",5,1),("6",5,2),("*",5,3),
("1",6,0),("2",6,1),("3",6,2),("-",6,3),
("0",7,0),(".",7,1),("00",7,2),("+",7,3)
]

for (t,r,c) in buttons:
    create_button(t, lambda x=t: click(x), r, c)

# -------- SCI --------
create_button("sin", sin_func,8,0)
create_button("cos", cos_func,8,1)
create_button("tan", tan_func,8,2)
create_button("log", log_func,8,3)

create_button("ln", ln_func,9,0)
create_button("√", sqrt_func,9,1)
create_button("x²", square_func,9,2)
create_button("π", lambda: click(str(math.pi)),9,3)

create_button("x³", cube_func,10,0)
create_button("∛", cbrt_func,10,1)
create_button("xʸ", power_func,10,2)
create_button("%", percent_func,10,3)

create_button("±", sign_func,11,0)
create_button("x!", factorial_func,11,1)
create_button("(", lambda: click("("),11,2)
create_button(")", lambda: click(")"),11,3)

# -------- GRID --------
for i in range(12):
    root.grid_rowconfigure(i, weight=1)
for j in range(5):
    root.grid_columnconfigure(j, weight=1)

root.mainloop()