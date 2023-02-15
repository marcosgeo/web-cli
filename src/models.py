# models.py

from bumbo.orm import Table, Column

class Book(Table):
    author = Column(str)
    name = Column(str)

