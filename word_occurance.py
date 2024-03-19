import os
import csv
import re
import logging
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(filename='pdf_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(file_path, search_word):
    occurrences = []
    total_occurrences = 0
    with open(file_path, 'rb') as file:
        try:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                matches = re.finditer(rf'\b{search_word}(?:[-\w]*)\b', text, re.IGNORECASE)
                for match in matches:
                    total_occurrences += 1
                    start_index = max(0, match.start() - 30)
                    end_index = min(len(text), match.end() + 30)
                    context = text[start_index:end_index]
                    all_words = re.findall(r'\b\w+\b', text, re.IGNORECASE) #tämä ehkä pois
                    all_words_str = ' '.join(all_words) #tämä ehkä pois
                    occurrences.append((file_path, context, all_words_str, total_occurrences)) # Jos otetaan pois niin tästäkin
                    logging.info(f"Found occurrence of '{search_word}' in '{file_path}' - Context: {context}")
        except Exception as e:
            logging.error(f"Error processing PDF file '{file_path}': {e}")
            if 'encrypted' in str(e).lower():
                logging.error(f"The file '{file_path}' is encrypted and cannot be processed.")
    return occurrences

def process_pdf_files_in_folder(folder_path, search_word):
    all_occurrences = []
    total_occurrences = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_file_path = os.path.join(folder_path, file_name)
            logging.info(f"Processing file: {pdf_file_path}")
            try:
                occurrences = extract_text_from_pdf(pdf_file_path, search_word)
                all_occurrences.extend(occurrences)
                total_occurrences += len(occurrences)
            except Exception as e:
                logging.error(f"Error processing file {pdf_file_path}: {e}")
    return all_occurrences, total_occurrences

# Search word
search_word = "add what you want to search"

# Directory containing PDF files

pdf_folder_path = 'Data/Aineisto'

# Process PDF files and extract occurrences
all_occurrences, total_occurrences = process_pdf_files_in_folder(pdf_folder_path, search_word)

# Write results to CSV file
with open(f'{search_word}_occurrences.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Filename', 'Context', 'All Words', 'Occurrences'])  # Include 'Occurrences' in the header
    for file_path, context, all_words_str, occurrences in all_occurrences:
        csv_writer.writerow([file_path, context, all_words_str, occurrences])  # Write filename, context, all words, and occurrences to CSV

logging.info(f"Total occurrences of '{search_word}' across all files: {total_occurrences}")
