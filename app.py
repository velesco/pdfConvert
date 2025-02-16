from flask import Flask, request, send_file
from docx2pdf import convert
import os
import tempfile

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_document():
    """
    Endpoint to convert DOCX to PDF
    Expects a DOCX file in the request with key 'document'
    Returns the converted PDF file with original filename but .pdf extension
    """
    if 'document' not in request.files:
        return {'error': 'No document provided'}, 400
        
    document = request.files['document']
    
    if not document.filename.endswith('.docx'):
        return {'error': 'File must be a DOCX document'}, 400

    try:
        # Get original filename and create PDF filename
        original_name = document.filename
        pdf_name = os.path.splitext(original_name)[0] + '.pdf'
        
        # Create temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded DOCX
            docx_path = os.path.join(temp_dir, 'input.docx')
            document.save(docx_path)
            
            # Create PDF path
            pdf_path = os.path.join(temp_dir, 'output.pdf')
            
            # Convert document
            convert(docx_path, pdf_path)
            
            # Return the PDF file with original name
            return send_file(
                pdf_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=pdf_name
            )
            
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8820)