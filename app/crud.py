
from app import db


class CRUDBase(db.Model):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def get_data(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_paginated_search(cls, query=None, page=1, per_page=10):
        if query:
            # Perform search with pagination
            return cls.query.filter(
                (cls.title.ilike(f'%{query}%')) | (cls.ingredients.ilike(f'%{query}%'))
            ).paginate(page=page, per_page=per_page, error_out=False)
        else:
            # Return all items paginated if no search query is provided
            return cls.query.paginate(page=page, per_page=per_page, error_out=False)


    def update(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
