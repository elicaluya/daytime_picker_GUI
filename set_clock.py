__author__ = 'Caluya'

# From http://www.ferg.org/thinking_in_tkinter/tt070_py.txt
# Adapted by A. Hornof 2017
# Based off of starter sample code by Anthony Hornof

from tkinter import *
import sound
import wave
import time

# Added functions so that the concatenated files will be able to play
# Copied from stackoverflow post
# https://stackoverflow.com/questions/46538867/attributeerror-wave-write-instance-has-no-attribute-exit
def _trivial__enter__(self):
    return self
def _self_close__exit__(self, exc_type, exc_value, traceback):
    self.close()

wave.Wave_read.__exit__ = wave.Wave_write.__exit__ = _self_close__exit__
wave.Wave_read.__enter__ = wave.Wave_write.__enter__ = _trivial__enter__

# Global strings for navigating through sound files
nav_path = "wav_files_provided/miscellaneous_f/"
num_path = "wav_files_provided/numbers_f/"
days_path = "wav_files_provided/days_of_week_f/"
my_sounds_path = "my_sounds/"
YOU_SELECTED = nav_path + "you_selected_f.wav"
EXIT_TIME = 5           # enough time to say final time

class MyApp:
    def __init__(self, parent):
        self.myParent = parent
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()
        self.myParent.bind("<j>", self.keyPress)  # ajh
        self.myParent.bind("<k>", self.keyPress)  # ajh
        self.myParent.bind("<space>", self.okButtonClick)
        
        # Index to move through the states to change settings
        self.state_index = 0
        # Int to indicate if the user is editing a field
        self.edit_state = 0
        
        # Limits and lists for looping through days, hours, and minutes
        # Also base indexes for days, hours, and minutes
        self.days_list = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
        self.current_day = 0
        self.day_limit = 7
        self.current_hour = 0
        self.hour_limit = 24
        self.current_min = 0
        self.min_limit = 60
        self.temp_sound = "temp.wav"
        self.time_sound = "hour.wav"
        
        # Variables that are chosen by the user
        # initialized to the basic settings
        self.day_selection = self.days_list[self.current_day]
        self.hour_selection = "12"
        self.min_selection = "0"+str(self.current_min)
        self.ampm_selection = "AM"
  
        # Create the settings buttons to change day, hour, or minute
        # Start with Set Day first selected
        self.dayButton = Button(self.myContainer1)
        self.dayButton.configure(text="Set Day", background = "light blue")
        self.dayButton.grid(row = 0,column = 0)
        self.hourButton = Button(self.myContainer1)
        self.hourButton.configure(text="Set Hour", background="yellow")
        self.hourButton.grid(row=0, column=1)
        self.minButton = Button(self.myContainer1)
        self.minButton.configure(text="Set Minutes", background="yellow")
        self.minButton.grid(row=0, column=2)
        
        # Button for finishing program when the user wants to confirm the final time
        self.finishButton = Button(self.myContainer1)
        self.finishButton.configure(text= "FINISH",background = "orange")
        self.finishButton.grid(row=0,column=3)
        
        # Labels for edit menu
        self.current_label = Label(self.myContainer1)
        self.current_label.configure(text= "Current: ")
        self.k_button = Button(self.myContainer1)
        self.k_button.configure(text ="UP")
        self.k_button.bind("<Button-1>",self.k_edit)
        self.j_button = Button(self.myContainer1)
        self.j_button.configure(text ="DOWN")
        self.j_button.bind("<Button-1>",self.j_edit)
        
        # labels that show the current selection and preceding and succeeding selections
        self.selection = Label(self.myContainer1)
        self.selection.configure(text = "current", font = 15)
        self.k_index = Label(self.myContainer1)
        self.k_index.configure(text = "k")
        self.j_index = Label(self.myContainer1)
        self.j_index.configure(text = "j")
        
        # OK button that will confirm actions like changing a setting or finishing th program
        self.okButton = Button(self.myContainer1)
        # The background colors appear in Windows but not on a Macintosh.
        self.okButton.configure(text="OK", background= "green")
        self.okButton.grid(row = 4, column = 0)
        self.okButton.focus_force()         ### (0)
        self.okButton.bind("<Button-1>", self.okButtonClick)
        
        # Cancel Button binded to cancel function for closing program
        self.cancel = Button(self.myContainer1)
        self.cancel.configure(text="Cancel", background="red")
        self.cancel.grid(row = 4, column = 2)
        self.cancel.bind("<Button-1>",self.cancelClick)
        

    # Move from main state into edit state
    def okButtonClick(self, event):
        if (self.edit_state == 0):                  # Relay to user of the setting they chose before going opening edit menu
            self.edit_state = 1
            if (self.state_index == 0):
                self.changeToEdit(self.edit_state,0)
                sound.combine_wav_files(self.temp_sound,YOU_SELECTED,nav_path + "Set_day_of_week_f.wav")
                sound.Play(self.temp_sound)
            elif (self.state_index == 1):
                self.changeToEdit(self.edit_state,1)
                sound.combine_wav_files(self.temp_sound, YOU_SELECTED, nav_path + "Set_hour_f.wav")
                sound.Play(self.temp_sound)
            elif (self.state_index == 2):
                self.changeToEdit(self.edit_state,2)
                sound.combine_wav_files(self.temp_sound, YOU_SELECTED, nav_path + "Set_minutes_f.wav")
                sound.Play(self.temp_sound)
            elif (self.state_index == 3):                   # User is done and wants to confirm their final time
                # checking if minute is zero so o_clock.wav is played
                if (self.current_min == 0):
                    sound.combine_wav_files(self.temp_sound, my_sounds_path + "final_time.wav",
                                            days_path + self.day_selection + "_f.wav",
                                            num_path + self.hour_selection + "_f.wav",
                                            nav_path+"o_clock_f.wav",
                                            nav_path + self.ampm_selection + "_f.wav")
                    sound.Play(self.temp_sound)
                    time.sleep(EXIT_TIME)                   # Sleep so program has enough time to say final time
                    self.myParent.destroy()                 # before closing
                # checking if single digit minute so that oh.wav is played before minute
                elif (self.current_min < 10 and self.current_min > 0):
                    sound.combine_wav_files(self.temp_sound,my_sounds_path + "final_time.wav",
                                        days_path+self.day_selection+"_f.wav",
                                        num_path+self.hour_selection+"_f.wav",
                                        num_path+"oh_f.wav",num_path+self.min_selection+"_f.wav",
                                        nav_path+self.ampm_selection+"_f.wav")
                    sound.Play(self.temp_sound)
                    time.sleep(EXIT_TIME)
                    self.myParent.destroy()
                # Any other minute will be played without any extra wav files
                elif (self.current_min >= 10):
                    sound.combine_wav_files(self.temp_sound, my_sounds_path + "final_time.wav",
                                            days_path + self.day_selection + "_f.wav",
                                            num_path + self.hour_selection + "_f.wav",
                                            num_path + self.min_selection + "_f.wav",
                                            nav_path + self.ampm_selection + "_f.wav")
                    sound.Play(self.temp_sound)
                    time.sleep(EXIT_TIME)
                    self.myParent.destroy()
                
        elif (self.edit_state == 1):            # When confirming an edit
            if (self.state_index == 0):         # Confirming an edit of the day
                self.day_selection = self.days_list[self.current_day]
                sound.combine_wav_files(self.temp_sound,YOU_SELECTED,
                            days_path+ self.days_list[self.current_day] + "_f.wav")
                sound.Play(self.temp_sound)
            elif(self.state_index == 1):        # Confirming edit of hour
                sound.combine_wav_files(self.temp_sound,YOU_SELECTED,
                                        num_path+self.hour_selection+"_f.wav",
                                        nav_path+self.ampm_selection+"_f.wav")
                sound.Play(self.temp_sound)
            elif (self.state_index == 2):       # Confirming edit of minute
                sound.combine_wav_files(self.temp_sound,YOU_SELECTED,
                                        num_path+self.min_selection+"_f.wav")
                sound.Play(self.temp_sound)
            
            self.edit_state = 0
            self.changeToEdit(self.edit_state,self.state_index)     # Change back to main menu state
            
    # Close the app
    def cancelClick(self, event):
        self.myParent.destroy()
        
    # Checks the current state index and changes the color to act as indicator
    def changeState(self, state):
        if (state == 0):
            self.dayButton["background"] = "light blue"    # Light blue means currently selected
            self.minButton["background"] = "yellow"         # yellow means not selected
            self.hourButton["background"] = "yellow"
            self.finishButton["background"] = "orange"       # FINISH button is orange because it is special
            say_state = nav_path + "Set_day_f.wav"      # Announce current state
            sound.Play(say_state)
        elif (state == 1):
            self.hourButton["background"] = "light blue"
            self.dayButton["background"] = "yellow"
            self.minButton["background"] = "yellow"
            self.finishButton["background"] = "orange"
            say_state = nav_path + "Set_hour_f.wav"
            sound.Play(say_state)
        elif (state == 2):
            self.minButton["background"] = "light blue"
            self.hourButton["background"] = "yellow"
            self.dayButton["background"] = "yellow"
            self.finishButton["background"] = "orange"
            say_state = nav_path + "Set_minutes_f.wav"
            sound.Play(say_state)
        elif (state == 3):
            self.minButton["background"] = "yellow"
            self.hourButton["background"] = "yellow"
            self.dayButton["background"] = "yellow"
            self.finishButton["background"] = "light blue"
            say_state = my_sounds_path + "finish.wav"
            sound.Play(say_state)
            
    # Make the edit fields appear and disappear depending if the user wants to edit or not
    def changeToEdit(self,edit,state):
        # Make edit menu appear by putting them into the grid
        if (edit == 1):
            self.k_button.grid(row=1, column=1)
            self.k_index.grid(row=1, column =2)
            self.current_label.grid(row=2, column=1)
            self.selection.grid(row = 2, column =2)
            self.j_button.grid(row=3, column=1)
            self.j_index.grid(row=3, column=2)
            self.setEditMenu(state)
            
        # Make edit menu disappear by removing all elements from the grid
        else:
            self.k_button.grid_remove()
            self.k_index.grid_remove()
            self.current_label.grid_remove()
            self.selection.grid_remove()
            self.j_button.grid_remove()
            self.j_index.grid_remove()
         
    # Function to change the values in the edit menu according to the user's current selection
    def setEditMenu(self, state):
        k = 0           # Indexes for the entries
        j = 0           # in the k and j labels
        if (state == 0):            # change day
            k = self.current_day + 1
            j = self.current_day -1
            if (k == self.day_limit):
                k = 0
            if (j == -1):
                j = 6
            # Display change in current index/ selection
            self.k_index.configure(text=self.days_list[k])
            self.selection.configure(text=self.days_list[self.current_day])
            self.j_index.configure(text = self.days_list[j])
        elif (state == 1):              # change the hour
            k = self.current_hour + 1
            j = self.current_hour - 1
            self.setHour(self.current_hour,k,j)
        elif (state == 2):              # change the minute
            k = self.current_min + 1
            j = self.current_min -1
            self.setMin(self.current_min,k,j)
            
    # Function that responds to k button presses in which the user wants to go up the list
    # Moves through days, hours, and minutes according to the state_index
    def k_edit(self, event):
        select = 0      # values that represent the labels
        k = 0           # in which the user's index will correspond to
        j = 0
        # When the user wants to edit the day
        if (self.state_index == 0):
            select = self.current_day + 1
            k = select + 1
            j = select - 1
            if (select == self.day_limit):
                select = 0
                k = 1
            if (k == self.day_limit):
                k = 0
            if (j == -1):
                j = 6
            
            # Chnage text in labels according to current index
            self.selection["text"] = self.days_list[select]
            self.k_index["text"] = self.days_list[k]
            self.j_index["text"] = self.days_list[j]
            sound.Play(days_path + self.days_list[select] + "_f.wav")   # Announce current day
            self.current_day = select
        
        # Editing the hour
        elif (self.state_index == 1):
            select = self.current_hour + 1
            k = select + 1
            j = select - 1
            self.setHour(select,k,j)      # Call function to set Hour labels for us
        
        # Editing the minutes
        elif (self.state_index == 2):
            select = self.current_min + 1
            k = select + 1
            j = select - 1
            self.setMin(select,k,j)     # Call function to set minute labels for us
            
        # Update GUI to changes made in labels
        self.selection.update_idletasks()
        self.k_index.update_idletasks()
        self.j_index.update_idletasks()

    # Function that responds to j button presses in which the user wants to go down the list
    # Moves through days, hours, and minutes according to the state_index
    def j_edit(self,event):
        select = 0
        k = 0
        j = 0
        if (self.state_index == 0):
            select = self.current_day - 1
            k = select + 1
            j = select - 1
            if (select == -1):
                select = 6
            if (k == self.day_limit):
                k = 0
            if (j == -1):
                j = 6
            self.selection["text"] = self.days_list[select]
            self.k_index["text"] = self.days_list[k]
            self.j_index["text"] = self.days_list[j]
            sound.Play(days_path + self.days_list[select] + "_f.wav")
            self.current_day = select

        elif (self.state_index == 1):
            select = self.current_hour - 1
            k = select + 1
            j = select - 1
            self.setHour(select, k, j)
        
        elif (self.state_index == 2):
            select = self.current_min - 1
            k = select + 1
            j = select - 1
            self.setMin(select,k,j)
        
        # Update display of gui to changes made in labels
        self.selection.update_idletasks()
        self.k_index.update_idletasks()
        self.j_index.update_idletasks()
        
    # Function for displaying the correct hour in the current label as well as the up and down labels
    # Need to pay attention to hour index because of AM/PM
    # (Very "hacky" code but I was in a rush to complete project)
    def setHour(self,select,k,j):
        # Set base cases for when the index goes over or below the limit
        if (select == -1):
            select = 23
            j = 22
            k = 0
        elif (select == self.hour_limit):
            select = 0
            k = 1
            j = 23
        if (k == self.hour_limit):
            k = 0
        if (j == -1):
            j = 23
        self.current_hour = select      # Set the current hour to the new index
        
        # Need to check if single digit because wav file requires "0" infornt of number
        # Also need index above 12 to correspond to PM and below 12 to AM
        if (select == 0):                  # 0 corresponds to 12 AM
            self.selection["text"] = "12 AM"
            sound.combine_wav_files(self.time_sound, num_path + "12_f.wav", nav_path + "AM_f.wav")
            sound.Play(self.time_sound)
            self.hour_selection = "12"              # set final hour_selection to selected hour
            self.ampm_selection = "AM"              # final AM or PM corresponds to index
        elif (select == 12):               # 12 PM
            self.selection["text"] = "12 PM"
            sound.combine_wav_files(self.time_sound, num_path + "12_f.wav", nav_path + "PM_f.wav")
            sound.Play(self.time_sound)
            self.hour_selection = "12"
            self.ampm_selection = "PM"
        elif (select > 0 and select < 10):      # Hours between 12 AM and 10 AM
            self.selection["text"] = str(select) + " AM"
            sound.combine_wav_files(self.time_sound, num_path + "0" + str(select) + "_f.wav", nav_path + "AM_f.wav")
            sound.Play(self.time_sound)
            self.hour_selection = "0" + str(select)
            self.ampm_selection = "AM"
        elif (select < 12 and select > 9):          # Hours between 10 AM and 12 PM
            self.selection["text"] = str(select) + " AM"
            sound.combine_wav_files(self.time_sound, num_path + str(select) + "_f.wav", nav_path + "AM_f.wav")
            sound.Play(self.time_sound)
            self.hour_selection = str(select)
            self.ampm_selection = "AM"
        elif (select > 12 and select < 22):         # Hours between 12 PM and 10 PM
            self.selection["text"] = str(select - 12) + " PM"
            sound.combine_wav_files(self.time_sound, num_path + "0" + str(select - 12) + "_f.wav", nav_path + "PM_f.wav")
            sound.Play(self.time_sound)
            self.hour_selection = "0"+str(select-12)
            self.ampm_selection = "PM"
        elif (select > 21):                     # Hours between 10 PM and 12 AM
            self.selection["text"] = str(select - 12) + " PM"
            sound.combine_wav_files(self.time_sound, num_path + str(select - 12) + "_f.wav", nav_path + "PM_f.wav")
            sound.Play(self.time_sound)
            self.hour_selection = str(select-12)
            self.ampm_selection = "PM"
        
        # Making sure the K and J labels correspond correctly to AM and PM
        if (k == 0):
            self.k_index["text"] = "12 AM"
        elif (k == 12):
            self.k_index["text"] = "12 PM"
        elif (k < 12):
            self.k_index["text"] = str(k) + " AM"
        elif (k > 12):
            self.k_index["text"] = str(k - 12) + " PM"
    
        if (j == 0):
            self.j_index["text"] = "12 AM"
        elif (j == 12):
            self.j_index["text"] = "12 PM"
        elif (j < 12):
            self.j_index["text"] = str(j) + " AM"
        elif (j > 12):
            self.j_index["text"] = str(j - 12) + " PM"
    
    # Similar to setHour function but for minutes and does not require checking of AM/PM
    def setMin(self,select,k,j):
        if (select == -1):
            select = 59
            j = 58
            k = 0
        elif (select == self.min_limit):
            select = 0
            k = 1
            j = 59
        if (k == self.min_limit):
            k = 0
        if (j == -1):
            j = 59
        self.current_min = select
        # Need to check if single digit because wav file require "0" in front of number
        if (select < 10):
            self.selection["text"] = str(select)
            self.k_index["text"] = str(k)
            self.j_index["text"] = str(j)
            sound.combine_wav_files(self.time_sound,num_path+"0"+str(select)+"_f.wav")
            sound.Play(self.time_sound)
            self.min_selection = "0"+str(self.current_min)      # Set final min_selection
        elif (select >= 10):
            self.selection["text"] = str(select)
            self.k_index["text"] = str(k)
            self.j_index["text"] = str(j)
            sound.combine_wav_files(self.time_sound, num_path + str(select) + "_f.wav")
            sound.Play(self.time_sound)
            self.min_selection = str(self.current_min)
    
    # read the character and increase or decrease depending if it is J or K
    def keyPress(self, event):
        if (self.edit_state == 0):
            if (event.char == "k"):             # Increase the index if the key is K
                self.state_index += 1
                if (self.state_index == 4):         # Make sure to loop if the index gets too high
                    self.state_index = 0
                self.changeState(self.state_index)
            elif (event.char == "j"):               # Decrease if key is J
                self.state_index -= 1
                if (self.state_index == -1):            # Loop through if index gets too low
                    self.state_index = 3
                self.changeState(self.state_index)
        # When the user wants to edit a field
        else:
            if (event.char == "k"):
                self.k_edit(event)
            if (event.char == "j"):
                self.j_edit(event)
       
root = Tk()
myapp = MyApp(root)
root.mainloop()