from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load FAQ data
faq = pd.read_csv("faq.csv")

# -------------------------
# GET ALL FAQs
# -------------------------
@app.route("/faqs", methods=["GET"])
def get_faqs():
    faqs = faq.to_dict(orient="records")
    return jsonify(faqs)


# -------------------------
# GET ONE FAQ
# -------------------------
@app.route("/faqs/<int:id>", methods=["GET"])
def get_faq(id):
    if id < 1 or id > len(faq):
        return jsonify({"error": "FAQ not found"}), 404

    faq_data = faq.iloc[id - 1].to_dict()
    return jsonify(faq_data)


# -------------------------
# CREATE FAQ
# -------------------------
@app.route("/faqs", methods=["POST"])
def add_faq():
    global faq

    data = request.get_json()

    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Question and answer are required"}), 400

    new_row = pd.DataFrame({
        "Question": [question],
        "Answer": [answer]
    })

    faq = pd.concat([faq, new_row], ignore_index=True)

    faq.to_csv("faq.csv", index=False)

    return jsonify({
        "message": "FAQ added successfully",
        "question": question,
        "answer": answer
    }), 201


# -------------------------
# UPDATE FAQ
# -------------------------
@app.route("/faqs/<int:id>", methods=["PUT"])
def update_faq(id):
    global faq

    if id < 1 or id > len(faq):
        return jsonify({"error": "FAQ not found"}), 404

    data = request.get_json()

    question = data.get("question")
    answer = data.get("answer")

    if question:
        faq.at[id - 1, "Question"] = question

    if answer:
        faq.at[id - 1, "Answer"] = answer

    faq.to_csv("faq.csv", index=False)

    return jsonify({
        "message": "FAQ updated successfully"
    })


# -------------------------
# DELETE FAQ
# -------------------------
@app.route("/faqs/<int:id>", methods=["DELETE"])
def delete_faq(id):
    global faq

    if id < 1 or id > len(faq):
        return jsonify({"error": "FAQ not found"}), 404

    faq = faq.drop(faq.index[id - 1]).reset_index(drop=True)

    faq.to_csv("faq.csv", index=False)

    return jsonify({
        "message": "FAQ deleted successfully"
    })


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)