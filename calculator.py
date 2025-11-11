import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Global variables
# -----------------------------
current_expression = ""
memory = 0.0
history = []

# -----------------------------
# Calculator Logic
# -----------------------------
def update_expression(value):
    global current_expression
    current_expression += str(value)
    display_var.set(current_expression)

def clear_expression():
    global current_expression
    current_expression = ""
    display_var.set("")

def backspace():
    global current_expression
    current_expression = current_expression[:-1]
    display_var.set(current_expression)

def toggle_sign():
    global current_expression
    if current_expression:
        if current_expression.startswith("-"):
            current_expression = current_expression[1:]
        else:
            current_expression = "-" + current_expression
    display_var.set(current_expression)

def calculate_result():
    global current_expression
    try:
        result = eval(current_expression)
        history.append(f"{current_expression} = {result}")
        current_expression = str(result)
        display_var.set(current_expression)
    except ZeroDivisionError:
        messagebox.showerror("Error", "Division by zero!")
    except Exception:
        messagebox.showerror("Error", "Invalid expression!")

# -----------------------------
# Memory Functions
# -----------------------------
def memory_add():
    global memory
    try:
        memory += float(display_var.get())
    except ValueError:
        pass

def memory_subtract():
    global memory
    try:
        memory -= float(display_var.get())
    except ValueError:
        pass

def memory_recall():
    update_expression(memory)

def memory_clear():
    global memory
    memory = 0.0

# -----------------------------
# History Functions
# -----------------------------
def show_history():
    if history:
        messagebox.showinfo("History", "\n".join(history))
    else:
        messagebox.showinfo("History", "No calculations yet.")

def clear_history():
    history.clear()
    messagebox.showinfo("History", "History cleared!")

# -----------------------------
# Keyboard Bindings
# -----------------------------
def key_press(event):
    key = event.keysym
    if key in "0123456789":
        update_expression(key)
    elif key in ["plus", "KP_Add"]:
        update_expression("+")
    elif key in ["minus", "KP_Subtract"]:
        update_expression("-")
    elif key in ["asterisk", "KP_Multiply"]:
        update_expression("*")
    elif key in ["slash", "KP_Divide"]:
        update_expression("/")
    elif key in ["percent"]:
        update_expression("%")
    elif key == "period":
        update_expression(".")
    elif key in ["Return", "KP_Enter"]:
        calculate_result()
    elif key == "BackSpace":
        backspace()
    elif key == "Escape":
        clear_expression()
    elif key == "F9":
        toggle_sign()

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Ubuntu Purple Calculator")
root.geometry("380x580")
root.resizable(False, False)
root.config(bg="#5E2750")  # Ubuntu mid-aubergine

# Bind keyboard
root.bind("<Key>", key_press)

# -----------------------------
# Display
# -----------------------------
display_var = tk.StringVar()
display = tk.Entry(
    root, textvariable=display_var,
    font=("Consolas", 26, "bold"),
    bg="#77216F", fg="#FFFFFF",
    justify="right", state="readonly",
    readonlybackground="#77216F",
    relief="flat", highlightthickness=2,
    highlightcolor="#9E63A8", bd=5
)
display.pack(fill="both", ipadx=10, ipady=15, padx=12, pady=20)

# -----------------------------
# Button Styles
# -----------------------------
btn_font = ("Segoe UI", 14, "bold")

# Ubuntu Purple Palette
color_bg = "#5E2750"
num_color = "#77216F"
op_color = "#9E63A8"
mem_color = "#00BFFF"
special_color = "#C19BBE"
hover_color = "#AF5CCF"
fg_color = "#FFFFFF"

# -----------------------------
# Hover Effects
# -----------------------------
def on_enter(e):
    e.widget['bg'] = hover_color

def on_leave(e):
    label = e.widget['text']
    if label.isdigit() or label == ".":
        e.widget['bg'] = num_color
    elif label in ["+", "-", "*", "/", "%", "="]:
        e.widget['bg'] = op_color
    elif "M" in label:
        e.widget['bg'] = mem_color
    else:
        e.widget['bg'] = special_color

# -----------------------------
# Button Actions
# -----------------------------
def button_click(label):
    if label == "C":
        clear_expression()
    elif label == "⌫":
        backspace()
    elif label == "=":
        calculate_result()
    elif label == "±":
        toggle_sign()
    elif label == "MC":
        memory_clear()
    elif label == "MR":
        memory_recall()
    elif label == "M+":
        memory_add()
    elif label == "M-":
        memory_subtract()
    else:
        update_expression(label)

# -----------------------------
# Button Layout
# -----------------------------
buttons = [
    ["MC", "MR", "M+", "M-"],
    ["C", "⌫", "±", "%"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

for r, row in enumerate(buttons):
    frame_row = tk.Frame(root, bg=color_bg)
    frame_row.pack(expand=True, fill="both", pady=2)
    for c, label in enumerate(row):
        color = (
            num_color if label.isdigit() or label == "." else
            op_color if label in ["+", "-", "*", "/", "%", "="] else
            mem_color if "M" in label else
            special_color
        )
        fg = fg_color if color != special_color else "#000000"
        btn = tk.Button(
            frame_row, text=label,
            font=btn_font, bg=color, fg=fg,
            activebackground=hover_color,
            relief="flat", bd=0,
            highlightthickness=0, padx=10, pady=10,
            command=lambda l=label: button_click(l)
        )
        btn.pack(side="left", expand=True, fill="both", padx=6, pady=4)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

# -----------------------------
# History Buttons
# -----------------------------
hist_frame = tk.Frame(root, bg=color_bg)
hist_frame.pack(pady=12)

tk.Button(
    hist_frame, text="Show History",
    font=("Segoe UI", 12, "bold"), bg="#77216F", fg="#FFFFFF",
    relief="flat", bd=0, padx=10, pady=5, command=show_history
).pack(side="left", padx=10)

tk.Button(
    hist_frame, text="Clear History",
    font=("Segoe UI", 12, "bold"), bg="#9E63A8", fg="#FFFFFF",
    relief="flat", bd=0, padx=10, pady=5, command=clear_history
).pack(side="left", padx=10)

# -----------------------------
# Run App
# -----------------------------
root.mainloop()
