from pathlib import Path
import pdfplumber as pdfp
import pypdf
from pypdf import PdfReader,PdfWriter
import string as str
import pandas as pd
import numpy as np
from tqdm import tqdm

# importing tabular data
df = pd.read_excel(r"C:\Users\togarro\Documents\NJSLA_ISR_Split\SID_Other_ID_Export.xlsx") #--> file wuith SIDs and Local IDs

# creating SID len variable
df['State ID'] = df['State ID'].astype('string') #--> casting column data as a string
df['Local ID'] = df['Local ID'].astype('string')
sid_len = len(df['State ID'][0]) #--> len of SID

# variables
search_text = 'ID: ' #--> substring search
search_text_len = len(search_text) #--> len object of the substring
sid = [] #--> creating an empty list

# creating folder_path variables
folder_path = Path(r"C:\Users\togarro\NJSLA_ISR_Script_Exports\SY_24_NJSLA_MAT_ISR")

# creating qa variable
length_qa = 0

# for loop leveraging iterdir() method to iterate over files in folder
for file_path in folder_path.iterdir():
    pdf_object = f"{file_path}"
    reader = PdfReader(pdf_object)
    writer = PdfWriter() #--> instantiating PDF Writer
    doc_len = len(reader.pages)//2 #--> returning number of pages, divided by 2 to account for 2 page documents
    
    # opening pdf with pdfplumber and searching for text using a for loop
    with pdfp.open(pdf_object) as pdf:
        for i, pages in enumerate(tqdm(pdf.pages[::2],desc = 'Retrieving SIDs')): #--> extracting text from every other page and using tqdm to track progress
            text = pages.extract_text_simple() #--> creating string object
            start = text.find(search_text) #--> assigning the index of the search text to start variable
            end = start +  search_text_len + sid_len #--> assigning the index to stop extracting text to the end variable
            sid.append(text[start:end].split(':')[1].strip()) #--> appening and manipulating extracted text from PDF file
    
    #totaling sids in sid list through each iteration 
    length_qa += doc_len

    
     #qa
    if length_qa == len(sid):
        # error handling
        try:
            for i, page_num in enumerate(tqdm(range(0,len(reader.pages),2), desc = 'Splitting NJSLA ISRs')): #--> creating a range of all even pages of the document
                writer = PdfWriter() #--> resets the writer object in each iteration of the loop
                page_name = df[df['State ID'].isin(sid)].reset_index(drop = True)['Local ID'].iloc[i]  #--> returns other id based on indexing of df based on 
                writer.add_page(reader.pages[page_num]) #--> adding first page to PDF export
                if page_num <= len(reader.pages): #--> conditional to ensure that that page num is not outside of index
                    writer.add_page(reader.pages[page_num +1]) #--> adding second page to PDF export
                with open(f'/Users/togarro/NJSLA_ISR_Script_Exports/SY_24_MATH/{page_name}.pdf','wb') as f: #--> file writing
                       writer.write(f)
        # returning the missing SID when there is an error
        except:
            print(f'The State ID {sid[i]} is missing from the sid export!')
