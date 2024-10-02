import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# .env ファイルを読み込む
load_dotenv()

# 環境変数からログイン情報を取得
login_id = os.getenv('GS_LOGIN_ID')
password = os.getenv('GS_PASSWORD')

# 今日の日付を取得 (例: 28日)
today = datetime.now().day

# ChromeDriverのServiceを使って設定
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# ログインページへ移動
driver.get("https://st10.bycloud.jp/gsession/ascot/common/cmn002.do")

# 2秒待機（ページが完全に読み込まれるのを待つ）
time.sleep(2)

# 現在のURLを取得
current_url = driver.current_url

# 未ログインページかどうか確認し、ボタンを押す
if current_url == "https://st10.bycloud.jp/gsession/ascot/common/cmn002.do":
    print("未ログインのページです")

    # ログインボタンをクリックする
    try:
        login_page_button = driver.find_element(By.XPATH, '//*[@id="contair"]/div/div[3]/div/button')
        login_page_button.click()
        print("ログインボタンをクリックしました")
    except Exception as e:
        print(f"ログインボタンのクリックに失敗しました: {e}")

# 3秒待機して次のページに遷移
time.sleep(3)

# ログインフォームにログインIDとパスワードを入力
try:
    # ログインIDを入力
    login_id_field = driver.find_element(By.XPATH, '/html/body/div/form/div[2]/ul/li[1]/div[2]/input')
    login_id_field.send_keys(login_id)
    
    # パスワードを入力
    password_field = driver.find_element(By.XPATH, '/html/body/div/form/div[2]/ul/li[2]/div[2]/input')
    password_field.send_keys(password)
    
    # ログインボタンをクリック
    login_button = driver.find_element(By.XPATH, '/html/body/div/form/div[2]/input')
    login_button.click()
    
    print("ログインに成功しました。")
except Exception as e:
    print(f"ログインに失敗しました: {e}")

# 3秒待機して次のページに遷移
time.sleep(3)

# iframeに切り替える（XPathを適宜変更）
try:
    iframe_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bodyFrame')))
    #print(iframe_element.get_attribute('id'))
    
    #driver.switch_to.frame(iframe_element)
    driver.switch_to.frame(1)
    print("iframe に切り替わりました。")

     # iframe内で要素を探す（XPath を適宜変更）
    target_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tooltips_sch"]/table/tbody/tr[4]/td[1]/a/div/div')))
    element_text = target_element.text.strip()
    print(f"取得したテキスト: {element_text}")
    
    # テキストが "出社" なら、次の処理を行う
    if element_text == "出社":
        print("出社状態です。処理を開始します。")
        
        # ラジオボタンをオンにする
        zaiseki_radio = driver.find_element(By.XPATH, '//*[@id="sts_huzai"]')
        zaiseki_radio.click()
        print("ラジオボタンをオンにしました。")
        
        # 在席状況フィールドに「今日の日付 + 退社」を入力
        status_field = driver.find_element(By.XPATH, '//*[@id="zaiseki_zskmain"]/form/table/tbody/tr[2]/td/div[2]/input')
        status_field.clear()
        status_text = f"{today}日 退社"
        status_field.send_keys(status_text)
        print(f"在席状況を '{status_text}' に設定しました。")
        
        # 変更ボタンをクリック
        change_button = driver.find_element(By.XPATH, '//*[@id="zaiseki_zskmain"]/form/table/tbody/tr[2]/td/div[2]/button')
        change_button.click()
        print("変更ボタンをクリックしました。")
    
    # テキストが "TW" なら、次の処理を行う
    elif element_text == "TW":
        print("TW状態です。処理を開始します。")
        
        # ラジオボタンをオンにする
        zaiseki_radio = driver.find_element(By.XPATH, '//*[@id="sts_huzai"]')
        zaiseki_radio.click()
        print("ラジオボタンをオンにしました。")
        
        # 在席状況フィールドに「今日の日付 + TW終了」を入力
        status_field = driver.find_element(By.XPATH, '//*[@id="zaiseki_zskmain"]/form/table/tbody/tr[2]/td/div[2]/input')
        status_field.clear()
        status_text = f"{today}日 TW終了"
        status_field.send_keys(status_text)
        print(f"在席状況を '{status_text}' に設定しました。")
        
        # 変更ボタンをクリック
        change_button = driver.find_element(By.XPATH, '//*[@id="zaiseki_zskmain"]/form/table/tbody/tr[2]/td/div[2]/button')
        change_button.click()
        print("変更ボタンをクリックしました。")
    else:
        print("出社状態ではありません。処理をスキップします。")

except TimeoutException:
    print("指定した要素が見つかりませんでした。")
except Exception as e:
    print(f"処理に失敗しました: {e}")

# iframeから元のコンテンツに戻す
driver.switch_to.default_content()