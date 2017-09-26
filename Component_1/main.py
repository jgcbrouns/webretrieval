from repository import *
from authentication import *

if __name__ == "__main__":
    db = get_db()

    add_amount(db, "keyword", 1, 2)
    add_amount(db, "keyword", 1, 2)
    add_amount(db, "keyword", 1, 2)
    remove_amount(db, "keyword", 1, 2)
    add_amount(db, "keyword", 1, 2)
    update_amount(db, "keyword", 1, 6)
