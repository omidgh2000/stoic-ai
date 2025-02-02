import PyPDF2
import re
import string
import tiktoken

def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
        
    print("PDF converted to text successfully!")



def clean_up(input_txt, output_txt):
     # Keep letters, numbers, spaces, and standard punctuation
    allowed_chars = string.ascii_letters + string.digits + string.punctuation + " \n"
    
    with open(input_txt, "r", encoding="utf-8") as file:
        text = file.read()

    text = "".join(c for c in text if c in allowed_chars)
    text = text.replace("\t", " ")    # Replace all tabs with a single space
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    text = re.sub(r"\n{2,}", "\n", text)  # Replace multiple newlines with a single newline
    text = re.sub(r"\b[A-Z]{2,}\b", "", text)     # Remove full uppercase words (e.g., "HELLO", "WORLD", but not "DeepSeek" or "Python")
    text = text.replace("\r\n", "\n").replace("\r", "\n") #to ensure consistent Unix-style line endings
    
    text = re.sub(r"\b[A-Z]{2,}\b", "", text)


        # Save cleaned text
    with open(output_txt, "w", encoding="utf-8") as file:
        file.write(text)

    print("Text cleaned and saved successfully!")
    
 
 
def tokenize_text_file(input_txt, output_txt, model="cl100k_base"):
    # Load the tokenizer (DeepSeek likely follows OpenAI's encoding)
    enc = tiktoken.get_encoding(model)

    # Read the cleaned text file
    with open(input_txt, "r", encoding="utf-8") as file:
        text = file.read()

    # Tokenize the text
    tokens = enc.encode(text)
    token_count = len(tokens)

    # Save tokenized text as a space-separated string
    with open(output_txt, "w", encoding="utf-8") as file:
        file.write(" ".join(map(str, tokens)))

    print(f"✅ Tokenization complete! Total tokens: {token_count}")
    return token_count

   
if __name__ == "__main__":
    #pdf_path = 'The Power Of Now - Eckhart Tolle.pdf'
    output_txt = 'The Power of Now.txt'
    output2_txt = 'The Pwer of Now2.txt'
    output3_txt = 'The Pwer of Now3.txt'
    output_tiktok_txt = 'The Power of Now (Tokenized).txt'
    #pdf_to_text(pdf_path, output_txt)
    #clean_up(output2_txt, output3_txt)
    token_count = tokenize_text_file(output3_txt, output_tiktok_txt)
    print(f"📌 Tokenized file saved as: {output_tiktok_txt}")


