from flask import Flask, request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="library managgement"
    )
mycurser = db.cursor()


@app.route("/insert_book", methods=['post'])
def add_a():
    try:

        input_data = request.get_json()
        for i in input_data:
            print(i)
            bookname = i['bookname']
            bookid = i['bookid']
            author = i['author']
            gener = i['gener']
            total = i['total']
            mycurser.execute('''insert into books values(%s,%s,%s,%s,%s)''', (bookname, bookid, author, gener, total))
            print("Inserted")
        db.commit()
        mycurser.close()
        db.close()
        return {'status': 'succesfully inserted'}

    except Exception as e:
        print(f"error : {str(e)}")
        return {'status':"invalid"}


@app.route("/insert_userdata", methods=['post'])
def add_userdata():
    try:

        input_data = request.get_json()
        for i in input_data:
            print(i)
            username = i['username']
            userid = i['userid']
            emailid = i['emailid']
            phone = i['phone']
            active = i['active']
            mycurser.execute('''insert into user_details values(%s,%s,%s,%s,%s)''',
                             (username, userid, emailid, phone, active))
            print("Inserted")
        db.commit()
        mycurser.close()
        db.close()
        return {'status':'succesfully inserted'}
    except Exception as e:
        print(f"error : {str(e)}")
        return {'status': 'invalid'}


@app.route("/update_userdata", methods=['post'])
def update_data():
    try:

        input_data = request.get_json()
        print(input_data)
        username = input_data["username"]
        emailid = input_data["emailid"]
        phone = input_data["phone"]
        query = f'''update user_details  set emailid="{emailid}",phone="{phone}" where username="{username}"'''
        print(query)
        mycurser.execute(query)
        print("updated")
        db.commit()
        mycurser.close()
        db.close()
        return {'status':'succesfully updated','info':query}
    except Exception as e:
        print(f"erroe : {str(e)}")
        return {'status':'invalid'}



@app.route("/delete_userdata", methods=['post'])
def add_f():
   try:
        input_data = request.get_json()
        active = input_data['active']
        query = f'''DELETE FROM user_details WHERE active="{active}"'''

        print(query)
        mycurser.execute(query)
        print("deleted")
        db.commit()
        mycurser.close()
        db.close()
        return {'status':'succesfully deleted','info':query}
   except Exception as e:
       print(f"error : {str(e)}")
       return {'status':"invalid"}


@app.route("/insert_issued_book", methods=['post'])
def add_book_data():
    try:
        mycurser = db.cursor()
        input_data = request.get_json()

        bookid = input_data['bookid']
        userid = input_data['userid']
        issued_date = input_data["issued_date"]
        expected_return = input_data["expected_return"]
        mycurser.execute('''insert into issued_books values(%s,%s,%s,%s)''', (bookid, userid, issued_date, expected_return))
        print("Inserted")
        total = f''' select  * from books where bookid="{bookid}"'''
        mycurser.execute(total)
        res = mycurser.fetchall()
        for i in res:
            tot = i[-1]
            print(type(tot))
            total = tot - 1
            print(total)
        if total>=1:
            query3=f'''update books set total="{total}" where bookid="{bookid}"'''
            mycurser.execute(query3)
        else:
            print("no books avilable")
        db.commit()
        mycurser.close()
        db.close()
        return {"status":"successfully insrted and updated","info":query3}
    except Exception as e:
        print(f"error : {str(e)}")
        return {'status':'invalid'}

@app.route("/insert_returned_book", methods=['post'])
def add_return_book_data():
    try:
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
        return {"status" : "succuessully inserted"}
    except Exception as e:
        print(f"error:{str(e)} ")
        return {"status":"invalid"}





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1000)
