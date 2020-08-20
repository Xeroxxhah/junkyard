import hashlib
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


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
    with open('.PasSBox/users.txt', 'r') as file:
        data = file.read()
        if string in data:
            return True
        else:
            return False



def sign_up():
    username = input('Enter username: ')
    password = input('Enter Master Password: ')
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
    print('Profile Created sucessfully...')



def Chng_ms_ps():
    username = input('Enter username: ')
    old_pass = input('Enter Old Password: ')
    hashed_old = hash_pass(old_pass)
    if user_exist(username):
        oldpasfil = open('.PasSBox/' + username + '/' + username + '.mps', 'r')
        for pas in oldpasfil:
            if pas != hashed_old:
                print('Access Denied!!!')
                quit()
            else:
                os.remove('.PasSBox/' + username + '/' + username + '.mps')
                newpas = input('Enter New Password:')
                new_pass_hash = hash_pass(newpas)
                newpasfile = open('.PasSBox/' + username + '/' + username + '.mps', 'w')
                newpasfile.write(new_pass_hash)
                newpasfile.close()
                print('Password updated sucessfully...')
    else:
        print('No such user exists...')


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


def service_exists(username,service):
    with open('.PasSBox/'+username+'/service.log', 'r') as file:
        data = file.read()
        if service in data:
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
            file.close()
    else:
        print('No such service exists')



def view_srvices(username):
    file = open('.PasSBox/'+username+'/service.log', 'r')
    for service in file:
        print(service)
    file.close()






def menu(username, key):
    print('Welcome ',username)
    print('\n 1:Store Password \n 2:View Password \n 3:View Services \n 4:Change Master Password')
    option = input('Choose Option: ')
    if option == '1':
        store_pass(username, key)
    elif option == '2':
        view_pass(username, key)
    elif option == '3':
        view_srvices(username)
    elif option == '4':
        Chng_ms_ps()
    else:
        print('Wrong Option')



def sign_in():
    username = input('Enter username: ')
    password = input('Enter Master password: ')
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
    opt = input('\n 1:Sign up \n 2:Sign in \n')
    if opt == '1':
        sign_up()
    elif opt == '2':
        sign_in()
    else:
        print('Wrong option!!!')

main()
