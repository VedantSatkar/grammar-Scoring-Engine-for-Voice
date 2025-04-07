from flask import Flask, render_template, jsonify
from main import grammar_scoring_pipeline_from_mic

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    result = grammar_scoring_pipeline_from_mic()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)