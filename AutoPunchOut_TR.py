import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# .envファイルからIDとパスワードを取得
login_id = os.getenv('TL_LOGIN_ID')
password = os.getenv('TL_PASSWORD')

# Chromeのオプションを設定
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # ヘッドレスモードで実行する場合
# chrome_options.add_argument("--disable-gpu")  # GPUを無効化
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriverを自動インストールして使用
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # 指定されたURLを開く
    driver.get('https://clie-s2.biz/CL_WF79002120231106/page/login.jsp;jsessionid=E40299DAC2EEA15CDDAB0E476759DAC0')

    # ログインIDを入力
    id_input = driver.find_element(By.XPATH, '//*[@id="user"]')
    id_input.send_keys(login_id)

    # パスワードを入力
    password_input = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys(password)

    # ログインボタンをクリック
    login_button = driver.find_element(By.XPATH, '//*[@id="submit"]')
    login_button.click()

    # 5秒間待機（ログイン処理完了のため）
    time.sleep(5)

    # 打刻ボタンをクリック
    punch_in_button = driver.find_element(By.XPATH, '//*[@id="sidA_TIME_REC_OUT"]')
    punch_in_button.click()

    # 打刻ボタンがクリックされた後、さらに確認用の処理を入れることができます。
    # 例: 打刻完了メッセージやページの変化を確認

    # もう少し待機して、打刻が正常に完了したか確認することも可能
    time.sleep(2)

finally:
    # ブラウザを閉じる
    driver.quit()
