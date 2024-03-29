import datetime
import math
import os
import subprocess
import sys
import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox
from tkinter.simpledialog import askfloat

from docxtpl import DocxTemplate
from num2words import num2words
from tkcalendar import DateEntry

from formula_average_price import PriceCalculator
from test_get_price_and_year_form_links import CarScraper


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.analog_cars_data = []
        self.ru_month = {
            1: 'января',
            2: 'февраля',
            3: 'марта',
            4: 'апреля',
            5: 'мая',
            6: 'июня',
            7: 'июля',
            8: 'августа',
            9: 'сентября',
            10: 'октября',
            11: 'ноября',
            12: 'декабря'
        }
        self.master = master
        self.master.title("Эксперт")
        self.master.geometry("800x500")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.client_tab()
        self.average_price_var = tk.StringVar()
        self.average_price_minus_5_var = tk.StringVar()
        self.entry_average_price = tk.Entry(self.master)
        self.entry_average_price.pack()
        self.car_tab()
        self.otchet_tab()
        self.price_calculator = PriceCalculator()

    def create_widgets(self):
        # Создаем вкладки
        self.tabControl = ttk.Notebook(self.master)
        self.client = ttk.Frame(self.tabControl)
        self.car = ttk.Frame(self.tabControl)
        self.analog_cars = ttk.Frame(self.tabControl)
        self.otchet = ttk.Frame(self.tabControl)
        self.upload_images = ttk.Frame(self.tabControl)

        # Добавляем вкладки в основное окно
        self.tabControl.add(self.client, text="Клиент")
        self.tabControl.add(self.car, text="Автомобиль")
        self.tabControl.add(self.analog_cars, text="Аналоги авто")
        self.tabControl.add(self.otchet, text="Отчет")
        self.tabControl.pack(expand=1, fill="both")

    def client_tab(self):
        # Определяем поля и метки для ввода данных собственника авто
        self.label_owner_surname = tk.Label(self.client, text="Фамилия собственника:")
        self.label_owner_surname.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_surname = ttk.Entry(self.client)
        self.entry_owner_surname.grid(row=0, column=1, padx=5, pady=5)

        self.label_owner_name = tk.Label(self.client, text="Имя собственника:")
        self.label_owner_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_name = ttk.Entry(self.client)
        self.entry_owner_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_owner_patronymic = tk.Label(self.client, text="Отчество собственника:")
        self.label_owner_patronymic.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_patronymic = ttk.Entry(self.client)
        self.entry_owner_patronymic.grid(row=2, column=1, padx=5, pady=5)

        self.label_owner_address = tk.Label(self.client, text="Прописка собственника:")
        self.label_owner_address.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_address = ttk.Entry(self.client)
        self.entry_owner_address.grid(row=3, column=1, padx=5, pady=5)

        self.label_customer_surname = tk.Label(self.client, text="Фамилия заказчика:")
        self.label_customer_surname.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_surname = ttk.Entry(self.client)
        self.entry_customer_surname.grid(row=4, column=1, padx=5, pady=5)

        self.label_customer_name = tk.Label(self.client, text="Имя заказчика:")
        self.label_customer_name.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_name = ttk.Entry(self.client)
        self.entry_customer_name.grid(row=5, column=1, padx=5, pady=5)

        self.label_customer_patronymic = tk.Label(self.client, text="Отчество заказчика:")
        self.label_customer_patronymic.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_patronymic = ttk.Entry(self.client)
        self.entry_customer_patronymic.grid(row=6, column=1, padx=5, pady=5)

    def car_tab(self):
        def toggle_vin_entry():
            if self.vin_number_var.get():
                self.entry_vin.delete(0, tk.END)
                self.entry_vin.insert(0, "Отсутствует")
                self.entry_vin.config(state="disabled")
            else:
                self.entry_vin.delete(0, tk.END)
                self.entry_vin.config(state="normal")

            if self.body_number_var.get():
                self.entry_body_number.delete(0, tk.END)
                self.entry_body_number.insert(0, "Отсутствует")
                self.entry_body_number.config(state="disabled")
            else:
                self.entry_body_number.delete(0, tk.END)
                self.entry_body_number.config(state="normal")

            if self.chassis_number_var.get():
                self.entry_chassis_number.delete(0, tk.END)
                self.entry_chassis_number.insert(0, "Отсутствует")
                self.entry_chassis_number.config(state="disabled")
            else:
                self.entry_chassis_number.delete(0, tk.END)
                self.entry_chassis_number.config(state="normal")

        def validate_entry_length(entry_text):
            if len(entry_text) <= 17:
                return True
            else:
                return False

        def format_data(data):
            words = data.split(" ")
            formatted_data = "_".join(word.strip() for word in words if word.strip())
            return formatted_data

        def get_and_scrape():
            try:
                brand = format_data(self.entry_car_brand.get().lower())
                model = format_data(self.entry_car_model.get().lower())
                year = self.spinbox_year_of_manufacture.get()

                if not brand or not model or not year:
                    raise ValueError("Все поля должны быть заполнены")

                self.car = CarScraper(brand, model, int(year))
                self.car_data = self.car.scrape()
                self.analog_cars_tab()

                # Вывод сообщения о успешном завершении
                messagebox.showinfo("Успех", "Поиск аналогов успешно завершен")


            except Exception as e:
                messagebox.showerror("Ошибка", f'{str(e)}\nПроверьте адресную строку!')



        # Определяем поля и метки для ввода данных об авто
        self.label_car_brand = tk.Label(self.car, text="Марка:")
        self.label_car_brand.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_car_brand = ttk.Entry(self.car)
        self.entry_car_brand.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.label_car_model = tk.Label(self.car, text="Модель:")
        self.label_car_model.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_car_model = ttk.Entry(self.car)
        self.entry_car_model.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.label_type_category = tk.Label(self.car, text="Тип ТС, Категория:")
        self.label_type_category.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_type_category = ttk.Entry(self.car)
        self.entry_type_category.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.label_country_of_origin = tk.Label(self.car, text="Страна производства:")
        self.label_country_of_origin.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_country_of_origin = ttk.Entry(self.car)
        self.entry_country_of_origin.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.label_vin = tk.Label(self.car, text="VIN:")
        self.label_vin.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_vin = ttk.Entry(self.car, validate="key")
        self.entry_vin['validatecommand'] = (self.entry_vin.register(validate_entry_length), '%P')
        self.entry_vin.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.vin_number_var = tk.BooleanVar()
        self.vin_checkbox = ttk.Checkbutton(self.car, text="Отсутствует", variable=self.vin_number_var,
                                            command=toggle_vin_entry)
        self.vin_checkbox.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.label_body_number = tk.Label(self.car, text="Номер кузова:")
        self.label_body_number.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_body_number = ttk.Entry(self.car)
        self.entry_body_number.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.body_number_var = tk.BooleanVar()
        self.body_number_checkbox = ttk.Checkbutton(self.car, text="Отсутствует", variable=self.body_number_var,
                                                    command=toggle_vin_entry)
        self.body_number_checkbox.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        self.label_chassis_number = tk.Label(self.car, text="Номер шасси:")
        self.label_chassis_number.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_chassis_number = ttk.Entry(self.car)
        self.entry_chassis_number.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.chassis_number_var = tk.BooleanVar()
        self.chassis_number_checkbox = ttk.Checkbutton(self.car, text="Отсутствует", variable=self.chassis_number_var,
                                                       command=toggle_vin_entry)
        self.chassis_number_checkbox.grid(row=4, column=2, padx=5, pady=5, sticky="w")

        self.label_license_plate_number = tk.Label(self.car, text="Гос. номер:")
        self.label_license_plate_number.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.entry_license_plate_number = ttk.Entry(self.car)
        self.entry_license_plate_number.grid(row=5, column=3, padx=5, pady=5, sticky="w")

        self.label_year_of_manufacture = tk.Label(self.car, text="Год выпуска:")
        self.label_year_of_manufacture.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.spinbox_year_of_manufacture = tk.Spinbox(self.car, from_=1900, to=2050, increment=1)
        self.spinbox_year_of_manufacture.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.label_transmission = tk.Label(self.car, text="Коробка передач:")
        self.label_transmission.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.combobox_transmission = ttk.Combobox(self.car, values=['АКПП', 'МКПП'])
        self.combobox_transmission.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        self.label_color = tk.Label(self.car, text="Цвет:")
        self.label_color.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_color = ttk.Entry(self.car)
        self.entry_color.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.label_number_of_seats = tk.Label(self.car, text="Число мест:")
        self.label_number_of_seats.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.spinbox_number_of_seats = tk.Spinbox(self.car, from_=1, to=200, increment=1)
        self.spinbox_number_of_seats.grid(row=6, column=3, padx=5, pady=5, sticky="w")

        self.label_engine_power = tk.Label(self.car, text="Мощность двигателя:")
        self.label_engine_power.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.spinbox_engine_power = tk.Spinbox(self.car, from_=1, to=1500, increment=1)
        self.spinbox_engine_power.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        self.label_engine_capacity = tk.Label(self.car, text="Объем двигателя:")
        self.label_engine_capacity.grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.spinbox_engine_capacity = tk.Spinbox(self.car, from_=1, to=10000, increment=1)
        self.spinbox_engine_capacity.grid(row=7, column=3, padx=5, pady=5, sticky="w")

        self.label_technical_passport = tk.Label(self.car, text="Технический паспорт:")
        self.label_technical_passport.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entry_technical_passport = ttk.Entry(self.car)
        self.entry_technical_passport.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        self.label_srts = tk.Label(self.car, text="СРТС:")
        self.label_srts.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        self.entry_srts = ttk.Entry(self.car)
        self.entry_srts.grid(row=8, column=3, padx=5, pady=5, sticky="w")

        self.submit_button = tk.Button(self.car, text="Поиск аналогов", command=get_and_scrape)
        self.submit_button.grid(row=10, column=0, columnspan=4, padx=5, pady=5)




    def analog_cars_tab(self):
        self.variance = float
        self.listbox1 = tk.Listbox(self.analog_cars)
        self.listbox1.pack(expand=True, fill="both", padx=10, pady=10)
        self.listbox1.bind("<Double-Button-1>", self.listbox1_double_click)

        for link, data in self.car_data.items():
            # Добавляем ссылку вместе с годом и ценой
            self.listbox1.insert(tk.END, f"Цена: {data['price']}₽, Год выпуска: {data['year']}, Ссылка: {link}")

        self.listbox2 = tk.Listbox(self.analog_cars)
        self.listbox2.pack(expand=True, fill="both", padx=10, pady=10)

        self.add_button = tk.Button(self.analog_cars, text="Добавить", command=self.add_analog)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.remove_button = tk.Button(self.analog_cars, text="Удалить", command=self.remove_analog)
        self.remove_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.confirm_analogs_button = ttk.Button(self.analog_cars, text="Подтвердить аналоги",
                                                 command=self.confirm_analogs)
        self.confirm_analogs_button.pack(side=tk.LEFT, padx=10, pady=5)

    def update_analog_prices(self):
        analog_prices = []
        for analog_data in self.analog_cars_data:
            price = float(analog_data.get('price'))
            coefficient = analog_data.get('coefficient', 1.0)
            adjusted_price = price * coefficient
            analog_data['adjusted_price'] = adjusted_price
            analog_prices.append(adjusted_price)

        # Обновляем цены предложений в калькуляторе
        self.price_calculator.update_offer_prices(analog_prices)

        # Обновляем среднюю цену и другие значения
        average_price = self.price_calculator.compute_average_offer_price()
        self.average_price_var.set(f"Средняя цена: {round(average_price, 2)}₽")
        self.average_price_minus_5_var.set(
            f"Средняя цена (с учетом 5% поправочного коэффициента): {round(average_price * 0.95, 2)}₽")
        self.entry_average_price.delete(0, tk.END)
        self.entry_average_price.insert(0, str(average_price))

    def add_analog(self):
        index = self.listbox1.curselection()
        if not index:
            return

        selected_item = self.listbox1.get(index)
        self.listbox2.insert(tk.END, selected_item)

        analog_data = {
            "year": selected_item.split('Год выпуска: ')[1].split(',')[0].strip(),
            "price": selected_item.split('Цена: ')[1].split('₽')[0].strip(),
            "link": selected_item.split('Ссылка: ')[1].strip(),
            "coefficient": 1.0  # Добавить поправочный коэффициент по умолчанию
        }

        self.analog_cars_data.append(analog_data)

        self.update_analog_prices()

    def listbox1_double_click(self, event):
        index = self.listbox1.curselection()
        if not index:
            return
        selected_item = self.listbox1.get(index)
        link = selected_item.split('Ссылка: ')[1].strip()
        webbrowser.open(link)

    def extract_prices(self, data):
        prices = []
        for item in data:
            price = item.get('price')
            if price is not None:
                prices.append(float(price))
        return prices

    def remove_analog(self):
        index = self.listbox2.curselection()
        if index:
            self.listbox2.delete(index)
            del self.analog_cars_data[index[0]]
            self.update_analog_prices()

    def confirm_analogs(self):
        # Проверка, что выбран хотя бы один аналог
        if not self.analog_cars_data:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите аналоги авто")
            return

        # Создаем словарь для хранения коэффициентов аналогов
        analog_coefficients = {}

        # Вывод окна с вопросом о необходимости исправления коэффициентов
        answer = messagebox.askyesno("Исправление коэффициентов", "Необходимо исправить коэффициенты?")

        if answer:
            for i, analog_data in enumerate(self.analog_cars_data):
                coefficient = askfloat("Исправление поправочного коэффициента",
                                       f"Введите поправочный коэффициент для аналога с годом выпуска {analog_data['year']} и ценой {analog_data['price']}:")
                if coefficient is not None:
                    # Округляем коэффициент до двух значений после запятой
                    coefficient = round(coefficient, 2)
                    analog_data['coefficient'] = coefficient
                    analog_coefficients[i] = coefficient

                # Закрываем окно после установки коэффициента для последнего аналога
                if i == len(self.analog_cars_data) - 1:
                    self.master.focus_set()

        self.update_analog_prices()

    def otchet_tab(self):
        # Получение текущей даты
        current_date = datetime.date.today()
        current_month = current_date.month
        current_year = current_date.year
        formatted_month = str(current_month).zfill(2)

        # Определяем поля и метки для ввода данных об отчете
        self.label_date_of_create = tk.Label(self.otchet, text="Дата составления отчета:")
        self.label_date_of_create.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_date_of_create = ttk.Entry(self.otchet)
        self.entry_date_of_create.insert(0, f'{current_date.day} {self.ru_month[current_month]} {current_year} года')
        self.entry_date_of_create.grid(row=0, column=1, padx=5, pady=5)

        self.label_evaluation_date = tk.Label(self.otchet, text="Дата оценки:")
        self.label_evaluation_date.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_evaluation_date = DateEntry(self.otchet, width=12, background='white', foreground='black',
                                               borderwidth=2)
        self.entry_evaluation_date.grid(row=1, column=1, padx=5, pady=5)

        self.label_number_of_otchet = tk.Label(self.otchet, text="Номер отчета:")
        self.label_number_of_otchet.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_number_of_otchet = ttk.Entry(self.otchet)
        self.entry_number_of_otchet.insert(0, f"/{formatted_month}-{current_year}")
        self.entry_number_of_otchet.grid(row=2, column=1, padx=5, pady=5)

        self.button_generate_report = ttk.Button(self.otchet, text="Сгенерировать отчет",
                                                 command=self.generate_word_file)
        self.button_generate_report.grid(row=5, column=0, padx=5, pady=5)

        self.label_average_price = tk.Label(self.otchet, textvariable=self.average_price_var)
        self.label_average_price.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.label_average_price_minus_5 = tk.Label(self.otchet, textvariable=self.average_price_minus_5_var)
        self.label_average_price_minus_5.grid(row=4, column=0, padx=5, pady=5, sticky="w")


    def generate_word_file(self):
        def calculate_prices(calculator):
            analog_prices = [float(analog["price"]) * analog.get("coefficient", 1.0) for analog in
                             self.analog_cars_data]

            # обновление цен предложений в калькуляторе
            calculator.update_offer_prices(analog_prices)

            # вычисление минимальной и максимальной цены
            min_price = min(analog_prices) if analog_prices else None
            max_price = max(analog_prices) if analog_prices else None

            # вычисление средней и конечной цены
            final_average_offer_price = calculator.compute_final_average_offer_price()
            final_price = calculator.compute_final_price()

            # вычисление стандартной ошибки и доверительного интервала
            standard_error = calculator.compute_standard_error()
            confidence_interval = calculator.compute_confidence_interval()

            return min_price, max_price, final_average_offer_price, final_price, standard_error, confidence_interval

        calculator = PriceCalculator()
        template_path = os.path.join('default.docx')
        template = DocxTemplate(template_path)
        month, day, year = self.entry_evaluation_date.get().split("/")
        min_price, max_price, final_average_offer_price, final_price, standard_error, confidence_interval = calculate_prices(
            calculator)
        lower_bound, upper_bound = confidence_interval
        accuracy = calculator.compute_accuracy()
        if math.isnan(final_price):
            messagebox.showerror("Ошибка", "Невозможно вычислить итоговую цену.")
            return
        # Преобразование итоговой цены в словесное представление
        final_price_words = num2words(int(final_price), lang='ru').capitalize()

        context = {
            "owner_surname": self.entry_owner_surname.get().title(),
            "owner_name": self.entry_owner_name.get().title(),
            "owner_patronymic": self.entry_owner_patronymic.get().title(),
            "owner_address": self.entry_owner_address.get(),
            "customer_surname": self.entry_customer_surname.get().title(),
            "customer_name": self.entry_customer_name.get().title(),
            "customer_patronymic": self.entry_customer_patronymic.get().title(),
            "car_brand": self.entry_car_brand.get().title(),
            "car_model": self.entry_car_model.get().title(),
            "type_category": self.entry_type_category.get().title(),
            "country_of_origin": self.entry_country_of_origin.get().title(),
            "vin": self.entry_vin.get().upper(),
            "body_number": self.entry_body_number.get().upper(),
            "chassis_number": self.entry_chassis_number.get().upper(),
            "license_plate_number": self.entry_license_plate_number.get(),
            "year_of_manufacture": self.spinbox_year_of_manufacture.get(),
            "transmission": self.combobox_transmission.get(),
            "color": self.entry_color.get().title(),
            "number_of_seats": self.spinbox_number_of_seats.get(),
            "engine_power": self.spinbox_engine_power.get(),
            "engine_capacity": self.spinbox_engine_capacity.get(),
            "technical_passport": self.entry_technical_passport.get(),
            "srts": self.entry_srts.get(),

            "date_of_create": self.entry_date_of_create.get(),
            "evaluation_date": f'{day} {self.ru_month[int(month)]} 20{year} года',
            "number_of_otchet": self.entry_number_of_otchet.get(),
            "evaluation_date_analog": f'{str(day).zfill(2)}.{str(month).zfill(2)}.{year}',

            "analog1_year": self.analog_cars_data[0]["year"] if len(self.analog_cars_data) >= 1 else "",
            "analog1_price": self.analog_cars_data[0]["price"] if len(self.analog_cars_data) >= 1 else "",
            "analog1_coefficient": round(self.analog_cars_data[0]["coefficient"], 2) if len(
                self.analog_cars_data) >= 1 else 1.0,

            "analog2_year": self.analog_cars_data[1]["year"] if len(self.analog_cars_data) >= 2 else "",
            "analog2_price": self.analog_cars_data[1]["price"] if len(self.analog_cars_data) >= 2 else "",
            "analog2_coefficient": round(self.analog_cars_data[1]["coefficient"], 2) if len(
                self.analog_cars_data) >= 2 else 1.0,

            "analog3_year": self.analog_cars_data[2]["year"] if len(self.analog_cars_data) >= 3 else "",
            "analog3_price": self.analog_cars_data[2]["price"] if len(self.analog_cars_data) >= 3 else "",
            "analog3_coefficient": round(self.analog_cars_data[2]["coefficient"], 2) if len(
                self.analog_cars_data) >= 3 else 1.0,

            "analog4_year": self.analog_cars_data[3]["year"] if len(self.analog_cars_data) >= 4 else "",
            "analog4_price": self.analog_cars_data[3]["price"] if len(self.analog_cars_data) >= 4 else "",
            "analog4_coefficient": round(self.analog_cars_data[3]["coefficient"], 2) if len(
                self.analog_cars_data) >= 4 else 1.0,

            "min_price": int(min_price),
            "max_price": int(max_price),
            "final_average_offer_price": int(final_average_offer_price),
            "final_price": int(final_price),
            "final_price_words": final_price_words,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "accuracy": int(accuracy),
        }

        template.render(context)
        output_file = (f'{self.entry_owner_surname.get().title()}{self.entry_car_brand.get().title()}'
                       f'{self.entry_car_model.get().title()}.docx')
        # Сохранение Word-файла
        template.save(output_file)

        # Проверка, был ли успешно создан файл
        if not os.path.exists(output_file):
            messagebox.showerror("Ошибка", "Не удалось создать Word-файл")
        else:
            # Показать информационное окно для уведомления пользователя об успешном создании файла
            messagebox.showinfo("Файл создан", "Word-файл успешно создан.")

        # Открытие сгенерированного файла
        if sys.platform == "win32":
            subprocess.call(['start', output_file], shell=True)
        elif sys.platform == "darwin":
            subprocess.call(['open', output_file])
        else:
            subprocess.call(['xdg-open', output_file])


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
