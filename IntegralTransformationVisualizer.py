import tkinter as tk
from tkinter import ttk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.special import jv

# Определение символов для SymPy
x, ksi = sp.symbols('x ksi')

class IntegralTransformationVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация интегрального преобразования")
        self.root.geometry("800x600")
        
        # Инициализация графиков
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        
        # Поля ввода для функций и параметров
        self.create_widgets()
        
        # Отрисовка начальных графиков
        self.calc_and_plot_F()
    
    def create_widgets(self):
        """Создаем виджеты для ввода данных и отображения графиков"""
        # Поля для ввода функций f(x) и K(x, ksi)
        ttk.Label(self.root, text="f(x):").grid(row=0, column=0)
        self.f_entry = ttk.Entry(self.root, width=40)
        self.f_entry.grid(row=0, column=1)
        self.f_entry.insert(0, "exp(x*I*0.1)")  # Пример функции по умолчанию
        
        ttk.Label(self.root, text="K(x, ksi):").grid(row=1, column=0)
        self.k_entry = ttk.Entry(self.root, width=40)
        self.k_entry.grid(row=1, column=1)
        self.k_entry.insert(0, "besselj(0, alpha*x*ksi)*x")  # Пример функции по умолчанию
        
        # Поля для ввода параметров
        self.create_param_entry("alpha:", "1.0", 2)
        self.create_param_entry("a:", "1.0", 3)
        self.create_param_entry("b:", "5.0", 4)
        self.create_param_entry("n_x:", "1000", 5)
        self.create_param_entry("p:", "0.0", 6)
        self.create_param_entry("q:", "3.0", 7)
        self.create_param_entry("m_ksi:", "1000", 8)
        
        # Кнопка обновления графиков
        update_button = ttk.Button(self.root, text="Обновить графики", command=self.calc_and_plot_F)
        update_button.grid(row=9, column=1)
        
        # Поле для графиков Matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=10, columnspan=3)
    
    def create_param_entry(self, label_text, default_value, row):
        """Утилита для создания полей ввода параметров"""
        ttk.Label(self.root, text=label_text).grid(row=row, column=0)
        entry = ttk.Entry(self.root, width=10)
        entry.grid(row=row, column=1)
        entry.insert(0, default_value)
        setattr(self, f"{label_text.strip(':').replace(' ', '_')}_entry", entry)
    
    def calc_and_plot_F(self):
        """Основная функция для расчета и построения графиков"""
        # Получаем параметры
        alpha = float(self.alpha_entry.get())
        a = float(self.a_entry.get())
        b = float(self.b_entry.get())
        n = int(self.n_x_entry.get())
        p = float(self.p_entry.get())
        q = float(self.q_entry.get())
        m = int(self.m_ksi_entry.get())
        
        # Получаем функции f(x) и K(x, ksi) из символьного ввода
        fx = sp.sympify(self.f_entry.get())
        K = sp.sympify(self.k_entry.get()).subs('alpha', alpha)
        
        # Диапазоны значений
        hx = (b - a) / n
        x_diapason = np.linspace(a, b, n)
        ksi_diapason = np.linspace(p, q, m)
        
        # Векторизируем вычисление f(x) для всех значений x
        f_func = sp.lambdify(x, fx, 'numpy')
        f_values = f_func(x_diapason)
        
        # Векторизируем вычисление матрицы A
        K_func = sp.lambdify([x, ksi], K, modules={'numpy': np, 'besselj': jv})
        X, KSI = np.meshgrid(x_diapason, ksi_diapason)
        A = K_func(X, KSI)
        
        # Вычисляем F
        F = A @ f_values * hx
        
        # Очищаем предыдущий график
        self.ax.clear()
        
        # Построение графиков Arg и Abs на одном изображении
        self.ax.plot(ksi_diapason, np.angle(F), 'b', label='Arg')
        self.ax.plot(ksi_diapason, np.abs(F), 'g', label='Abs')
        
        # Добавляем легенду и заголовок
        self.ax.legend()
        self.ax.set_title(f'Parameters: alpha={alpha}, a={a}, b={b}, p={p}, q={q}')
        
        # Обновляем холст с графиком
        self.canvas.draw()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = IntegralTransformationVisualizer(root)
    root.mainloop()




