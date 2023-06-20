import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-dev-shm-usage")  
driver = webdriver.Chrome(options=options)


def send_message_to_host(account, destination, message):
    email, password = account

    driver.get('https://www.airbnb.com')

    # Log in to the Airbnb account
    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(email)

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()


    search_input = driver.find_element(By.NAME, 'query')
    search_input.send_keys(destination)
    search_input.submit()
    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, '_8ssblpx'))
    )

    first_listing = search_results.find_element(By.CLASS_NAME, '_1u6jnjh')
    first_listing.click()

    contact_host_button = driver.find_element(By.XPATH, "//button[contains(@class, '_10fsovrc')]")
    contact_host_button.click()

    message_input = driver.find_element(By.XPATH, "//textarea[contains(@class, '_6p7dvyj')]")
    message_input.send_keys(message)

    send_button = driver.find_element(By.XPATH, "//button[contains(@class, '_8imhtxs')]")
    send_button.click()

    st.write('Account:', email)
    st.write('Message sent to host')
    st.write('---')


def perform_automation(accounts, destination, message, batch_size=10, delay_between_batches=60):
    num_accounts = len(accounts)
    num_batches = num_accounts // batch_size

    for i in range(num_batches):
        batch_start = i * batch_size
        batch_end = (i + 1) * batch_size
        batch_accounts = accounts[batch_start:batch_end]

        for account in batch_accounts:
            send_message_to_host(account, destination, message)

        if i < num_batches - 1:
            st.write(f'Sleeping for {delay_between_batches} seconds...')
            time.sleep(delay_between_batches)

    remaining_accounts = accounts[num_batches * batch_size:]
    for account in remaining_accounts:
        send_message_to_host(account, destination, message)

    driver.quit()



def main():
    st.title("Airbnb Automation Bot")

    # Input fields
    num_accounts = st.number_input("Number of Airbnb accounts", min_value=1, step=1)
    accounts = []
    for i in range(num_accounts):
        email = st.text_input(f"Email {i+1}", key=f"email_input_{i}")
        password = st.text_input(f"Password {i+1}", type="password", key=f"password_input_{i}")
        if email and password:
            accounts.append((email, password))
        else:
            st.warning("Please provide all the required information for each account.")

    destination = st.text_input("Destination")
    message = st.text_area("Message to send to host")

    if st.button("Run Automation"):
        if accounts and destination and message:
            perform_automation(accounts, destination, message)
        else:
            st.warning("Please provide all the required information.")



if __name__ == '__main__':
    main()
