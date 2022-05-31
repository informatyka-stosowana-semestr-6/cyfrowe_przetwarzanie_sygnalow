from email.policy import default
from logic import *
from logic import Signal, SIGNALS
import scipy.signal as scipysignal
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle

signal_A = None
signal_B = None
result_signal = None

def create_chart():
    if signal_menu_var.get() == signal_options[0]:
        signal = signal_A
    elif signal_menu_var.get() == signal_options[1]:
        signal = signal_B
    else:
        signal = result_signal
    figure = plt.Figure(figsize=(6, 6), dpi=100)
    fig = figure.add_subplot(111)
    if signal.discrete:
        if signal_menu_var.get() == signal_options[0]:
            fig.scatter(signal_A.x_values, signal_A.y_values)
        elif signal_menu_var.get() == signal_options[1]:
            fig.scatter(signal_B.x_values, signal_B.y_values)
        else:
            fig.scatter(result_signal.x_values, result_signal.y_values)
    else:
        if signal_menu_var.get() == signal_options[0]:
            fig.plot(signal_A.x_values, signal_A.y_values)
        elif signal_menu_var.get() == signal_options[1]:
            fig.plot(signal_B.x_values, signal_B.y_values)
        else:
            fig.plot(result_signal.x_values, result_signal.y_values)
    figure.savefig('wykres.png')
    scatter = FigureCanvasTkAgg(figure, chart_frame)
    scatter.get_tk_widget().grid(row=0, column=2, rowspan=5)

def create_sampled_signal():
    figure_sampled = plt.Figure(figsize=(6, 6), dpi=100)
    fig = figure_sampled.add_subplot(111)
    if signal_menu_var.get() == signal_options[0]:
        temp_y = signal_A.y_values
        # print(num_of_samples.get())
        temp_y = scipysignal.resample_poly(temp_y, 10, int(float(signal_A.signal_duration) * signal_A.freq))
        temp_x = np.linspace(float(signal_A.start_time),float(signal_A.start_time) + float(signal_A.signal_duration),
                                        num=len(temp_y))
        fig.scatter(temp_x, temp_y)
    elif signal_menu_var.get() == signal_options[1]:
        fig.scatter(signal_B.x_values, signal_B.y_values)
    else:
        fig.scatter(result_signal.x_values, result_signal.y_values)
    figure_sampled.savefig('sampled.png')
    scatter = FigureCanvasTkAgg(figure_sampled, sampling_frame)
    scatter.get_tk_widget().grid(row=0, column=2, rowspan=5)


def create_histogram():
    global signal_A, signal_B
    figure = plt.Figure(figsize=(6, 6), dpi=100)
    fig = figure.add_subplot(111)
    if signal_menu_var.get() == signal_options[0]:
        fig.hist(signal_A.y_values, bins=10, edgecolor="black")
    elif signal_menu_var.get() == signal_options[1]:
        fig.hist(signal_B.y_values, bins=10, edgecolor="black")
    else:
        fig.hist(result_signal.y_values, bins=10, edgecolor="black")
    figure.savefig('histogram.png')
    hist = FigureCanvasTkAgg(figure, histogram_frame)
    hist.get_tk_widget().grid(row=0, column=2, rowspan=5)


def create_charts():
    create_chart()
    create_histogram()
    create_sampled_signal()


def create_signal():
    global signal_A, signal_B
    params = [  amplitude.get(), 
                start_time.get(), 
                signal_duration.get(), 
                base_period.get(), 
                fill_factor.get(),
                jump_time.get(), 
                probability.get()   ]
    new_signal = Signal(signal_type.get(), frequency.get(), params)
    new_signal.generate_signal()
    if signal_menu_var.get() == signal_options[0]:
        signal_A = new_signal
    elif signal_menu_var.get() == signal_options[1]:
        signal_B = new_signal
    create_charts()
    update_parameters()

#Saves as binary and as text file
def save_to_file():
    filename = fd.asksaveasfilename(initialdir=".")
    if filename:
        with open(filename, "wb") as file:
            if signal_menu_var.get() == signal_options[0]:
                pickle.dump(signal_A, file)
            elif signal_menu_var.get() == signal_options[1]:
                pickle.dump(signal_B, file)
            else:
                pickle.dump(result_signal, file)

def read_from_file():
    global signal_A, signal_B, result_signal
    filename = fd.askopenfilename(initialdir=".")
    if filename:
        with open(filename, "rb") as file:
            signal = pickle.load(file)
            if signal_menu_var.get() == signal_options[0]:
                signal_A = signal
            elif signal_menu_var.get() == signal_options[1]:
                signal_B = signal
            else:
                result_signal = signal
            create_charts()
            update_parameters()

def create_method_menu():
    global exec_2_method_var
    for widget in exec_2_selection_second_menu_frame.winfo_children():
        widget.destroy()
    exec_2_method_lbl = Label(exec_2_selection_second_menu_frame, text="Wybierz metode:", width=15)
    exec_2_method_lbl.grid(row=2, column=0)
    exec_2_method_var.trace('w', switch_chart)
    exec_2_method = OptionMenu(exec_2_selection_second_menu_frame, exec_2_method_var, *exec_2_methods)
    exec_2_method.config(width=45)
    exec_2_method.grid(row=3,column=0)

# Switch chart if option menu was used
def switch_chart(*args):
    global exec_2_methods
    if exec_2_operation_var.get() == exec_2_operations[0]:
        exec_2_methods = ["-"]
        for widget in exec_2_selection_second_menu_frame.winfo_children():
            widget.destroy()
        num_of_samples_lbl = Label(exec_2_selection_second_menu_frame, text="Liczba probek:")
        num_of_samples_entry = Entry(exec_2_selection_second_menu_frame, textvariable=num_of_samples)
        num_of_samples_lbl.grid(row=2, column=0)
        num_of_samples_entry.grid(row=2, column=1)
    elif exec_2_operation_var.get() == exec_2_operations[1]:
        exec_2_methods = ["Kwantyzacja rownomierna z obcieciem", "Kwantyzacja rownomierna z zaokragleniem"]
        create_method_menu()
    else:
        exec_2_methods = ["Ekstrapolacja zerowego rzedu", "Interpolacja pierwszego rzedu", "Rekonstrukcja w oparciu o funkcje sinc"]
        create_method_menu()

    if signal_menu_var.get() == signal_options[0]:
        if not signal_A:
            destroy_widgets_and_clear_parameters()
        else:
            update_parameters()
            create_charts()
    elif signal_menu_var.get() == signal_options[1]:
        if not signal_B:
            destroy_widgets_and_clear_parameters()
        else:
            update_parameters()
            create_charts()
    elif signal_menu_var.get() == signal_options[2]:
        if not result_signal:
            destroy_widgets_and_clear_parameters()
        else:
            update_parameters()
            create_charts()


def update_parameters():
    global signal_type
    if signal_menu_var.get() == signal_options[0]:
        signal_temp = signal_A
    elif signal_menu_var.get() == signal_options[1]:
        signal_temp = signal_B
    else:
        signal_temp = result_signal
    signal_type.set(signal_temp.signal_type)
    amplitude.delete(0, END)
    amplitude.insert(0, signal_temp.amplitude)
    start_time.delete(0, END)
    start_time.insert(0, signal_temp.start_time)
    signal_duration.delete(0, END)
    signal_duration.insert(0, signal_temp.signal_duration)
    base_period.delete(0, END)
    base_period.insert(0, signal_temp.base_period)
    fill_factor.delete(0, END)
    fill_factor.insert(0, signal_temp.fill_factor)
    sred_ui.set(signal_temp.avg)
    avg_bez_ui.set(signal_temp.avg_bezwzgl)
    wart_sku_ui.set(signal_temp.wart_skuteczna)
    warian_ui.set(signal_temp.wariancja)
    moc_sr_ui.set(signal_temp.moc_srednia)


def destroy_widgets_and_clear_parameters():
    amplitude.delete(0, END)
    start_time.delete(0, END)
    signal_duration.delete(0, END)
    base_period.delete(0, END)
    fill_factor.delete(0, END)
    for widget in chart_frame.winfo_children():
        widget.destroy()
    for widget in histogram_frame.winfo_children():
        widget.destroy()


def dodaj():
    global result_signal
    result_signal = signal_A.dodaj(signal_B)


def usun():
    global result_signal
    result_signal = signal_A.usun(signal_B)


def mnozenie():
    global result_signal
    result_signal = signal_A.mnozenie(signal_B)


def dzielenie():
    global result_signal
    result_signal = signal_A.dzielenie(signal_B)

root = Tk()
root.geometry("1300x800")

#Notebook - zakladki do o przechowywania wykresow i statystyk
notebook = ttk.Notebook(root)
notebook.grid(row=1, column=5, rowspan=4, columnspan=3, pady=10, padx=10)


# Wybor sygnalu S1, S2, S3...
signal_option_lbl = Label(root, text="Rodzaj sygnalu:", width=15)
signal_option_lbl.grid(row=0, column=0)
signal_type = StringVar()
signal_type.set(SIGNALS[0])
signal_type_menu = OptionMenu(root, signal_type, *SIGNALS)
signal_type_menu.config(width=45)
signal_type_menu.grid(row=0, column=1)

# Wybor sygnalu A, B, wynikowego
signal_options = ["Sygnal A", "Sygnal B", "Wynik"]

signal_selection_menu_frame = Frame(root)
signal_selection_menu_frame.grid(row=1, column=0, columnspan=2)

signal_option_menu_lbl = Label(signal_selection_menu_frame, text="Wybierz sygnal:", width=15)
signal_option_menu_lbl.grid(row=0, column=0)

signal_menu_var = StringVar()
signal_menu_var.set(signal_options[0])
signal_menu_var.trace('w', switch_chart)

signal_menu = OptionMenu(signal_selection_menu_frame, signal_menu_var, *signal_options)
signal_menu.config(width=45)
signal_menu.grid(row=0,column=1)

# Parametry - opisy i text fieldy
paramsFrame = Frame(root)
paramsFrame.grid(row=2, column=0, columnspan=2)

amplitude_lbl = Label(paramsFrame, text="Amplituda:", width=22)
amplitude_lbl.grid(row=1, column=0)

start_time_lbl = Label(paramsFrame, text="Czas poczatkowy:", width=22)
start_time_lbl.grid(row=2, column=0)

signal_duration_lbl = Label(paramsFrame, text="Czas trwania sygnalu:", width=22)
signal_duration_lbl.grid(row=3, column=0)

base_period_lbl = Label(paramsFrame, text="Okres podstawowy:", width=22)
base_period_lbl.grid(row=4, column=0)

fill_factor_lbl = Label(paramsFrame, text="Wspolczynnik wypelnienia:", width=22)
fill_factor_lbl.grid(row=5, column=0)

jump_time_lbl = Label(paramsFrame, text="Dlugosc skoku:", width=22)
jump_time_lbl.grid(row=6, column=0)

probability_lbl = Label(paramsFrame, text="Prawdopodobienstwo:", width=22)
probability_lbl.grid(row=7, column=0)

frequency_lbl = Label(paramsFrame, text="Czestotliwosc probkowania:", width=22)
frequency_lbl.grid(row=9, column=0)

amplitude = Entry(paramsFrame, width=38)
amplitude.grid(row=1, column=1)

start_time = Entry(paramsFrame, width=38)
start_time.grid(row=2, column=1)

signal_duration = Entry(paramsFrame, width=38)
signal_duration.grid(row=3, column=1)

base_period = Entry(paramsFrame, width=38)
base_period.grid(row=4, column=1)

fill_factor = Entry(paramsFrame, width=38)
fill_factor.grid(row=5, column=1)

jump_time = Entry(paramsFrame, width=38)
jump_time.grid(row=6, column=1)

probability = Entry(paramsFrame, width=38)
probability.grid(row=7, column=1)

frequency = Entry(paramsFrame, width=38)
frequency.insert(0, "60")
frequency.grid(row=9, column=1)


# Przyciski
buttonsFrame = Frame(root)
buttonsFrame.grid(row=3, column=0, columnspan=2)

generate_button = Button(buttonsFrame, text="Potwierdz", command=create_signal)
generate_button.grid(row=0, column=0, columnspan=2, sticky="news")

save_to_file_button = Button(buttonsFrame, text="Zapisz plik", command=save_to_file)
save_to_file_button.grid(row=0, column=2, sticky="news")

read_from_file_button = Button(buttonsFrame, text="Wczytaj plik", command=read_from_file)
read_from_file_button.grid(row=0, column=3, sticky="news")

add_button = Button(buttonsFrame, text="Dodawanie", command=dodaj)
add_button.grid(row=1, column=0, sticky="news")

sub_button = Button(buttonsFrame, text="Odejmowanie", command=usun)
sub_button.grid(row=1, column=1, sticky="news")

mul_button = Button(buttonsFrame, text="Mnozenie", command=mnozenie)
mul_button.grid(row=1, column=2, sticky="news")

div_button = Button(buttonsFrame, text="Dzielenie", command=dzielenie)
div_button.grid(row=1, column=3, sticky="news")

# Zadanie 2
# Wybor operacji
exec_2_operations = ["Probkowanie", "Kwantyzacja", "Rekonstrukcja sygnalu"]

exec_2_selection_menu_frame = Frame(root)
exec_2_selection_menu_frame.grid(row=4, column=0, columnspan=2)

exec_2_operation_lbl = Label(exec_2_selection_menu_frame, text="Wybierz operacje:", width=15)
exec_2_operation_lbl.grid(row=0, column=0)

exec_2_operation_var = StringVar()
exec_2_method_var = StringVar()
exec_2_operation_var.set(exec_2_operations[0])
exec_2_operation_var.trace('w', switch_chart)

exec_2_operation = OptionMenu(exec_2_selection_menu_frame, exec_2_operation_var, *exec_2_operations)
exec_2_operation.config(width=45)
exec_2_operation.grid(row=1, column=0)

exec_2_selection_second_menu_frame = Frame(exec_2_selection_menu_frame)
exec_2_selection_second_menu_frame.grid(row=2, column=0)


num_of_samples = StringVar()
num_of_samples.set(10)
num_of_samples_lbl = Label(exec_2_selection_second_menu_frame, text="Liczba probek:")
num_of_samples_entry = Entry(exec_2_selection_second_menu_frame, textvariable=num_of_samples)
# num_of_samples_entry.insert(END, 10)
num_of_samples_lbl.grid(row=2, column=0)
num_of_samples_entry.grid(row=2, column=1)
#drugie menu wywolane jest w funkcji switch_chart



# Wykres
chart_frame = Frame(notebook, height=600, width=600)
notebook.add(chart_frame, text="Wykres")

# Histogram
histogram_frame = Frame(notebook, height=600, width=600)
notebook.add(histogram_frame, text="Histogram")

# Statystyki
stats = Frame(notebook, height=600, width=600)
notebook.add(stats, text="Statystyki", sticky="")

# Probkowanie
sampling_frame = Frame(notebook, height=600, width=600)
notebook.add(sampling_frame, text="Probkowanie")

# Kwantyzacja
quant_frame = Frame(notebook, height=600, width=600)
notebook.add(quant_frame, text="Kwantyzacja")

# Rekonstrukcja
reconstruction_frame = Frame(notebook, height=600, width=600)
notebook.add(reconstruction_frame, text="Rekonstrukcja")

sred_lbl = Label(stats, text="Wartosc srednia: ", pady=10)
sred_lbl.grid(row=1, column=0)

bez_avg_lbl = Label(stats, text="Wartosc srednia bezwzgledna: ", pady=10)
bez_avg_lbl.grid(row=2, column=0)

wart_skut_lbl = Label(stats, text="Wartosc skuteczna: ", pady=10)
wart_skut_lbl.grid(row=3, column=0)

wariancja_lbl = Label(stats, text="Wariancja: ", pady=10)
wariancja_lbl.grid(row=4, column=0)

moc_sre_lbl = Label(stats, text="Moc srednia: ", pady=10)
moc_sre_lbl.grid(row=5, column=0)

sred_ui = StringVar()
avg_bez_ui = StringVar()
wart_sku_ui = StringVar()
warian_ui = StringVar()
moc_sr_ui = StringVar()

sred_ui_lbl = Label(stats, text="0", textvariable=sred_ui, pady=20)
sred_ui_lbl.grid(row=1, column=1)

avg_bez_ui_lbl = Label(stats, text="0", textvariable=avg_bez_ui, pady=20)
avg_bez_ui_lbl.grid(row=2, column=1)

wart_sku_ui_lbl = Label(stats, text="0", textvariable=wart_sku_ui, pady=20)
wart_sku_ui_lbl.grid(row=3, column=1)

warian_ui_lbl = Label(stats, text="0", textvariable=warian_ui, pady=20)
warian_ui_lbl.grid(row=4, column=1)

moc_sr_ui_lbl = Label(stats, text="0", textvariable=moc_sr_ui, pady=20)
moc_sr_ui_lbl.grid(row=5, column=1)


root.mainloop()
