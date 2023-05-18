import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkinter import filedialog

from docxtpl import DocxTemplate

import datetime
import calendar

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
        self.master.title("Оценка авто")
        self.master.geometry("800x600")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.client_tab()
        self.average_price_var = tk.StringVar()
        self.average_price_minus_5_var = tk.StringVar()
        self.entry_average_price = tk.Entry(self.master)
        self.entry_average_price.pack()
        self.car_tab()
        self.analog_cars_tab()
        self.otchet_tab()



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

        def validate_entry_length(entry_text):
            if len(entry_text) <= 17:
                return True
            else:
                return False

        # Определяем поля и метки для ввода данных об авто
        self.label_car_brand = tk.Label(self.car, text="Марка:")
        self.label_car_brand.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_car_brand = ttk.Entry(self.car)
        self.entry_car_brand.grid(row=0, column=1, padx=5, pady=5)

        self.label_car_model = tk.Label(self.car, text="Модель:")
        self.label_car_model.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_car_model = ttk.Entry(self.car)
        self.entry_car_model.grid(row=0, column=3, padx=5, pady=5)

        self.label_type_category = tk.Label(self.car, text="Тип ТС, Категория:")
        self.label_type_category.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_type_category = ttk.Entry(self.car)
        self.entry_type_category.grid(row=1, column=1, padx=5, pady=5)

        self.label_country_of_origin = tk.Label(self.car, text="Страна производства:")
        self.label_country_of_origin.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_country_of_origin = ttk.Entry(self.car)
        self.entry_country_of_origin.grid(row=1, column=3, padx=5, pady=5)

        self.label_vin = tk.Label(self.car, text="VIN:")
        self.label_vin.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_vin = tk.Entry(self.car, validate="key")
        self.entry_vin['validatecommand'] = (self.entry_vin.register(validate_entry_length), '%P')
        self.entry_vin.grid(row=2, column=1, padx=5, pady=5)

        self.label_body_number = tk.Label(self.car, text="Номер кузова:")
        self.label_body_number.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_body_number = tk.Entry(self.car)
        self.entry_body_number.grid(row=2, column=3, padx=5, pady=5)

        self.label_chassis_number = tk.Label(self.car, text="Номер шасси:")
        self.label_chassis_number.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_chassis_number = tk.Entry(self.car)
        self.entry_chassis_number.grid(row=3, column=1, padx=5, pady=5)

        self.label_license_plate_number = tk.Label(self.car, text="Гос. номер:")
        self.label_license_plate_number.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_license_plate_number = tk.Entry(self.car)
        self.entry_license_plate_number.grid(row=3, column=3, padx=5, pady=5)

        self.label_year_of_manufacture = tk.Label(self.car, text="Год выпуска:")
        self.label_year_of_manufacture.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.spinbox_year_of_manufacture = tk.Spinbox(self.car, from_=1900, to=2050, increment=1)
        self.spinbox_year_of_manufacture.grid(row=4, column=1, padx=5, pady=5)

        self.label_transmission = tk.Label(self.car, text="Коробка передач:")
        self.label_transmission.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.label_transmission = ttk.Combobox(self.car, values=['АКПП', 'МКПП'])
        self.label_transmission.grid(row=4, column=3, padx=5, pady=5)

        self.label_color = tk.Label(self.car, text="Цвет:")
        self.label_color.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entry_color = ttk.Entry(self.car)
        self.entry_color.grid(row=7, column=1, padx=5, pady=5)

        self.entry_number_of_seats = tk.Label(self.car, text="Число мест:")
        self.entry_number_of_seats.grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.entry_number_of_seats = tk.Spinbox(self.car, from_=1, to=200, increment=1)
        self.entry_number_of_seats.grid(row=7, column=3, padx=5, pady=5)

        self.entry_engine_power = tk.Label(self.car, text="Мощность двигателя:")
        self.entry_engine_power.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entry_engine_power = tk.Spinbox(self.car, from_=1, to=1500, increment=1)
        self.entry_engine_power.grid(row=8, column=1, padx=5, pady=5)

        self.entry_engine_capacity = tk.Label(self.car, text="Объем двигателя:")
        self.entry_engine_capacity.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        self.entry_engine_capacity = tk.Spinbox(self.car, from_=1, to=10000, increment=1)
        self.entry_engine_capacity.grid(row=8, column=3, padx=5, pady=5)

        self.entry_technical_passport = tk.Label(self.car, text="Технический паспорт:")
        self.entry_technical_passport.grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.entry_technical_passport = ttk.Entry(self.car)
        self.entry_technical_passport.grid(row=10, column=1, padx=5, pady=5)

        self.entry_srts = tk.Label(self.car, text="СРТС:")
        self.entry_srts.grid(row=10, column=2, padx=5, pady=5, sticky="w")
        self.entry_srts = ttk.Entry(self.car)
        self.entry_srts.grid(row=10, column=3, padx=5, pady=5)

        def validate_entry_length(entry_text):
            if len(entry_text) <= 17:
                return True
            else:
                return False


    def analog_cars_tab(self):
        # Инициализируем экземпляр CarScraper
        self.car = CarScraper('toyota', 'probox', '2004')
        self.car_data = self.car.scrape()

        self.listbox1 = tk.Listbox(self.analog_cars)
        self.listbox1.pack(expand=True, fill="both", padx=10, pady=10)

        for link, data in self.car_data.items():
            self.listbox1.insert(tk.END, f"Цена: {data['price']}₽, Год выпуска: {data['year']}")

        self.listbox2 = tk.Listbox(self.analog_cars)
        self.listbox2.pack(expand=True, fill="both", padx=10, pady=10)

        self.add_button = tk.Button(self.analog_cars, text="Добавить", command=self.add_analog)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.remove_button = tk.Button(self.analog_cars, text="Удалить", command=self.remove_analog)
        self.remove_button.pack(side=tk.LEFT, padx=10, pady=5)

    def update_average_price(self):
        average_price = self.calculate_average_price()
        self.average_price_var.set(f"Средняя цена: {round(average_price,2)}₽")
        self.average_price_minus_5_var.set(f"Средняя цена (с учетом 5% поправочного коэффицента): {round(average_price * 0.95, 2)}₽")
        self.entry_average_price.delete(0, tk.END)
        self.entry_average_price.insert(0, str(average_price))

    def add_analog(self):
        index = self.listbox1.curselection()
        if index:
            selected_item = self.listbox1.get(index)
            self.listbox2.insert(tk.END, selected_item)
            self.update_average_price()

            # Создаем словарь с данными об аналогах автомобилей
            analog_data = {
                "year": selected_item.split('Год выпуска: ')[1].strip(),
                "price": selected_item.split('Цена: ')[1].split('₽')[0].strip()
            }

            # Добавляем данные об аналоге в список аналогов
            self.analog_cars_data.append(analog_data)

    def remove_analog(self):
        index = self.listbox2.curselection()
        if index:
            self.listbox2.delete(index)
            self.update_average_price()

    def calculate_average_price(self):
        total_price = 0
        number_of_cars = 0

        for car in self.listbox2.get(0, tk.END):
            price = int(car.split(':')[1].split('₽')[0].strip())
            total_price += price
            number_of_cars += 1

        if number_of_cars == 0:
            return 0  # или любое другое значение по умолчанию
        else:
            return total_price / number_of_cars

    def otchet_tab(self):
        # Получение текущей даты
        current_date = datetime.date.today()
        current_month = current_date.month
        current_year = current_date.year
        formatted_month = str(current_month).zfill(2)
        # index = self.listbox2.curselection()
        # selected_analog = self.listbox2.get(index)

        # Определяем поля и метки для ввода данных об отчете
        self.label_date_of_create = tk.Label(self.otchet, text="Дата составления отчета:")
        self.label_date_of_create.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_date_of_create = ttk.Entry(self.otchet)
        self.entry_date_of_create.insert(0, f'{current_date.day} {self.ru_month[current_month]} {current_year}')
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

        template = DocxTemplate('/home/anatolii/python_project/pythonProjectOcenka/exm.docx')
        month, day, year = self.entry_evaluation_date.get().split("/")
        print(self.analog_cars_data)

        # Replace the placeholders with the chosen data
        context = {
            "owner_surname": self.entry_owner_surname.get(),
            "owner_name": self.entry_owner_name.get(),
            "owner_patronymic": self.entry_owner_patronymic.get(),
            "owner_address": self.entry_owner_address.get(),
            "customer_surname": self.entry_customer_surname.get(),
            "customer_name": self.entry_customer_name.get(),
            "customer_patronymic": self.entry_customer_patronymic.get(),
            "car_brand": self.entry_car_brand.get(),
            "car_model": self.entry_car_model.get(),
            "type_category": self.entry_type_category.get(),
            "country_of_origin": self.entry_country_of_origin.get(),
            "vin": self.entry_vin.get(),
            "body_number": self.entry_body_number.get(),
            "chassis_number": self.entry_chassis_number.get(),
            "license_plate_number": self.entry_license_plate_number.get(),
            "year_of_manufacture": self.spinbox_year_of_manufacture.get(),
            "transmission": self.label_transmission.get(),
            "color": self.entry_color.get(),
            "number_of_seats": self.entry_number_of_seats.get(),
            "engine_power": self.entry_engine_power.get(),
            "engine_capacity": self.entry_engine_capacity.get(),
            "technical_passport": self.entry_technical_passport.get(),
            "srts": self.entry_srts.get(),
            "date_of_create": self.entry_date_of_create.get(),
            "evaluation_date": f'{day} {self.ru_month[int(month)]} 20{year} года',
            "number_of_otchet": self.entry_number_of_otchet.get(),


            "analog1_year": self.analog_cars_data[0]["year"] if len(self.analog_cars_data) >= 1 else "",
            "analog1_price": self.analog_cars_data[0]["price"] if len(self.analog_cars_data) >= 1 else "",

            "analog2_year": self.analog_cars_data[1]["year"] if len(self.analog_cars_data) >= 2 else "",
            "analog2_price": self.analog_cars_data[1]["price"] if len(self.analog_cars_data) >= 2 else "",

            "analog3_year": self.analog_cars_data[2]["year"] if len(self.analog_cars_data) >= 3 else "",
            "analog3_price": self.analog_cars_data[2]["price"] if len(self.analog_cars_data) >= 3 else "",

            "analog4_year": self.analog_cars_data[3]["year"] if len(self.analog_cars_data) >= 4 else "",
            "analog4_price": self.analog_cars_data[3]["price"] if len(self.analog_cars_data) >= 4 else "",
        }

        # Render the template with the context
        template.render(context)

        # Save the Word file
        template.save('output.docx')

        # Show a message box to inform the user that the file has been generated
        messagebox.showinfo("File Generated", "The Word file has been generated successfully.")





if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
