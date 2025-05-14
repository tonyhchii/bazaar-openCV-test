from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import json

# Configure stealth options
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_argument("--window-size=1920,1080")

# For headless mode (add these if needed)
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

url = "https://www.howbazaar.gg/items?isShowingAdvancedFilters=false"
driver.get(url)

data = []
previous_count = 0
scroll_attempts = 0
max_attempts = 10 
scroll_pause_time = 1.5  # Base wait time

# Get initial height
last_height = driver.execute_script("return document.body.scrollHeight")

try:
    while scroll_attempts < max_attempts:
        # Scroll in random increments to appear more human-like
        scroll_height = random.randint(300, 800)
        current_scroll = driver.execute_script("return window.pageYOffset")
        driver.execute_script(f"window.scrollTo(0, {current_scroll + scroll_height});")
        
        # Randomize wait times
        randomized_wait = scroll_pause_time + random.random() * 2
        time.sleep(randomized_wait)
        
        # Wait for new items to load
        try:
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, 'div._ah')) > previous_count
            )
        except:
            pass
        
        # Check for new content
        new_height = driver.execute_script("return document.body.scrollHeight")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        current_items = soup.find_all('div', class_='_ah')
        
        if len(current_items) > previous_count:
            print(f"Loaded {len(current_items)} items...")
            previous_count = len(current_items)
            scroll_attempts = 0  # Reset counter on successful load
            last_height = new_height
        else:
            # Try alternative scroll method if stuck
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_attempts += 1
            
            # Final check after hard scroll
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            last_height = new_height

except Exception as e:
    print(f"Stopped early due to error: {str(e)}")

# Final collection of all items
soup = BeautifulSoup(driver.page_source, 'html.parser')
items = soup.find_all('div', class_='shadow-md')

for item in items:
    name_div = item.select_one(".text-2xl")
    name = name_div.text.strip() if name_div else "Unknown"

    img_tag = item.select_one("img.object-fill")
    img_url = img_tag["src"] if img_tag else "No Image"

    tag_divs = item.select("div.text-xs")
    size = None
    for tag in tag_divs:
        tag_text = tag.get_text(strip=True)
        if tag_text in ["Small", "Medium", "Large"]:
            size = tag_text
            break

    data.append({
        "name": name,
        "image": img_url,
        "size": size or "Not Specified"
        })
    
driver.quit()

# Save to JSON
with open('items.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Successfully scraped {len(data)} items. Saved to items.json")