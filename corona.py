import json
import requests
import tkinter as Tk
from tkinter import messagebox
from tkinter import simpledialog
from difflib import SequenceMatcher
import os


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def main():
    while True:
        try:
            try:
                application_window.destroy()
            except:
                pass
            application_window = Tk.Tk()
            application_window.withdraw()
            answer = simpledialog.askstring("Corona Update", "אנא הזן שם עיר או בחר מהרשימה:", parent=application_window)
            if answer is None:
                return None
            url = 'https://data.gov.il/api/3/action/datastore_search?' \
                  'resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&sort=Date desc&limit=1&filters={"City_Name":\"' + answer + '\"}'

            results = json.loads(requests.get(url).text)['result']['records'][0]
            application_window.destroy()
            break
        except:
            closest_city = ''
            with open(r'cities.txt', 'r',encoding='utf8') as cities:
                closest = 0
                city = 'some string'
                while city != '':
                    city = cities.readline().replace('\n', '')
                    similarity = similar(city, answer)
                    if similarity > closest:
                        closest = similarity
                        closest_city = city
            messagebox.showinfo(f"שגיאה", f"שם עיר לא תקין\nאולי התכוונת ל: {closest_city}")


    root = Tk.Tk()
    f1 = Tk.Frame(root)
    f2 = Tk.Frame(root)
    root.wm_title('Corona Update')
    root.resizable(width=False, height=False)
    FONT = ('Arial', 20)
    FONT2 = ('Arial', 16)
    date = '/'.join(results['Date'].split('-')[::-1])
    color = what_color(results['colour'])
    Tk.Label(f2, text=":עיר", font=FONT).grid(row=0)
    Tk.Label(f1, text=f"{results['City_Name']}", font=FONT).grid(row=0)
    Tk.Label(f2, text=":צבע העיר", font=FONT).grid(row=1)
    Tk.Label(f1, text=f"{results['colour']}", font=FONT, fg=color).grid(row=1)
    Tk.Label(f2, text=":מספר החולה האחרון", font=FONT).grid(row=2)
    Tk.Label(f1, text=f"{results['_id']}", font=FONT).grid(row=2)
    Tk.Label(f2, text=":תאריך המקרה", font=FONT).grid(row=3)
    Tk.Label(f1, text=f"{date}", font=FONT).grid(row=3)
    Tk.Label(f2, text=":*חולים", font=FONT).grid(row=4)
    Tk.Label(f1, text=f"{results['Cumulative_verified_cases']}", font=FONT).grid(row=4)
    Tk.Label(f2, text=":*מחלימים", font=FONT).grid(row=5)
    Tk.Label(f1, text=f"{results['Cumulated_recovered']}", font=FONT).grid(row=5)
    Tk.Label(f2, text=":*מתים", font=FONT).grid(row=6)
    Tk.Label(f1, text=f"{results['Cumulated_deaths']}", font=FONT).grid(row=6)
    Tk.Label(f2, text=":*בדיקות", font=FONT).grid(row=7)
    Tk.Label(f1, text=f"{results['Cumulated_number_of_tests']}", font=FONT).grid(row=7)
    Tk.Label(f2, text=":תזמון עדכון יומי", font=FONT).grid(row=8)
    f3 = Tk.Frame(f1, height='42')
    hourstr = Tk.StringVar(root, '00')
    minstr = Tk.StringVar(root, '00')
    secstr = Tk.StringVar(root, '00')
    Tk.Spinbox(f3, from_=00, to=23, wrap=True, textvariable=hourstr, width=3, state="readonly").place(in_=f3, anchor="c", relx=.2, rely=.5)
    Tk.Label(f3, text=':', font=FONT2).place(in_=f3, anchor="c", relx=.35, rely=.5)
    Tk.Spinbox(f3, from_=00, to=59, wrap=True, textvariable=minstr, width=3, state="readonly").place(in_=f3, anchor="c", relx=.5, rely=.5)
    Tk.Label(f3, text=':', font=FONT2).place(in_=f3, anchor="c", relx=.65, rely=.5)
    Tk.Spinbox(f3, from_=00, to=59, wrap=True, textvariable=secstr, width=3, state="readonly").place(in_=f3, anchor="c", relx=.8, rely=.5)
    f3.grid(row=8, sticky="nsew")
    Tk.Button(f1, text="תזמן", command=lambda: schedule(hourstr.get(), minstr.get(), secstr.get())).grid(row=10)
    f4 = Tk.Frame(f2, height='50')
    Tk.Label(f4, text="חישוב מצטבר *").pack(side="right")
    Tk.Label(f4, font=FONT2).pack()
    f4.grid(row=9, sticky="nsew")
    f1.grid(row=0, column=0)
    f2.grid(row=0, column=1)
    Tk.mainloop()


def schedule(hours, minutes, seconds):
    schedule_time = ''
    if int(hours) < 10:
        schedule_time += f'0{hours}:'
    else:
        schedule_time += f'{hours}:'
    if int(minutes) < 10:
        schedule_time += f'0{minutes}:'
    else:
        schedule_time += f'{minutes}:'
    if int(seconds) < 10:
        schedule_time += f'0{seconds}'
    else:
        schedule_time += f'{seconds}'
    file_path = str(os.path.abspath(__file__))[:-2]+'exe'
    os.system(f'SchTasks /Create /SC DAILY /TN "corona" /TR "{file_path}" /ST {schedule_time}')


def what_color(color):
    try:
        colors = {"ירוק": "green", "אדום": "red", "כתום": "orange", "צהוב": "yellow"}
        label_color = colors[color]
    except:
        label_color = "black"
    return label_color


if __name__ == "__main__":
    main()
