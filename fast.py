import requests
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def check_hash(line):
    match = re.search(r'(.*)\\(.*):(.*):(.*):(.*):(.*):(.*):(.*)', str(line))
    username = match.group(2)
    uid = match.group(3)
    nthash = match.group(5)
    first_five = nthash[:5]
    r = requests.get(f"https://api.nthashes.com/search/{first_five}")
    last_ten = nthash[-10:]
    resp = r.text
    code = r.status_code
    if last_ten in resp:
        with open("leaked_hashes.txt", "a") as f:
            f.write(f"[-] User {username}:{uid} with hash {nthash} has been leaked\n")
        print(f"[-] User {username}:{uid} with hash {nthash} has been leaked")
    elif code == 404:
        print(f"[+] User {username}:{uid} with hash {nthash} is not found in breachdb")
    else:
        print(f"[+] User {username}:{uid} with hash {nthash} is secured")
    #print(f"[+] check for {username}:{uid} with hash {nthash} completed successfully")

def hash_list():
    with open('ntlm_hashes.txt', 'r') as f:
        ntlm_hashes = f.readlines()
        with ThreadPoolExecutor() as executor:
            executor.map(check_hash, ntlm_hashes)

if __name__ == '__main__':
    start_time = datetime.now()
    hash_list()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))