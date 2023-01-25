import pyAesCrypt
"""The program encrypts/decrypts a text file with a symmetric block encryption algorithm AES."""

password = input('Введіть пароль для шифрування файлу: ')

# encryption process
pyAesCrypt.encryptFile('data.txt', 'data_in.txt.aes', password)

# decryption process
pyAesCrypt.decryptFile('data_in.txt.aes', 'dataout.txt', password)