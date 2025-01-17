# ---------------  Imports  ---------------


import matplotlib.pyplot as plt
import numpy as np
import re
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


# ---------------  Variables  ---------------


# -- Tkinter GUI Variables and Lists --


# GUI Theme
color1 = '#CAFF70'
color2 = '#CB9D23'
color3 = '#CB9D23'


# Window Variable Default Values
x_min = -60
x_max = 60
y_min = -40
y_max = 40
step = 0.001


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
a = []
b = []
asymptotes = []


# ---------------  Functions  ---------------


def format_polynomial(equation):
    """Formats the equation into something that is legible for python."""
    # Replaces ^ with ** for exponents
    equation = equation.replace('^', '**')
    # Implicit multiplication for numbers next to 'x'
    equation = re.sub(r'(?<=\d)(x)', r'*\1', equation)  # ex: 2x -> 2*x
    equation = re.sub(r'(x)(\d)', r')*\2', equation)  # ex: x2 -> x*2
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
        x_min = float(entry_x_min.get())  # Floats integer value
        x_max = float(entry_x_max.get())
        y_min = float(entry_y_min.get())
        y_max = float(entry_y_max.get())
        step = float(entry_step.get())
        equation = entry_equation.get()  # No float needed because it's a string
       
        print("Entries received!")
       
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
    global a, b, asymptotes, equation, x_min, x_max, y_min, y_max
    global axis_style, legend_style, limit_style, plot_style
   
    print("Graph is loading...")


    # Prepares the graph
    a, b, asymptotes = [], [], []  # Resets a, b, and asymptotes for new data
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
        if x != None:  # Doesn't plot limits
            a.append(x)
            b.append(y)


    # Sets y limits
    axes.set_ylim(y_min, y_max)
   
    # Shows the x and y axis lines
    if axis_style != "Hide":
        axes.axvline(x=0, color='grey', linestyle=(0, (2, 4)))
        axes.axhline(y=0, color='grey', linestyle=(0, (2, 4)))
   
    # Shows the main plot
    if plot_style != "Hide":
        if plot_style == "Grey":
            axes.plot(a, b, color="grey")
        elif plot_style == "Orange":
            axes.plot(a, b, color="orange")
        else:  # Makes the plot blue
            axes.plot(a, b, color="blue")
   
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
   
    graph_window = Toplevel()
    graph_window.geometry("800x600")
    graph_window.configure(background=color1)
    graph_window.title("Graph of " + equation)
   
    # -- TITLE --
    Label(graph_window, text='CALCULATOR', bg=color1, font=('arial', 24, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
   
    # -- LOAD GRAPH --
   
    try:
        # Opens the saved image and convert it to a Tkinter-compatible format
        img = Image.open(graph_image_path)
        img_tk = ImageTk.PhotoImage(img)
       
        # Creates a label widget to display the image
        graph = Label(graph_window, image=img_tk)
        graph.img = img_tk  # Keep a reference to prevent garbage collection
       
        # Positions the label in the window
        graph.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
    except Exception as e:
        print(f"Error loading or displaying the image: {e}")


# ---------------  GUI  --------------------


def create_graph_window():
    """Creates the main window for graph settings."""
    global axis_style_combobox, legend_style_combobox, limit_style_combobox, plot_style_combobox
    global entry_x_min, entry_x_max, entry_y_min, entry_y_max, entry_step, entry_equation


    # -- WINDOW --
    main = Tk()
    main.geometry('800x600')
    main.configure(background=color1)
    main.title('Windows 11')


    # -- TITLE --
    Label(main, text='CALCULATOR', bg=color1, font=('arial', 24, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)


    # -- WINDOW SETTINGS --


    # Window Settings Frame
    window_settings_frame = Frame(main, bg=color2, bd=5, relief=GROOVE)
    window_settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")


    # x_min
    Label(window_settings_frame, text='x-min:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=0, padx=10, pady=10)
    entry_x_min = Entry(window_settings_frame, width=8, font=('Arial', 12, 'bold'), bg=color2)
    entry_x_min.grid(row=0, column=1, padx=10, pady=10)
    entry_x_min.insert(0, str(x_min))
    # x_max
    Label(window_settings_frame, text='x-max:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=1, padx=10, pady=10)
    entry_x_max = Entry(window_settings_frame, width=8, font=('Arial', 12, 'bold'), bg=color2)
    entry_x_max.grid(row=1, column=1, padx=10, pady=10)
    entry_x_max.insert(0, str(x_max))
    # y_min
    Label(window_settings_frame, text='y-min:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=2, padx=10, pady=10)
    entry_y_min = Entry(window_settings_frame, width=8, font=('Arial', 12, 'bold'), bg=color2)
    entry_y_min.grid(row=2, column=1, padx=10, pady=10)
    entry_y_min.insert(0, str(y_min))
    # y_max
    Label(window_settings_frame, text='y-max:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=3, padx=10, pady=10)
    entry_y_max = Entry(window_settings_frame, width=8, font=('Arial', 12, 'bold'), bg=color2)
    entry_y_max.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    entry_y_max.insert(0, str(y_max))
    # Step
    Label(window_settings_frame, text='Step:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=4, padx=10, pady=10)
    entry_step = Entry(window_settings_frame, width=8, font=('Arial', 12, 'bold'), bg=color2)
    entry_step.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    entry_step.insert(0, str(step))


    # -- STYLE SETTINGS --


    # Style Settings Frame
    style_settings_frame = Frame(main, bg=color2, bd=5, relief=GROOVE)
    style_settings_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")


    # Y/X-Axis
    Label(style_settings_frame, text='Y/X-Axis:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=0, padx=10, pady=10)
    axis_style_combobox = ttk.Combobox(style_settings_frame, width=8, values=axis_styles, font=('Arial', 12, 'bold'), state="readonly")
    axis_style_combobox.grid(column=1, row=0, padx=10, pady=10, sticky="w")
    axis_style_combobox.bind("<<ComboboxSelected>>", axis_style_selected)
    # Legend
    Label(style_settings_frame, text='Legend:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=1, padx=10, pady=10)
    legend_style_combobox = ttk.Combobox(style_settings_frame, width=8, values=legend_styles, font=('Arial', 12, 'bold'), state="readonly")
    legend_style_combobox.grid(column=1, row=1, padx=10, pady=10, sticky="w")
    legend_style_combobox.bind("<<ComboboxSelected>>", legend_style_selected)
    # Limits
    Label(style_settings_frame, text='Limits:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=2, padx=10, pady=10)
    limit_style_combobox = ttk.Combobox(style_settings_frame, width=8, values=limit_styles, font=('Arial', 12, 'bold'), state="readonly")
    limit_style_combobox.grid(column=1, row=2, padx=10, pady=10, sticky="w")
    limit_style_combobox.bind("<<ComboboxSelected>>", limit_style_selected)
    # Plot
    Label(style_settings_frame, text='Plot:', bg=color2, font=('arial', 12, 'bold')).grid(column=0, row=3, padx=10, pady=10)
    plot_style_combobox = ttk.Combobox(style_settings_frame, width=8, values=plot_styles, font=('Arial', 12, 'bold'), state="readonly")
    plot_style_combobox.grid(column=1, row=3, padx=10, pady=10, sticky="w")
    plot_style_combobox.bind("<<ComboboxSelected>>", plot_style_selected)


    # -- EQUATION INPUT --


    equation_input_frame = Frame(main, bg=color2, bd=5, relief=GROOVE)
    equation_input_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")


    Label(equation_input_frame, text='EQUATION:', bg=color2, font=('arial', 18, 'bold')).grid(row=0, column=0, padx=5, pady=10, sticky="w")
    entry_equation = Entry(equation_input_frame, width=36, font=('Arial', 12, 'bold'), bg=color2)
    entry_equation.grid(row=0, column=1, padx=5, pady=10, sticky="w")
    entry_equation.insert(0, str(equation))


    # -- GRAPH BUTTON --
    Button(main, text='GRAPH', bg=color2, font=('helvetica', 24, 'bold'), command=graph_start, relief=GROOVE).grid(row=3, column=0, columnspan=2, pady=10)


    main.mainloop()


# Starts up the graph window
create_graph_window()


