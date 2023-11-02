from sqlalchemy.sql import text
from db import db

def get_reviews():
    result = db.session.execute(text("SELECT restaurants.*, locations.address, locations.city, categories.name,\
                                    AVG(reviews.stars) AS avg_stars, COUNT(reviews.id) AS review_count,\
                                    array_agg(reviews.comment) AS comments FROM restaurants \
                                    LEFT JOIN locations ON restaurants.id = locations.restaurant_id \
                                    LEFT JOIN reviews ON restaurants.id = reviews.restaurant_id \
                                    LEFT JOIN categories ON restaurants.id = categories.restaurant_id \
                                    GROUP BY restaurants.id , locations.id, categories.id"))
    return result.fetchall()

def add_review(restaurant_id, stars, comment):
    sql = text("INSERT INTO reviews (restaurant_id, stars, comment) VALUES (:restaurant_id, :stars, :comment)")
    db.session.execute(sql, {"restaurant_id":restaurant_id, "stars":stars, "comment":comment})
    db.session.commit()