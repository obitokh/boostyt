import time
import random
import threading
import requests  
import undetected_chromedriver as uc

driver_lock = threading.Lock()

def watch_video_thread(thread_id, video_url, agent, proxy):
    print(f"🚀 [Thread {thread_id}] ចាប់ផ្តើមដំណើរការជាមួយ IP: {proxy}")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--mute-audio")
    options.add_argument(f"user-agent={agent}")
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    driver = None
    try:
        with driver_lock:
            print(f"🛠️ [Thread {thread_id}] កំពុងរៀបចំ និងបើក Browser...")
            driver = uc.Chrome(options=options, version_main=149)
            time.sleep(2)
            
        driver.set_page_load_timeout(35)
        driver.get(video_url)
        
        watch_time = random.randint(15, 25)
        print(f"📺 [Thread {thread_id}] កំពុងមើលវីដេអូ រង់ចាំ {watch_time} វិនាទី...")
        time.sleep(watch_time)
        
        print(f"✅ [Thread {thread_id}] បញ្ចប់ការងារដោយជោគជ័យ!")
        
    except Exception as e:
        print(f"⚠️ [Thread {thread_id}] មានបញ្ហា (Proxy ដើរយឺត/ងាប់)៖ {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def get_live_proxies_fast_api(limit=100):  # 🔥 បង្កើន Limit ឱ្យទាញយក Proxy ម្តងបានច្រើន (រហូតដល់ ១០០ ឬលើសនេះ)
    print(f"\n🌐 កំពុងទាញយក Proxy ថ្មីៗខុសៗគ្នា ចំនួន {limit} ពី Proxyscrape API...")
    api_url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(api_url, timeout=30)
        all_proxies = response.text.strip().split("\r\n")
        # ចាប់យក IP ចម្រុះគ្នាដោយចៃដន្យតាមចំនួន Limit ដែលចង់បាន
        fetched_proxies = random.sample(all_proxies, limit) if len(all_proxies) >= limit else all_proxies[:limit]
        return fetched_proxies
    except Exception as e:
        print(f"❌ មិនអាចទាញយក Proxy បានទេ៖ {e}")
        return []

# ==================== ដំណើរការកម្មវិធីមេ (INFINITE AUTO-RUN) ====================
if __name__ == "__main__":
    target_video = "https://youtu.be/YuWlVPwXnsc?si=eAgDccQc5GPXVR0N"
    
    # បង្កើត User Agents Pool ឱ្យកាន់តែច្រើន ដើម្បីឱ្យ User នីមួយៗខុសៗគ្នាពិតប្រាកដ
    user_agents_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/21000101 Firefox/119.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    ]

    user_counter = 1  # ប្រើសម្រាប់រាប់ចំនួនសរុបនៃ User (Thread) ដែលបានបង្កើត

    # 🔥 Loop ដំណើរការឥតឈប់ឈរ បង្កើត User ថ្មីៗរហូតដល់បិទកម្មវិធី
    while True:
        # ទាញយក Proxy មកម្តង ១០០ IP ផ្សេងៗគ្នា
        proxies_pool = get_live_proxies_fast_api(limit=100)
        
        if proxies_pool and proxies_pool[0] != "":
            print(f"🎯 ទទួលបាន Proxy ថ្មីៗខុសគ្នាជំនាន់ថ្មីចំនួន {len(proxies_pool)} គ្រាប់!")
            
            for proxy in proxies_pool:
                if not proxy.strip():
                    continue
                    
                # ជ្រើសរើស User Agent ដោយចៃដន្យដើម្បីកុំឱ្យជាន់គ្នា
                random_agent = random.choice(user_agents_pool)
                
                # បង្កើត Thread ថ្មីសម្រាប់ User ម្នាក់ៗ
                t = threading.Thread(
                    target=watch_video_thread, 
                    args=(user_counter, target_video, random_agent, proxy)
                )
                t.start()  # 🔥 បើកឱ្យដំណើរការភ្លាមៗ (មិនប្រើ t.join() ទេ គឺលែងឱ្យវាហោះសេរី)
                
                user_counter += 1  # កើនចំនួន User បន្ទាប់
                
                # 💡 សម្រាកបន្តិច (០.៥ វិនាទី) មុននឹងបង្កើត User បន្ទាប់ ដើម្បីកុំឱ្យ CPU បុកឡើង ១០០% ខ្លាំងពេក
                time.sleep(0.5)
                
            print("\n🔄 បញ្ជូនកងទ័ព User ជុំនេះទៅអស់ហើយ! កំពុងទាញយក IP ថ្មីសម្រាប់បុកបន្តទៀត...")
        else:
            print("❌ គ្មានទិន្នន័យ Proxy ទេ! រង់ចាំ ១០ វិនាទី រួចសាកល្បងម្តងទៀត...")
            time.sleep(10)
