from PyPDF2 import PdfWriter, PdfReader
from getpass import getpass
"""This application encrypts PDF files with specific password.
   Created a 'Lorem Ipsum.pdf' for fast testing."""

pdf_file_writer = PdfWriter()
pdf_file_reader = PdfReader('Lorem Ipsum.pdf')

for page in range(len(pdf_file_reader.pages)):
    print(page)
    pdf_file_writer.add_page(pdf_file_reader.pages[page])

password = getpass(prompt='Введіть пароль: ')
pdf_file_writer.encrypt(password)

with open('protected.pdf', 'wb') as file:
    pdf_file_writer.write(file)
