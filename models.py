import os
import datetime
import atexit
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func
from dotenv import load_dotenv
load_dotenv()


USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")

PG_DSN = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"



engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}

class Board(Base):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String, nullable=False)


    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "description": self.description,
            "owner": self.owner
        }

Base.metadata.create_all(bind=engine)
atexit.register(engine.dispose)

# print(f"USER={USER}, PASSWORD={PASSWORD}, HOST={HOST}, PORT={PORT}, DB={DB}")

