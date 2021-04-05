import argparse, sys
import tkinter as tk
from tkinter import messagebox
import time
import os
import shutil
from datetime import date

def update_timeText():
    global timer, window_title

    if state:
            # Every time this function is called, increment 1 second
        timer[2] += 1

        if (timer[2] >= 60):
            timer[1] += 1
            timer[2] = 0

        elif (timer[1] >= 60):
            timer[0] += 1
            timer[1] = 0

        timeString = pattern.format(timer[0], timer[1], timer[2])

        # Update the timeText Label box with the current time
        timeText.configure(text=timeString)

    # Call the update_timeText() function after 1 second
    root.after(1000, update_timeText)

def start():
    global state, start_time

    if todays_task.get() == "Replace this text with todays task":
        tk.messagebox.showinfo(title='Enter Todays task', message='Pleae enter the task you will be doing in the text box before starting the timer')
        return
    else:
        start_time = time.time() #When start button pressed get start time

        session_task = todays_task.get() #get what task working on before hiding it
        todays_task.pack_forget() #Hides text box on start
        start_button.pack_forget() #Hide button on start
        reset_data_button.pack_forget() #Hide button on start

        state = True
        return session_task #Gives session task string to be saved

def pause():
    global state, total_paused_time, initial_pause_time
    pause.counter += 1 #counts how many times pause function has been called
    if (pause.counter % 2) != 0: #if number of times pause called is odd this means its paused
        initial_pause_time = time.time() #update global with new curr pause time
        state = False

    else: #It will be unpaused in this state
        end_pause_time = time.time()
        diff = end_pause_time - initial_pause_time
        total_paused_time += diff #add to total paused time global
        state = True

def read_in_time(): #Returns the total time value in seconds from file
    with open("time_files/total_time_list_raw.txt") as f:
        total_t = 0
        for line in f:
            total_t += int(line) #totals the individual time lines in the file

        mins = total_t // 60
        total_t = total_t % 60
        hours = mins // 60
        mins = mins % 60
        return ([int(hours),int(mins),round(total_t)])

def read_in_last_task():
    with open("time_files/time_logger_descriptive.txt") as f:
        lines = f.readlines()
        first_task = ("Last task duration and description will"
        " show up here after your first session")
        try: #Try Clause handling the exception if the file is empty
            most_recent_task = lines[-1]
            f.close()
            return most_recent_task
        except IndexError:
            return  first_task
        else:
            return first_task

def initialize():
    global state, timer, pattern
    state = False

    timer = read_in_time()
    timestr = 'Welcome Back ;)'

    timeText.configure(text=timestr)

def quitclock():
    try:
        get_end_session_time(start_time, total_paused_time)
    except TypeError:
        root.destroy()
    else:
        root.destroy()

def gt_zero(s):
    try:
        if int(s) > 0:
            return int(s)
        else:
            raise argparse.ArgumentTypeError('Time limit must be an int > 0')
    except:
        raise argparse.ArgumentTypeError('Time limit must be an int > 0')

def save_time_to_txt(sec):
    file_object = open("time_files/time_logger_descriptive.txt", 'a')

    today = date.today() #getting todays day
    d1 = today.strftime("%d/%m/%Y") #formating todays date into d/m/y
    the_task = start()

    u_time = sec #saves unformatted time
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60 #Converting to formatted time
    mins = mins % 60
    f_time = f"{int(hours)} Hours {int(mins)} Minutes {round(sec)} Seconds"

    file_object.write(f"\nLast time on {d1} I spent {f_time} on {the_task}") #write date to new line and also time spent formatted
    file_object.close() #close first file at end

    file_object = open("time_files/total_time_list_raw.txt", 'a')
    file_object.write(f"{round(u_time)}\n") #This is for total time save
    file_object.close()

def get_end_session_time(starting_time, paused_time=0):
    #need to run this at the end of the program (on exit button /quit clock)
    end_time = time.time()
    time_lapsed = end_time - (starting_time + paused_time) #considers paused time
    save_time_to_txt(time_lapsed)

def open_obs():
    """Unused in GIT version Starts OBS if you have a link file to your obs called obs.lnk in root"""
    try:
        os.startfile("obs.lnk") #Just for me
    except:
        pass

def ResetData():
    MsgBox = tk.messagebox.askquestion ('Reset data','Are you sure you want to reset all historical data, backups will be created in /backups folder',icon = 'warning')
    if MsgBox == 'yes':
          today = date.today() #Creating backups of data then clearing original
          d2 = today.strftime("-" + "%d" + "-" + "%m" + "-" + "%Y") #formating todays date into d/m/y
          shutil.copyfile('time_files\\time_logger_descriptive.txt',f'backups\\time_logger_descriptive_backup{d2}.txt')
          shutil.copyfile('time_files\\total_time_list_raw.txt',f'backups\\total_time_list_raw_backup{d2}.txt')
          file1 = open("time_files\\time_logger_descriptive.txt","r+")
          file1.truncate(0)
          file1.close()
          file2 = open("time_files\\total_time_list_raw.txt","r+")
          file2.truncate(0)
          file2.close()
          tk.messagebox.showinfo('Success','Data overwritten and backups created, the program will now quit, the program will close now to take effect')
          root.destroy()
    else:
        tk.messagebox.showinfo('Nada','Nothing has been deleted ;)')

def check_if_reset():
    """If both of the files are empty, hide the reset button"""
    filesize1 = os.path.getsize("time_files/time_logger_descriptive.txt")
    filesize2 = os.path.getsize("time_files/total_time_list_raw.txt")
    if filesize1 == 0 and filesize2 == 0:
        reset_data_button.pack_forget()
    else:
        pass

if __name__=='__main__':
    timestr = ''
    start_time = '' #Gets replaced with start time of program when start button pressed
    initial_pause_time = 0
    total_paused_time = 0
    pause.counter = 0

    parser = argparse.ArgumentParser(description='Time to mastery')
    parser.add_argument('--name', '-n', help='no help',
            default='MA$TERY CLOCK')
    parser.add_argument('--reverse', '-r', type = gt_zero,
            help='No Reverse feature')
    parser.add_argument('--size', '-s',
            help='Font size for the timer', default='48')
    values = parser.parse_args()
    window_title = values.name
    font_size = values.size

    # Simple status flag; False => timer is not running, True otherwise
    state = False
    # For the padding format
    pattern = '{0:04d}:{1:02d}:{2:02d}'

    root = tk.Tk()
    root.wm_title(window_title)
    root.iconphoto(False, tk.PhotoImage(file='icon/icon.jpg'))

    # Create a timeText Label (a text box)
    timeText = tk.Label( root,
            text = timestr, font = ("Halvetica",font_size),
            background = 'black', foreground = 'green')
    timeText.pack(fill='x')

    #Adding last session text from file
    last_session_text = tk.Label( root,
            text = read_in_last_task(), font = ("Halvetica",11),
            background = 'black', foreground = 'green')
    last_session_text.pack(fill='x')

    #Adding in text entry field
    todays_task = tk.Entry(root, justify='center', font="Halvetica 10 bold", fg='red', bg='white')
    todays_task.insert(10, "Replace this text with todays task")
    todays_task.pack(fill='x')

    start_button = tk.Button(root, text='Start', command=start)
    start_button.pack(fill='x')

    other_buttons = [  ('Pause/Unpause', pause),
            ('Quit', quitclock) ]
    for btn in other_buttons:
        tk.Button(root, text = btn[0], command=btn[1]).pack(fill='x')

    reset_data_button =  tk.Button(root, text='Reset All Data', command=ResetData)
    reset_data_button.pack(fill='x')

    root.protocol('WM_DELETE_WINDOW', quitclock)
    #if user clicks X still save data as if quit was clicked

    #open_obs() #Attempts to open OBS on program start
    check_if_reset()
    initialize()
    update_timeText()
    root.mainloop()
