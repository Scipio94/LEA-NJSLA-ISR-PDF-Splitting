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

# creating pdf_object
pdf_object = r"C:\Users\togarro\NJSLA_ISR_Script_Exports\SY_24_NJSLA_MAT_ISR\pcspr24_NJ-034390-070_ISR_Spring_Grade_7_Mathematics_TestingOrg.pdf"

# importing pdf using pypdf
reader = PdfReader(pdf_object)
writer = PdfWriter() #--> instantiating PDF Writer
doc_len = len(reader.pages)//2 #--> returning number of pages, divided by 2 to account for 2 page documents

print(f'The pdf document contains {round(doc_len)} documents')

# variables
search_text = 'ID: ' #--> substring search
search_text_len = len(search_text) #--> len object of the substring
sid = [] #--> creating an empty list

# opening pdf with pdfplumber and searching for text using a for loop
with pdfp.open(pdf_object) as pdf:
    for i, pages in enumerate(tqdm(pdf.pages[::2],desc = 'Retrieving SIDs')): #--> extracting text from every other page and using tqdm to track progress
        text = pages.extract_text_simple() #--> creating string object
        start = text.find(search_text) #--> assigning the index of the search text to start variable
        end = start +  search_text_len + sid_len #--> assigning the index to stop extracting text to the end variable
        sid.append(text[start:end].split(':')[1].strip()) #--> appening and manipulating extracted text from PDF file
        
# create a dataframe for extracted SIDs
sid_df = pd.DataFrame({'State ID':sid})

# reseting index
sid_df = sid_df.reset_index(drop = True)

# merging dfs based on SID
sid_merged_df = sid_df.merge(df, how = 'inner', on = 'State ID')

# statement to see if there were any sids missing
print(f'There are {sid_df[~sid_df['State ID'].isin(df['State ID'])].shape[0]} SIDs missing from the merge file')

# creating count variable to coun the number of iteration through the loop
count = 0

# creating qa variable
qa = doc_len == rows #--> doc_len and rows should be equal

# conditional statement - if conditional met will run for loop, if not will print error statement
if qa == True:

    for i, page_num in enumerate(tqdm(range(0,len(reader.pages),2), desc = 'Splitting NJSLA ISRs')): #--> creating a range of all even pages of the document
        writer = PdfWriter() #--> resets the writer object in each iteration of the loop
        page_name = sid_merged_df['Local ID'].iloc[i]  #--> returns other id based on indexing of df based on 
        writer.add_page(reader.pages[page_num]) #--> adding first page to PDF export
        if page_num <= len(reader.pages): #--> conditional to ensure that that page num is not outside of index
            writer.add_page(reader.pages[page_num +1]) #--> adding second page to PDF export
        with open(f'/Users/togarro/NJSLA_ISR_Script_Exports/SY_24_ELA/{page_name}.pdf','wb') as f: #--> file writing
                writer.write(f)
        count += 1 #--> adding 1 to the count object after each iteration through the for loop

    print(f'{count} PDF documents were successfully created')  #--> print statement to confirm that documents were created
            
else:
    print(f'There is an error, and the for loop was not excecuted.\nCheck to ensure that pages in the PDF and rows in the df are equal.\nPDF Page:{doc_len}\nDataframe Rows:{rows}')
        
