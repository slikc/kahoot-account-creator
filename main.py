#https://github.com/slikc
import          requests
import          uuid
import          base64
import          time
import          random
import          string
from colorama import Fore
requests.packages.urllib3.disable_warnings()

namevar = input('Name of bots ==> ')
passtouse = input('Password of bots ==> ')

ratelimitvios = 0

def generate_hjsession():
    timestamp = str(round(time.time() * 1000))
    data = {"id": str(uuid.uuid4()), "created": timestamp, "inSample": False}
    return base64.b64encode(bytes(str(data), 'utf-8')).decode()

def gen_uuid():
    return str(uuid.uuid4())

def gen_username():
    randompart = ''.join(random.choice(string.digits) for i in range(6))
    return namevar + '_' + randompart

def main():
    global ratelimitvios
    if ratelimitvios == 4:
        print(f'{Fore.RED}[RATELIMIT]{Fore.RESET} Rate limit hit 4 times, waiting 10 seconds')
        time.sleep(10)
        ratelimitvios = 0
    time.sleep(0.1)
    st = time.time()
    session = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'cookie': 'generated_uuid={0}; hjsession={1}'.format(gen_uuid(), generate_hjsession())
    }
    #https://create.kahoot.it/rest/users
    headers = {
        'referer': 'https://create.kahoot.it/auth/register/signup-options',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'cookie': 'generated_uuid={0}'.format(gen_uuid())
    }
    json1 = {
        'birthday': [
            2000,
            4,
            19
        ],
        'consents': {
            'internalMarketing': False,
            'termsConditions': True
        },
        'email': str(random.randint(100000, 999999))+'_slikc@gmail.com',
        'locale': 'en',
        'password': passtouse, # anything (must meet requirements)
        'primary_usage': 'social', # change these to change the account type
        'primary_usage_type': 'FAMILY', # this too
        'username': gen_username()
    }
    r = session.post('https://create.kahoot.it/rest/users', headers=headers, verify=False, json=json1)
    if r.status_code != 500:
        if 'error' in r.text:
            print(f'{Fore.YELLOW}[{r.status_code}]{Fore.RESET} Error Creating Account: {r.text}')
            return
        et = time.time()
        print(f'{Fore.GREEN}[{r.status_code}]{Fore.RESET} {json1["email"]}:{json1["password"]} - {et-st}s')
        UUID = r.json()['user']['uuid']
        json = {
            'grant_type': 'password',
            'username': json1['email'],
            'password': json1['password']
        }
        r = session.post('https://create.kahoot.it/rest/authenticate', headers=headers, json=json, verify=False)
        try:
            if r.json()['user']['activated'] == True:
                with open('accounts.txt', 'a') as f:
                    f.write(f'{json1["email"]}:{json1["password"]}\n')
                print(f'{Fore.GREEN}[{r.status_code}]{Fore.RESET} Account Activated Successfully!')
        except:
            if r.json()['error'] == 'V_ERROR':
                print(f'{Fore.YELLOW}[{r.status_code}]{Fore.RESET} Account failed to activate: {r.json()["reason"]}')
                ratelimitvios += 1
            else:
                print(f'{Fore.YELLOW}[{r.status_code}]{Fore.RESET} Account failed to activate: {r.text}')
    else:
        print(f'{Fore.YELLOW}[{r.status_code}]{Fore.RESET} Error Creating Account: {r.json()["error"]}')
    print()

threads = 1

while True:
    main()

# while True:
#     if threading.active_count() <= threads:
#         try:
#             threading.Thread(target = main).start()
#         except:
#             pass
