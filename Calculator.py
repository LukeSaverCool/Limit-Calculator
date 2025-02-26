# ---------------  Imports        ---------------

import matplotlib.pyplot as plt
import numpy as np
import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# ---------------  Variables  ---------------

# -- Tkinter GUI Variables and Lists --

# GUI Theme
color1 = '#CAFF70'
color2 = '#CB9D23'
color3 = '#111111'

# Window Variable Default Values
window_defaults = {
    "x_min": -60,
    "x_max": 60,
    "y_min": -40,
    "y_max": 40,
    "step": 0.001
}

# Initialize variables
x_min = window_defaults["x_min"]
x_max = window_defaults["x_max"]
y_min = window_defaults["y_min"]
y_max = window_defaults["y_max"]
step = window_defaults["step"]

# Equation Input Variable
equation = "(40x^2 + 40x + 7) / ((x + 30)(x - 15)(x - 40))"

# Color Set Lists
warm_colors = ["red", "orange", "#FFCC00"]
cold_colors = ["purple", "green", "blue"]
rainbow_colors = ["red", "purple", "green", "orange", "blue"]

# ComboBox Lists
axis_styles = ["Show", "Hide"]
legend_styles = ["Show", "Hide"]
limit_styles = ["Grey", "Warm", "Cold", "Rainbow", "Hide"]
plot_styles = ["Grey", "Orange", "Blue", "Hide"]

# -- Matplotlib Graphing Variables and Lists --

fig = plt.figure()
axes = fig.add_subplot(111)

# Container Lists
x_values = []
y_values = []
asymptotes = []
horizontal_asymptotes = []

# ---------------  Functions  ---------------

def format_polynomial(equation):
    """Formats the equation into something that is legible for python."""
    # Replaces ^ with ** for exponents
    equation = equation.replace('^', '**')
    # Implicit multiplication for numbers next to 'x'
    equation = re.sub(r'(?<=\d)(x)', r'*\1', equation)  # ex: 2x -> 2*x
    equation = re.sub(r'(x)(\d)', r'*\2', equation)  # ex: x2 -> x*2
    # Implicit multiplication for parentheses next to 'x'
    equation = re.sub(r'(?<=x)(\()', r'*\1', equation)  # ex: x(x + 1) -> x*(x + 1)
    equation = re.sub(r'(\))(x)', r')*\2', equation)  # ex: (x + 1)x -> (x + 1)*x
    # Implicit multiplication for parentheses next to a number
    equation = re.sub(r'(?<=\d)(\()', r'*\1', equation)  # ex: 2(x + 1) -> 2*(x + 1)
    equation = re.sub(r'(\))(\d)', r')*\2', equation)  # ex: (x + 1)2 -> (x + 1)*2
    # Implicit multiplication for parentheses next to each other
    equation = re.sub(r'(\))(\()', r')*\2', equation)  # ex: (x+1)(x+2) -> (x+1)*(x+2)
    return equation


def calc_limit(x):
    """Finds the asymptotes and adds them to the list."""
    global asymptotes
    rounded_x = round(x, 1)  # Rounds the asymptotes to the nearest whole number
    asymptotes.append(rounded_x)
    return np.nan  # Returns asymptotes as NaN to avoid errors


def get_highest_degree_and_coefficient(poly):
    """Extracts the highest degree and its coefficient from a polynomial."""
    highest_degree = 0  # Initialize the highest degree
    coefficient = 0  # Initialize the coefficient of the highest degree term
    current_coefficient = ""  # Temporary storage for the current coefficient
    current_degree = ""  # Temporary storage for the current degree
    in_coefficient = True  # Flag to indicate if we are parsing the coefficient part
    in_degree = False  # Flag to indicate if we are parsing the degree part

    for char in poly:
        if char.isdigit() or char == '.':
            # If we are parsing the coefficient part
            if in_coefficient:
                current_coefficient += char
            # If we are parsing the degree part
            elif in_degree:
                current_degree += char
        elif char == 'x':
            in_coefficient = False  # Switch to parsing the degree part
            in_degree = True
            if not current_coefficient:
                current_coefficient = "1"  # Default coefficient is 1 if not specified
        elif char == '^':
            continue  # Skip the '^' character
        else:
            # If we encounter a non-digit, non-'x', non-'^' character, process the term
            if current_degree:
                degree = int(current_degree)
                coeff = float(current_coefficient)
                if degree > highest_degree:
                    highest_degree = degree
                    coefficient = coeff
            # Reset temporary storage and flags for the next term
            current_coefficient = ""
            current_degree = ""
            in_coefficient = True
            in_degree = False

    # Process the last term in the polynomial
    if current_degree:
        degree = int(current_degree)
        coeff = float(current_coefficient)
        if degree > highest_degree:
            highest_degree = degree
            coefficient = coeff

    return highest_degree, coefficient


def calculate_horizontal_asymptote(formatted_equation):
    """Calculates the horizontal asymptote of the rational function."""
    global horizontal_asymptotes

    # Split the equation into numerator and denominator
    numerator, denominator = formatted_equation.split('/')

    # Get the highest degree and coefficient of the numerator
    num_degree, num_coefficient = get_highest_degree_and_coefficient(numerator)

    # Get the highest degree and coefficient of the denominator
    denom_degree, denom_coefficient = get_highest_degree_and_coefficient(denominator)

    # Determine the HA based on the degrees of the numerator and denominator
    if num_degree < denom_degree:
        hasymptote = 0  # y = 0 if the degree of the numerator is less than the degree of the denominator
    elif num_degree == denom_degree:
        hasymptote = num_coefficient / denom_coefficient  # y = ratio of leading coefficients if degrees are equal
    else:
        hasymptote = None  # No HA if the degree of the numerator is greater than the degree of the denominator

    # Append the hasymptote to the list if it is not None
    if hasymptote is not None:
        horizontal_asymptotes.append(hasymptote)

    return hasymptote


error = 0
def calculate_y(x, formatted_equation):
    """Calculates y based on the formatted equation."""
    try:
        # Uses eval to evaluate the equation at each x
        eval_context = {"x": x}
        result = eval(formatted_equation, {}, eval_context)  # Computes value of equation at x
       
        # Finds asymptotes and deals with them
        if np.isnan(result) or abs(result) > 1e6:  # Detects if result is NaN or goes to infinity
            calc_limit(x)
            return None  # Returns as None so limits are skipped
        return result

    # Addresses ZeroDivisionError for limits
    except ZeroDivisionError:
        calc_limit(x)
        return None  # Returns as None so limits are skipped
   
    # Addresses any other user errors
    except Exception as e:
        global error
        if error == 0:
            print(f"ERROR: {e}")
            error = 1


# Entry Event Handler
def get_input_values():
    """Gets input values for use."""
    global x_min, x_max, y_min, y_max, step, equation
    try:
        x_min = float(x_min_entry.get())  # Float for integer value
        x_max = float(x_max_entry.get())
        y_min = float(y_min_entry.get())
        y_max = float(y_max_entry.get())
        step = float(step_entry.get())
        equation = equation_entry.get()  # No float needed because it's a string
       
    # Addresses value errors
    except ValueError:
        print("ERROR: Please enter valid numerical values!")


# ComboBox Event Handlers
def axis_style_selected(event):
    axis_style = axis_style_combobox.get()
    print(f"Selected axis style: {axis_style}")
def legend_style_selected(event):
    legend_style = legend_style_combobox.get()
    print(f"Selected legend style: {legend_style}")
def limit_style_selected(event):
    limit_style = limit_style_combobox.get()
    print(f"Selected limit style: {limit_style}")
def plot_style_selected(event):
    plot_style = plot_style_combobox.get()
    print(f"Selected plot style: {plot_style}")

# ---------------  Plotting  ---------------

def graph_start():
    """Handles the event where the graph button is pressed, starts the graph."""
    global x_values, y_values, asymptotes, equation, window_defaults
    global axis_style, legend_style, limit_style, plot_style
   
    print("Graph is loading...")

    # Prepares the graph
    x_values, y_values, asymptotes = [], [], []  # Resets a, b, and asymptotes for new data
    formatted_equation = format_polynomial(equation)
   
    # Gets the combobox styles
    axis_style = axis_style_combobox.get()
    legend_style = legend_style_combobox.get()
    limit_style = limit_style_combobox.get()
    plot_style = plot_style_combobox.get()
   
    # Plots the graph
    fig, axes = plt.subplots()
    for x in np.arange(x_min, x_max, step):  # Sets x limits and step
        y = calculate_y(x, formatted_equation)
        if x is not None:  # Doesn't plot limits
            x_values.append(x)
            y_values.append(y)

    # Sets y limits
    axes.set_ylim(y_min, y_max)
   
    # Shows the x and y axis lines
    if axis_style != "Hide":
        axes.axvline(x=0, color='grey', linestyle=(0, (2, 4)))
        axes.axhline(y=0, color='grey', linestyle=(0, (2, 4)))
   
    # Shows the main plot
    if plot_style != "Hide":
        if plot_style == "Grey":
            axes.plot(x_values, y_values, color="grey")
        elif plot_style == "Orange":
            axes.plot(x_values, y_values, color="orange")
        else:  # Makes the plot blue
            axes.plot(x_values, y_values, color="blue")
   
    # Shows the asymptotes
    if limit_style != "Hide":
        color_map = {
            "Grey": ["grey"],
            "Warm": warm_colors,
            "Cold": cold_colors,
            "Rainbow": rainbow_colors
        }
        colors = color_map.get(limit_style, ["grey"])
        for asymptote, color in zip(asymptotes, colors * (len(asymptotes) // len(colors) + 1)):
            axes.axvline(x=asymptote, color=color, linestyle='--', label=f"Asymptote x = {asymptote}")
   
    # Shows the legend
    if legend_style != "Hide":
        plt.legend()
   
    # Shows the graph title
    plt.title("Graph of " + equation)
   
    # Saves the graph as an image
    graph_image_path = 'graph_image.png'
    plt.savefig(graph_image_path, bbox_inches='tight')
   
    # ------ Graph GUI ------
   
    # -- WINDOW --
    graph_window = tk.Toplevel()
    graph_window.geometry("575x525")
    graph_window.configure(background=color1)
    graph_window.title("Graph of " + equation)
   
    # -- TITLE --
    graph_title_label = ttk.Label(graph_window, text='CALCULATOR',
          background=color1,
          font=('arial', 24, 'bold'))
    graph_title_label.grid(row=0, column=0, columnspan=2, pady=10)
   
    # -- LOAD GRAPH --
   
    try:
        # Opens the saved image and convert it to a Tkinter-compatible format
        img = Image.open(graph_image_path)
        img_tk = ImageTk.PhotoImage(img)
       
        # Creates a label widget to display the image
        graph = ttk.Label(graph_window, image=img_tk)
        graph.img = img_tk  # Keep a reference to prevent garbage collection
       
        # Positions the label in the window
        graph.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
    except Exception as e:
        print(f"Error loading or displaying the image: {e}")

# ---------------  GUI  --------------------

def create_graph_window():
    """Creates the main window for graph settings."""
    global axis_style_combobox, legend_style_combobox, limit_style_combobox, plot_style_combobox
    global x_min_entry, x_max_entry, y_min_entry, y_max_entry, step_entry, equation_entry

    settings = tk.Tk()
    settings.geometry('500x500')
    settings.configure(background=color1)
    settings.title('Windows 11')

    # -- STYLE --
    style = ttk.Style(settings)
    style.configure('TLabel', background=color2, foreground=color3, font=('Arial', 12, 'bold'))
    style.configure('TEntry', background=color2, foreground=color3, font=('Arial', 12, 'bold'))
    style.configure('TFrame', background=color2, foreground=color3, relief=tk.GROOVE, padding=10)
    style.configure('TButton', background=color2, foreground=color3, font=('Arial', 24, 'bold'))

    # -- TITLE --
    settings_title_label = ttk.Label(settings, text='CALCULATOR',
                                     background=color1,
                                     font=('arial', 24, 'bold'))
    settings_title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # -- WINDOW SETTINGS --
    # Window Settings Frame
    window_settings_frame = ttk.Frame(settings, style='TFrame')
    window_settings_frame.grid(row=1, column=0, padx=30, pady=10, sticky="n")

    # x_min
    x_min_label = ttk.Label(window_settings_frame, text='x-min:', style='TLabel')
    x_min_label.grid(column=0, row=0, padx=10, pady=10)

    x_min_entry = ttk.Entry(window_settings_frame, width=8, style='TEntry')
    x_min_entry.grid(row=0, column=1, padx=10, pady=10)
    x_min_entry.insert(0, str(x_min))

    # x_max
    x_max_label = ttk.Label(window_settings_frame, text='x-max:', style='TLabel')
    x_max_label.grid(column=0, row=1, padx=10, pady=10)

    x_max_entry = ttk.Entry(window_settings_frame, width=8, style='TEntry')
    x_max_entry.grid(row=1, column=1, padx=10, pady=10)
    x_max_entry.insert(0, str(x_max))

    # y_min
    y_min_label = ttk.Label(window_settings_frame, text='y-min:', style='TLabel')
    y_min_label.grid(column=0, row=2, padx=10, pady=10)


    y_min_entry = ttk.Entry(window_settings_frame, width=8, style='TEntry')
    y_min_entry.grid(row=2, column=1, padx=10, pady=10)
    y_min_entry.insert(0, str(y_min))

    # y_max
    y_max_label = ttk.Label(window_settings_frame, text='y-max:', style='TLabel')
    y_max_label.grid(column=0, row=3, padx=10, pady=10)

    y_max_entry = ttk.Entry(window_settings_frame, width=8, style='TEntry')
    y_max_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    y_max_entry.insert(0, str(y_max))

    # Step
    step_label = ttk.Label(window_settings_frame, text='Step:', style='TLabel')
    step_label.grid(column=0, row=4, padx=10, pady=10)

    step_entry = ttk.Entry(window_settings_frame, width=8, style='TEntry')
    step_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    step_entry.insert(0, str(step))

    # -- STYLE SETTINGS --
    # Style Settings Frame
    style_settings_frame = ttk.Frame(settings, style='TFrame')
    style_settings_frame.grid(row=1, column=1, padx=30, pady=10, sticky="n")

    # Y/X-Axis
    axis_style_label = ttk.Label(style_settings_frame, text='Y/X-Axis:', style='TLabel')
    axis_style_label.grid(column=0, row=0, padx=10, pady=10)

    axis_style_combobox = ttk.Combobox(style_settings_frame,
                                       width=8,
                                       values=axis_styles,
                                       font=('Arial', 12, 'bold'),
                                       state="readonly")
    axis_style_combobox.grid(column=1, row=0, padx=10, pady=10, sticky="w")
    axis_style_combobox.bind("<<ComboboxSelected>>", axis_style_selected)

    # Legend
    legend_style_label = ttk.Label(style_settings_frame, text='Legend:', style='TLabel')
    legend_style_label.grid(column=0, row=1, padx=10, pady=10)

    legend_style_combobox = ttk.Combobox(style_settings_frame,
                                         width=8,
                                         values=legend_styles,
                                         font=('Arial', 12, 'bold'),
                                         state="readonly")
    legend_style_combobox.grid(column=1, row=1, padx=10, pady=10, sticky="w")
    legend_style_combobox.bind("<<ComboboxSelected>>", legend_style_selected)

    # Limits
    limit_style_label = ttk.Label(style_settings_frame, text='Limits:', style='TLabel')
    limit_style_label.grid(column=0, row=2, padx=10, pady=10)

    limit_style_combobox = ttk.Combobox(style_settings_frame,
                                        width=8,
                                        values=limit_styles,
                                        font=('Arial', 12, 'bold'),
                                        state="readonly")
    limit_style_combobox.grid(column=1, row=2, padx=10, pady=10, sticky="w")
    limit_style_combobox.bind("<<ComboboxSelected>>", limit_style_selected)

    # Plot
    plot_style_label = ttk.Label(style_settings_frame, text='Plot:', style='TLabel')
    plot_style_label.grid(column=0, row=3, padx=10, pady=10)

    plot_style_combobox = ttk.Combobox(style_settings_frame,
                                       width=8,
                                       values=plot_styles,
                                       font=('Arial', 12, 'bold'),
                                       state="readonly")
    plot_style_combobox.grid(column=1, row=3, padx=10, pady=10, sticky="w")
    plot_style_combobox.bind("<<ComboboxSelected>>", plot_style_selected)

    # -- EQUATION INPUT --
    equation_input_frame = ttk.Frame(settings, style='TFrame')
    equation_input_frame.grid(row=2, column=0, columnspan=2, padx=30, pady=30, sticky="n")

    equation_label = ttk.Label(equation_input_frame, text='EQUATION:', style='TLabel')
    equation_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

    equation_entry = ttk.Entry(equation_input_frame,
                               width=36,
                               style='TEntry')
    equation_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")
    equation_entry.insert(0, str(equation))

    # -- GRAPH BUTTON --
    graph_button = ttk.Button(settings, text='GRAPH', style='TButton', command=graph_start)
    graph_button.grid(row=3, column=0, columnspan=2, pady=10)

    settings.mainloop()

equation = "(40x^2 + 40x + 7) / ((x + 30)(x - 15)(x - 40))"
formatted_equation = format_polynomial(equation)

for x in np.arange(x_min, x_max, step):  # Sets x limits and step
        y = calculate_y(x, formatted_equation)
        if x is not None:  # Doesn't plot limits
            x_values.append(x)
            y_values.append(y)

#calculate_horizontal_asymptote(formatted_equation)

#print('Horizontal asymptotes:', horizontal_asymptotes)
print('Vertical asymptotes:', asymptotes)

# Starts up the graph window
#create_graph_window()
