import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from groq import Groq  # Assuming 'groq' is a placeholder for the actual Groq client library

# Specify the exact location of chromedriver.exe
chrome_driver_path = r'F:\myCode\chromedriver-win64\chromedriver.exe'


class QuotedInsightsTwitterBot:
    def __init__(self):
        # Initialize the Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

        # Initialize Groq client
        load_dotenv()
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def get_groq_quote(self, user_prompt):
        # Use Groq's chat model to generate a quote based on the user's prompt
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "you are a helpful quote generator who writes tweets about love."},
                {"role": "user", "content": user_prompt}
            ],
            model="mixtral-8x7b-32768",
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content

    def tweet_at_someone(self, message):
        # Navigate to Twitter and log in (Simplified version, consider using Twitter's API for more complex interactions)
        self.driver.get("https://twitter.com/login")
        username_field = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        password_field = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')

        # Assuming environmental variables for security
        username_field.send_keys(os.getenv('TWITTER_USERNAME'))
        password_field.send_keys(os.getenv('TWITTER_PASSWORD'))

        # Compose a new tweet
        compose_tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
        compose_tweet.click()

        # Enter the tweet content
        tweet_content_field = self.driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block')
        tweet_content_field.send_keys(message)

        # Tweet it
        tweet_button = self.driver.find_element(By.XPATH, '//div[@role="button"][contains(text(),"Tweet")]')
        tweet_button.click()

        # Close the browser session
        self.driver.quit()


# Usage example with dynamic user prompts for the bot
if __name__ == "__main__":
    bot = QuotedInsightsTwitterBot()
    user_prompt = input("Please type a prompt: ")
    quote = bot.get_groq_quote(user_prompt)
    tweet_message = f"Quote of the day: {quote} #Love #Quote"
    bot.tweet_at_someone(tweet_message)
