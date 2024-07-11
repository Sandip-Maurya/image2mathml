import os, time
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from py_scripts.full_lat_converter import full_lat_converter
from py_scripts.mathpix_module import img2lat_by_mathpix
from py_scripts.removebg import removebg_fn

UPLOAD_FOLDER = "./static/images/usr_imgs"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/getcode", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:

            return "'file' not in request.files"
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":

            return "File not selected"
        if file and allowed_file(file.filename):
            filename_user = file.filename
            ext = filename_user.split(".")[-1]
            file_name_time_based = str(time.time()).replace(".", "dot")
            file.filename = f"{file_name_time_based}.{ext}"
            filename = secure_filename(file.filename)
            # print(filename_user, filename)
            full_filename = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            # print(full_filename)
            file.save(full_filename)
            try:
                lat_str = img2lat_by_mathpix(full_filename)
                # print(lat_str)
                mathml = full_lat_converter(lat_str)
                if 'tabular' in lat_str:
                    lat_str = lat_str.replace('tabular', 'array')
                    lat_str = lat_str.replace('$', '')

            except Exception as e:
                return f"""
                <h2>Problem occured in uploaded Image</h2>
                <h3>Probably Mathpix has not detected the image content properly.</h3>
                <p>Report the problem to Sandip Sir</p>
                <p> The error is:    {e} </p>
                """

            return render_template("show.html", user_image=full_filename, mathml=mathml, latex = lat_str)

    return render_template("error_page.html")


@app.route("/removebg", methods=["POST"])
def removebg():
    global full_filename_output
    if "file" not in request.files:
        return "'file' not in request.files"
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        return "File not selected"

    if file and allowed_file(file.filename):
        filename_user = file.filename
        ext = filename_user.split(".")[-1]
        file_name_time_based = str(time.time()).replace(".", "dot")
        file.filename = f"{file_name_time_based}.{ext}"
        filename = secure_filename(file.filename)
        # print(filename_user, filename)
        full_filename = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        # print(full_filename)
        file.save(full_filename)
        try:
            full_filename_output = removebg_fn(full_filename)

        except Exception as e:
            return """
                <h2>Problem occured in uploaded Image</h2>
                <h3>Probably Mathpix has not detected the image content properly.</h3>
                <p>Report the problem to Sandip Sir</p>
                """

        return render_template(
            "removebg.html",
            user_image=full_filename,
            user_image_output=full_filename_output,
        )


@app.route("/download")
def download():
    path = full_filename_output
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    from waitress import serve
    # serve(app, host="0.0.0.0", port=8080, threads=True)
    app.run(host="0.0.0.0", port=8080)
