from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you do not want a browser window to open
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the web driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the URL of the page
url = "https://eservice.sba.gov.sa/en/directory/7"  # Replace with the actual URL

# Open the URL
driver.get(url)

# Function to extract and print information
def extract_info():
    # Extract the name of the firm
    firm_name = driver.find_element(By.CSS_SELECTOR, '.navy-text.pt-5').text
    print(f"Firm Name: {firm_name}")
    
    # Extract the email
    email = driver.find_element(By.CSS_SELECTOR, 'a[href^="mailto"]').text
    print(f"Email: {email}")
    
    # Extract the phone number
    phone = driver.find_element(By.CSS_SELECTOR, 'a[href^="tel"]').text
    print(f"Phone: {phone}")
    
    # Extract address
    address_elements = driver.find_elements(By.CSS_SELECTOR, '.card-body ul li span')
    address = ', '.join([element.text for element in address_elements])
    print(f"Address: {address}")
    
    # Extract services
    services_elements = driver.find_elements(By.CSS_SELECTOR, '.badge.badge-pill.badge-info a')
    services = [element.text for element in services_elements]
    print("Services:")
    for service in services:
        print(f"  - {service}")

# Call the function to extract information
extract_info()

# Close the driver
driver.quit()