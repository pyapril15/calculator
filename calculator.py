import tkinter as tk
from tkinter import ttk

# Font
DEFAULT_FONT_STYLE = ("Arial", 20)
SMALL_FONT_STYLE = ("Arial", 16)
LARGE_FONT_STYLE = ("Arial", 40, "bold")
DIGITS_FONT_STYLE = ("Arial", 24, "bold")

# Color
OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"
LIGHT_BLUE = "#CCEDFF"
LABEL_COLOR = "#25265E"


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("350x550")
        self.resizable(width=False, height=False)
        self.title("Calculator")
        i = tk.PhotoImage(file="./image/calculator.png")
        self.iconphoto(True, i)

        self.total_exp = ""
        self.current_exp = ""

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            '.': (4, 1), 0: (4, 2)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.button_frame = self.create_button_frame()
        self.button_frame.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.button_frame.rowconfigure(i, weight=1)
            self.button_frame.columnconfigure(i, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

        self.bind_keys()

    def bind_keys(self):
        self.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.bind(key, lambda event, operator=key: self.append_operator(operator))

        self.bind("C", lambda event: self.clear())
        self.bind("c", lambda event: self.clear())
        self.bind("<BackSpace>", lambda event: self.do_backspace())

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = ttk.Label(self.display_frame, text=self.total_exp, background=LIGHT_GRAY, foreground=LABEL_COLOR,
                                font=SMALL_FONT_STYLE, anchor=tk.E)
        total_label.pack(fill=tk.BOTH, expand=True, padx=24)

        label = tk.Label(self.display_frame, text=self.current_exp, anchor=tk.E, background=LIGHT_GRAY,
                         foreground=LABEL_COLOR, font=LARGE_FONT_STYLE)
        label.pack(fill=tk.BOTH, expand=True, padx=24)

        return total_label, label

    def create_display_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def create_button_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.button_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               bd=0, command=lambda x=operator: self.append_operator(x), cursor='hand2')
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.button_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               bd=0, command=lambda x=digit: self.add_to_expression(x), cursor='hand2')
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_clear_button(self):
        button = tk.Button(self.button_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           bd=0, command=self.clear, cursor='hand2')
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def create_square_button(self):
        button = tk.Button(self.button_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           bd=0, command=self.square, cursor='hand2')
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def create_sqrt_button(self):
        button = tk.Button(self.button_frame, text="x\u221a", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           bd=0, command=self.sqrt, cursor='hand2')
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def create_equals_button(self):
        button = tk.Button(self.button_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           bd=0, command=self.evaluate, cursor='hand2')
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def evaluate(self):
        self.total_exp += self.current_exp
        self.update_total_label()

        try:
            self.current_exp = str(eval(self.total_exp))
            self.total_exp = ""
        except Exception:
            self.total_exp = ""
            self.current_exp = "Error"
        finally:
            self.update_total_label()
            self.update_label()

    def add_to_expression(self, value):
        if self.current_exp == "Error":
            self.current_exp = ""
            self.update_label()
        self.current_exp += str(value)
        self.update_label()

    def append_operator(self, operator):
        if self.current_exp == "Error":
            self.current_exp = ""
        if self.current_exp != "":
            self.current_exp += operator
            self.total_exp += self.current_exp
            self.current_exp = ""
            self.update_total_label()
            self.update_label()
        else:
            pass

    def square(self):
        self.current_exp = str(eval(f"{self.current_exp}**2"))
        self.update_label()

    def sqrt(self):
        self.current_exp = str(eval(f"{self.current_exp}**0.5"))
        self.update_label()

    def do_backspace(self):
        if self.current_exp != "":
            self.current_exp = self.current_exp[0:-1]
            self.update_label()
        else:
            self.current_exp = ""
            self.update_label()

    def clear(self):
        self.current_exp = ""
        self.total_exp = ""
        self.update_label()
        self.update_total_label()

    def update_total_label(self):
        expression = self.total_exp
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_exp[:10])


if __name__ == "__main__":
    calculator = Calculator()
    calculator.mainloop()
