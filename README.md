# PDF Splitting
Python script to split PDFs by page and label the output based on the primary key found on the PDF file.

## Packages
1. [pypdf](https://pypi.org/project/pypdf/) - used to split the pdf by page, label, and write create PDF files

~~~ python
import pypdf
from pypdf import PdfReader,PdfWriter

# importing pdf using pypdf
reader = PdfReader(r"C:\Users\togarro\Documents\NJSLA_ISR_Split\pcspr25_NJ-034390-070_ISR_Spring_Grade_8_ELA.pdf")
writer = PdfWriter() #--> instantiating PDF Writer
doc_len = len(reader.pages)/2 #--> returning number of pages, divided by 2 to account for 2 page documents

print(f'The pdf document contains {round(doc_len)} documents')

# creating count variable to coun the number of iteration through the loop
count = 0

# creating qa variable
qa = doc_len == rows #--> doc_len and rows should be equal

# conditional statement - if conditional met will run for loop, if not will print error statement
if qa == True:

# for loop to split into two page long PDF
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

~~~

### PDF Split Methodology
- Conditional statement to ensure that the for loop only runs if the conditions are met, if the condition is not met, an error statement is returned
- Using a for loop to iterate through and index each page using the enunmerate function. In this case, the page numbers are the range of pages in the reader object starting at zero and ending at the total number of pages increasing by two (2), e.g. 0,2,4,etc.
- Resetting the writer object after every iteration
- Creating a page_name object based on indexing
- Adding two pages to the writer object, the first page is page_num object.The second page is the page_num variable + 1 with a conditional statement ensuring that the page_num object does not exceed number of pages in the reader object.
- Exporting PDF file
- Count tracker to count the number of iterations through the for loop
- Printing a statment with the total numbers of documents created using the count object

2. [pdfplumber](https://pypi.org/project/pdfplumber/) - used to extract text from each page of the PDF based on searched substring text

~~~ python
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
~~~

3. [tqdm](https://pypi.org/project/tqdm/) - used to display a progrss tracker to guage progress of various parts of the ISR splitting process

~~~ python
from tqdm import tqdm

 with pdfp.open(pdf_object) as pdf:
        for i, pages in enumerate(tqdm(pdf.pages[::2],desc = 'Retrieving SIDs')): #--> extracting text from every other page and using tqdm to track progress
            text = pages.extract_text_simple() #--> creating string object
            start = text.find(search_text) #--> assigning the index of the search text to start variable
            end = start +  search_text_len + sid_len #--> assigning the index to stop extracting text to the end variable
            sid.append(text[start:end].split(':')[1].strip()) #--> appening and manipulating extracted text from PDF file
~~~

4. [pathlib](https://pypi.org/project/pathlib/) - used to access and perform actions on files wihin folders.

~~~ python
# creating folder_path variables
folder_path = Path(r"C:\Users\togarro\NJSLA_ISR_Script_Exports\SY_24_NJSLA_MAT_ISR")

# for loop leveraging iterdir() method to iterate over files in folder
for file_path in folder_path.iterdir():
    pdf_object = f"{file_path}"
    reader = PdfReader(pdf_object)
    writer = PdfWriter() #--> instantiating PDF Writer
    doc_len = len(reader.pages)//2 #--> returning number of pages, divided by 2 to account for 2 page documents
~~~ 
