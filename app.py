from flask import Flask, request, send_file
import os
import tempfile
import subprocess
import traceback

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_document():
    try:
        print("Request received")
        print("Files in request:", request.files)
        
        if 'document' not in request.files:
            print("No document in request")
            return {'error': 'No document provided'}, 400
            
        document = request.files['document']
        print(f"Received file: {document.filename}")
        
        if not document.filename.endswith('.docx'):
            print("Invalid file type")
            return {'error': 'File must be a DOCX document'}, 400

        # Create temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded DOCX
            docx_path = os.path.join(temp_dir, 'input.docx')
            document.save(docx_path)
            print(f"Saved DOCX to: {docx_path}")
            
            # Create PDF path
            pdf_path = os.path.join(temp_dir, 'output.pdf')
            print(f"PDF will be saved to: {pdf_path}")
            
            # Convert using LibreOffice
            print("Starting conversion...")
            process = subprocess.run([
                'libreoffice',
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                temp_dir,
                docx_path
            ], capture_output=True, text=True)
            
            if process.returncode != 0:
                print(f"Conversion failed: {process.stderr}")
                return {'error': 'PDF conversion failed'}, 500

            # LibreOffice creates the PDF with the same name as input but .pdf extension
            converted_pdf = os.path.join(temp_dir, 'input.pdf')
            
            if not os.path.exists(converted_pdf):
                print("PDF file was not created")
                return {'error': 'PDF conversion failed'}, 500
                
            print("Sending file back to client")
            return send_file(
                converted_pdf,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=os.path.splitext(document.filename)[0] + '.pdf'
            )
            
    except Exception as e:
        print("Error occurred:")
        print(traceback.format_exc())
        return {'error': str(e)}, 500

if __name__ == '__main__':
    print("Starting Flask server on port 8820...")
    app.run(host='0.0.0.0', port=8820, debug=True)