#!/usr/bin/env python3

from helium import *
from selenium.webdriver.chrome.options import Options
import argparse
import os
import time

timesheets = {
        "customer_id": "",
        "login": "",
        "password": "",
        "url": "https://www.timesheets.com.au/TPLogin/Default.asp"
        }

fieldglass = {
        "login": "",
        "password": "",
        "url": "https://www.fieldglass.net/"
        }

def show_splash_screen():
    ascii_art = r"""
___________.__                           .__                  __   
\__    ___/|__|  _____    ____     ______|  |__    /\|\/\   _/  |_ 
  |    |   |  | /     \ _/ __ \   /  ___/|  |  \  _)    (__ \   __\
  |    |   |  ||  Y Y  \\  ___/   \___ \ |   Y  \ \_     _/  |  |  
  |____|   |__||__|_|  / \___  > /____  >|___|  /   )    \   |__|  
                     \/      \/       \/      \/    \/\|\/         
                 __                            __                  
_____    __ __ _/  |_  ____    _____  _____  _/  |_  ____ _______  
\__  \  |  |  \\   __\/  _ \  /     \ \__  \ \   __\/  _ \\_  __ \ 
 / __ \_|  |  / |  | (  <_> )|  Y Y  \ / __ \_|  | (  <_> )|  | \/ 
(____  /|____/  |__|  \____/ |__|_|  /(____  /|__|  \____/ |__|    
     \/  
    """
    print(ascii_art)

def start_chrome_with_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Update this path if necessary

    start_chrome(options=chrome_options)

def run_timesheets():
    start_chrome_with_options()
    go_to(timesheets['url'])
    wait_until(Button('LOGON').exists)
    write(timesheets['customer_id'], into='Customer ID')
    write(timesheets['login'], into='Logon ID')
    write(timesheets['password'], into='Password')
    click('LOGON')

    wait_until(S('.week-addedit').exists)
    click(S('.week-addedit'))

    wait_until(S('#Project_0_0_chosen').exists)
    click(S('#Project_0_0_chosen'))
    write('O-GFRLINF1-025')  # Project code
    press(ENTER)
    click(S('#FinishTime_0_0'))
    for i in range(5):
        write('8')
        press(TAB)
    click('Save')

    wait_until(Image(alt='Click here to Confirm your Timesheet once it is Complete.').exists)
    click(Image(alt='Click here to Confirm your Timesheet once it is Complete.'))
    time.sleep(1)
    alert = get_driver().switch_to.alert
    alert.accept()

    time.sleep(8)
    kill_browser()


def run_fieldglass():
    start_chrome_with_options()
    go_to(fieldglass['url'])

    wait_until(Button('Sign In').exists)
    write(fieldglass['login'], into='Username')
    write(fieldglass['password'], into='Password')
    click('Sign In')

    wait_until(S('#viewMenu_3_timeAndExpense_header_link').exists)
    click('Complete time sheet')

    wait_until(Button('Submit').exists)
    for i in range(5):
        write('8')
        press(TAB)

    for i in range(2):
        wait_until(Button('Submit').exists)
        click(Button('Submit'))

    wait_until(S('#update').exists)
    click(S('#update'))

    time.sleep(8)
    kill_browser()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse command-line arguments.")
    
    parser.add_argument('-t', '--timesheet', action='store_true', help='Process timesheet')
    parser.add_argument('-f', '--fieldglass', action='store_true', help='Process fieldglass')
    
    args = parser.parse_args()
    
    return args


def populate_secrets_from_env():
    timesheets['customer_id'] = os.getenv('TIMESHEETS_CUSTOMER_ID')
    timesheets['login'] = os.getenv('TIMESHEETS_LOGIN')
    timesheets['password'] = os.getenv('TIMESHEETS_PASSWORD')
    fieldglass['login'] = os.getenv('FIELDGLASS_LOGIN')
    fieldglass['password'] = os.getenv('FIELDGLASS_PASSWORD')
    print("Secrets populated from environment variables:")
    print("Timesheets customer ID: " + timesheets['customer_id'])
    print("Timesheets login: " + timesheets['login'])
    print("Fieldglass login: " + fieldglass['login'])
    


if __name__ == "__main__":
    show_splash_screen()
    args = parse_arguments()
    populate_secrets_from_env()
    
    if args.timesheet:
        print("Timesheet processing selected.")
        run_timesheets()
    if args.fieldglass:
        print("Fieldglass processing selected.")
        run_fieldglass()
