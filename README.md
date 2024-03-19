# pdfseekker

I had a problem where i had over 100+ pdf files that where all hundreds of pages long. I wanted to check how many times a word occurances in each file and then grab the word + what exists before and after the word + the occurances.


Initially, I experimented with incorporating tkinter, but it seemed unnecessary since the code itself is quite straightforward. It begins by converting the PDFs to text format, then utilizes regular expressions to locate the desired word. Once found, it extracts the word along with the preceding and following 30 characters. This process is repeated for every file in the folder.

During random spot checks on word counts, the results consistently matched, indicating the code's reliability. While the PDF converter functions reasonably well, performance could be enhanced by using file formats more easily convertible to text, such as Word or plain text.






Oh, and if someone is desperate enough to use any part of this in a production environment, please don't.
