import hashlib
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import getpass

def key_gen(passwords):
    password_provided = passwords
    password = password_provided.encode()
    salt = b'\xf7\xd3\x86D\xaa\x82\xaa\xf6\xd2\x1a.\xaa\xfe!{@'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def md5(string):
    return hashlib.md5(string.encode).hexdigest()

def encrypt(key,password):
    f = Fernet(key)
    encrypted = f.encrypt(password)
    return encrypted



def decrypt(key,encrypted):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted

def hash_pass(string):
    return hashlib.sha512(string.encode('utf-8')).hexdigest()


def user_exist(string):
    if os.path.exists('.PasSBox/'+string):
        return True
    else:
        return False




def sign_up():
    username = input('Enter username: ')
    password = getpass.getpass()
    key = key_gen(password)
    hashed_pass = hash_pass(password)
    if user_exist(username):
        print('username taken... \n Chose another')
        quit()
    file = open('.PasSBox/users.txt', 'a+')
    file.write(username+'\n')
    file.close()
    os.mkdir('.PasSBox/'+username)
    pfile = open('.PasSBox/'+username+'/'+username+'.mps', 'w')
    pfile.write(hashed_pass)
    pfile.close()
    log = open('.PasSBox/'+username+'/service.log', 'w')
    log.write('')
    log.close()
    rec_key = Fernet.generate_key()
    hashed_key = hash_pass(rec_key.decode())
    hkfile = open('.PasSBox/'+username+'/'+username+'.rkey', 'w')
    hkfile.write(hashed_key)
    hkfile.close()
    print('Profile Created sucessfully...')
    print('Note: This is your account recovery key, keep it safe \n')
    print(rec_key.decode())

def recover():
    username = input('Enter your username: ')
    rec_key = input('Enter recovery key: ')
    if user_exist(username):
        enc_key = hash_pass(rec_key)
        rkfile = open('.PasSBox/' + username + '/' + username + '.rkey', 'r')
        for hashh in rkfile:
            if str(hashh) not in enc_key:
                print('Key did not matched...')
                quit()
            else:
                New_password = getpass.getpass()
                hashed_pass = hash_pass(New_password)
                os.remove('.PasSBox/' + username + '/' + username + '.mps')
                pfile = open('.PasSBox/' + username + '/' + username + '.mps', 'w')
                pfile.write(hashed_pass)
                pfile.close()
                print('Password updated sucessfully...')
    else:
        print('No such user exists...')



def Chng_ms_ps():
    username = input('Enter username: ')
    old_pass = getpass.getpass()
    hashed_old = hash_pass(old_pass)
    if user_exist(username):
        oldpasfil = open('.PasSBox/' + username + '/' + username + '.mps', 'r')
        for pas in oldpasfil:
            if pas != hashed_old:
                print('Access Denied!!!')
                quit()
            else:
                os.remove('.PasSBox/' + username + '/' + username + '.mps')
                newpas = getpass.getpass()
                new_pass_hash = hash_pass(newpas)
                newpasfile = open('.PasSBox/' + username + '/' + username + '.mps', 'w')
                newpasfile.write(new_pass_hash)
                newpasfile.close()
                print('Password updated sucessfully...')
                pause = input()
    else:
        print('No such user exists...')
        pause = input()


def store_pass(username, key):
    service = input('Enter service name (facebook, etc): ')
    password = input('Enter Password: ')
    enc_pass = encrypt(key, password.encode())
    ufile = open('.PasSBox/'+username+'/'+service+'.pas', 'wb')
    ufile.write(enc_pass)
    ufile.close()
    service_log = open('.PasSBox/'+username+'/service.log', 'a+')
    service_log.write(service+'\n')
    service_log.close()
    print('Password Stored Sucessfully...')
    pause = input()



def service_exists(username,service):
    with open('.PasSBox/'+username+'/service.log', 'r') as file:
        data = file.read()
        for serv in data:
            if serv == service:
                return True
            else:
                return False
    file.close()


def view_pass(username, key):
    service = input('Enter service name: ')
    if service_exists(username,service):
        with open('.PasSBox/' + username + '/' + service + '.pas', 'rb') as file:
            data = file.read()
            dec = decrypt(key, data)
            print('Password: ', dec.decode())
            pause = input()
            file.close()
    else:
        print('No such service exists')
        pause = input()



def view_srvices(username):
    file = open('.PasSBox/'+username+'/service.log', 'r')
    print('[Services]')
    for service in file:
        print(service)
    file.close()
    pause = input()


def remove_acc():
    print('Account Remove'.upper())
    username = input('Enter username:')
    password = getpass.getpass()
    if user_exist(username):
        hashed_pass = hash_pass(password)
        pfile = open('.PasSBox/'+username+'/'+username+'.mps')
        stored_hash =  pfile.read()
        if stored_hash == hashed_pass:
            print('Do you really want to remove your account? \nAfter this oprestion none of your data will be left!')
            print('If you are sure then type "Yes do it"')
            us_ch = input('Remove Account? ')
            if us_ch == "yes do it":
                os.system('rm -rf .PasSBox/'+username)
            else:
                print('Aborting...')
                quit()
        else:
            print('Access Denied!!!')
    else:
        print('No such user exists...')
        quit()



def bye_banner():
    os.system('clear')
    print('-'*50)
    print(' Thanks for using PasSBox \n Author: M.Nauman Azeem \n Report any bug at xeroxxhah@pm.me \n Bye...')
    print('-'*50)



def menu(username, key):
    while True:
        os.system('clear')
        banner()
        print('Welcome ', username)
        print('\n 1:Store Password \n 2:View Password \n 3:View Services \n 4:Change Master Password \n 5:exit')
        option = input('Choose Option: ')
        if option == '1':
            store_pass(username, key)
        elif option == '2':
            view_pass(username, key)
        elif option == '3':
            view_srvices(username)
        elif option == '4':
            Chng_ms_ps()
        elif option == '5':
            bye_banner()
            quit()
        else:
            print('Wrong Option')


def sign_in():
    username = input('Enter username: ')
    password = getpass.getpass()
    hashed_pass = hash_pass(password)
    key = key_gen(password)
    if user_exist(username):
        pfile = open('.PasSBox/'+username+'/'+username+'.mps', 'r')
        for h1sh in pfile:
            if hashed_pass != h1sh:
                print('Access Denied... \n nyc try...')
                quit()
            else:
                menu(username, key)
        pfile.close()
    else:
        print(username+' does not exist \n Signup first')



def banner():
    print('*'*50)
    print('PasSBox by x1vi0r')
    print('Safe and Secure way to store your passwords')
    print('*'*50)


def main():
    banner()
    opt = input('\n [1]---(Sign up) \n [2]---(Sign in) \n [3]---(Recover Account) \n [4]---(Remove Account)\n [5]---(Exit)\n [*]___\n       |-----|---\n       |-----|--- ')
    if opt == '1':
        sign_up()
    elif opt == '2':
        sign_in()
    elif opt == '3':
        recover()
    elif opt == '4':
        remove_acc()
    elif opt == '5':
        quit()
    else:
        print('Wrong option!!!')

main()
