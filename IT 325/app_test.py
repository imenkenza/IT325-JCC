from flask import Flask
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Test API',
    'uiversion': 3
 }
Swagger(app)
 
@app.route("/test")
def test_route():
   return "Hello, World!"

if __name__ == "__main__":
   app.run(debug=True)