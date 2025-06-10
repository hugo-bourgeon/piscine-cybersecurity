# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_opt.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/10 15:57:28 by hubourge          #+#    #+#              #
#    Updated: 2025/06/10 17:56:47 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import sys
import os
import hmac
import hashlib
import struct
import time
from cryptography.fernet import Fernet
    
def get_content_file(filepath):
    try:
        with open(filepath, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: Could not read file '{args.file}'.")
        sys.exit(1)
    
    return file_content

def save_encrypted_key(hex_key):
    try:
        # Generate key
        encryption_key = Fernet.generate_key()
        fernet = Fernet(encryption_key)
        
        # Encrypt key
        encrypted_hex_key = fernet.encrypt(hex_key.encode())
        
        # Save
        with open("ft_otp.key", "wb") as f:
            f.write(encryption_key + b":" + encrypted_hex_key)
        
        return True
        
    except Exception as e:
        print(f"Error: Could not save key - {e}")
        return False

def handle_g_mode(filepath):
    file_content = get_content_file(filepath)

    # Del leading and whitespace
    file_content = file_content.strip()

    # Check length
    if (len(file_content) != 64):
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        sys.exit(1)

    # Hexadecimal validation
    try:
        int(file_content, 16)
    except ValueError:
        print("./ft_otp: error: key must contain only hexadecimal characters.")
        sys.exit(1)

    # Save key
    if save_encrypted_key(file_content):
        print("Key was successfully saved in ft_otp.key")
    else:
        sys.exit(1)
        
def hotp(key, counter):
    # 1: Generate HMAC-SHA1
    key_bytes = bytes.fromhex(key)                                          # Convert hex to bytes
    counter_bytes = struct.pack(">Q", counter)                              # Convert counter to bytes (big-endian)
    hmac_digest = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest() # Generate HMAC-SHA1
    
    # 2: Truncate
    offset = hmac_digest[-1] & 0x0f                                     # Last 4 bits of last byte
    truncated = struct.unpack(">I", hmac_digest[offset:offset+4])[0]    # Extract 4 bytes, convert to int
    truncated &= 0x7fffffff                                             # Only positive value
    
    # 3: Calculate HOTP value
    hotp_value = truncated % 1000000 # 6-digit OTP
    
    return f"{hotp_value:06d}"

def load_encrypted_key(filepath):
    try:
        with open(filepath, "rb") as f:
            content = f.read()
            encryption_key, encrypted_hex_key = content.split(b":", 1)
        
        fernet = Fernet(encryption_key)
        hex_key = fernet.decrypt(encrypted_hex_key).decode()
        return hex_key
    except Exception as e:
        print(f"./ft_otp: error: could not read or decrypt key - {e}")
        sys.exit(1)

def handle_k_mode(filepath):
    if not os.path.exists(filepath):
        print("./ft_otp: error: no key found. Please use -g mode to generate a key.")
        sys.exit(1)

    hex_key = load_encrypted_key(filepath)
    counter = int(time.time()) // 30
    otp_code = hotp(hex_key, counter)
    
    print(otp_code)
    
def parse_args():
    parser = argparse.ArgumentParser()
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g",
                        action="store_true",
                        help="Enable -g mode")
    group.add_argument("-k",
                        action="store_true",
                        help="Enable -k mode")
    parser.add_argument("file",
                        help="File to process")

    args = parser.parse_args()

    return args
    
def main():
    args = parse_args()

    if (args.g):
        handle_g_mode(args.file)
    elif (args.k):
        handle_k_mode(args.file)

if __name__ == "__main__":
    main()