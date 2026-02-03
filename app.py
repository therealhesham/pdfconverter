import io
from flask import Flask, render_template, request, send_file
from flask_cors import CORS
import img2pdf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    # Simple HTML form for uploading files
    return '''
    <!doctype html>
    <title>Image to PDF</title>
    <h1>Upload Images to convert to PDF</h1>
    <form method="post" action="/convert" enctype="multipart/form-data">
      <input type="file" name="images" multiple accept="image/*">
      <input type="submit" value="Convert to PDF">
    </form>
    '''

@app.route('/convert', methods=['POST'])
def convert():
    if 'images' not in request.files:
        return "No files uploaded", 400
    
    files = request.files.getlist("images")
    
    # Filter out empty filenames
    img_list = []
    for f in files:
        if f.filename != '':
            # Read the file content into bytes
            img_list.append(f.read())

    if not img_list:
        return "No images selected", 400

    try:
        # Convert images to PDF bytes
        pdf_bytes = img2pdf.convert(img_list)
        
        # Create a binary stream from the PDF bytes
        pdf_io = io.BytesIO(pdf_bytes)
        pdf_io.seek(0)

        # Return the PDF file to the user
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='converted.pdf'
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3015, debug=True)