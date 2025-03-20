from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# User details
CALENDLY_URL = "https://calendly.com/matejotys/30minutes"
USER_NAME = "Radka Test"
USER_EMAIL = "radarudova@gmail.com"
UK_TIMEZONE = "UK"  # Adjust if needed
MEETING_TYPE = "Google Meet"
DATE = "24"  # Date to select
TIME = "15:30"  # Time to select

# Start WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")  # Required for Heroku
options.add_argument("--disable-dev-shm-usage")  # Fixes memory issues
options.add_argument("--user-data-dir=/tmp/user-data")  # Avoids user data conflict
options.add_argument("--remote-debugging-port=9222")  # Allows debugging

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(CALENDLY_URL)
wait = WebDriverWait(driver, 10)

### ✅ STEP 1: SELECT TIMEZONE ###
# Click the timezone dropdown
timezone_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "timezone-field")))
timezone_dropdown.click()

# Wait for the input field and type "UK"
timezone_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#timezone-menu input")))
timezone_input.send_keys("UK")
time.sleep(2)  # Allow time for the list to refresh

# Select the correct option that contains "UK, Ireland, Lisbon Time"
timezone_options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[role='option']")))
for option in timezone_options:
    if "UK, Ireland, Lisbon Time" in option.text:
        option.click()
        break  # Stop looping once we find the correct one

time.sleep(2)  # Allow time for list to load

### ✅ STEP 2: SELECT DATE ###
# Wait for the calendar to load
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='calendar']")))

# Click the correct date
date_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(@aria-label, 'March {DATE}') and contains(@aria-label, 'Times available')]")))
date_button.click()
time.sleep(4)


# ✅ STEP 3: SELECT TIME SLOT

# Wait for time slots to load
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-container='time-button']")))

# Get all available time slots
available_times = driver.find_elements(By.CSS_SELECTOR, "button[data-container='time-button']")

# Print available times for debugging
available_times_text = [t.text.strip() for t in available_times]
print("Available times:", available_times_text)

# Try to find the exact time
selected_time = None
for time_slot in available_times:
    if time_slot.text.strip() == TIME:
        selected_time = time_slot
        break

# If the exact time isn't found, print an error and exit
if not selected_time:
    print(f"❌ ERROR: Requested time {TIME} not found! Available options: {available_times_text}")
    driver.quit()
    exit()

# Scroll to and click the correct time slot
driver.execute_script("arguments[0].scrollIntoView();", selected_time)  # Ensure visibility
time.sleep(1)  # Short delay before clicking
selected_time.click()
print(f"✅ Successfully selected time: {TIME}")

### ✅ STEP 4: CLICK "NEXT" TO CONFIRM ###
next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Next')]")))
next_button.click()

print("✅ Successfully clicked 'Next' button.")

### ✅ STEP 5: FILL IN NAME & EMAIL ###
name_field = wait.until(EC.presence_of_element_located((By.ID, "full_name_input")))
email_field = wait.until(EC.presence_of_element_located((By.ID, "email_input")))

name_field.send_keys(USER_NAME)
email_field.send_keys(USER_EMAIL)

print(f"✅ Entered name: {USER_NAME}, email: {USER_EMAIL}")

### ✅ STEP 6: SELECT MEETING LOCATION (Google Meet) ###
MEETING_TYPE = "Google Meet"  # Options: "Google Meet", "Zoom", "Microsoft Teams"

# Find all location labels
location_labels = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//label")))

# Click the label containing the correct meeting type
for label in location_labels:
    if MEETING_TYPE in label.text:
        driver.execute_script("arguments[0].scrollIntoView();", label)  # Ensure visibility
        time.sleep(1)  # Short delay
        label.click()
        print(f"✅ Selected meeting type: {MEETING_TYPE}")
        break
submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
submit_button.click()

print("✅ Successfully clicked 'Schedule Event' button.")

# Allow time for confirmation message to appear before closing
time.sleep(5)
driver.quit()


