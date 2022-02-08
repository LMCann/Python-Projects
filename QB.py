from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import winsound
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from selenium.common.exceptions import WebDriverException

splitOdds=[]
viableBets=0
quickbet=True
#pass
username=input("Username: ")
password=getpass("pass: ")

#=================================================================================================
#   SETUP
#=================================================================================================

PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

frequency = 2000  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second

driver.get("https://www.betfair.com/sport/inplay")

#=================================================================================================
#   COOKIES AND LOGIN
#=================================================================================================

def login():

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        element.click()
    except:
        print("Error")
    
    username_textbox = driver.find_element_by_id("ssc-liu")
    username_textbox.send_keys(username)

    password_textbox = driver.find_element_by_id("ssc-lipw")
    password_textbox.send_keys(password)

    login_button = driver.find_element_by_id("ssc-lis")
    login_button.submit()

#=================================================================================================
#   Remove Bets
#=================================================================================================

def removeBets():
    try:
        remove_bets_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "remove-all-bets"))
        )
        remove_bets_button.click()
        print("bets removed")
    except WebDriverException:
        print("Remove Bets Element is not clickable")
    
    driver.refresh()
    time.sleep(1)
    
#=================================================================================================
#   Enter Stake
#=================================================================================================

def enterStake(wallet_amount):
    try:
        element1 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "stake"))
        )
        stake = element1
        stake.send_keys(wallet_amount)
        print("Stake Entered")
    except:
        print("Cannot find stake textbox or enter stake")
        try:
            removeBets()
            # ----------
            # Possible part to remove:
            element2 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "betslip-expand-button"))
            )
            element2.click()
            print("betslip opened to remove bets")
            removeBets()
            # ----------
        except:
            print("cannot open betslip")
        

#=================================================================================================
#   Close Betslip
#=================================================================================================

def closeBetslip():
    try:
        close_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "close-betslip"))
        )
        close_button.click()
        print("Bet Placed!")
        print(datetime.datetime.now().strftime("%H:%M"))
        print("!!!!!!!!!!!!!!")
        winsound.Beep(frequency, duration)
        
    except WebDriverException:
        print("Close Slip Element is not clickable")
        removeBets()

#=================================================================================================
#   Place Bet Button Click
#=================================================================================================

def clickPlaceBet():
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "place-bets-button"))
        )
        element.click()
        print("Place Bet Button Clicked")
    except:
        #   Wallet Amount not recognised. Needs refreshing.
        print("Cannot click place bets button")
        removeBets()

#=================================================================================================
#   PLACE BET LOGIC
#=================================================================================================

def placeBet():

    wallet_amount = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ssc-wla"))
    )
    wallet_amount = wallet_amount.text.strip("£")

    if betPlaced() != True:
        print("Money Available For Bet")
        enterStake(wallet_amount)
        clickPlaceBet()
        closeBetslip()
        time.sleep(1)

    else:
        removeBets()
        time.sleep(5)

#=================================================================================================
#   SET FRACTIONAL ODDS
#=================================================================================================

def setFractionalOdds():
    try:
        oddsSetting = driver.find_element_by_id("select-odds-setting")
        if oddsSetting.text == "Decimal":
            oddsSetting.click()
            fractionalOption = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located(By.LINK_TEXT("Fractional"))
            )
            fractionalOption.click()
        else:
            pass
    except:
        pass

#=================================================================================================
#   BET PLACED BOOLEAN
#=================================================================================================

def betPlaced():

    try:
        wallet_amount = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ssc-wla"))
        )
        wallet_amount = wallet_amount.text.strip("£")
    except:
        driver.refresh()
    
    try:
        if(float(wallet_amount)>0.00):
            return False
        else:
            return True
    except:
        return True

#=================================================================================================
#   ADD VIABLE BETS TO BETSLIP LOGIC
#=================================================================================================

def loopThroughToFindViableBets():
    setFractionalOdds()
    viableBets=0
    containers = driver.find_elements_by_class_name("event-information")
    
    if(betPlaced()!=True):

        for container in containers:
            try:
                for odds in container.find_elements_by_class_name("ui-runner-price"):
                    homeScore = container.find_element_by_class_name("ui-score-home")
                    awayScore = container.find_element_by_class_name("ui-score-away")
                    elapsedTime = container.find_element_by_class_name("ui-time-stop-format")
                    if conditionsMet(odds, homeScore, awayScore, elapsedTime):
                        viableBets+=1
                        try:
                            odds.click()
                            print("!!!!!!!!!!!!!!")
                            print("Viable Bet Clicked")
                            print(container.find_element_by_class_name("home-team-name").text)
                            placeBet()
                        except:
                            time.sleep(1)
            except:
                pass
        
        if viableBets==0:
            driver.refresh()
            time.sleep(2)

    else:
        time.sleep(5)
        driver.refresh()

#=================================================================================================
#   CONDITIONS MET BOOLEAN
#=================================================================================================

def conditionsMet(odds, homeScore, awayScore, elapsedTime):

    if int(odds.text.split("/")[0])==1 and int(odds.text.split("/")[1])>=40 and int(elapsedTime.text.strip("′"))>=88 and abs(int(homeScore.text)-int(awayScore.text)) >= 2:
        print("goal diff two")
        return True
    elif int(odds.text.split("/")[0])==1 and int(odds.text.split("/")[1])>=40 and int(elapsedTime.text.strip("′"))>=80 and abs(int(homeScore.text)-int(awayScore.text)) >= 3:
        print("goal diff three")
        return True
    elif int(odds.text.split("/")[0])==1 and int(odds.text.split("/")[1])>=40 and int(elapsedTime.text.strip("′"))>=60 and abs(int(homeScore.text)-int(awayScore.text)) >= 4:
        print("goal diff four")
        return True
    elif int(odds.text.split("/")[0])==1 and int(odds.text.split("/")[1])>=40 and int(elapsedTime.text.strip("′"))>=50 and abs(int(homeScore.text)-int(awayScore.text)) >= 5:
        print("goal diff five")
        return True
    else:
        return False
    
#=================================================================================================
#   START AND ITERATE
#=================================================================================================

login()
while quickbet==True:
    loopThroughToFindViableBets()


# When there's more money in the wallet the stake amount could be changed to put a fraction of the
# wallet amount on the draw so that even if they score 2 it still wins, in this case the draw odds
# would need to be 450/1 and the stake could be 1/500 of the wallet amount with the rest going on 
# the 1/200 odds to make it worth it. So that would need checking