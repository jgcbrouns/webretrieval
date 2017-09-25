from repository import *
from authentication import *

if __name__ == "__main__":

    db = get_db()
    add_country(db)
    print get_country(db)
    print say_hi(db)
