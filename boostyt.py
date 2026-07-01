import time
import random
import threading
import requests  
import undetected_chromedriver as uc
import os
from concurrent.futures import ThreadPoolExecutor

# កំណត់ចំនួន Browser ខ្ពស់បំផុតដែលអាចបើកដំណើរការស្របគ្នាក្នុងពេលតែមួយ (ការពារកុំឱ្យគាំង RAM)
MAX_CONCURRENT_BLAST = 5  

driver_lock = threading.Lock()

def watch_video_thread(thread_id, video_url, agent, proxy):
    print(f"🚀 [Thread {thread_id}] ចាប់ផ្តើមដំណើរការជាមួយ IP: {proxy}")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--mute-audio")
    options.add_argument(f"user-agent={agent}")
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    if os.name == 'nt': 
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    driver = None
    try:
        with driver_lock:
            print(f"🛠️ [Thread {thread_id}] កំពុងរៀបចំ និងបើក Browser...")
            
            if os.name != 'nt':
                driver = uc.Chrome(options=options, version_main=149)
            else:
                driver = uc.Chrome(options=options)
                
            time.sleep(2)
            
        driver.set_page_load_timeout(45)
        driver.get(video_url)
        
        watch_time = random.randint(25, 60)
        print(f"📺 [Thread {thread_id}] កំពុងមើលវីដេអូ រង់ចាំ {watch_time} វិនាទី...")
        time.sleep(watch_time)
        
        print(f"✅ [Thread {thread_id}] បញ្ចប់ការងារដោយជោគជ័យ!")
        
    except Exception as e:
        print(f"⚠️ [Thread {thread_id}] មានបញ្ហា៖ {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def get_live_proxies_fast_api():
    print("\n🌐 កំពុងទាក់ទងទៅ Proxyscrape API ដើម្បីទាញយក Proxy ថ្មីៗល្បឿនលឿន (យកទាំងអស់)...")
    api_url = "https://raw.githubusercontent.com/obitokh/proxy/refs/heads/main/proxyscrape_premium_http_proxies.txt"
    try:
        response = requests.get(api_url, timeout=30)
        all_proxies = [line.strip() for line in response.text.split("\r\n") if line.strip()]
        # លាយឡំ Proxy ឱ្យមានភាពចៃដន្យ
        random.shuffle(all_proxies)
        return all_proxies
    except Exception as e:
        print(f"❌ មិនអាចទាញយក Proxy បានទេ៖ {e}")
        return []

# ==================== ដំណើរការកម្មវិធីមេ (AUTO-RUN LOOP) ====================
if __name__ == "__main__":
    target_video = "https://youtu.be/YuWlVPwXnsc?si=fT4Jz57tYtv40hrs"
    round_count = 1  
    global_user_counter = 1  # បញ្ជីរាប់ឈ្មោះ User កើនឡើងទៅមុខឥតដែនកំណត់

    user_agents_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/21000101 Firefox/119.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
    ]

    # 🔥 Loop រត់រហូតមិនចេះឈប់លើ Cloud
    while True:
        print(f"\n⚡🔄⚡ ================== ចាប់ផ្តើមរត់ AUTO ជុំទី {round_count} ================== ⚡🔄⚡")
        
        proxies_pool = get_live_proxies_fast_api()
        
        if proxies_pool and proxies_pool[0] != "":
            print(f"🎯 ទទួលបាន {len(proxies_pool)} Proxies សម្រាប់បុកក្នុងជុំនេះ!")
            print(f"⚙️ ប្រព័ន្ធនឹងបើកដំណើរការត្រួតគ្នាខ្ពស់បំផុតម្តង {MAX_CONCURRENT_BLAST} Threads ដើម្បីរក្សាទម្រង់ RAM។")
            
            # ប្រើប្រាស់ ThreadPoolExecutor ដើម្បីគ្រប់គ្រងទិន្នន័យ User ឥតដែនកំណត់ដោយសុវត្ថិភាព
            with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_BLAST) as executor:
                for proxy in proxies_pool:
                    random_agent = random.choice(user_agents_pool)
                    
                    # បញ្ជូន Thread ទៅដំណើរការ និងបង្កើនលេខ User រហូត
                    executor.submit(watch_video_thread, global_user_counter, target_video, random_agent, proxy)
                    global_user_counter += 1
                    
                    # ពន្យារពេល ២ វិនាទីមុននឹងបើក Browser បន្ទាប់ កុំឱ្យ CPU ដំណើរការខ្លាំងពេក
                    time.sleep(2)

            print(f"\n🎉 [មេកង] ជុំទី {round_count} ត្រូវបានបញ្ចប់សព្វគ្រប់!")
            round_count += 1  # បូកជុំឡើងទៅមុខឥតកំណត់
            
            # សម្រាក ១០ វិនាទី មុននឹងទាញ API បុកជុំថ្មី
            print("⏳ សម្រាក ១០ វិនាទី មុននឹងចាប់ផ្តើមជុំបន្ទាប់...")
            time.sleep(10)
        else:
            print("❌ គ្មានទិន្នន័យ Proxy ទេ! រង់ចាំ ៣០ វិនាទី រួចសាកល្បងទៅបឺតយកម្តងទៀត...")
            time.sleep(30)
