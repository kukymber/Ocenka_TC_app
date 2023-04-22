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
        self.upload_images_tab()

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
        self.tabControl.add(self.upload_images, text="Загрузка изображений")
        self.tabControl.pack(expand=1, fill="both")
    def client_tab(self):
        # Определяем поля и метки для ввода данных собственника авто
        self.label_owner_surname = tk.Label(self.client, text="Фамилия собственника:")
        self.label_owner_surname.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_surname = tk.Entry(self.client)
        self.entry_owner_surname.grid(row=0, column=1, padx=5, pady=5)

        self.label_owner_name = tk.Label(self.client, text="Имя собственника:")
        self.label_owner_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_name = tk.Entry(self.client)
        self.entry_owner_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_owner_patronymic = tk.Label(self.client, text="Отчество собственника:")
        self.label_owner_patronymic.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_patronymic = tk.Entry(self.client)
        self.entry_owner_patronymic.grid(row=2, column=1, padx=5, pady=5)

        self.label_owner_address = tk.Label(self.client, text="Прописка собственника:")
        self.label_owner_address.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_owner_address = tk.Entry(self.client)
        self.entry_owner_address.grid(row=3, column=1, padx=5, pady=5)

        self.label_evaluation_date = tk.Label(self.client, text="Дата оценки:")
        self.label_evaluation_date.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_evaluation_date = tk.Entry(self.client)
        self.entry_evaluation_date.grid(row=4, column=1, padx=5, pady=5)

        self.label_customer_surname = tk.Label(self.client, text="Фамилия заказчика:")
        self.label_customer_surname.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_surname = tk.Entry(self.client)
        self.entry_customer_surname.grid(row=5, column=1, padx=5, pady=5)

        self.label_customer_name = tk.Label(self.client, text="Имя заказчика:")
        self.label_customer_name.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_name = tk.Entry(self.client)
        self.entry_customer_name.grid(row=6, column=1, padx=5, pady=5)

        self.label_customer_patronymic = tk.Label(self.client, text="Отчество заказчика:")
        self.label_customer_patronymic.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entry_customer_patronymic = tk.Entry(self.client)
        self.entry_customer_patronymic.grid(row=7, column=1, padx=5, pady=5)
    def car_tab(self):
        pass
    def analog_cars_tab(self):
        pass
    def otchet_tab(self):
        pass

    def upload_images_tab(self):
        # Создаем словарь для хранения путей к загруженным фотографиям
        self.photo_paths = {}

        # Создаем метки и кнопки для загрузки фотографий
        labels = ["Свидетельство о смерти:", "ПТС:", "Свидетельство о регистрации ТС:", "Паспорт заказчика:"]
        for i, label in enumerate(labels):
            label = tk.Label(self.upload_images, text=label)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            button = tk.Button(self.upload_images, text="Загрузить фото", command=lambda idx=i: self.upload_photo(idx))
            button.grid(row=i, column=1, padx=5, pady=5)

        # Создаем метку для отображения пути к выбранной фотографии
        self.label_photo_path = tk.Label(self.upload_images, text="")
        self.label_photo_path.grid(row=len(labels), column=0, columnspan=2, padx=5, pady=10)

    # Создаем функцию для загрузки изображения и применения OCR
    def load_image(self):
        # Show file dialog to choose image
        file_path = filedialog.askopenfilename()
        if file_path:
            # Reading an image in default mode
            img = cv2.imread(file_path)

            # Rotate image for scan numbers
            img2 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Read image and translate in text and numbers
            text = pytesseract.image_to_string(img, lang="rus")
            numbers = pytesseract.image_to_string(img2, lang="rus")

            # Create lists with data
            word_list = text.split()
            numbers_list = numbers.split()

            seria = [elem for elem in word_list if any(char.isalpha() for char in elem)]

            def filter_objects(lst):
                result = []
                # iterate over each element in the list
                for element in lst:
                    # remove non-letter characters from the element
                    element = ''.join(filter(str.isalpha, element))
                    # check if the filtered element starts with a letter and ends with a letter
                    if element and element[0].isalpha() and element[-1].isalpha():
                        # check if the length of the element is greater than 1
                        if len(element) > 2:
                            # if it is, append it to the result list (if it's not already there)
                            if element not in result:
                                result.append(element)
                # sort the result list in alphabetical order and then reverse the order
                result = sorted(result, key=str.lower, reverse=True)
                return result

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()