import tkinter as tk
from tkinter import ttk, messagebox
import math
import statistics
from datetime import date, datetime
import ast
import operator



# Optional packages:
# pip install sympy matplotlib numpy

# ---------------- SAFE CALCULATOR ----------------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}

FUNCTIONS = {
    "sin": math.sin, "cos": math.cos,
    "tan": math.tan, "sqrt": math.sqrt,
    "log": math.log, "log10": math.log10,
    "exp": math.exp, "factorial": math.factorial,
    "abs": abs, "pi": math.pi, "e": math.e
}


def calculate_expression(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -evaluate(node.operand)
            if isinstance(node.op, ast.UAdd):
                return evaluate(node.operand)

        if isinstance(node, ast.Name) and node.id in FUNCTIONS:
            value = FUNCTIONS[node.id]
            if not callable(value):
                return value

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name in FUNCTIONS and callable(FUNCTIONS[name]):
                return FUNCTIONS[name](*[evaluate(a) for a in node.args])

        raise ValueError("Invalid mathematical expression")

    return evaluate(tree)


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("ADVANCED CALCULATOR")
root.geometry("900x700")
root.configure(bg="#eaf0f6")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Arial", 11),
    padding=7
)

title = tk.Label(
    root,
    text="ADVANCED CALCULATOR",
    font=("Arial", 22, "bold"),
    bg="#eaf0f6",
    fg="#17365d"
)
title.pack(pady=15)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=10)


def create_tab(name):
    frame = ttk.Frame(notebook, padding=15)
    notebook.add(frame, text=name)
    return frame


# ==================================================
# 1. BASIC CALCULATOR
# ==================================================

basic_tab = create_tab("Basic Calculator")

basic_entry = tk.Entry(
    basic_tab,
    font=("Arial", 20),
    justify="right"
)
basic_entry.pack(fill="x", pady=15)


def basic_button(value):
    if value == "C":
        basic_entry.delete(0, tk.END)

    elif value == "=":
        try:
            result = calculate_expression(basic_entry.get())
            basic_entry.delete(0, tk.END)
            basic_entry.insert(0, str(result))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    else:
        basic_entry.insert(tk.END, value)


buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "C", "+"],
    ["(", ")", "%", "="]
]

for row in buttons:
    frame = ttk.Frame(basic_tab)
    frame.pack(fill="x")

    for value in row:
        ttk.Button(
            frame,
            text=value,
            command=lambda v=value: basic_button(v)
        ).pack(side="left", expand=True, fill="x", padx=3, pady=3)


# ==================================================
# 2. SCIENTIFIC CALCULATOR
# ==================================================


# ==================================================
# 2. SCIENTIFIC CALCULATOR - CORRECTED
# ==================================================


# SCIENTIFIC CALCULATOR TAB


# ================= SCIENTIFIC CALCULATOR =================

scientific_tab = create_tab("Scientific Calculator")

# Heading
ttk.Label(
    scientific_tab,
    text="SCIENTIFIC CALCULATOR",
    font=("Arial", 14, "bold")
).pack(pady=3)

ttk.Label(
    scientific_tab,
    text="Angles are in radians",
    font=("Arial", 9)
).pack(pady=2)

# Input display
sci_entry = tk.Entry(
    scientific_tab,
    font=("Arial", 14),
    justify="right",
    bd=3
)
sci_entry.pack(fill="x", padx=15, pady=5, ipady=4)

# Result display
result_frame = tk.LabelFrame(
    scientific_tab,
    text="CALCULATION RESULT",
    font=("Arial", 9, "bold")
)
result_frame.pack(fill="x", padx=15, pady=4)

sci_result = tk.Label(
    result_frame,
    text="Result will appear here",
    font=("Arial", 12, "bold"),
    fg="green",
    bg="white",
    anchor="e",
    padx=8,
    pady=6
)
sci_result.pack(fill="x")

# Safe calculation function
def calculate_expression(expression):

    import ast
    import math
    import operator

    functions = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "factorial": math.factorial,
        "abs": abs
    }

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod
    }

    def evaluate(node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return node.value
            raise ValueError("Invalid number")

        elif isinstance(node, ast.Name):
            if node.id == "pi":
                return math.pi
            if node.id == "e":
                return math.e
            raise ValueError("Unknown value")

        elif isinstance(node, ast.BinOp):
            operation = operators.get(type(node.op))
            if operation is None:
                raise ValueError("Invalid operator")
            return operation(evaluate(node.left), evaluate(node.right))

        elif isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)
            if isinstance(node.op, ast.USub):
                return -value
            if isinstance(node.op, ast.UAdd):
                return value
            raise ValueError("Invalid operation")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function")

            function = functions.get(node.func.id)
            if function is None or node.keywords:
                raise ValueError("Unsupported function")

            return function(*[evaluate(arg) for arg in node.args])

        else:
            raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


# Calculate button function
def scientific_calculate():

    try:
        expression = sci_entry.get().strip()

        if not expression:
            raise ValueError("Please enter a calculation.")

        result = calculate_expression(expression)

        sci_result.config(
            text=f"Result: {result:.10g}" if isinstance(result, float)
            else f"Result: {result}",
            fg="green"
        )

    except Exception as error:
        sci_result.config(
            text="Calculation Error",
            fg="red"
        )
        messagebox.showerror("Calculation Error", str(error))


# Insert button value
def insert_function(value):
    sci_entry.insert(tk.INSERT, value)
    sci_entry.focus_set()


# Clear function
def clear_scientific():
    sci_entry.delete(0, tk.END)
    sci_result.config(
        text="Result will appear here",
        fg="green"
    )


# Scientific buttons
scientific_buttons_frame = ttk.Frame(scientific_tab)
scientific_buttons_frame.pack(padx=5, pady=4)

functions = [
    "sin(", "cos(", "tan(", "sqrt(", "log(",
    "log10(", "exp(", "factorial(", "abs(", "pi",
    "e", "**", "(", ")", "/",
    "7", "8", "9", "4", "5",
    "6", "1", "2", "3", "0",
    ".", "+", "-", "*", "%"
]

for i, function in enumerate(functions):
    ttk.Button(
        scientific_buttons_frame,
        text=function,
        width=9,
        command=lambda f=function: insert_function(f)
    ).grid(
        row=i // 5,
        column=i % 5,
        padx=2,
        pady=2,
        sticky="nsew"
    )

# Operation buttons
operation_frame = ttk.Frame(scientific_tab)
operation_frame.pack(pady=3)

ttk.Button(
    operation_frame,
    text="CLEAR",
    command=clear_scientific
).pack(side="left", padx=5)

ttk.Button(
    operation_frame,
    text="CALCULATE RESULT",
    command=scientific_calculate
).pack(side="left", padx=5)

# ==================================================
# 3. STATISTICAL CALCULATOR
# ==================================================

stats_tab = create_tab("Statistics")

ttk.Label(
    stats_tab,
    text="Enter numbers separated by commas",
    font=("Arial", 12)
).pack(pady=10)

stats_entry = ttk.Entry(stats_tab, font=("Arial", 14))
stats_entry.pack(fill="x", pady=10)

stats_output = tk.Text(stats_tab, height=15, font=("Arial", 12))
stats_output.pack(fill="both", expand=True)


def calculate_statistics():
    try:
        numbers = [
            float(x.strip())
            for x in stats_entry.get().split(",")
            if x.strip()
        ]

        if not numbers:
            raise ValueError("Enter at least one number")

        output = f"""
COUNT: {len(numbers)}
SUM: {sum(numbers)}
MEAN: {statistics.mean(numbers)}
MEDIAN: {statistics.median(numbers)}
MINIMUM: {min(numbers)}
MAXIMUM: {max(numbers)}
RANGE: {max(numbers)-min(numbers)}
MODE: {statistics.multimode(numbers)}
"""

        if len(numbers) >= 2:
            output += f"""
SAMPLE VARIANCE: {statistics.variance(numbers)}
SAMPLE STANDARD DEVIATION: {statistics.stdev(numbers)}
POPULATION VARIANCE: {statistics.pvariance(numbers)}
POPULATION STANDARD DEVIATION: {statistics.pstdev(numbers)}
"""

        stats_output.delete("1.0", tk.END)
        stats_output.insert(tk.END, output)

    except Exception as error:
        messagebox.showerror("Statistics Error", str(error))


ttk.Button(
    stats_tab,
    text="Calculate Statistics",
    command=calculate_statistics
).pack(pady=10)


# ==================================================
# 4. EQUATION SOLVER
# ==================================================

equation_tab = create_tab("Equation Solver")

ttk.Label(
    equation_tab,
    text="Enter equation (Example: x**2 - 5*x + 6 = 0)",
    font=("Arial", 12)
).pack(pady=15)

equation_entry = ttk.Entry(equation_tab, font=("Arial", 14))
equation_entry.pack(fill="x", pady=10)

equation_result = ttk.Label(
    equation_tab,
    text="Solutions will appear here",
    font=("Arial", 12)
)
equation_result.pack(pady=20)


def solve_equation():
    try:
        import sympy as sp # type: ignore

        x = sp.symbols("x")
        expression = equation_entry.get().replace("^", "**")

        if "=" in expression:
            left, right = expression.split("=", 1)
            equation = sp.sympify(left) - sp.sympify(right)
        else:
            equation = sp.sympify(expression)

        solutions = sp.solve(equation, x)

        equation_result.config(
            text="Solutions: " + str(solutions)
        )

    except ImportError:
        messagebox.showerror(
            "Missing Package",
            "Install SymPy: pip install sympy"
        )

    except Exception as error:
        messagebox.showerror("Equation Error", str(error))


ttk.Button(
    equation_tab,
    text="SOLVE EQUATION",
    command=solve_equation
).pack(pady=10)


# ==================================================
# 5. GRAPH CREATION
# ==================================================


# GRAPH CREATION TAB

graph_tab = create_tab("Graph Creation")

ttk.Label(
    graph_tab,
    text="GRAPH CREATION",
    font=("Arial", 18, "bold")
).pack(pady=15)


# Select graph type

ttk.Label(
    graph_tab,
    text="Select Graph Type",
    font=("Arial", 12)
).pack(pady=5)

graph_type = tk.StringVar(value="Line Graph")

graph_dropdown = ttk.Combobox(
    graph_tab,
    textvariable=graph_type,
    values=["Line Graph", "Bar Graph", "Pie Chart"],
    state="readonly",
    font=("Arial", 12)
)

graph_dropdown.pack(fill="x", padx=20, pady=10)


# Function input

ttk.Label(
    graph_tab,
    text="Enter Function or Data",
    font=("Arial", 12)
).pack(pady=5)

graph_entry = ttk.Entry(
    graph_tab,
    font=("Arial", 14)
)

graph_entry.insert(0, "sin(x)")
graph_entry.pack(fill="x", padx=20, pady=10)


# Chart creation function

def create_graph():

    try:
        import numpy as np
        import matplotlib.pyplot as plt
        import ast

        selected = graph_type.get()
        expression = graph_entry.get().strip()

        if not expression:
            messagebox.showerror(
                "Input Error",
                "Please enter function or data"
            )
            return

        # LINE GRAPH

        if selected == "Line Graph":

            x = np.linspace(-10, 10, 500)

            expression = expression.replace("^", "**")

            allowed = {
                "x": x,
                "pi": np.pi,
                "e": np.e,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "sqrt": np.sqrt,
                "log": np.log,
                "log10": np.log10,
                "exp": np.exp,
                "abs": np.abs
            }

            tree = ast.parse(expression, mode="eval")

            y = eval(
                compile(tree, "<graph>", "eval"),
                {"__builtins__": {}},
                allowed
            )

            if np.isscalar(y):
                y = np.full_like(x, y)

            y = np.asarray(y)

            if y.shape != x.shape:
                raise ValueError("Invalid function")

            plt.figure(figsize=(8, 5))

            plt.plot(
                x, y,
                linewidth=2,
                label="y = " + expression
            )

            plt.axhline(0, color="black")
            plt.axvline(0, color="black")

            plt.xlabel("X Axis")
            plt.ylabel("Y Axis")
            plt.title("Line Graph")

            plt.grid(True)
            plt.legend()

        # BAR GRAPH

        elif selected == "Bar Graph":

            values = [
                float(value.strip())
                for value in expression.split(",")
            ]

            labels = [
                f"Category {i+1}"
                for i in range(len(values))
            ]

            plt.figure(figsize=(8, 5))

            plt.bar(
                labels,
                values
            )

            plt.xlabel("Categories")
            plt.ylabel("Values")
            plt.title("Bar Graph")

            plt.grid(axis="y")

        # PIE CHART

        elif selected == "Pie Chart":

            values = [
                float(value.strip())
                for value in expression.split(",")
            ]

            if any(value < 0 for value in values):
                raise ValueError(
                    "Pie chart values cannot be negative"
                )

            if sum(values) <= 0:
                raise ValueError(
                    "Enter at least one positive value"
                )

            labels = [
                f"Category {i+1}"
                for i in range(len(values))
            ]

            plt.figure(figsize=(7, 7))

            plt.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title("Pie Chart")

        plt.tight_layout()
        plt.show()

    except Exception as error:

        messagebox.showerror(
            "Graph Error",
            str(error)
        )


# Create Graph Button

ttk.Button(
    graph_tab,
    text="CREATE GRAPH",
    command=create_graph
).pack(pady=20)


# ==================================================
# 6. BMI CALCULATOR
# ==================================================

bmi_tab = create_tab("BMI Calculator")

ttk.Label(
    bmi_tab,
    text="BMI CALCULATOR",
    font=("Arial", 18, "bold")
).pack(pady=15)

ttk.Label(bmi_tab, text="Height (cm)").pack()
height_entry = ttk.Entry(bmi_tab)
height_entry.pack(pady=5)

ttk.Label(bmi_tab, text="Weight (kg)").pack()
weight_entry = ttk.Entry(bmi_tab)
weight_entry.pack(pady=5)

bmi_result = ttk.Label(
    bmi_tab,
    text="BMI result will appear here",
    font=("Arial", 13, "bold")
)
bmi_result.pack(pady=20)


def calculate_bmi():
    try:
        height = float(height_entry.get()) / 100
        weight = float(weight_entry.get())

        if height <= 0 or weight <= 0:
            raise ValueError("Enter positive values")

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal range"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity range"

        bmi_result.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}"
        )

    except Exception as error:
        messagebox.showerror("BMI Error", str(error))


ttk.Button(
    bmi_tab,
    text="CALCULATE BMI",
    command=calculate_bmi
).pack(pady=10)


# ==================================================
# 7. AGE CALCULATOR
# ==================================================

age_tab = create_tab("Age Calculator")

ttk.Label(
    age_tab,
    text="AGE CALCULATOR",
    font=("Arial", 18, "bold")
).pack(pady=15)

ttk.Label(
    age_tab,
    text="Enter Date of Birth (YYYY-MM-DD)"
).pack()

dob_entry = ttk.Entry(age_tab, font=("Arial", 14))
dob_entry.pack(pady=10)

age_result = ttk.Label(
    age_tab,
    text="Age will appear here",
    font=("Arial", 13, "bold")
)
age_result.pack(pady=20)


def calculate_age():
    try:
        dob = datetime.strptime(
            dob_entry.get(),
            "%Y-%m-%d"
        ).date()

        today = date.today()

        if dob > today:
            raise ValueError("Date cannot be in the future")

        years = today.year - dob.year

        if (today.month, today.day) < (dob.month, dob.day):
            years -= 1

        days = (today - dob).days

        age_result.config(
            text=f"Age: {years} years\nTotal Days Lived: {days}"
        )

    except Exception as error:
        messagebox.showerror("Age Error", str(error))


ttk.Button(
    age_tab,
    text="CALCULATE AGE",
    command=calculate_age
).pack(pady=10)


# ==================================================
# RUN APPLICATION
# ==================================================

root.mainloop()
