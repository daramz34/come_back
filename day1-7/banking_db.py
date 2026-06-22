from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Numeric, Text, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL = "sqlite:///./campus_bank.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    receiver = Column(String(50), nullable=False)
    amount = Column(Numeric(12,2))
    reference_note = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def seed_transactions():
    db = SessionLocal()

    try:
        if db.query(Transaction).count() == 0:
            print("Seeding transaction logs...")

            t1 = Transaction(name="Daramz", receiver="BroCode", amount=5000.00, reference_note="Payment for design files")
            t2 = Transaction(name="Koded", receiver="Daramz", amount=12000.50, reference_note="Backend tutoring fee")
            t3 = Transaction(name="Dollar", receiver="Koded", amount=3200.00, reference_note="Domain subscription split")


            db.add_all([t1,t2,t3])
            db.commit() #commit/ save them permantly to the file

            print("Successfully saved 3 transactions")
        else:
            print("Transaction already exist.")
    
    except Exception as e:
        print(f"AN error occured during seeding: {e}")
        db.rollback()
    finally:
        db.close()
        
init_db()
seed_transactions()