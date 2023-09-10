import os
import pdfquery
import pandas as pd

# Function to extract data from PDF using PDFQuery
def extract_data_from_pdf(pdf_path):
    pdf = pdfquery.PDFQuery(pdf_path)
    pdf.load()
    
    # Define your queries here to extract specific data
    keyword1 =  pdf.pq('LTTextLineHorizontal:contains("{}")'.format("Any Keyword"))[0] 
    x1_0 = float(keyword1.get('x0',0)) 
    y1_0 = float(keyword1.get('y0',0)) - 10
    x1_1 = float(keyword1.get('x1',0))                 #set the co-ordinates according to need
    y1_1 = float(keyword1.get('y1',0)) - 10
    data1 = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x1_0, y1_0, x1_1, y1_1)).text()
    keyword2 =  pdf.pq('LTTextLineHorizontal:contains("{}")'.format("Any Keyword"))[0] 
    x2_0 = float(keyword2.get('x0',0))
    y2_0 = float(keyword2.get('y0',0)) - 40
    x2_1 = float(keyword2.get('x1',0)) + 220           #set the co-ordinates according to need
    y2_1 = float(keyword2.get('y1',0)) - 10
    data2 = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x2_0, y2_0, x2_1, y2_1)).text()
    # Add more queries as needed
    
    return data1, data2  # Return extracted data as lists

# Function to save data to a CSV file
def save_to_csv(data1, data2, output_csv):
    # Create a DataFrame for the extracted data
    df = pd.DataFrame({'Buyer Order no.': data1, 'Shipping Address': data2}, index=[0])
    
    # Append the DataFrame to the existing CSV file or create a new file if it doesn't exist
    if os.path.exists(output_csv):
        df.to_csv(output_csv, mode='a', index=False, header=False)
    else:
        df.to_csv(output_csv, index=False)

# Main function to process all PDFs in a directory
def process_pdfs(input_dir, output_csv):
    for pdf_file in os.listdir(input_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, pdf_file)
            
            # Extract data from the PDF
            extracted_data1, extracted_data2 = extract_data_from_pdf(pdf_path)
            
            # Save the extracted data to the CSV file
            save_to_csv(extracted_data1, extracted_data2, output_csv)

if __name__ == "__main__":
    input_directory = 'orders'  # Replace with the directory containing your PDFs
    output_csv = 'output.csv'  # Specify the output CSV file path
    
    # Process all PDFs in the input directory and save to a single CSV file
    process_pdfs(input_directory, output_csv)
