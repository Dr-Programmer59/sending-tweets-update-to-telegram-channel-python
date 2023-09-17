from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from telegram import InputFile
from selenium.webdriver.common.by import By


import time

import asyncio
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
import requests


async def send_telegram_message_with_buttons(text,url,imagelink):
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot = Bot(token='Bot-token')

    # Replace 'CHAT_ID' with the chat ID of the user or group where you want to send the message
    chat_id = 'channel id'

    # Replace 'Your message here' with the message you want to send
    message_text =text

    # Create an inline keyboard with buttons
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='SOURCE', url=url)],
           
        ]
    )
    if imagelink=="":
    # Send the message with the inline keyboard
        await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboard)
    else:
       
        await bot.send_photo(chat_id=chat_id, caption=message_text, reply_markup=keyboard, photo=imagelink )


driver = webdriver.Chrome()
driver.get("https://twitter.com/i/flow/login")
time.sleep(5)
my_user_name = driver.find_element(By.TAG_NAME,"label")
my_user_name.send_keys("username")
next_button = driver.find_elements(By.CLASS_NAME,"css-18t94o4")[2]
next_button.click()

time.sleep(5)

password_box = driver.find_elements(By.TAG_NAME,"input")[1]

password_box.send_keys("password")

login_button = driver.find_elements(By.CLASS_NAME,"css-18t94o4")[3]
login_button.click()

time.sleep(5)

user_twitter_id ="usernamtotrack"
driver.get(f"https://twitter.com/{user_twitter_id}")

#account = driver.find_elements(By.CLASS_NAME,"css-18t94o4")[48].send_keys(Keys.ENTER)

time.sleep(10)

# number_of_posts = driver.find_elements(By.CLASS_NAME,"css-901oao")[51].text
# print(number_of_posts)
already_Tweets=[]
number_of_posts = driver.find_elements(By.TAG_NAME,"article")
print(len(number_of_posts))
for i,posts in enumerate(number_of_posts):
    # print(posts.text)
    # posts_TExt=driver.execute_script(f"""return document.getElementsByTagName("article")[{i}].querySelector(`div[data-testid="tweetText"]`)""")
    links=posts.find_elements(By.TAG_NAME,"a")
    for link in links:
            if "status" in link.get_attribute("href") and "analytics" not in link.get_attribute("href"):
                postlink=link.get_attribute("href")
                already_Tweets.append(link.get_attribute("href"))
  


print(already_Tweets)
while True:
    number_of_posts = driver.find_elements(By.TAG_NAME,"article")
    print(len(number_of_posts))
  
    for i,posts in enumerate(number_of_posts):
        links=posts.find_elements(By.TAG_NAME,"a")
        for link in links:
            if "status" in link.get_attribute("href") and "analytics" not in link.get_attribute("href"):
                postlink=link.get_attribute("href")
        # print(posts.text)
        posts_TExt=driver.execute_script(f"""return document.getElementsByTagName("article")[{i}].querySelector(`div[data-testid="tweetText"]`)""")

        if postlink not in already_Tweets:
            
            image=driver.execute_script(f"""return document.getElementsByTagName("article")[{i}].querySelector(`div[data-testid="tweetPhoto"]`)""")
            if image:
                    imgl=image.find_element(By.TAG_NAME,"img").get_attribute("src")
            else:
                    imgl=""
      

            asyncio.run(send_telegram_message_with_buttons(posts_TExt.text,postlink,imgl))
            already_Tweets.append(postlink)
            print(postlink)

    time.sleep(10)
    driver.refresh()
    time.sleep(5)
