from flask import Flask, request, jsonify, make_response
from flask_restx import Resource, Namespace
from database.database import Database

user = Namespace('user')

@user.route('')
class UserManagement(Resource):
    def get(self):
        # GET method 구현 부분
        db = Database()
        userInfoRequest = request.args.to_dict()

        id = userInfoRequest['id']
        pwd = userInfoRequest['password']

        query = "SELECT * FROM user WHERE id = '" + id + "'"
        userInfoDB = db.execute_one(query)

        db.close()

        if userInfoDB is None:
            return make_response(jsonify({'message' : '해당 유저가 존재하지 않음'}), 400)
        
        if pwd != userInfoDB['pw']:
            return make_response(jsonify({'message' : '아이디나 비밀번호 불일치'}), 400)
       
        return make_response(jsonify({'nickname' : userInfoDB['nickname']}), 200)

    def post(self):
        # POST method 구현 부분
        db = Database()
        newUser = request.get_json()

        id = newUser['id']
        pwd = newUser['password']
        nickname = newUser['nickname']

        query = "SELECT * FROM user WHERE id = '" + id + "'"
        userInfoDB = db.execute_one(query)

        if userInfoDB is None:
            query = "INSERT INTO user VALUES ('" + id + "','" + pwd + "','" + nickname + "')"
            db.execute(query)
            db.commit()
            db.close()
            return make_response(jsonify({'is_success' : True, 'message' : '유저 생성 성공'}), 200)
        
        db.close()
        return make_response(jsonify({'is_success' : False, 'message' : '이미 있는 유저'}), 400)


    def put(self):
        # PUT method 구현 부분
        db = Database()
        newUser = request.get_json()

        id = newUser['id']
        pwd = newUser['password']
        nickname = newUser['nickname']

        query = "SELECT * FROM user WHERE id = '" + id + "'"
        userInfoDB = db.execute_one(query)

        if userInfoDB is None or pwd != userInfoDB['pw']:
            db.close()
            return make_response(jsonify({'is_success' : False, 'message' : '아이디나 비밀번호 불일치'}), 400)
        
        if nickname == userInfoDB['nickname']:
            db.close()
            return make_response(jsonify({'is_success' : False, 'message' : '현재 닉네임과 같음'}), 400)
        
        query = "UPDATE user SET nickname = '" + nickname + "' WHERE id = '" + id + "'"
        db.execute(query)
        db.commit()
        db.close()
        return make_response(jsonify({'is_success' : True, 'message' : '유저 닉네임 변경 성공'}), 200)

    
    def delete(self):
        # DELETE method 구현 부분
        db = Database()
        userInfo = request.get_json()

        id = userInfo['id']
        pwd = userInfo['password']

        query = "SELECT * FROM user WHERE id = '" + id + "'"
        userInfoDB = db.execute_one(query)

        if userInfoDB is None or pwd != userInfoDB['pw']:
            db.close()
            return make_response(jsonify({'is_success' : False, 'message' : '아이디나 비밀번호 불일치'}), 400)
        
        query = "DELETE FROM user WHERE id = '" + id + "'"
        db.execute(query)
        db.commit()
        db.close()
        return make_response(jsonify({'is_success' : True,'message' : '유저 삭제 성공'}), 200)