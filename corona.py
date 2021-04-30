import json
import requests
import tkinter as Tk
from tkinter import simpledialog
from tkinter import messagebox
import os


def main():
    while True:
        try:
            application_window = Tk.Tk()
            application_window.withdraw()
            answer = simpledialog.askstring("Corona Update", "אנא הזן שם עיר:", parent=application_window)
            if answer is None:
                return None
            url = 'https://data.gov.il/api/3/action/datastore_search?' \
                  'resource_id=8a21d39d-91e3-40db-aca1-f73f7ab1df69&sort=Date desc&limit=1&filters={"City_Name":\"' + answer + '\"}'

            results = json.loads(requests.get(url).text)['result']['records'][0]
            break
        except:
            messagebox.showinfo("שגיאה", "שם עיר לא תקין")

    root = Tk.Tk()
    frame = Tk.Frame(root, width='200')
    frame.grid()
    root.wm_title('Corona Update')
    root.resizable(width=False, height=False)
    FONT = ('Arial', 20)
    FONT2 = ('Arial', 16)
    color = what_color(results['colour'])
    Tk.Label(root, text=f"עיר: {results['City_Name']}", font=FONT).grid(row=1, column=1)
    Tk.Label(root, text=f"צבע העיר: {results['colour']}", font=FONT, fg=color).grid(row=2, column=1)
    Tk.Label(root, text=f"מספר החולה האחרון: {results['_id']}", font=FONT).grid(row=3, column=1)
    Tk.Label(root, text=f"תאריך המקרה: {results['Date']}", font=FONT).grid(row=4, column=1)
    Tk.Label(root, text=f"חולים (מצטבר): {results['Cumulative_verified_cases']}", font=FONT).grid(row=5, column=1)
    Tk.Label(root, text=f"מחלימים (מצטבר): {results['Cumulated_recovered']}", font=FONT).grid(row=6, column=1)
    Tk.Label(root, text=f"מתים (מצטבר): {results['Cumulated_deaths']}", font=FONT).grid(row=7, column=1)
    Tk.Label(root, text=f"בדיקות (מצטבר): {results['Cumulated_number_of_tests']}", font=FONT).grid(row=8, column=1)
    Tk.Label(root, text="תזמון יומי:", font=FONT).grid(row=9, column=1)
    hourstr = Tk.StringVar(root, '00')
    minstr = Tk.StringVar(root, '00')
    secstr = Tk.StringVar(root, '00')
    f1 = Tk.Frame(root)
    Tk.Spinbox(f1, from_=00, to=23, wrap=True, textvariable=hourstr, width=3, state="readonly").place(in_=f1, anchor="c", relx=.2, rely=.5)
    Tk.Label(f1, text=':', font=FONT2).place(in_=f1, anchor="c", relx=.35, rely=.5)
    Tk.Spinbox(f1, from_=00, to=59, wrap=True, textvariable=minstr, width=3, state="readonly").place(in_=f1, anchor="c", relx=.5, rely=.5)
    Tk.Label(f1, text=':', font=FONT2).place(in_=f1, anchor="c", relx=.65, rely=.5)
    Tk.Spinbox(f1, from_=00, to=59, wrap=True, textvariable=secstr, width=3, state="readonly").place(in_=f1, anchor="c", relx=.8, rely=.5)
    f1.grid(row=9, column=0, sticky="nsew")
    Tk.Button(root, text="תזמן", command=lambda: do(hourstr.get(), minstr.get(), secstr.get())).grid(row=10, column=0)
    Tk.mainloop()


def do(hours, minutes, seconds):
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
