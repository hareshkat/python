from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import resume_parser as resumeparser
import PyPDF2
import docx2txt

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

class resumeparserapi(Resource):

  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('file_path', type = str, required = True, help = 'file_path field is required')
    super(resumeparserapi, self).__init__()

  def get(self):
    return "Hello"

  def post(self):
    if request.method=="POST":
      args = self.reqparse.parse_args()
      path = args['file_path']
      data = ''
      extension = path.split(".")[-1]
      if extension == "txt":
          f = open(path, 'r')
          data = f.read()
          f.close()
      elif extension == "pdf":
          finalresult = ''
          with open(path, 'rb') as f:
              pdf = PyPDF2.PdfFileReader(f)
              noofpages=pdf.getNumPages()
              for i in range(noofpages):
                  page = pdf.getPage(i)
                  result=page.extractText()
                  finalresult= finalresult+""+result
          data=finalresult.replace("\n", "").strip()
      elif extension=='docx':
          data = docx2txt.process(path)
      else:
          return (str(extension) + " extension not supported")

      if data != '':
        Name,FirstName,LastName,Email,Mobile_Number,skills,Gender,Role,Company,education,Experience,Institution,Marital,Nationality,PassportNo,DateofBirth=resumeparser.Resume_Path(data)
        data={"Name":Name,
              "FirstName":FirstName,
              "LastName":LastName,
              "Email":Email,
              "Mobile_No":Mobile_Number,
              "Skills":skills,
              "Gender":Gender,
              "Role":Role,
              "Company":Company,
              "Education":education,
              "Experience":Experience,
              "Institution":Institution,
              "Marital":Marital,
              "Nationality":Nationality,
              "PassportNo":PassportNo,
              "DOB":DateofBirth
                }
        return jsonify(data)

api.add_resource(resumeparserapi, '/')
if __name__ == '__main__':
  app.run(debug = True)
