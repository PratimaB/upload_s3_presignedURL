import boto3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# S3 Bucket name and region
S3_BUCKET = "S3-bucket-name"
S3_REGION = "region"

# S3 Client Setup (credentials automatically picked from IAM role)
s3 = boto3.client("s3", region_name=S3_REGION)

# Route for file upload
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files['file']
        if file:
            file_name = file.filename
            s3.upload_fileobj(file, S3_BUCKET, file_name)
            return redirect(url_for('success', filename=file_name))
    return render_template('upload.html')

# Route to generate a presigned URL for download
@app.route("/download/<filename>")
def download_file(filename):
    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': filename},
            ExpiresIn=300  # URL expiry time in seconds
        )
        return redirect(presigned_url)
    except Exception as e:
        return str(e)

# Success Page
@app.route("/success/<filename>")
def success(filename):
    return render_template('success.html', filename=filename)

if __name__ == "__main__":
    # Bind to 0.0.0.0 to make the app accessible from external IPs
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
