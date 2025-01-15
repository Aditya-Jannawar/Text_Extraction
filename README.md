**Text Extraction**

I developed a web application to allow users to upload a PDF or image file, extract text, edit it in a textarea, and export the updated text as a PDF or Word document. I used Python for the backend with Flask, and I created the frontend using HTML, CSS, and JavaScript.
Development Steps
1.	Setting Up Flask and Project Structure
I began by setting up a Flask application as the backend server. I defined the project structure to include routes for uploading files, extracting text, displaying it on the web interface, and exporting it. I created a dedicated folder to store generated export files for easy retrieval.
2.	Implementing PDF Conversion and Text Extraction
I used PyMuPDF to handle PDF inputs by converting each page into an image, which facilitated text extraction. I utilized Tesseract OCR for extracting text from both images and PDF pages, allowing flexibility for different input types. This extracted text was then sent to the frontend to be displayed in a textarea.
3.	Frontend UI with Editable Text Area
For the frontend, I built a simple HTML interface with JavaScript to handle file uploads and display the extracted text in an editable textarea. This allowed users to make changes before exporting. I also used CSS to enhance the UI, ensuring it was clean and easy to use.

4.	Exporting Edited Text to PDF and Word
I implemented an export feature by creating a new API route that accepted the edited text and the desired export format (PDF or Word). To generate the PDF, I used the fpdf library, ensuring the text was wrapped and formatted appropriately. For Word documents, I used python-docx to save the text as a .docx file.
5.	Handling Unicode and File Serving
To prevent encoding issues, I converted text to ASCII, replacing any unsupported Unicode characters. I set up a separate file download route in Flask to serve the generated files directly, allowing users to download their exported PDF or Word documents.
6.	Frontend Download Integration
I configured JavaScript on the frontend to handle the download automatically when it received the download link from the server. This created a seamless user experience, making it easy for users to save their edited text locally.
Output:
 
