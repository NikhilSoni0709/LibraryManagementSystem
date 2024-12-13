
# built-in
import uvicorn
import sys


from src.LibrarySystem import LibrarySystem
from src.Persistance.database import Base, db_engine

Base.metadata.create_all(bind=db_engine)
app = LibrarySystem()
uvicorn.run(app, host=sys.argv[1], port=int(sys.argv[2]), log_level='info')