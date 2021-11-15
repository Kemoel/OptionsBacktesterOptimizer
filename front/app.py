import flask
import csv
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

@app.route('/')
def home():
   return flask.render_template('page.html')

# @app.route('/', methods=['POST'])
# def handle_data():
#     projectpath = flask.request.form['projectFilepath']
#     print(projectpath)
#     return flask.render_template('page.html')

@app.route('/get_csv', methods=["GET","POST"])
def get_csv():
   csv_dir  = ".\static"
   csv_file = flask.request.form.get('csv_name')
   csv_path = os.path.join(csv_dir, csv_file+'.csv')
   return flask.send_file(csv_path, as_attachment=True, attachment_filename=csv_file)


if __name__ == "__main__":
   app.run()