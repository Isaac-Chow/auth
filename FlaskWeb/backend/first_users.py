from app import db, User, app

def create_users():
    user1 = User(username='johnnyDoe13', password='Password101!')
    user2 = User(username='janeDoe13', password='Password102!')
    user3 = User(username='jillDoe13', password='Password103!')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_users()