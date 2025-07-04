from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------- Product Model --------------------
class Product(db.Model):
    __tablename__ = 'products'  # חייב להיות זהה ל־ForeignKey

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    cost = db.Column(db.Float)
    stock_level = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)

    # ✅ קשר דו-כיווני עם RestockLog
    restock_logs = db.relationship(
        "RestockLog",
        backref="product",  # מאפשר self.product מתוך RestockLog
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "category": self.category,
            "price": self.price,
            "cost": self.cost,
            "stock_level": self.stock_level,
            "low_stock_threshold": self.low_stock_threshold,
        }


# -------------------- RestockLog Model --------------------
class RestockLog(db.Model):
    __tablename__ = 'restock_log'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete="CASCADE"),
        nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "quantity": self.quantity,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
