from sqlalchemy.sql import text
from db import db


def get_all_restaurants():
    result = db.session.execute(text("SELECT * FROM restaurants"))
    return result.fetchall()

def search_restaurants(substring):
    
    sql = text("SELECT * FROM restaurants WHERE LOWER(name) LIKE '%' || LOWER('" + substring + "') || '%'")
    
    '''
    Flaw no.3 fix
    sql = text("SELECT * FROM restaurants WHERE LOWER(name) LIKE '%' || LOWER(:substring) || '%'")
    
    '''
    result = db.session.execute(sql, {"substring":substring})
    filtered_restaurants = result.fetchall()
    print(filtered_restaurants)

    return filtered_restaurants 

def delete_restaurant(restaurant_id):
    sql1 = text("DELETE FROM locations WHERE restaurant_id=:restaurant_id")
    db.session.execute(sql1, {"restaurant_id": restaurant_id})
    sql2 = text("DELETE FROM reviews WHERE restaurant_id=:restaurant_id")
    db.session.execute(sql2, {"restaurant_id": restaurant_id})


    sql3 = text("DELETE FROM categories WHERE restaurant_id=:restaurant_id")
    db.session.execute(sql3, {"restaurant_id": restaurant_id})


    sql4 = text("DELETE FROM restaurants WHERE id=:restaurant_id")
    db.session.execute(sql4, {"restaurant_id": restaurant_id})

    db.session.commit()

def add_restaurant(name, address, city, categories):
    check_for_name = text("SELECT * FROM restaurants WHERE name = :name")

    existing_restaurant = db.session.execute(check_for_name, {"name": name}).fetchone()
    if existing_restaurant:
        print('ollaa ifis')
        return False

    sql1 = text("INSERT INTO restaurants (name) VALUES (:name)")
    db.session.execute(sql1, {"name": name})
    restaurant_id = db.session.execute(text("SELECT currval('restaurants_id_seq')")).fetchone()[0]
    sql2 = text("INSERT INTO locations (restaurant_id, address, city) VALUES (:restaurant_id, :address, :city)")
    db.session.execute(sql2, {"restaurant_id": restaurant_id, "address": address, "city": city})

    sql3 = text("INSERT INTO categories (name, restaurant_id) VALUES (:name, :restaurant_id)")
    db.session.execute(sql3, {"name": categories, "restaurant_id": restaurant_id})
    db.session.commit()

    return True
    