#pip install selenium pandas openpyxl
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

test_results = []

def log_bug(bug_id, summary, expected, actual, status="FAIL"):
    test_results.append({
        "Bug ID": bug_id, "Summary": summary,
        "Expected": expected, "Actual": actual, "Status": status
    })
    print(f"{bug_id}: {summary}")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()

URL = "https://ginngo.github.io/test_login/buggy_login.html"

try:
    start_time = time.time()
    driver.get(URL)
    wait = WebDriverWait(driver, 5)
    
    try:
        email_field = wait.until(EC.visibility_of_element_located((By.ID, "email")))
        load_time = time.time() - start_time
    except:
        load_time = 999

    pass_field = driver.find_element(By.ID, "password")
    
    # BUG-LOGIN-001
    pass_field.click()
    pass_field.send_keys("123456")
    pass_field.send_keys(Keys.ENTER)
    time.sleep(0.5)
    try:
        driver.switch_to.alert.dismiss()
    except NoAlertPresentException:
        log_bug("BUG-LOGIN-001", "Phím Enter không gửi form", "Submit form", "Không phản hồi")

    # BUG-LOGIN-002
    mobile_spacing = driver.find_element(By.CLASS_NAME, "mobile-spacing")
    if mobile_spacing.size['height'] > 200:
        log_bug("BUG-LOGIN-002", "Khoảng trống đẩy nút Login", "Khoảng cách hợp lý", "Khoảng trống quá lớn")

    # BUG-LOGIN-003
    email_field.click()
    email_field.send_keys(Keys.TAB)
    active_element = driver.switch_to.active_element
    if active_element.get_attribute("id") != "password":
        log_bug("BUG-LOGIN-003", "Tab nhảy sai thứ tự", "Focus Password", f"Focus ID: {active_element.get_attribute('id')}")

    # BUG-LOGIN-004
    checkbox = driver.find_element(By.ID, "remember")
    if checkbox.size['width'] < 44 or checkbox.size['height'] < 44:
        log_bug("BUG-LOGIN-004", "Checkbox quá nhỏ", ">= 44x44 px", f"{checkbox.size['width']}x{checkbox.size['height']} px")

    # BUG-LOGIN-005
    eye_icon = driver.find_element(By.CLASS_NAME, "eye-icon")
    if "-" in eye_icon.value_of_css_property("right"):
        log_bug("BUG-LOGIN-005", "Icon Eye bị lệch", "right >= 0", f"right: {eye_icon.value_of_css_property('right')}")

    # BUG-LOGIN-006
    container = driver.find_element(By.CLASS_NAME, "login-container")
    if container.size['width'] > 600:
        log_bug("BUG-LOGIN-006", "Lỗi Responsive", "Co dãn 100%", f"Fix width {container.size['width']}px")

    # BUG-LOGIN-007
    email_field.clear()
    email_field.send_keys("emailkhonghople")
    driver.find_element(By.ID, "btnLogin").click()
    time.sleep(1)
    try:
        alert = driver.switch_to.alert
        if "thành công" in alert.text.lower():
            log_bug("BUG-LOGIN-007", "Không Validate Email", "Báo lỗi", "Báo thành công")
        alert.accept()
    except NoAlertPresentException:
        pass

    # BUG-LOGIN-008
    driver.find_element(By.CLASS_NAME, "social-btn").click()
    time.sleep(0.5)
    try:
        driver.switch_to.alert.dismiss()
    except NoAlertPresentException:
        log_bug("BUG-LOGIN-008", "Nút Social Login chết", "Chuyển trang", "Không phản hồi")

    # BUG-LOGIN-009
    if pass_field.get_attribute("type") != "password":
        log_bug("BUG-LOGIN-009", "Lộ mật khẩu Plain text", "type='password'", f"type='{pass_field.get_attribute('type')}'")

    # BUG-LOGIN-010
    if load_time > 2.0:
        log_bug("BUG-LOGIN-010", "Load trang chậm", "< 2.0s", f"{load_time:.2f}s")

finally:
    driver.quit()

if test_results:
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    file_path = os.path.join(downloads_path, "Bug_Report_Ordered.xlsx")
    
    pd.DataFrame(test_results).to_excel(file_path, index=False)
    print(f"\n🎉 HOÀN THÀNH! File báo cáo đã được tải xuống tại:\n👉 {file_path}")
