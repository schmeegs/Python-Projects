import argparse, sys
import tkinter as tk
from tkinter import messagebox
import time
import os
import shutil
from datetime import date
import pandas as pd

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

            #main timer ends, starting secondary timer below
        c_timer[2] += 1

        if (c_timer[2] >= 60):
            c_timer[1] += 1
            c_timer[2] = 0

        elif (c_timer[1] >= 60):
            c_timer[0] += 1
            c_timer[1] = 0

        timeString = pattern.format(timer[0], timer[1], timer[2]) #main
        c_timeString = secondary_pattern.format(c_timer[0], c_timer[1], c_timer[2]) #current session

        # Update the timeText Label box with the current time
        timeText.configure(text=timeString) #main
        timeText2.configure(text=c_timeString) #current session

    # Call the update_timeText() function after 1 second
    root.after(1000, update_timeText)

def is_first_use():
    """If its users first time using program then hide current time since curr time will == total time"""
    filesize3 = os.path.getsize("time_files/total_time_list_raw.txt")
    if filesize3 >= 1:
        session_text.pack(fill='x') #pack button on start for session text
        timeText2.pack(fill='x') #the actual session timer pack to screen on start
    else:
        pass

def start():
    global state, start_time

    if todays_task.get() == "What are you doing today? Replace all this text with todays task":
        tk.messagebox.showinfo(title='Enter Todays task', message='Pleae enter the task you will be doing in the text box before starting the timer')
        return
    else:
        start_time = time.time() #When start button pressed get start time

        session_task = todays_task.get() #get what task working on before hiding it
        todays_task.pack_forget() #Hides text box on start
        start_button.pack_forget() #Hide button on start
        reset_data_button.pack_forget() #Hide button on start
        export_excel_button.pack_forget()
        pause_button.config(state="normal") #Enable pause button on start button press

        is_first_use() #check to see if it should pack current session time after > 1 uses

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
            f.close() #might not need this close
            return most_recent_task
        except IndexError:
            return  first_task
        else:
            return first_task

def initialize():
    global state, timer, pattern, secondary_pattern, c_timer
    state = False

    timer = read_in_time() #for main timer
    timestr = 'Welcome Back ;)'

    c_timer = [0,0,0] #start current timer
    session_timestr = 'Current session elapsed time will go here'

    timeText.configure(text=timestr) #For main timer
    timeText2.configure(text=session_timestr) #For session timer

def quitclock():
    try:
        if (pause.counter % 2) != 0:
            pause() #if user pauses then quits without unpausing, execute
            #pause function to get the pause difference time to be accounted for
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

def save_time_to_txt(sec): #this is the last function to get executed
    file_object = open("time_files/time_logger_descriptive.txt", 'a')

    today = date.today() #getting todays day
    d1 = today.strftime("%d/%m/%Y") #formating todays date into d/m/y

    the_task = start() #Grabs the session task from start function, could be improved?

    u_time = sec #saves unformatted time
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60 #Converting to formatted time
    mins = mins % 60
    f_time = f"{int(hours)} Hours {int(mins)} Minutes {round(sec)} Seconds"

    file_object.write(f"\nLast time on {d1} you spent {f_time} on {the_task}") #write date to new line and also time spent formatted
    file_object.close() #close first file at end

    file_object = open("time_files/total_time_list_raw.txt", 'a')
    file_object.write(f"{round(u_time)}\n") #This is for total time save
    file_object.close()

    f = open("time_files/excel_logger.txt", 'a') #logging excel time format
    f.write(f"{d1},{int(hours)},{int(mins)},{round(sec)},{f_time},{round(u_time)},{the_task}\n")
    f.close()

def save_to_excel():
    today = date.today() #Creating backups of data then clearing original
    d2 = today.strftime("-" + "%d" + "-" + "%m" + "-" + "%Y") #formating todays date into d/m/y
    df = pd.read_csv('time_files/excel_logger.txt', sep=',')
    df.to_excel(f'excel_exports/excel_export{d2}.xlsx', index=False)
    tk.messagebox.showinfo('Success','All previous sessions exported to excel successfully in the /excel_exports folder')

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
          shutil.copyfile('time_files\\excel_logger.txt',f'backups\\excel_logger_backup{d2}.txt')

          file1 = open("time_files\\time_logger_descriptive.txt","r+")
          file1.truncate(0)
          file1.close()
          file2 = open("time_files\\total_time_list_raw.txt","r+")
          file2.truncate(0)
          file2.close()
          file3 = open("time_files\\excel_logger.txt","w+")
          file3.write("Date,Hours,Minutes,Seconds,Session Time (formatted),Total session time (seconds),That Days Task\n")
          file3.close()
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
        export_excel_button.pack_forget()
    else:
        pass

if __name__=='__main__':
    timestr = '' #for main total time loop
    session_timestr = '' #for current session time loop
    start_time = '' #Gets replaced with start time of program when start button pressed
    initial_pause_time = 0
    total_paused_time = 0
    pause.counter = 0

    parser = argparse.ArgumentParser(description='Time to mastery')
    parser.add_argument('--name', '-n', help='no help',
            default='MA$TERY CLOCK v2')
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
    secondary_pattern = '{0:02d}:{1:02d}:{2:02d}' #for the current session time

    root = tk.Tk()
    root.wm_title(window_title)
    root.iconphoto(False, tk.PhotoImage(file='icon/icon.jpg'))

    intro_text = tk.Label( root,
            text = "Total Time Spent:", font = ("Halvetica",11),
            background = 'black', foreground = 'green')
    intro_text.pack(fill='x',side='top')

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
    todays_task.insert(10, "What are you doing today? Replace all this text with todays task")
    todays_task.pack(fill='x')

    start_button = tk.Button(root, text='Start', command=start)
    start_button.pack(fill='x')

    pause_button = tk.Button(root, text='Pause/Unpause', command=pause, state='disabled')
    pause_button.pack(fill='x') #Starts pause button in disabled state

    reset_data_button =  tk.Button(root, text='Reset All Data', command=ResetData)
    reset_data_button.pack(fill='x')

    export_excel_button =  tk.Button(root, text='Export to Excel', command=save_to_excel)
    export_excel_button.pack(fill='x')

    session_text = tk.Label( root, #Add current session time text, only pack when start
            text = 'Current Session Time:', font = ("Halvetica",11),
            background = 'black', foreground = 'green')

    #Adding in current session time field underneith
    timeText2 = tk.Label( root,
            text = session_timestr, font = ("Halvetica",11),
            background = 'black', foreground = 'green')

    ###Quit button commented out below as it's not needed, pressing X achieves same effect
    #other_buttons = [  ('Quit', quitclock) ] #If I want to list off more buttons
    #for btn in other_buttons:
        #tk.Button(root, text = btn[0], command=btn[1]).pack(fill='x')

    #if user clicks X still save data as if quit was clicked
    root.protocol('WM_DELETE_WINDOW', quitclock)

    #open_obs() #Attempts to open OBS on program start
    check_if_reset()
    initialize()
    update_timeText()
    root.mainloop()
