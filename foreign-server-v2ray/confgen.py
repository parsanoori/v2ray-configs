#!/usr/bin/env python3

import os

# for qr code generation
import qrcode

# for parsing json data
import json


domain = 'FOREIGNDOMAIN'
port = 443
path = '/trojan'
security = 'tls'
type = 'ws'


def gen_url_v2rayng(email, password):
    return (
        f'trojan://{password}@{domain}:{port}?path={path.replace("/", "%2F")}&security=tls&type=ws#{email}\n'
    )

def gen_url_shadowrocket(email, password):
    return (
        f'trojan://{password}@{domain}:{port}?allowInsecure=1&tfo=1&plugin=obfs-local;'
        f'obfs=websocket;obfs-host=;obfs-uri={path}#{email}\n'
    )

def print_qr(qr):
    # Get the QR code image as a matrix of boolean values
    qr_matrix = qr.get_matrix()

    # print the qr code in the terminal
    for row in qr_matrix:
        for col in row:
            if col:
                print('██', end='')
            else:
                print('  ', end='')
        print()

def url_to_qr(url, filename):
    # generate the qr code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True) 

    # save the qr code in a png file
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

    return qr


def gen_outputs(email, password, do_print=False):
    # generate the urls
    url_v2rayng = gen_url_v2rayng(email, password)
    url_shadowrocket = gen_url_shadowrocket(email, password)

    # save the text files
    with open(f'textv2ng/{email}.txt', 'w') as f:
        f.write(url_v2rayng)

    # save the text files
    with open(f'textsr/{email}.txt', 'w') as f:
        f.write(url_shadowrocket)


    # generate the qr code for v2rayng
    qr_v2rayng = url_to_qr(url_v2rayng, 'qrv2ng/' + email + '.png')

    # generate the qr code for shadowrocket
    qr_shadowrocket = url_to_qr(url_shadowrocket, 'qrsr/' + email + '.png')

    if do_print:
        print(f'Config for {email}')
        print(f'Password: {password}')
        print(f'URL for v2rayng: {url_v2rayng}')
        print(f'URL for shadowrocket: {url_shadowrocket}')
        
        print('QR code for v2rayng:')
        print_qr(qr_v2rayng)

        print('QR code for shadowrocket:')
        print_qr(qr_shadowrocket)


def gen_configs():
    # open the config file
    with open('config.json') as json_file:
        data = json.load(json_file)
    
        # iterate over inbounds/settings/clients and generate the qr code
        for client in data['inbounds'][0]['settings']['clients']:

            # generate the config
            print(f'Generating config for {client["email"]}')
            gen_outputs(client['email'], client['password'], do_print=False)



def get_config(entry):
    # open the config file
    with open('config.json') as json_file:
        data = json.load(json_file)

        # iterate over inbounds/settings/clients and generate the qr code
        for client in data['inbounds'][0]['settings']['clients']:
            if entry in client['email']:

                # generate the config
                print(f'Generating config for {client["email"]}')
                gen_outputs(client['email'], client['password'], do_print=True)



if __name__ == '__main__':
    # create the directory for saving the qrcodes if it doesn't exist
    if not os.path.exists('qrv2ng'):
        os.makedirs('qrv2ng')

    # create the directory for saving the texts if it doesn't exist
    if not os.path.exists('textv2ng'):
        os.makedirs('textv2ng')

    # create the directory for the qrcodes if it doesn't exist
    if not os.path.exists('qrsr'):
        os.makedirs('qrsr')

    # create the directory for the texts if it doesn't exist
    if not os.path.exists('textsr'):
        os.makedirs('textsr')


    # user options: 1. generate all configs 2. generate a specific config
    print('Welcome to the trojan config generator')
    print('1. generate all configs')
    print('2. generate a specific config')
    option = input('Enter your option: ')

    if option == '1':
        gen_configs()
    elif option == '2':
        entry = input('Enter the email of the client or part of it: ')
        get_config(entry)
    else:
        print('Invalid option')
        exit(1)






