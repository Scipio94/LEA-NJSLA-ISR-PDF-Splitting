{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "bfb15227-dfdf-4d5f-8719-c3e372aa8203",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pdfplumber as pdfp\n",
    "import pypdf\n",
    "from pypdf import PdfReader,PdfWriter\n",
    "import string as str\n",
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "4183f5f9-9756-45a9-8b44-98f68d0a7e48",
   "metadata": {},
   "outputs": [],
   "source": [
    "# importing tabular data\n",
    "df = pd.read_excel(r\"C:\\Users\\togarro\\Documents\\NJSLA_ISR_Split\\SID_Other_ID_Export.xlsx\") #--> file wuith SIDs and Local IDs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "052d72c7-1fb8-4254-8004-92c64a81c2ab",
   "metadata": {},
   "outputs": [],
   "source": [
    "# creating SID len variable\n",
    "df['State ID'] = df['State ID'].astype('string') #--> casting column data as a string\n",
    "sid_len = len(df['State ID'][0]) #--> len of SID"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "ae85dedf-23fd-4252-9175-6048f60d6491",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The pdf document contains 216 documents\n"
     ]
    }
   ],
   "source": [
    "# importing pdf using pypdf\n",
    "reader = PdfReader(r\"C:\\Users\\togarro\\Documents\\NJSLA_ISR_Split\\pcspr25_NJ-034390-070_ISR_Spring_Grade_8_ELA.pdf\")\n",
    "writer = PdfWriter() #--> instantiating PDF Writer\n",
    "doc_len = len(reader.pages)/2 #--> returning number of pages, divided by 2 to account for 2 page documents\n",
    "\n",
    "print(f'The pdf document contains {round(doc_len)} documents')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "683928c8-2b6f-4844-8eea-ed77c21d69d3",
   "metadata": {},
   "outputs": [],
   "source": [
    "# variables\n",
    "search_text = 'ID: ' #--> substring search\n",
    "search_text_len = len(search_text) #--> len object of the substring\n",
    "sid = [] #--> creating an empty list\n",
    "\n",
    "# opening pdf with pdfplumber and searching for text using a for loop\n",
    "with pdfp.open(r\"C:\\Users\\togarro\\Documents\\NJSLA_ISR_Split\\pcspr25_NJ-034390-070_ISR_Spring_Grade_8_ELA.pdf\") as pdf:\n",
    "    for pages in pdf.pages: #--> range to extract text from odd pages\n",
    "        text = pages.extract_text_simple() #--> creating string object\n",
    "        start = text.find(search_text) #--> assigning the index of the search text to start variable\n",
    "        end = start +  search_text_len + sid_len #--> assigning the index to stop extracting text to the end variable\n",
    "        sid.append(text[start:end]) #--> appening extracted text from the PDF to list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "3df80fa5-282a-467e-91a6-fcf1e2a0e137",
   "metadata": {},
   "outputs": [],
   "source": [
    "# creating sid_df from list\n",
    "sid_df = pd.DataFrame({'State ID':sid})\n",
    "\n",
    "# removing blank values from the sid_df\n",
    "sid_df = sid_df[sid_df['State ID'] != '']\n",
    "\n",
    "# returning SID\n",
    "sid_df['State ID'] = sid_df['State ID'].str.split(':').str[1].str.strip()\n",
    "\n",
    "# casting as string\n",
    "sid_df['State ID'] = sid_df['State ID'].astype('string')\n",
    "\n",
    "# creating rows variable\n",
    "rows = sid_df.shape[0]\n",
    "\n",
    "# merging dfs based on SID\n",
    "sid_merged_df = sid_df.merge(df, how = 'inner', on = 'State ID')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "334d6623-f91f-4119-a8d7-ed7c70a6517d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "There are 0 SIDs missing from the merge file\n"
     ]
    }
   ],
   "source": [
    "# statement to see if there were any sids missing\n",
    "print(f'There are {sid_df[~sid_df['State ID'].isin(df['State ID'])].shape[0]} SIDs missing from the merge file')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6ab21580-e065-48e7-9f5b-1799dc0aa80d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# creating count variable to coun the number of iteration through the loop\n",
    "count = 0\n",
    "\n",
    "# creating qa variable\n",
    "qa = doc_len == rows #--> doc_len and rows should be equal\n",
    "\n",
    "# conditional statement - if conditional met will run for loop, if not will print error statement\n",
    "if qa == True:\n",
    "\n",
    "    for i, page_num in enumerate(range(0,len(reader.pages),2)): #--> creating a range of all even pages of the document\n",
    "        writer = PdfWriter() #--> resets the writer object in each iteration of the loop\n",
    "        page_name = sid_merged_df['Local ID'].iloc[i]  #--> returns other id based on indexing of df based on \n",
    "        writer.add_page(reader.pages[page_num]) #--> adding first page to PDF export\n",
    "        if page_num <= len(reader.pages): #--> conditional to ensure that that page num is not outside of index\n",
    "            writer.add_page(reader.pages[page_num +1]) #--> adding second page to PDF export\n",
    "        with open(f'/Users/togarro/NJSLA_ISR_Script_Exports/{page_name}.pdf','wb') as f: #--> file writing\n",
    "                writer.write(f)\n",
    "        count += 1 #--> adding 1 to the count object after each iteration through the for loop\n",
    "\n",
    "    print(f'{count} PDF documents were successfully created')  #--> print statement to confirm that documents were created\n",
    "            \n",
    "else:\n",
    "    print(f'There is an error, and the for loop was not excecuted.\\nCheck to ensure that pages in the PDF and rows in the df are equal.\\nPDF Page:{doc_len}\\nDataframe Rows:{rows}')\n",
    "\n",
    "        "
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
