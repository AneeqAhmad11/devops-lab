"""Selenium test for the DevOps Task Manager.

Usage:  python test_selenium.py http://<ALB-DNS-NAME>
"""
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost"

driver = webdriver.Chrome()  # opens a visible Chrome window
try:
    driver.get(url)
    time.sleep(1)

    # Test 1: verify the page heading
    heading = driver.find_element(By.ID, "page-title").text
    assert heading == "DevOps Task Manager", f"Wrong heading: {heading}"
    print("PASS: heading found ->", heading)

    # Test 2: add a task and verify it appears in the list
    task_name = "Selenium test task " + str(int(time.time()))
    driver.find_element(By.ID, "task-input").send_keys(task_name)
    driver.find_element(By.ID, "add-btn").click()
    time.sleep(1)

    items = [li.text for li in driver.find_elements(By.CSS_SELECTOR, "#task-list li")]
    assert task_name in items, "Task was not added"
    print("PASS: task added and visible ->", task_name)

    print("ALL TESTS PASSED")
    time.sleep(3)  # keep the browser open briefly for your screenshot
finally:
    driver.quit()
