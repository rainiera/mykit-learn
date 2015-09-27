__author__ = 'rainierababao'

import time
import rethinkdb as r

r.connect('localhost', 28015, db='yelp').repl()

def rethink_speed_test_list():
    """Time to make a connection and generate a list of all the
    five-star reviews in the data set.
    """
    t0 = time.time()
    cursor = r.table('reviews').filter(r.row['stars'] == 5).run()
    t1 = time.time()
    five_star_reviews = [document for document in cursor]
    t2 = time.time()
    print ('time to make db conn: {0}').format(t1-t0)
    print ('time to generate list: {0}').format(t2-t1)
    print ('num 5-star reviews {0}').format(len(five_star_reviews))

def rethink_speed_test_count():
    t0 = time.time()
    count = r.table('reviews').count(lambda review: review['stars'] == 5).run()
    t1 = time.time()
    print ('time to count 5-star reviews: {0}').format(t1-t0)
    print ('num 5-star reviews {0}').format(count)


if __name__ == "__main__":
    rethink_speed_test_count()
