import time
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# Suppress Selenium logs
options = Options()
options.add_argument("--headless")  # Ensure the browser window is hidden
options.add_argument("--disable-gpu")  # Disable GPU rendering for better performance
options.add_argument("--no-sandbox")  # Ensure the sandbox is not used for better performance
options.add_argument("--disable-dev-shm-usage")  # Avoid issues with shared memory
options.add_argument("--log-level=3")  # Suppress console warnings and errors

# Suppress browser console logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize the webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to scrape data from a page
def scrape_page(page_num):
    url = f"https://eservice.sba.gov.sa/en/lawyers?page={page_num}"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-body')))
    
    lawyers = []
    
    cards = driver.find_elements(By.CLASS_NAME, 'card-body')
    for card in cards:
        try:
            name = card.find_element(By.TAG_NAME, 'h6').text
        except:
            name = 'N/A'
        try:
            city = card.find_element(By.XPATH, ".//div[contains(text(), 'المدينة')]/following-sibling::div").text
        except:
            city = 'N/A'
        try:
            licence_no = card.find_element(By.XPATH, ".//div[contains(text(), 'رقم الرخصة')]/following-sibling::div").text
        except:
            licence_no = 'N/A'
        try:
            licence_status = card.find_element(By.XPATH, ".//div[contains(text(), 'حالة الرخصة')]/following-sibling::div").text
        except:
            licence_status = 'N/A'
        try:
            expiry_date = card.find_element(By.XPATH, ".//div[contains(text(), 'انتهاء الرخصة')]/following-sibling::div").text
        except:
            expiry_date = 'N/A'
        try:
            profile_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except:
            profile_url = 'N/A'
            
        lawyers.append({
            'Name': name,
            'City': city,
            'Licence Number': licence_no,
            'Licence Status': licence_status,
            'Expiry Date': expiry_date,
            'Profile URL': profile_url
        })
    
    return lawyers

# Load existing data
try:
    existing_lawyers = pd.read_excel('lawyers_data.xlsx')
except FileNotFoundError:
    existing_lawyers = pd.DataFrame()

start_page = 1 + len(existing_lawyers) // 20
# Iterate through all the pages
for page in tqdm(range(start_page, 610)):
    lawyers = scrape_page(page)
    df = pd.DataFrame(lawyers)
    
    # Combine new data with existing data
    combined_lawyers = pd.concat([existing_lawyers, df], ignore_index=True)
    
    # Drop duplicates
    combined_lawyers.drop_duplicates(subset=['Name', 'City', 'Licence Number', 'Licence Status', 'Expiry Date', 'Profile URL'], inplace=True)
    
    # Save to Excel
    combined_lawyers.to_excel('lawyers_data.xlsx', index=False)
    
    # Update existing data
    existing_lawyers = combined_lawyers
    
    # Delay to prevent overloading the server
    time.sleep(2)

# Close the browser
driver.quit()

print("Scraping complete. Data saved to lawyers_data.xlsx.")
