from fastapi import FastAPI
from auth_project.database import SessionLocal, Base, engine, Item, init_db


def seed_db():
    init_db()

    db = SessionLocal()

    try:
        print("Checking if we have items already...")
        if db.query(Item).count() == 0:
            print("Database Empty. Inserting 5 premium campus items")


            item1 = Item(name="Essentals calculus Textbook", description="MTH 102 TXT", price=4500.00)
            item2 = Item(name="Lab coat", description="White chem/phy coat", price=3500.00)
            item3 = Item(name="Scentific Calculator", description="MTH 102 TXT", price=4500.00)
            item4 = Item(name="Hp laptop", description="MTH 102 TXT", price=4500.00)
            item5 = Item(name="Mini Desk Fan", description="MTH 102 TXT", price=4500.00)

            db.add_all([item1, item2, item3, item4, item5])
            db.commit()
            print("Successfully inserted 5 sample items into the database")
        else:
            print("DB already contains records")

    except Exception as e:
        print(f"AN error occured during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
