from argparse import Action
import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import timedelta  
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date
from selenium.webdriver.common.keys import Keys
import locale

input_file_url_price = pd.read_csv("Price.csv")
url_input = input_file_url_price.url
num_input =input_file_url_price.num

#check local date format
locale.setlocale(locale.LC_ALL, '')
lastdate = date(date.today().year, 12, 31)

root = Tk()
root.geometry('500x400')
root.title("NFTs - List for Sale on OpenSea  ")
input_save_lists = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
is_polygon = BooleanVar()
is_polygon.set(False)

def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )

def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud") 


def save_duration():
    duration_value.set(value=duration_value.get())
    # print(duration_value.get())

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_lists.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_lists, outfile)

###input objects###
start_num_input = InputField("Start Number: (*)", 3, 0, 2)
end_num_input = InputField("How many to list?: (*)", 4, 0, 3)
price = InputField("Price: (*)", 5, 0, 4)
title = InputField("Title:", 6, 0, 5)

###save inputs###
def save():
    input_save_lists.insert(0, upload_path)
    #start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    price.save_inputs(4)
    title.save_inputs(5)
    
  

# _____MAIN_CODE_____
def main_program_loop():
    ###START###
    project_path = main_directory
    file_path = upload_path
    start_num1 = int(start_num_input.input_field.get())
    start_num = start_num1 -1
    end_num1 = int(end_num_input.input_field.get())
    end_num = end_num1 -1
    loop_price = float(price.input_field.get())
    loop_title = title.input_field.get()
     

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    ###wait for methods
    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )
        
    def wait_css_selectorTest(code):
        wait.until(
            ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
        )    

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))


    while end_num >= start_num:
        print("Started Listing for Sale " +  loop_title +" "+ str(start_num + 1))
        driver.get(url_input[start_num]) #change1
        # time.sleep(3)
        print("Amount")
        wait_css_selector("input[placeholder='Amount']")
        amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
        amount.send_keys(str(loop_price))
        dur = driver.find_element(By.XPATH,"//*[@id='duration']/div[2]").click()
        time.sleep(1)

        #duration
        duration_date = duration_value.get()
            #print(duration_date)
            # time.sleep(60)
        if duration_date == 1 : 
            endday = (date.today() + timedelta(days=1)).day
            endmonth = (date.today() + timedelta(days=1)).month
                #print(endday, endmonth)
        if duration_date == 3 : 
            endday = (date.today() + timedelta(days=3)).day
            endmonth = (date.today() + timedelta(days=3)).month
                #print(endday, endmonth)
        if duration_date == 7 : 
            endday = (date.today() + timedelta(days=7)).day
            endmonth = (date.today() + timedelta(days=7)).month   
                #print(endday, endmonth)       
        if duration_date == 30:
            endday = (date.today() + relativedelta(months=+1)).day
            endmonth = (date.today() + relativedelta(months=+1)).month
                #print(endday, endmonth)
        if duration_date == 60:
            endday = (date.today() + relativedelta(months=+2)).day
            endmonth = (date.today() + relativedelta(months=+2)).month
                #print(endday, endmonth)
        if duration_date == 90:
            endday = (date.today() + relativedelta(months=+3)).day
            endmonth = (date.today() + relativedelta(months=+3)).month
                #print(endday, endmonth)
        if duration_date == 120:
            endday = (date.today() + relativedelta(months=+4)).day
            endmonth = (date.today() + relativedelta(months=+4)).month  
                #print(endday, endmonth) 
        if duration_date == 150:
            endday = (date.today() + relativedelta(months=+5)).day
            endmonth = (date.today() + relativedelta(months=+5)).month  
                #print(endday, endmonth)  
        if duration_date == 180:
            endday = (date.today() + relativedelta(months=+6)).day
            endmonth = (date.today() + relativedelta(months=+6)).month   
                #print(endday, endmonth)

        if duration_date != 30:
            amount.send_keys(Keys.TAB)
            time.sleep(0.8)
                # wait_xpath('//*[@id="duration"]')
                # driver.find_element_by_xpath('//*[@id="duration"]').click()
                
            wait_xpath('//*[@role="dialog"]/div[2]/div[2]/div/div[2]/input')
            select_durationday = driver.find_element_by_xpath('//*[@role="dialog"]/div[2]/div[2]/div/div[2]/input')
            driver.execute_script("arguments[0].click();", select_durationday)
            time.sleep(0.8)
                
            if lastdate.strftime('%x')[:2] == "12":
                    #print("is month first")
                select_durationday.send_keys(str(endmonth))
                select_durationday.send_keys(str(endday))
                select_durationday.send_keys(Keys.ENTER)
                time.sleep(1)
            elif lastdate.strftime('%x')[:2] == "31":
                  #print("is day first")
                select_durationday.send_keys(str(endday))
                select_durationday.send_keys(str(endmonth))
                select_durationday.send_keys(Keys.ENTER)
                time.sleep(1)
            else:
                print("invalid date format: change date format to MM/DD/YYYY or DD/MM/YYYY")

        wait_css_selector("button[type='submit']")
        listing = driver.find_element_by_css_selector("button[type='submit']")
        driver.execute_script("arguments[0].click();", listing)
        time.sleep(2)

        print("signing")
        wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 kXZare fzwDgL']")
        sign = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 kXZare fzwDgL']")
        driver.execute_script("arguments[0].click();", sign)
        time.sleep(2)

        main_page = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle

        # change the control to signin page
        driver.switch_to.window(login_page)

        if is_polygon.get():
            try:
                driver.find_element(By.XPATH, "//*[@id='app-content']/div/div[2]/div/div[3]/div[1]").click()
                time.sleep(0.7)
            except: 
                wait_xpath("//div[@class='signature-request-message__scroll-button']")
                polygonscrollsign = driver.find_element(By.XPATH, "//div[@class='signature-request-message__scroll-button']")
                driver.execute_script("arguments[0].click();", polygonscrollsign)
                time.sleep(0.7)

            try:
                wait_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]')
                driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]').click()
                time.sleep(0.7)
            except:
                wait_xpath('//button[text()="Sign"]')
                metasign = driver.find_element(By.XPATH, '//button[text()="Sign"]')
                driver.execute_script("arguments[0].click();", metasign)
                time.sleep(0.7)
        else:
            try:
                driver.find_element(By.XPATH, "//*[@id='app-content']/div/div[2]/div/div[3]/div[1]").click()
                time.sleep(0.7)
            except: 
                wait_xpath("//div[@class='signature-request-message__scroll-button']")
                scrollsign = driver.find_element(By.XPATH, "//div[@class='signature-request-message__scroll-button']")
                driver.execute_script("arguments[0].click();", scrollsign)
                time.sleep(0.7)

            try:
                wait_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]')
                driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]').click()
                time.sleep(0.7)
            except:
                wait_xpath('//button[text()="Sign"]')
                metasign = driver.find_element(By.XPATH, '//button[text()="Sign"]')
                driver.execute_script("arguments[0].click();", metasign)
                time.sleep(0.7)
       
        # change control to main page
        driver.switch_to.window(main_page)
        time.sleep(0.7)

        start_num = start_num + 1
        print('NFT Listed for Sale!')

duration_value = IntVar()
duration_value.set(value=180)

duration_date = Frame(root, padx=0, pady=1)
duration_date.grid(row=10, column=1, sticky=(N, W, E, S))
tk.Radiobutton(duration_date, text='1 day', variable=duration_value, value=1, anchor="w", command=save_duration, width=8,).grid(row=0, column=1)
tk.Radiobutton(duration_date, text="3 days", variable=duration_value, value=3, anchor="w", command=save_duration, width=8, ).grid(row=0, column=2)
tk.Radiobutton(duration_date, text="7 days", variable=duration_value, value=7, anchor="w", command=save_duration, width=8,).grid(row=0, column=3)
tk.Radiobutton(duration_date, text="30 days", variable=duration_value, value=30, anchor="w", command=save_duration, width=8,).grid(row=0, column=4)
tk.Radiobutton(duration_date, text="60 days", variable=duration_value, value=60, anchor="w", command=save_duration, width=8,).grid(row=0,  column=5)
tk.Radiobutton(duration_date, text="90 days", variable=duration_value, value=90, anchor="w",command=save_duration,  width=8,).grid(row=1, columnspan=1, column=1)
tk.Radiobutton(duration_date, text="120 days", variable=duration_value, value=120, anchor="w", command=save_duration, width=8).grid(row=1, columnspan=1, column=2)
tk.Radiobutton(duration_date, text="150 days", variable=duration_value, value=150, anchor="w", command=save_duration, width=8).grid(row=1, columnspan=1, column=3)
tk.Radiobutton(duration_date, text="180 days", variable=duration_value, value=180, anchor="w", command=save_duration, width=8).grid(row=1, columnspan=1, column=4)
duration_date.label = Label(root, text="Duration:", anchor="w", width=20, height=1 )
duration_date.label.grid(row=10, column=0, padx=12, pady=2)

#####BUTTON ZONE#######
button_save = tkinter.Button(root, width=20, text="Save Form", command=save) 
button_save.grid(row=23, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
#isPolygon = tkinter.Checkbutton(root, text='Polygon Blockchain', var=is_polygon)
#isPolygon.grid(row=20, column=0)
open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=22, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Update Price file with url")
upload_folder_input_button.grid(row=21, column=1)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        Name_change_img_folder_button(new_dict[0])
        upload_path = new_dict[0]
except FileNotFoundError:
    pass
#####BUTTON ZONE END#######
root.mainloop()
