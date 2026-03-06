{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "741af28c-54d1-4cba-843b-1de3e794deb3",
   "metadata": {},
   "source": [
    "# LEA NJSLA ISR Batch PDF Splitting\n",
    "\n",
    "The goal of this python script is to split NJSLA ISRs and create a two page pdf and name the PDF with a student's State ID within a folder containing multiple ISR files. The following packages were used to complete this task:\n",
    "\n",
    " Creating a script to split PDFs and assingn the local id as the file name for the ouput. The following packages were used below:\n",
    "- [pdfplumber](https://pypi.org/project/pdfplumber/)\n",
    "- [pypdf](https://pypi.org/project/pypdf/)\n",
    "- [tqdm](https://pypi.org/project/tqdm/)\n",
    "\n",
    "This script focuses on extracting text via a searching for a substring on the document"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "a53e4c6a-9278-4135-9126-ea8340c13e9a",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "from pathlib import Path\n",
    "import pdfplumber as pdfp\n",
    "import pypdf\n",
    "from pypdf import PdfReader,PdfWriter\n",
    "import string as str\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "from tqdm import tqdm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "6e1c04f8-a0d3-4f16-b3a4-4ecaf4709197",
   "metadata": {},
   "outputs": [],
   "source": [
    "# importing tabular data\n",
    "df = pd.read_excel(r\"C:\\Users\\togarro\\Documents\\NJSLA_ISR_Split\\SID_Other_ID_Export.xlsx\") #--> file wuith SIDs and Local IDs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "2a356d03-602e-4e7f-a0b7-46f00a588fb2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# creating SID len variable\n",
    "df['State ID'] = df['State ID'].astype('string') #--> casting column data as a string\n",
    "df['Local ID'] = df['Local ID'].astype('string')\n",
    "sid_len = len(df['State ID'][0]) #--> len of SID"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "f4101515-bd62-41ce-9efd-5be96591e00b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# variables\n",
    "search_text = 'ID: ' #--> substring search\n",
    "search_text_len = len(search_text) #--> len object of the substring\n",
    "sid = [] #--> creating an empty list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "142d2bf2-7c6f-4cfe-8b47-accb63d57a76",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Retrieving SIDs: 100%|██████████| 176/176 [01:07<00:00,  2.60it/s]\n",
      "Splitting NJSLA ISRs: 100%|██████████| 176/176 [00:10<00:00, 16.85it/s]\n",
      "Retrieving SIDs: 100%|██████████| 3/3 [00:01<00:00,  2.02it/s]\n",
      "Splitting NJSLA ISRs: 100%|██████████| 3/3 [00:00<00:00, 14.00it/s]\n",
      "Retrieving SIDs: 100%|██████████| 1/1 [00:00<00:00,  1.42it/s]\n",
      "Splitting NJSLA ISRs: 100%|██████████| 1/1 [00:00<00:00, 10.68it/s]\n"
     ]
    }
   ],
   "source": [
    "# creating folder_path variables\n",
    "folder_path = Path(r\"C:\\Users\\togarro\\NJSLA_ISR_Script_Exports\\SY_24_NJSLA_MAT_ISR\")\n",
    "\n",
    "# creating qa variable\n",
    "length_qa = 0\n",
    "\n",
    "# for loop leveraging iterdir() method to iterate over files in folder\n",
    "for file_path in folder_path.iterdir():\n",
    "    pdf_object = f\"{file_path}\"\n",
    "    reader = PdfReader(pdf_object)\n",
    "    writer = PdfWriter() #--> instantiating PDF Writer\n",
    "    doc_len = len(reader.pages)//2 #--> returning number of pages, divided by 2 to account for 2 page documents\n",
    "    \n",
    "    # opening pdf with pdfplumber and searching for text using a for loop\n",
    "    with pdfp.open(pdf_object) as pdf:\n",
    "        for i, pages in enumerate(tqdm(pdf.pages[::2],desc = 'Retrieving SIDs')): #--> extracting text from every other page and using tqdm to track progress\n",
    "            text = pages.extract_text_simple() #--> creating string object\n",
    "            start = text.find(search_text) #--> assigning the index of the search text to start variable\n",
    "            end = start +  search_text_len + sid_len #--> assigning the index to stop extracting text to the end variable\n",
    "            sid.append(text[start:end].split(':')[1].strip()) #--> appening and manipulating extracted text from PDF file\n",
    "    \n",
    "    #totaling sids in sid list through each iteration \n",
    "    length_qa += doc_len\n",
    "\n",
    "    \n",
    "    #qa\n",
    "    if length_qa == len(sid):\n",
    "        for i, page_num in enumerate(tqdm(range(0,len(reader.pages),2), desc = 'Splitting NJSLA ISRs')): #--> creating a range of all even pages of the document\n",
    "            writer = PdfWriter() #--> resets the writer object in each iteration of the loop\n",
    "            page_name = df[df['State ID'].isin(sid)].reset_index(drop = True)['Local ID'].iloc[i]  #--> returns other id based on indexing of df based on \n",
    "            writer.add_page(reader.pages[page_num]) #--> adding first page to PDF export\n",
    "            if page_num <= len(reader.pages): #--> conditional to ensure that that page num is not outside of index\n",
    "                writer.add_page(reader.pages[page_num +1]) #--> adding second page to PDF export\n",
    "            with open(f'/Users/togarro/NJSLA_ISR_Script_Exports/SY_24_MATH/{page_name}.pdf','wb') as f: #--> file writing\n",
    "                    writer.write(f)  "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
