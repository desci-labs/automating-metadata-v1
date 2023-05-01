#from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import fitz #pdf reading library
import json
import os

os.environ["OPENAI_API_KEY"] = "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"

def pdfMetadata(filepath): 
    """
    This returns basic descriptive metadata for the PDF. 

    VARS: 
        Filepath: the path of the file you want to upload. 

    RETURNS: 
        metadata: This is the basic function of the Fitz library. 
        It scrapes the PDF for any embedded metadata. 
    """
    doc = fitz.open(filepath)
    metadata = doc.metadata
    return metadata 

def contentmetadata(document, topics):
    contentMetadata = {}

    index = VectorstoreIndexCreator().from_loaders([document])

    for i in range(len(topics)):
        query = "what is the {} of this paper?".format(topics[i])
        contentMetadata[topics[i]] = index.query(query)

    return contentMetadata
     
def main():

    filepath = "/Users/desot1/downloads/220225_capstone_draft2.pdf"
    
    loader = PyMuPDFLoader(filepath)

    categories = ["names given", "university of the author(s)"]# ['Research Question', 'Alterative Approaches', 'Hypothesis', 'Methodology', 'Results', 'Inferences']

    content = contentmetadata(loader, categories)

    descriptive = pdfMetadata(filepath)

    metadata = [descriptive, content]

    print(metadata)
    
    with open("metadata.json", "w") as write_file:
        json.dump(metadata, write_file, indent=4)  

    return metadata

if __name__ == "__main__":
    main()