import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you do not want a browser window to open
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the web driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load URLs from Excel file
df_urls = pd.read_excel('Law_Firm_Links.xlsx', sheet_name='SheetJS')  # Ensure the correct sheet name
urls = df_urls['Url'].tolist()


try:
    previous_data = pd.read_excel('Scraped_Law_Firm_Data_3.xlsx', sheet_name='Sheet1')  # Ensure the correct sheet name
except FileNotFoundError:
    previous_data = pd.DataFrame(columns=["URL", "Firm Name", "Email", "Phone", "Address", "Services"])

# Prepare a list to store scraped data
data = []

# Function to extract information
def extract_info(url):
    driver.get(url)
    try:
        firm_name = driver.find_element(By.CSS_SELECTOR, '.navy-text.pt-5').text
    except:
        firm_name = "N/A"
        
    try:
        email = driver.find_element(By.CSS_SELECTOR, 'a[href^="mailto"]').text
    except:
        email = "N/A"
        
    try:
        phone = driver.find_element(By.CSS_SELECTOR, 'a[href^="tel"]').text
    except:
        phone = "N/A"
        
    try:
        address_elements = driver.find_elements(By.CSS_SELECTOR, '.card-body ul li span')
        address = ', '.join([element.text for element in address_elements])
    except:
        address = "N/A"
        
    try:
        services_elements = driver.find_elements(By.CSS_SELECTOR, '.badge.badge-pill.badge-info a')
        services = [element.text for element in services_elements]
    except:
        services = []

    return {
        "URL": url,
        "Firm Name": firm_name,
        "Email": email,
        "Phone": phone,
        "Address": address,
        "Services": ', '.join(services)
    }

# Iterate over URLs and scrape data
for url in tqdm(urls, desc="Scraping"):
    if url not in previous_data['URL'].values:
        info = extract_info(url)
        data.append(info)
        new_df = pd.DataFrame([info])
        previous_data = pd.concat([previous_data, new_df], ignore_index=True)
        previous_data.to_excel('Scraped_Law_Firm_Data_3.xlsx', index=False)

# Close the driver
driver.quit()

print("Scraping completed and data saved to 'Scraped_Law_Firm_Data.xlsx'.")
