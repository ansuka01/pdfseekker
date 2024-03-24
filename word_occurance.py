import os
import re
import logging
import csv
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(filename='pdf_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of search words



words = ['']
#Directory containing PDF files
pdf_folder_path = 'Aineisto_laajennettu'




#Käydään läpi pdf-kohtaisesti ja yritetään löytää sanalistan mukaan osumia.
def extract_text_from_pdf(file_path, search_words):
    occurrences_per_file = []
    with open(file_path, 'rb') as file:
        try:
            pdf_reader = PdfReader(file)
            #Ensin per sivu ja siihen indeksin avulla sivnumero
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                text = page.extract_text()
                #Jokaiselle sivulle haetaan sanakohtainesti mätsi
                for search_word in search_words:
                    #loopataan mätsit
                    matches = re.finditer(rf'(?<!\S){search_word}\S*', text, re.IGNORECASE)
                    for match in matches:
                        start_index_word = match.start() 
                        end_index_word = match.end() 
                        word_found = text[start_index_word:end_index_word].strip() 
                        start_index_context = max(0, match.start() - 100)
                        end_index_context = min(len(text), match.end() + 100)
                        context = text[start_index_context:end_index_context].replace('\n', ' ').replace(',', '')
                        occurrences_per_file.append((context, word_found, page_num)) 
                        logging.info(f"Found occurrence of '{search_word}' in '{file_path}' - Context: {context}")
        except Exception as e:
            logging.error(f"Error processing PDF file '{file_path}': {e}")
            if 'encrypted' in str(e).lower():
                logging.error(f"The file '{file_path}' is encrypted and cannot be processed.")
    return occurrences_per_file


#Loopataan koko folderi läpi.
def process_pdf_files_in_folder(folder_path, search_words):
    all_occurrences = []
    total_occurrences = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_file_path = os.path.join(folder_path, file_name)
            #Tavoitteena etsiä pdf-päätteiset filut ja luoda oikealaiset kokonaiset polut jota käyttää.
            logging.info(f"Processing file: {pdf_file_path}")
            try:
                occurrences_per_looped_file = [] 
                for word in search_words:
                    word_occurrences = extract_text_from_pdf(pdf_file_path, [word]) #Haetaan word_occurancet. Käytetään aiemmin tehtyä funkkaria, joka hakee jokaisesta filusta annetun sanan avulla.
                    occurrences_per_looped_file.extend(word_occurrences) #Lisätään occurances
                    total_occurrences += len(word_occurrences)
                all_occurrences.extend([(context, word, file_name, page_num) for context, word, page_num in occurrences_per_looped_file])
            except Exception as e:
                logging.error(f"Error processing file {pdf_file_path}: {e}")
    return all_occurrences, total_occurrences

# Loopataan kaikki
for word in words:
    all_occurrences, total_occurrences = process_pdf_files_in_folder(pdf_folder_path, [word])
    with open(f'{word}_occurrences.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', 'Context', 'Word', 'Page Number']) 
        for context, found_word, filename, page_num in all_occurrences:
            csv_writer.writerow([filename, context, found_word, page_num])  
    logging.info(f"Total occurrences of '{word}' across all files: {total_occurrences}")
    logging.info(all_occurrences)
