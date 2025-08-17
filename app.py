# Notes Taking App (Flask)
# Subject: Software Development 1
# -------------------------------------------------
# কীভাবে কাজ করে (short):
# - নোটগুলো একটি সাধারণ টেক্সট ফাইল (notes.txt) এ সেভ হয়
# - হোমপেজে নোট দেখায়, নতুন নোট যোগ করা যায়, এবং ডিলিট করা যায়
# - Flask টেমপ্লেট (Jinja) দিয়ে HTML রেন্ডার করা হয়

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
FILE_NAME = "notes.txt"

def load_notes():
    """ফাইল থেকে সব নোট পড়ে লিস্ট হিসেবে রিটার্ন করে"""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def save_notes(notes):
    """লিস্টের সব নোট ফাইলে সেভ করে (প্রতিটি লাইনে একটি নোট)"""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(note + "\n")

@app.route("/", methods=["GET", "POST"])
def index():
    notes = load_notes()
    if request.method == "POST":
        new_note = request.form.get("note", "").strip()
        if new_note:
            notes.append(new_note)
            save_notes(notes)
        return redirect(url_for("index"))
    return render_template("index.html", notes=notes)

@app.route("/delete/<int:index>", methods=["GET"])
def delete(index):
    notes = load_notes()
    if 0 <= index < len(notes):
        notes.pop(index)
        save_notes(notes)
    return redirect(url_for("index"))

if __name__ == "__main__":
    # debug=True রাখা হয়েছে যাতে ডেভেলপমেন্টে auto-reload হয়
    app.run(debug=True)