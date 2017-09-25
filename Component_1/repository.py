def add_country(db):
    db.countries.insert({"name" : "Canada"})

def get_country(db):
    return db.countries.find_one()

def say_hi(db):
    return "test"
