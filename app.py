from application import app, socketio

if __name__ == "__main__":
    socketio.run(app, debug=True)

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name=user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name=user))

#
# password = b"test"
# salt = bcrypt.gensalt(rounds=15)
# hash_pass = bcrypt.hashpw(password, salt)
# print(hash_pass)
#
# if bcrypt.checkpw(password, hash_pass):
#    print("Password is correct")
# else:
#    print("Password is incorrect")