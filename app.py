"""
The project is a ChatGPT-based tool. It helps users to come up with the initial idea of image or visualization design.
Users can input their description about what they want the tool shows. The tool will present the p5.js codes as well as
the corresponding picture accordingly.
"""
from flask import Flask
from flask import render_template
from flask import request
import openai

# Key for OpenAI authentication
KEY = "API KEY"

app = Flask(__name__)

"""
Link to main page: users may type their descriptions and submit through the text area of the main page.
-
Return file:
    index.html
"""
@app.route("/")
def index():
    return render_template("index.html")


"""
Output page: users will see the outcome of their input descriptions.
-
Return files:
    If user input is interpretable for the API, this function will link to 'pics.html'.
    If not, this function will link to the error page 'error.html'.
"""
@app.route("/open", methods=['POST'])
def getJs():
    openai.api_key = KEY
    input_text = request.form["desc"]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
            "content": "In the following request, show me your respinse with p5.js codes only. \
            Remember not to ask me to load any image or data in the codes and not to use variables that are not defined. \
            Don't show me the code of any blank canvas and ask me to put my own things. \
            Now, based on the principles above, use p5.js code to create a picture or visualization like this: "+input_text}
        ]
    )
    # API's entire response
    res = completion["choices"][0]['message']['content']  

    try:
        # Extract the pure codes from the API's response
        js_code = res.split("```")[1]
        js_code = js_code.replace("javascript","")
        return render_template("pics.html", desc = input_text, code = js_code)

    except IndexError:
        return render_template("error.html")



app.run(port=3000)