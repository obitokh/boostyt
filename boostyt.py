import time
import random
import threading
import uc_auth_proxy_selenium as uc  # 🔥 ប្តូរមកប្រើវិធីគាំទ្រ Proxy មាន Password ឱ្យបានត្រឹមត្រូវ
import os

driver_lock = threading.Lock()

def watch_video_thread(thread_id, video_url, agent, proxy_line):
    # ទម្រង់ទិន្នន័យ៖ user:pass@ip:port
    try:
        auth_part, ip_part = proxy_line.strip().split('@')
        username, password = auth_part.split(':')
        proxy_ip_port = ip_part
    except Exception:
        print(f"⚠️ [Thread {thread_id}] ទម្រង់ Proxy មិនត្រឹមត្រូវ៖ {proxy_line}")
        return

    print(f"🚀 [Thread {thread_id}] ចាប់ផ្តើមដំណើរការជាមួយ Premium IP: {proxy_ip_port}")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--mute-audio")
    options.add_argument(f"user-agent={agent}")
    
    # កំណត់ទិន្នន័យ Proxy ជាមួយ Username និង Password ឱ្យបានត្រឹមត្រូវ
    options.add_argument(f"--proxy-server=http://{proxy_ip_port}")
    
    # Arguments ចាំបាច់សម្រាប់ឱ្យ Linux លើ GitHub Actions រត់បានរលូនមិនគាំង
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    if os.name == 'nt': 
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    driver = None
    try:
        with driver_lock:
            print(f"🛠️ [Thread {thread_id}] កំពុងរៀបចំ និងបើក Browser...")
            
            # ប្រើប្រាស់ version_main=149 ឱ្យត្រូវគ្នានឹង Chrome របស់ GitHub Server
            # បន្ថែម seleniumwire_options សម្រាប់ហៅផ្ទាំងបញ្ចូល Username/Password អូតូ
            wire_options = {
                'proxy': {
                    'http': f'http://{username}:{password}@{proxy_ip_port}',
                    'https': f'https://{username}:{password}@{proxy_ip_port}',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            driver = uc.Chrome(options=options, version_main=149, seleniumwire_options=wire_options)
            time.sleep(2)
            
        driver.set_page_load_timeout(45)
        driver.get(video_url)
        
        watch_time = random.randint(15, 25)
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

# 🔥 មុខងារថ្មីសម្រាប់អាន Proxy ផ្ទាល់ពី File ដែលអ្នកបានផ្តល់ជូន
def load_proxies_from_file(file_name="proxyscrape_premium_http_proxies.txt"):
    print(f"\n📂 កំពុងអានទិន្នន័យ Premium Proxy ពីឯកសារ {file_name}...")
    if not os.path.exists(file_name):
        print(f"❌ រកមិនឃើញឯកសារ {file_name} ឡើយ!")
        return []
        
    with open(file_name, "r") as f:
        proxies = [line.strip() for line in f.readlines() if line.strip() and "@" in line]
    
    # ធ្វើការលាយបញ្ជីឱ្យចៃដន្យដើម្បីកុំឱ្យរត់ជាន់លំដាប់គ្នាដដែលៗ
    random.shuffle(proxies)
    return proxies

# ==================== ដំណើរការកម្មវិធីមេ (INFINITE AUTO-RUN) ====================
if __name__ == "__main__":
    target_video = "https://youtu.be/YuWlVPwXnsc?si=eAgDccQc5GPXVR0N"
    
    user_agents_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/21000101 Firefox/119.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    ]

    user_counter = 1  

    while True:
        # ហៅអាន Proxy ពី File មកប្រើម្តងទាំងអស់
        proxies_pool = load_proxies_from_file()
        
        if proxies_pool:
            print(f"🎯 ចាប់ផ្តើមបុកដំណើរការជាមួយ Premium Proxy ទាំងចំនួន {len(proxies_pool)} គ្រាប់!")
            
            for proxy in proxies_pool:
                random_agent = random.choice(user_agents_pool)
                
                t = threading.Thread(
                    target=watch_video_thread, 
                    args=(user_counter, target_video, random_agent, proxy)
                )
                t.start()  
                
                user_counter += 1  
                time.sleep(1.5)  # សម្រាក ១.៥ វិនាទី ដើម្បីកុំឱ្យ CPU Server គាំងពេលបើក Premium Proxy ច្រើនពេក
                
            print("\n🔄 បានប្រើប្រាស់បញ្ជី Proxy ក្នុងឯកសារអស់មួយជុំហើយ! កំពុងចាប់ផ្តើមជុំថ្មីឡើងវិញ...")
        else:
            print("❌ គ្មានទិន្នន័យ Proxy ក្នុង File ទេ! រង់ចាំ ៣០ វិនាទី...")
            time.sleep(30)
