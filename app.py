from flask import Flask ,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/todo"
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class Items(db.Model):
    __tablename__='items'

    item=db.Column(db.String(),primary_key=True)
    status=db.Column(db.String())

    def __init__(self,item,status):
        self.item=item
        self.status=status

    def __repr__(self):
        return f"<Item {self.item} {self.status}>"

@app.route('/')
def hello():
    return {"hello": "world"}

@app.route('/items', methods=['POST','GET'])
def handle_items():
    if request.method=='POST':
        if request.is_json:
            data=request.get_json()
            new_item=Items(item=data['item'],status=data['status'])
            db.session.add(new_item)
            db.session.commit()
            return {"message":f"item {new_item.item} has been ceated successfully"}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method=='GET':
        items=Items.query.all()
        results=[{
            "item":item.item,
            "status":item.status
        }for item in items]

        return {"count": len(results), "items": results}
    


@app.route('/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    item = Items.query.get_or_404(item_id)

    if request.method == 'GET':
        response = {
            "item": item.item,
            "status": item.status,
        }
        return {"message": "success", "item": response}

    elif request.method == 'PUT':
        data = request.get_json()
        item.item = data['item']
        item.status = data['status']
        db.session.add(item)
        db.session.commit()
        return {"message": f"Item {item.item} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item {item.item} successfully deleted."}


if __name__=="__main__":
    app.run(debug=True)