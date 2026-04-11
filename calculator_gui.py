import tkinter as tk
from tkinter import messagebox
import math
import re

root = tk.Tk()
root.title("Premium Calculator")
root.geometry("420x760")
root.configure(bg="black")

memory = 0.0
is_degree = True
dark_mode = True

# -------- DISPLAY --------
entry = tk.Entry(
    root,
    font=("Arial", 24),
    bg="black",
    fg="white",
    bd=0,
    justify="right",
    insertbackground="white",
)
entry.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=(10, 6), ipady=10)

# -------- HISTORY --------
history_frame = tk.Frame(root, bg="black")
history_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=(0, 8))

history_box = tk.Text(
    history_frame,
    height=5,
    bg="black",
    fg="gray",
    bd=0,
    wrap="word",
    font=("Arial", 10),
)
history_scroll = tk.Scrollbar(history_frame, command=history_box.yview)
history_box.configure(yscrollcommand=history_scroll.set)

history_box.pack(side="left", fill="both", expand=True)
history_scroll.pack(side="right", fill="y")

history_visible = True

# -------- HELPERS --------
def add_history(text: str) -> None:
    history_box.insert("end", text + "\n")
    history_box.see("end")

def get_entry_text() -> str:
    return entry.get().strip()

def set_entry(value: str) -> None:
    entry.delete(0, tk.END)
    entry.insert(0, value)

def append_text(value: str) -> None:
    entry.insert(tk.END, value)

def clear():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    if current:
        entry.delete(len(current) - 1, tk.END)

def toggle_history():
    global history_visible
    if history_visible:
        history_frame.grid_remove()
    else:
        history_frame.grid()
    history_visible = not history_visible

def save_history():
    try:
        with open("history.txt", "w", encoding="utf-8") as f:
            f.write(history_box.get("1.0", tk.END))
        messagebox.showinfo("Saved", "History saved to history.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save history:\n{e}")

def toggle_mode():
    global is_degree
    is_degree = not is_degree
    mode_btn.config(text="DEG" if is_degree else "RAD")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        bg_root = "black"
        bg_display = "black"
        fg_display = "white"
        bg_history = "black"
        fg_history = "gray"
        bg_top = "#666666"
        fg_top = "white"
        bg_main = "#2e2e2e"
        fg_main = "white"
        bg_op = "orange"
        bg_eq = "green"
        insert_bg = "white"
    else:
        bg_root = "#f4f4f4"
        bg_display = "white"
        fg_display = "black"
        bg_history = "#eeeeee"
        fg_history = "black"
        bg_top = "#c7c7c7"
        fg_top = "black"
        bg_main = "#dddddd"
        fg_main = "black"
        bg_op = "#e69500"
        bg_eq = "#0a9f2e"
        insert_bg = "black"

    root.configure(bg=bg_root)
    history_frame.configure(bg=bg_root)
    history_box.configure(bg=bg_history, fg=fg_history)
    entry.configure(bg=bg_display, fg=fg_display, insertbackground=insert_bg)

    for btn in top_buttons:
        btn.configure(bg=bg_top, fg=fg_top)

    for btn in main_buttons:
        btn.configure(bg=bg_main, fg=fg_main)

    for btn in op_buttons:
        btn.configure(bg=bg_op, fg="white")

    equal_btn.configure(bg=bg_eq, fg="white")

# -------- EXPRESSION PARSING --------
def preprocess_expression(expr: str) -> str:
    expr = expr.replace("÷", "/").replace("×", "*")
    expr = expr.replace("π", str(math.pi))

    # Replace standalone percentage like 50% -> (50/100)
    expr = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expr)

    return expr

def safe_eval(expr: str):
    expr = preprocess_expression(expr)
    allowed = set("0123456789+-*/(). ")
    if not all(ch in allowed for ch in expr):
        raise ValueError("Invalid characters in expression")
    return eval(expr, {"__builtins__": {}}, {})

# -------- BASIC --------
def click(val: str):
    current = entry.get()

    if val == ".":
        parts = re.split(r"[+\-*/()]", current)
        if parts and "." in parts[-1]:
            return

    append_text(val)

def equal():
    try:
        expr = get_entry_text()
        if not expr:
            return
        result = safe_eval(expr)
        add_history(f"{expr} = {result}")
        set_entry(str(result))
    except Exception:
        set_entry("Error")

# -------- MEMORY --------
def m_plus():
    global memory
    try:
        memory += float(preprocess_expression(get_entry_text()))
    except Exception:
        pass

def m_minus():
    global memory
    try:
        memory -= float(preprocess_expression(get_entry_text()))
    except Exception:
        pass

def m_recall():
    set_entry(str(memory))

def m_clear():
    global memory
    memory = 0.0

# -------- SCIENTIFIC --------
def current_value():
    text = preprocess_expression(get_entry_text())
    return float(text)

def sin_func():
    try:
        val = current_value()
        shown = val
        if is_degree:
            val = math.radians(val)
        res = round(math.sin(val), 10)
        set_entry(str(res))
        add_history(f"sin({shown}{'°' if is_degree else ''}) = {res}")
    except Exception:
        set_entry("Error")

def cos_func():
    try:
        val = current_value()
        shown = val
        if is_degree:
            val = math.radians(val)
        res = round(math.cos(val), 10)
        set_entry(str(res))
        add_history(f"cos({shown}{'°' if is_degree else ''}) = {res}")
    except Exception:
        set_entry("Error")

def tan_func():
    try:
        val = current_value()
        shown = val
        if is_degree:
            val = math.radians(val)
        res = round(math.tan(val), 10)
        set_entry(str(res))
        add_history(f"tan({shown}{'°' if is_degree else ''}) = {res}")
    except Exception:
        set_entry("Error")

def log_func():
    try:
        val = current_value()
        if val <= 0:
            raise ValueError
        res = round(math.log10(val), 10)
        set_entry(str(res))
        add_history(f"log({val}) = {res}")
    except Exception:
        set_entry("Error")

def ln_func():
    try:
        val = current_value()
        if val <= 0:
            raise ValueError
        res = round(math.log(val), 10)
        set_entry(str(res))
        add_history(f"ln({val}) = {res}")
    except Exception:
        set_entry("Error")

def sqrt_func():
    try:
        val = current_value()
        if val < 0:
            raise ValueError
        res = round(math.sqrt(val), 10)
        set_entry(str(res))
        add_history(f"√({val}) = {res}")
    except Exception:
        set_entry("Error")

def square_func():
    try:
        val = current_value()
        res = round(val ** 2, 10)
        set_entry(str(res))
        add_history(f"{val}² = {res}")
    except Exception:
        set_entry("Error")

def cube_func():
    try:
        val = current_value()
        res = round(val ** 3, 10)
        set_entry(str(res))
        add_history(f"{val}³ = {res}")
    except Exception:
        set_entry("Error")

def cbrt_func():
    try:
        val = current_value()
        res = round(math.copysign(abs(val) ** (1 / 3), val), 10)
        set_entry(str(res))
        add_history(f"∛({val}) = {res}")
    except Exception:
        set_entry("Error")

def power_func():
    append_text("**")

def percent_func():
    try:
        val = current_value()
        res = round(val / 100, 10)
        set_entry(str(res))
        add_history(f"{val}% = {res}")
    except Exception:
        set_entry("Error")

def sign_func():
    try:
        val = current_value()
        set_entry(str(-val))
    except Exception:
        set_entry("Error")

def reciprocal_func():
    try:
        val = current_value()
        if val == 0:
            raise ValueError
        res = round(1 / val, 10)
        set_entry(str(res))
        add_history(f"1/({val}) = {res}")
    except Exception:
        set_entry("Error")

def exp_func():
    try:
        val = current_value()
        res = round(math.exp(val), 10)
        set_entry(str(res))
        add_history(f"exp({val}) = {res}")
    except Exception:
        set_entry("Error")

def factorial_func():
    try:
        val = current_value()
        if val < 0 or int(val) != val:
            raise ValueError
        n = int(val)
        res = math.factorial(n)
        set_entry(str(res))
        add_history(f"{n}! = {res}")
    except Exception:
        set_entry("Error")

def insert_pi():
    append_text("π")

# -------- KEYBOARD SHORTCUTS --------
def on_keypress(event):
    key = event.keysym
    char = event.char

    if char and char in "0123456789":
        click(char)
        return "break"

    if char in "+-*/().":
        click(char)
        return "break"

    if char == "%":
        percent_func()
        return "break"

    if key == "Return":
        equal()
        return "break"

    if key == "BackSpace":
        backspace()
        return "break"

    if key == "Escape":
        clear()
        return "break"

    if char.lower() == "s":
        sin_func()
        return "break"

    if char.lower() == "c":
        cos_func()
        return "break"

    if char.lower() == "t":
        tan_func()
        return "break"

    if char.lower() == "l":
        log_func()
        return "break"

    if char.lower() == "n":
        ln_func()
        return "break"

    if char.lower() == "r":
        sqrt_func()
        return "break"

    if char.lower() == "p":
        insert_pi()
        return "break"

    if char == "!":
        factorial_func()
        return "break"

root.bind("<Key>", on_keypress)

# -------- BUTTON STYLE --------
top_buttons = []
main_buttons = []
op_buttons = []

def make_button(text, cmd, row, col, bg="#2e2e2e", fg="white", top=False, op=False):
    btn = tk.Button(
        root,
        text=text,
        command=cmd,
        bg=bg,
        fg=fg,
        font=("Arial", 12),
        bd=0,
        activebackground="#555555",
        activeforeground="white",
    )
    btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

    if top:
        top_buttons.append(btn)
    elif op:
        op_buttons.append(btn)
    else:
        main_buttons.append(btn)

    return btn

# -------- TOP ROW --------
mode_btn = make_button("DEG", toggle_mode, 2, 0, bg="#666666", top=True)
make_button("⌫", backspace, 2, 1, bg="#666666", top=True)
make_button("AC", clear, 2, 2, bg="#666666", top=True)
make_button("HIS", toggle_history, 2, 3, bg="#666666", top=True)
make_button("SAVE", save_history, 2, 4, bg="#666666", top=True)

# -------- MEMORY ROW --------
make_button("MC", m_clear, 3, 0, bg="#666666", top=True)
make_button("M+", m_plus, 3, 1, bg="#666666", top=True)
make_button("M-", m_minus, 3, 2, bg="#666666", top=True)
make_button("MR", m_recall, 3, 3, bg="#666666", top=True)
equal_btn = make_button("=", equal, 3, 4, bg="#ff9500", op=True)

# -------- MAIN GRID --------
main_layout = [
    [("7", lambda: click("7")), ("8", lambda: click("8")), ("9", lambda: click("9")), ("÷", lambda: click("/")), ("%", percent_func)],
    [("4", lambda: click("4")), ("5", lambda: click("5")), ("6", lambda: click("6")), ("×", lambda: click("*")), ("√", sqrt_func)],
    [("1", lambda: click("1")), ("2", lambda: click("2")), ("3", lambda: click("3")), ("−", lambda: click("-")), ("x²", square_func)],
    [("0", lambda: click("0")), ("00", lambda: click("00")), (".", lambda: click(".")), ("+", lambda: click("+")), ("x³", cube_func)],
    [("(", lambda: click("(")), (")", lambda: click(")")), ("π", insert_pi), ("∛", cbrt_func), ("xʸ", power_func)],
    [("sin", sin_func), ("cos", cos_func), ("tan", tan_func), ("log", log_func), ("ln", ln_func)],
    [("1/x", reciprocal_func), ("±", sign_func), ("x!", factorial_func), ("EXP", exp_func), ("☀️", toggle_theme)],
]

start_row = 4
for r, row_data in enumerate(main_layout, start=start_row):
    for c, (text, cmd) in enumerate(row_data):
        is_op = text in {"÷", "×", "−", "+", "="}
        bg = "#ff9500" if is_op else "#2e2e2e"
        make_button(text, cmd, r, c, bg=bg, op=is_op)

# -------- GRID CONFIG --------
for i in range(11):
    root.grid_rowconfigure(i, weight=1)

for j in range(5):
    root.grid_columnconfigure(j, weight=1)

# Start hidden history toggle state if desired:
# toggle_history()

root.mainloop()
