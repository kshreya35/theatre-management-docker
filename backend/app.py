from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models.user import users_collection
from models.theatre import theatres_collection
from models.booking import bookings_collection
from bson.objectid import ObjectId
from bson.son import SON
from datetime import datetime



app = Flask(__name__)
CORS(app)

# ------------------- HTML Pages -------------------

@app.route('/')
def index():
    return render_template('login.html')  # default landing page

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard_page():
    return render_template('admin_dashboard.html')

@app.route('/producer')
def producer_dashboard_page():
    return render_template('producer_dashboard.html')


# ------------------- User Registration -------------------
# POST: create/register user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    users_collection.insert_one(data)
    return jsonify({"message": "User added"}), 201

# GET: fetch all users (optional)
@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    for u in users:
        u["_id"] = str(u["_id"])
    return jsonify(users)

# GET: fetch single user by UID (needed for login)
@app.route('/api/users/<uid>', methods=['GET'])
def get_user_by_uid(uid):
    user = users_collection.find_one({"uid": uid})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404



# ------------------- Add Theatre (Admin) -------------------
@app.route('/api/theatres', methods=['POST'])
def add_theatre():
    data = request.json
    theatres_collection.insert_one({**data, "bookedBy": None})
    return jsonify({"message": "Theatre added"}), 201

# ------------------- Get All Theatres -------------------
@app.route('/api/theatres', methods=['GET'])
def get_theatres():
    theatres = list(theatres_collection.find())
    for t in theatres: t["_id"] = str(t["_id"])
    return jsonify(theatres)

# ------------------- Delete Theatre -------------------
@app.route('/api/theatres/<id>', methods=['DELETE'])
def delete_theatre(id):
    theatres_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Deleted"})

# ------------------- Search Theatres (Producer) -------------------
@app.route('/api/theatres/search', methods=['POST'])
def search_theatres():
    query = request.json
    condition = query.get("condition")
    seats = query.get("seats")
    date = query.get("date")

    filter_query = {}
    if date: filter_query["date"] = date
    if condition == "gt": filter_query["seats"] = {"$gt": seats}
    elif condition == "lt": filter_query["seats"] = {"$lt": seats}
    elif condition == "eq": filter_query["seats"] = seats

    theatres = list(theatres_collection.find(filter_query))
    for t in theatres: t["_id"] = str(t["_id"])
    return jsonify(theatres)

# ------------------- Book Theatre (Producer) -------------------

@app.route('/api/theatres/book/<id>', methods=['POST'])
def book_theatre(id):
    uid = request.json['uid']
    theatre = theatres_collection.find_one({"_id": ObjectId(id)})

    if not theatre:
        return jsonify({"error": "Theatre not found"}), 404

    # already booked check
    if theatre.get("bookedBy"):
        return jsonify({"error": "Already booked"}), 400

    # update theatre availability (OLD LOGIC KEPT)
    theatres_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"bookedBy": uid}}
    )

    # NEW: insert booking record
    bookings_collection.insert_one({
        "theatre_id": theatre["_id"],
        "theatre_name": theatre["name"],
        "uid": uid,
        "date": theatre.get("date"),
        "seats": theatre.get("seats"),
        "price": theatre.get("price"),
        "status": "booked",
        "booked_at": datetime.utcnow()
    })

    return jsonify({"message": "Booked successfully"})


# ------------------- Get Booked Theatres by Producer -------------------
@app.route('/api/theatres/booked/<uid>', methods=['GET'])
def get_booked_theatres(uid):

    bookings = list(bookings_collection.find({
        "uid": uid,
        "status": "booked"
    }))

    result = []

    for b in bookings:
        theatre_id = b.get("theatre_id")

        # 🔥 ALWAYS ensure ObjectId
        if isinstance(theatre_id, str):
            theatre_id = ObjectId(theatre_id)

        theatre = theatres_collection.find_one({"_id": theatre_id})

        if theatre:
            theatre["_id"] = str(theatre["_id"])
            result.append(theatre)

    return jsonify(result)


# ---------------------cancel bookings -----------------------------

@app.route('/api/theatres/cancel/<id>', methods=['POST'])
def cancel_booking(id):
    uid = request.json['uid']

    theatre_id = ObjectId(id)

    booking = bookings_collection.find_one({
        "theatre_id": theatre_id,
        "uid": uid,
        "status": "booked"
    })


    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # mark theatre available again
    theatres_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"bookedBy": None}}
    )

    # update booking history
    bookings_collection.update_one(
        {"_id": booking["_id"]},
        {"$set": {"status": "cancelled"}}
    )

    return jsonify({"message": "Booking cancelled"})


# ------------------- Aggregation: Available Theatres Summary -------------------
@app.route('/api/theatres/summary', methods=['GET'])
def theatre_summary():

    pipeline = [
        {
            "$lookup": {
                "from": "theatres",
                "localField": "theatre_id",
                "foreignField": "_id",
                "as": "theatre"
            }
        },
        {"$unwind": "$theatre"},

        {
            "$group": {
                "_id": "$theatre.date",
                "total": {"$sum": 1}
            }
        },

        {"$sort": {"_id": 1}}
    ]

    summary = list(bookings_collection.aggregate(pipeline))

    for s in summary:
        s["_id"] = str(s["_id"])

    return jsonify(summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

