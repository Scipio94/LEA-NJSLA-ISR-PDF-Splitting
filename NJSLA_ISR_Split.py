import pdfplumber as pdfp
import pypdf
from pypdf import PdfReader,PdfWriter
import string as str
import pandas as pd
import numpy as np

# importing tabular data
df = pd.read_excel(r"C:\Users\togarro\Documents\NJSLA_ISR_Split\SID_Other_ID_Export.xlsx") #--> file wuith SIDs and Local IDs

# creating SID len variable
df['State ID'] = df['State ID'].astype('string') #--> casting column data as a string
sid_len = len(df['State ID'][0]) #--> len of SID

# creating pdf_object
pdf_object = r"C:\Users\togarro\Documents\NJSLA_ISR_Split\pcspr25_NJ-034390-070_ISR_Spring_Grade_8_ELA.pdf"

# importing pdf using pypdf
reader = PdfReader(pdf_object)
writer = PdfWriter() #--> instantiating PDF Writer
doc_len = len(reader.pages)/2 #--> returning number of pages, divided by 2 to account for 2 page documents

print(f'The pdf document contains {round(doc_len)} documents')

# variables
search_text = 'ID: ' #--> substring search
search_text_len = len(search_text) #--> len object of the substring
sid = [] #--> creating an empty list

# opening pdf with pdfplumber and searching for text using a for loop
with pdfp.open(pdf_object) as pdf:
    for pages in pdf.pages: #--> range to extract text from odd pages
        text = pages.extract_text_simple() #--> creating string object
        start = text.find(search_text) #--> assigning the index of the search text to start variable
        end = start +  search_text_len + sid_len #--> assigning the index to stop extracting text to the end variable
        sid.append(text[start:end]) #--> appening extracted text from the PDF to list

# creating sid_df from list
sid_df = pd.DataFrame({'State ID':sid})

# removing blank values from the sid_df
sid_df = sid_df[sid_df['State ID'] != '']

# returning SID
sid_df['State ID'] = sid_df['State ID'].str.split(':').str[1].str.strip()

# casting as string
sid_df['State ID'] = sid_df['State ID'].astype('string')

# creating rows variable
rows = sid_df.shape[0]

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

    for i, page_num in enumerate(range(0,len(reader.pages),2)): #--> creating a range of all even pages of the document
        writer = PdfWriter() #--> resets the writer object in each iteration of the loop
        page_name = sid_merged_df['Local ID'].iloc[i]  #--> returns other id based on indexing of df based on 
        writer.add_page(reader.pages[page_num]) #--> adding first page to PDF export
        if page_num <= len(reader.pages): #--> conditional to ensure that that page num is not outside of index
            writer.add_page(reader.pages[page_num +1]) #--> adding second page to PDF export
        with open(f'/Users/togarro/NJSLA_ISR_Script_Exports/{page_name}.pdf','wb') as f: #--> file writing
                writer.write(f)
        count += 1 #--> adding 1 to the count object after each iteration through the for loop

    print(f'{count} PDF documents were successfully created')  #--> print statement to confirm that documents were created
            
else:
    print(f'There is an error, and the for loop was not excecuted.\nCheck to ensure that pages in the PDF and rows in the df are equal.\nPDF Page:{doc_len}\nDataframe Rows:{rows}')

        