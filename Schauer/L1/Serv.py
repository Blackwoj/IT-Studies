import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

path = os.getcwd()+'/files'
print(path)
app = Flask(__name__)
app.config['path'] = path


@app.route('/upload', methods=['GET', 'POST'])
def post_content():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['path'], filename))
            return "File transfer completed!"
    return '''    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>'''

@app.route('/<file>')
def get_content(file):
    line = request.args.get('line', default=1, type=int)
    if not os.path.exists(os.path.join(path, file)):
        ret = jsonify({'message': "file not found"})
        ret.status_code = 404
        return ret
    with open(os.path.join(path, file)) as file_name:
        temp = file_name.readlines()[line-1]
        ret = jsonify({'content': temp})
        ret.status_code = 200
    return ret

if __name__ == "__main__":
    app.run(port = 5002)