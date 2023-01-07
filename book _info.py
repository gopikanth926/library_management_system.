from flask import Flask, request
import mysql.connector

app = Flask(__name__)


@app.route("/insert_returned_book", methods=['post'])
def add_book_data():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="library managgement"
    )

    mycurser = db.cursor()

    input_data = request.get_json()

    bookid = input_data['bookid']
    userid = input_data['userid']
    date_of_return = input_data["date_of_return"]

    mycurser.execute('''insert into returned_books values(%s,%s,%s)''', (bookid, userid, date_of_return))
    print("Inserted")
    total = f''' select  * from books where bookid="{bookid}"'''
    mycurser.execute(total)
    res = mycurser.fetchall()
    for i in res:
        tot = i[-1]
        print(type(tot))
        total = tot + 1
        print(total)

        query3 = f'''update books set total="{total}" where bookid="{bookid}"'''
        mycurser.execute(query3)
        print(query3)

    db.commit()
    mycurser.close()
    db.close()
    return "True"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=2000)
