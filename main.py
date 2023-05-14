import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pytesseract
import cv2
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Оценка авто")
        self.master.geometry("800x600")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.client_tab()
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
        self.entry_owner_surname = ttk.Combobox(self.client)
        self.entry_owner_surname.grid(row=0, column=1, padx=5, pady=5)

        self.label_owner_name = tk.Label(self.client, text="Имя собственника:")
        self.label_owner_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_name = ttk.Combobox(self.client)
        self.entry_owner_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_owner_patronymic = tk.Label(self.client, text="Отчество собственника:")
        self.label_owner_patronymic.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_patronymic = ttk.Combobox(self.client)
        self.entry_owner_patronymic.grid(row=2, column=1, padx=5, pady=5)

        self.label_owner_address = tk.Label(self.client, text="Прописка собственника:")
        self.label_owner_address.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_address = ttk.Combobox(self.client)
        self.entry_owner_address.grid(row=3, column=1, padx=5, pady=5)

        self.label_evaluation_date = tk.Label(self.client, text="Дата оценки:")
        self.label_evaluation_date.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_evaluation_date = ttk.Combobox(self.client)
        self.entry_evaluation_date.grid(row=4, column=1, padx=5, pady=5)

        self.label_customer_surname = tk.Label(self.client, text="Фамилия заказчика:")
        self.label_customer_surname.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_surname = ttk.Combobox(self.client)
        self.entry_customer_surname.grid(row=5, column=1, padx=5, pady=5)

        self.label_customer_name = tk.Label(self.client, text="Имя заказчика:")
        self.label_customer_name.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_name = ttk.Combobox(self.client)
        self.entry_customer_name.grid(row=6, column=1, padx=5, pady=5)

        self.label_customer_patronymic = tk.Label(self.client, text="Отчество заказчика:")
        self.label_customer_patronymic.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_patronymic = ttk.Combobox(self.client)
        self.entry_customer_patronymic.grid(row=7, column=1, padx=5, pady=5)

    def car_tab(self):
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
        self.entry_vin = tk.Entry(self.car)
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

        self.label_color = tk.Label(self.car, text="Коробка передач:")
        self.label_color.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.entry_color = ttk.Combobox(self.car, values=['АКПП', 'МКПП'])
        self.entry_color.grid(row=4, column=3, padx=5, pady=5)

        self.label_color = tk.Label(self.car, text="Цвет:")
        self.label_color.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entry_color = ttk.Entry(self.car)
        self.entry_color.grid(row=7, column=1, padx=5, pady=5)

        self.label_color = tk.Label(self.car, text="Число мест:")
        self.label_color.grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.entry_color = tk.Spinbox(self.car, from_=1, to=200, increment=1)
        self.entry_color.grid(row=7, column=3, padx=5, pady=5)

        self.label_color = tk.Label(self.car, text="Мощность двигателя:")
        self.label_color.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entry_color = tk.Spinbox(self.car, from_=1, to=1500, increment=1)
        self.entry_color.grid(row=8, column=1, padx=5, pady=5)

        self.label_color = tk.Label(self.car, text="Объем двигателя:")
        self.label_color.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        self.entry_color = tk.Spinbox(self.car, from_=1, to=10000, increment=1)
        self.entry_color.grid(row=8, column=3, padx=5, pady=5)

        self.label_color = tk.Label(self.car, text="Технический паспорт:")
        self.label_color.grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.entry_color = ttk.Entry(self.car)
        self.entry_color.grid(row=10, column=1, padx=5, pady=5)

        self.label_color = tk.Label(self.car, text="СРТС:")
        self.label_color.grid(row=10, column=2, padx=5, pady=5, sticky="w")
        self.entry_color = ttk.Entry(self.car)
        self.entry_color.grid(row=10, column=3, padx=5, pady=5)




    def analog_cars_tab(self):
        pass
    def otchet_tab(self):
        pass

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()