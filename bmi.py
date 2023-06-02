import customtkinter as ctk
from settings import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=GREEN)
        self.title("BMI Calculator")
        self.geometry("400x450")
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")

        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=60)
        self.age_group = ctk.StringVar()
        self.gender = ctk.StringVar()
        self.bmi_string = ctk.StringVar()
        self.result_string = ctk.StringVar()
        self.update_bmi()

        self.height_int.trace("w", self.update_bmi)
        self.weight_float.trace("w", self.update_bmi)
        self.age_group.trace("w", self.update_result)
        self.gender.trace("w", self.update_result)

        ResultText(self, self.bmi_string, self.result_string)
        WeightInput(self, self.weight_float)
        HeightInput(self, self.height_int)
        AgeGenderInput(self, self.age_group, self.gender)

        self.mainloop()

    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter**2, 1)
        self.bmi_string.set(bmi_result)
        self.update_result()

    def update_result(self, *args):
        bmi = float(self.bmi_string.get())
        gender = self.gender.get()
        age_group = self.age_group.get()

        if gender == "female":
            minimal_bmi = 18
        elif gender == "male":
            minimal_bmi = 19

        if gender:
            if age_group == "25-34":
                minimal_bmi += 1
            elif age_group == "35-44":
                minimal_bmi += 2
            elif age_group == "45-54":
                minimal_bmi += 3
            elif age_group == "55-64":
                minimal_bmi += 4
            elif age_group == "65+":
                minimal_bmi += 5

            if bmi < minimal_bmi:
                self.result_string.set("Underweight")
            elif minimal_bmi <= bmi < minimal_bmi + 5:
                self.result_string.set("Normal")
            elif bmi >= minimal_bmi + 5:
                self.result_string.set("Overweight")


class ResultText(ctk.CTkFrame):
    def __init__(self, parent, bmi_string, result_string):
        bmi_font = ctk.CTkFont(FONT, MAIN_TEXT_SIZE, weight="bold")
        result_font = ctk.CTkFont(FONT, INPUT_FONT_SIZE)
        super().__init__(master=parent, fg_color=GREEN)
        self.grid(column=0, row=0, rowspan=2, sticky="nsew")

        bmi_label = ctk.CTkLabel(
            self, font=bmi_font, text_color=WHITE, textvariable=bmi_string
        )
        bmi_label.pack(expand=True, fill="both", anchor="center")
        result_label = ctk.CTkLabel(
            self, font=result_font, text_color=WHITE, textvariable=result_string
        )
        result_label.pack(expand=True, fill="both", anchor="center")


class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float):
        super().__init__(parent, fg_color=WHITE)
        font = ctk.CTkFont(FONT, INPUT_FONT_SIZE)
        self.weight_float = weight_float
        self.grid(column=0, row=2, sticky="nsew", padx=10, pady=10)

        self.rowconfigure(0, weight=1, uniform="b")
        self.columnconfigure((0, 4), weight=2, uniform="b")
        self.columnconfigure((1, 3), weight=1, uniform="b")
        self.columnconfigure(2, weight=3, uniform="b")

        self.weight_string = ctk.StringVar()
        self.weight_string.set(f"{round(self.weight_float.get(),1)}kg")
        label = ctk.CTkLabel(
            self, textvariable=self.weight_string, font=font, text_color=BLACK
        )
        label.grid(row=0, column=2)

        minus_button = ctk.CTkButton(
            self,
            command=lambda: self.update_weight(("minus", "large")),
            text="-",
            font=font,
            text_color=BLACK,
            fg_color=LIGHT_GRAY,
            hover_color=GRAY,
            corner_radius=BUTTON_RADIUS,
        )
        minus_button.grid(row=0, column=0, sticky="ns", padx=8, pady=8)

        small_minus_button = ctk.CTkButton(
            self,
            command=lambda: self.update_weight(("minus", "small")),
            text="-",
            font=font,
            text_color=BLACK,
            fg_color=LIGHT_GRAY,
            hover_color=GRAY,
            corner_radius=BUTTON_RADIUS,
        )
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)

        small_plus_button = ctk.CTkButton(
            self,
            command=lambda: self.update_weight(("plus", "small")),
            text="+",
            font=font,
            text_color=BLACK,
            fg_color=LIGHT_GRAY,
            hover_color=GRAY,
            corner_radius=BUTTON_RADIUS,
        )
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)

        plus_button = ctk.CTkButton(
            self,
            command=lambda: self.update_weight(("plus", "large")),
            text="+",
            font=font,
            text_color=BLACK,
            fg_color=LIGHT_GRAY,
            hover_color=GRAY,
            corner_radius=BUTTON_RADIUS,
        )
        plus_button.grid(row=0, column=4, sticky="ns", padx=8, pady=8)

    def update_weight(self, info=None):
        if info:
            amount = 1 if info[1] == "large" else 0.1
            if info[0] == "plus":
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
            self.weight_string.set(f"{round(self.weight_float.get(),1)}kg")


class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int):
        font = ctk.CTkFont(FONT, INPUT_FONT_SIZE)
        super().__init__(parent, fg_color=WHITE)
        self.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        slider = ctk.CTkSlider(
            self,
            variable=height_int,
            from_=100,
            to=220,
            command=self.update_text,
            button_color=GREEN,
            button_hover_color=DARK_GREEN,
            progress_color=GREEN,
            fg_color=LIGHT_GRAY,
        )
        slider.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())
        output_text = ctk.CTkLabel(
            self, textvariable=self.output_string, text_color=BLACK, font=font
        )
        output_text.pack(side="left", padx=20)

    def update_text(self, amount):
        text_string = str(int(amount))
        meter = text_string[0]
        cm = text_string[1:]
        self.output_string.set(f"{meter}.{cm}m")


class AgeGenderInput(ctk.CTkFrame):
    def __init__(self, parent, age_group, gender):
        font = ctk.CTkFont(FONT, SWITCH_FONT_SIZE)
        super().__init__(parent, fg_color=WHITE)
        self.age_group = age_group
        self.gender = gender
        self.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        self.rowconfigure((0, 1), weight=1, uniform="b")
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform="b")

        self.age_var = ctk.StringVar()
        age_label = ctk.CTkLabel(self, text="Age", font=font, text_color=BLACK)
        age_label.grid(row=0, column=0, sticky="ew")
        age_box = ctk.CTkComboBox(
            self,
            values=["19-24", "25-34", "35-44", "45-54", "55-64", "65+"],
            variable=self.age_var,
            command=lambda _: self.age_group.set(self.age_var.get()),
            state="readonly",
            font=font,
            hover=False,
            fg_color=WHITE,
            border_color=GREEN,
            button_color=GREEN,
            dropdown_fg_color=WHITE,
            dropdown_text_color=BLACK,
            text_color=BLACK,
            justify="center",
        )
        age_box.grid(row=1, column=0, padx=2)

        gender_label = ctk.CTkLabel(self, text="Gender", font=font, text_color=BLACK)
        gender_label.grid(row=0, column=2, columnspan=2)

        self.gender_var = ctk.StringVar()
        female_box = ctk.CTkRadioButton(
            self,
            text="Female",
            variable=self.gender_var,
            command=lambda: self.gender.set(self.gender_var.get()),
            font=font,
            text_color=BLACK,
            border_color=GREEN,
            hover=False,
            fg_color=DARK_GREEN,
            border_width_checked=10,
            value="female",
        )
        female_box.grid(row=1, column=2)
        male_box = ctk.CTkRadioButton(
            self,
            text="Male",
            variable=self.gender_var,
            command=lambda: self.gender.set(self.gender_var.get()),
            font=font,
            text_color=BLACK,
            border_color=GREEN,
            hover=False,
            fg_color=DARK_GREEN,
            border_width_checked=10,
            value="male",
        )
        male_box.grid(row=1, column=3)


if __name__ == "__main__":
    App()
