from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Configuration
job_url = "https://job-boards.greenhouse.io/grafanalabs/jobs/5336218004"
test_mode = True
pause_for_review = True

# Personal Information
personal_information = {
    "name": "Devdatta",
    "surname": "Talele",
    "email": "devtalele0@gmail.com",
    "phone": "9370091908",
    "city": "mumbai",
    "state": "maharashtra",
    "country": "india",
    "preferred_name": "Dev",
    "pronouns": "He/Him",
    "current_company": "hdge3",
    "social_profiles": {
        "linkedin": "https://linkedin.com/in/devdattatalele",
        "github": "https://github.com/devdattatalele",
        "twitter": "https://twitter.com/yourhandle",
        "portfolio": "https://devdattatalele.com",
        "stackoverflow": "https://stackoverflow.com/users/yourid",
        "other": "https://other-profile.com"
    },
    "address": "32,threetwo,road",
    "zip_code": "429112",
    "phone_prefix": "+91"
}

# Dropdown configurations
dropdowns = {
    "gender": "Male",
    "hispanic_ethnicity": "No",
    "veteran_status": "I am not a protected veteran",
    "disability_status": "No, I don't have a disability",
    "question_11886622004": "Yes",  # Are you currently eligible to work in your country of residence?
    "question_11886623004": "No",  # Do you now or in the future require visa sponsorship?
    "4000681004": "Male", #What gender identity do you most closely identify with?
    "4000691004": "No" #Are you a person of transgender experience?
}

# Specific Answers
specific_answers = {
    "what country and time zone are you based in?": "New York, NY",
}

resume_path = "/Users/dev16/Documents/Krya.ai/resume.pdf"

# Initialize WebDriver with options
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

def scroll_to_element(element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", element)
    time.sleep(0.5)  # Allow time for scrolling to complete

def fill_select(element_id, value):
    try:
        # Wait for the select element to be present
        select_element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
        scroll_to_element(select_element)
        
        # Find the parent element with class 'select-shell'
        select_shell = select_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'select-shell')]")
        
        # Click the control to open dropdown
        control = select_shell.find_element(By.CLASS_NAME, "select__control")
        scroll_to_element(control)
        ActionChains(driver).move_to_element(control).click().perform()
        time.sleep(0.5)
        
        # Wait for and click the option
        option_xpath = f"//div[contains(@class, 'select__option') and contains(text(), '{value}')]"
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        ActionChains(driver).move_to_element(option).click().perform()
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error filling select {element_id}: {str(e)}")

try:
    driver.get(job_url)
    time.sleep(2)

    # --- Personal Information ---
    driver.find_element(By.ID, "first_name").send_keys(personal_information["name"])
    driver.find_element(By.ID, "last_name").send_keys(personal_information["surname"])
    driver.find_element(By.ID, "preferred_name").send_keys(personal_information["preferred_name"])
    driver.find_element(By.ID, "email").send_keys(personal_information["email"])
    driver.find_element(By.ID, "phone").send_keys(personal_information["phone"])

    # --- Resume Upload ---
    resume_input = driver.find_element(By.ID, "resume")
    resume_input.send_keys(resume_path)
    time.sleep(5)  # Give it time to upload

    # --- Application Questions ---
    driver.find_element(By.ID, "question_11886619004").send_keys(personal_information["social_profiles"]["linkedin"])
    driver.find_element(By.ID, "question_11886620004").send_keys(personal_information["current_company"])
    driver.find_element(By.ID, "question_11886621004").send_keys(specific_answers["what country and time zone are you based in?"])

    # --- Handle all dropdowns ---
    for dropdown_id, dropdown_value in dropdowns.items():
        fill_select(dropdown_id, dropdown_value)
        time.sleep(1)  # Brief pause between dropdowns

    # --- Consent Checkbox ---
    try:
        consent_checkbox = driver.find_element(By.ID, "gdpr_demographic_data_consent_given_1")
        scroll_to_element(consent_checkbox)
        consent_checkbox.click()
    except Exception as e:
        print(f"Error with consent checkbox: {str(e)}")

    # --- Submit Application ---
    if test_mode:
        print("Test mode enabled. Application will not be submitted.")
    else:
        if pause_for_review:
            input("Please review the application and press Enter to submit...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        scroll_to_element(submit_button)
        submit_button.click()

    time.sleep(5)  # Give time for submission

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if test_mode:
        print("Test mode enabled. Keeping browser open for review.")
        input("Press Enter to close the browser...")
    driver.quit()