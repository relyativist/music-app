import requests
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://denis:1234Five@database/api"
db = SQLAlchemy(app)
ma = Marshmallow(app)

db.init_app(app)
Migrate(app,db)
db.create_all()


# creating the schema
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(250), nullable=False)
    collectionName = db.Column(db.String(250), nullable=False)
    trackName = db.Column(db.String(250), nullable=False)
    collectionPrice = db.Column(db.String(250), nullable=False)
    trackPrice = db.Column(db.String(250), nullable=False)
    releaseDate = db.Column(db.String(250), nullable=False)

    def __init__(self, kind, collectionName, trackName, collectionPrice, trackPrice, releaseDate):
        self.kind = kind
        self.collectionName = collectionName
        self.trackName = trackName
        self.collectionPrice = collectionPrice
        self.trackPrice = trackPrice
        self.releaseDate = releaseDate


class RecordSchema(ma.Schema):
    class Meta:
        fields = ("id", "kind", "collectionName", "trackName", "collectionPrice", "trackPrice", "releaseDate")


record_schema = RecordSchema()
records_schema = RecordSchema(many=True)


def clean_db():
    records = Record.query.all()
    for record in records:
        db.session.delete(record)
        db.session.commit()


def add_record(kind, collectionName, trackName, collectionPrice, trackPrice, releaseDate):
    record = Record(kind, collectionName, trackName, collectionPrice, trackPrice, releaseDate)
    db.session.add(record)
    db.session.commit()


def create_db(term="Guns and roses"):
    base_url = "https://itunes.apple.com/search"
    search_key = f"?term={term}"

    urlData = requests.get(base_url + search_key)
    records = urlData.json()
    if records:
        clean_db()
        temps_r = records["results"]
        for record in temps_r:
            try:
                kind = record["kind"]
                collectionName = record["collectionName"]
                trackName = record["trackName"]
                collectionPrice = record["collectionPrice"]
                trackPrice = record["trackPrice"]
                releaseDate = record["releaseDate"]

                add_record(kind, collectionName, trackName, collectionPrice, trackPrice, releaseDate)
            except Exception as e :
                print(e)


@app.route("/")
def home():
    create_db()
    data = Record.query.all()
    return render_template("home.html", data=records_schema.dump(data))


@app.route("/refresh", methods=["POST"])
def refresh():
    term = request.json["term"]
    create_db(term)
    data = Record.query.order_by(Record.releaseDate.desc()).all()
    return jsonify(records_schema.dump(data))


if __name__ == "__main__":
    #app.run("0.0.0.0", debug=True, port=8080)
    app.run()

