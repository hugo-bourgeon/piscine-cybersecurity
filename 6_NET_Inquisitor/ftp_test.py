# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ftp_test.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/23 17:24:19 by hubourge          #+#    #+#              #
#    Updated: 2025/06/24 16:37:19 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ftplib import FTP
import time

FTP_SERVER = "10.12.248.141"  # IP du serveur FTP
FTP_PORT = 21
FTP_USER = "testftp"
FTP_PASS = "testftp"

def ftp_test():
    ftp = FTP()
    ftp.connect(FTP_SERVER, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)

    # Création du fichier test en mode binaire
    with open("test_upload.txt", "wb") as f:
        f.write(b"FTP upload test.\n")

    # Upload du fichier
    with open("test_upload.txt", "rb") as f:
        ftp.storbinary("STOR test_upload.txt", f)
        print("-> File uploaded.")

    time.sleep(1)

    # Téléchargement du fichier
    with open("test_download.txt", "wb") as f:
        ftp.retrbinary("RETR test_upload.txt", f.write)
        print("-> File downloaded.")

    ftp.quit()
    print("-> FTP test completed.")

if __name__ == "__main__":
    ftp_test()