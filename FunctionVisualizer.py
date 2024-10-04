import tkinter as tk
from tkinter import ttk
from sympy import *
from sympy.core.sympify import SympifyError
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FunctionVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Function Visualizer")
        # Интерфейс для ввода функции
        self.func_label = tk.Label(self, text="Введите функцию в формате Sympy:")
        self.func_label.pack()
        self.func_entry = tk.Entry(self, width=50)
        self.func_entry.pack()
        
        # Кнопка для применения функции
        self.apply_button = tk.Button(self, text="Применить", command=self.apply_function)
        self.apply_button.pack()
        
        # Поле для ввода интервала и количества точек
        self.interval_label = tk.Label(self, text="Введите интервал (например, -10,10):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(self, width=20)
        self.interval_entry.pack()
        
        self.points_label = tk.Label(self, text="Количество точек:")
        self.points_label.pack()
        self.points_entry = tk.Entry(self, width=20)
        self.points_entry.pack()
        
        # Область для динамически создаваемых полей переменных
        self.variables_frame = tk.Frame(self)
        self.variables_frame.pack()
        
        # График
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack()
        
        self.func_expr = None
        self.variables = {}
    
    def apply_function(self):
        try:
            func_str = self.func_entry.get()
            self.func_expr = sympify(func_str)
            self.update_variables()
        except SympifyError:
            self.func_label.config(text="Ошибка в выражении, попробуйте еще раз.")
    
    def update_variables(self):
        # Очистить старые переменные
        for widget in self.variables_frame.winfo_children():
            widget.destroy()
        
        # Найти переменные в выражении
        variables = [s for s in self.func_expr.free_symbols if str(s) != 'x']
        self.variables = {str(var): tk.DoubleVar(value=1.0) for var in variables}
        
        for var in variables:
            label = tk.Label(self.variables_frame, text=f"{var}:")
            label.pack(side="left")
            entry = tk.Entry(self.variables_frame, textvariable=self.variables[str(var)], width=10)
            entry.pack(side="left")
        
        # Добавить кнопку для построения графика
        plot_button = tk.Button(self.variables_frame, text="Построить график", command=self.plot_function)
        plot_button.pack(side="left")
    
    def plot_function(self):
        interval_str = self.interval_entry.get()
        points_str = self.points_entry.get()
        
        try:
            x_min, x_max = map(float, interval_str.split(','))
            num_points = int(points_str)
        except ValueError:
            self.interval_label.config(text="Неверный интервал или количество точек.")
            return
        
        # Переменная x для построения графика
        x = symbols('x')
        
        # Подставить значения переменных
        func_lambdified = lambdify(x, self.func_expr.subs(
            {symbols(var): self.variables[var].get() for var in self.variables}))
        
        # Построить график
        x_vals = np.linspace(x_min, x_max, num_points)
        y_vals = func_lambdified(x_vals)
        
        self.ax.clear()
        self.ax.plot(x_vals, y_vals)
        self.canvas.draw()


if __name__ == "__main__":
    app = FunctionVisualizer()
    app.mainloop()
