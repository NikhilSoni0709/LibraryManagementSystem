
# built-in
import uvicorn


from src.LibrarySystem import LibrarySystem
from src.Persistance.database import Base, db_engine

Base.metadata.create_all(bind=db_engine)
app = LibrarySystem()
uvicorn.run(app, host="0.0.0.0", port=9773, log_level='info')