from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

import jwt
import datetime
import hashlib



@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({'id': payload['id']})
        return render_template('index.html')

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/signup')
def signup():
    msg = request.args.get("msg")
    return render_template('signup.html', msg=msg)


@app.route('/api/signup', methods=['POST'])
def api_signup():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'email': email_receive, 'pw': pw_hash})

    return jsonify({'result': 'success'})


@app.route('/api/login', methods=['POST'])
def api_login():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'email': email_receive, 'pw': pw_hash})
    user_info = db.users.find_one({})

    if result is not None:
        payload = {
            'id': user_info[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '다시 입력하세요. 아이디/비밀번호가 일치하지 않습니다.'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

