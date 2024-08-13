from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key
import uuid
import time
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

SECRET_KEY = '123456789'

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000', region_name='us-west-2')

def create_table():
    table = dynamodb.create_table(
        TableName='AppData',
        KeySchema=[
            {'AttributeName': 'PK', 'KeyType': 'HASH'},
            {'AttributeName': 'SK', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'GSI1',
                'KeySchema': [
                    {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            }
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='AppData')
    print("Table created successfully.")

table = dynamodb.Table('AppData')

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    user_id = str(uuid.uuid4())
    item = {
        'PK': f"USER#{user_id}",
        'SK': f"PROFILE#{user_id}",
        'AccountType': data['account_type'],
        'Email': data['email'],
        'Name': data['name']
    }
    table.put_item(Item=item)
    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

@app.route('/api/course', methods=['POST'])
def create_course():
    data = request.json
    course_id = str(uuid.uuid4())
    item = {
        'PK': f"COURSE#{course_id}",
        'SK': f"METADATA#{course_id}",
        'CourseTitle': data['title'],
        'CourseDescription': data['description'],
        'TeacherID': data['teacher_id']
    }
    table.put_item(Item=item)
    return jsonify({"message": "Course created successfully", "course_id": course_id}), 201

@app.route('/api/courses', methods=['GET'])
def list_courses():
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression=Key('GSI1PK').eq('COURSE')
    )
    courses = response.get('Items', [])
    return jsonify(courses), 200


@app.route('/api/enrollment', methods=['POST'])
def enroll_in_course():
    data = request.json
    item = {
        'PK': f"USER#{data['user_id']}",
        'SK': f"ENROLLMENT#{data['course_id']}",
        'EnrollmentDate': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    table.put_item(Item=item)
    return jsonify({"message": "Enrolled successfully"}), 201

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    response = table.get_item(Key={'PK': f"USER#{user_id}", 'SK': f"PROFILE#{user_id}"})
    item = response.get('Item')
    if not item:
        return jsonify({"message": "User not found"}), 404
    return jsonify(item), 200

@app.route('/api/user/<user_id>/enrollments', methods=['GET'])
def list_enrollments_for_user(user_id):
    response = table.query(
        KeyConditionExpression=Key('PK').eq(f"USER#{user_id}") & Key('SK').begins_with('ENROLLMENT#')
    )
    enrollments = response.get('Items', [])
    return jsonify(enrollments), 200


@app.route('/api/course/<course_id>', methods=['GET'])
def get_course(course_id):
    response = table.get_item(Key={'PK': f"COURSE#{course_id}", 'SK': f"METADATA#{course_id}"})
    item = response.get('Item')
    if not item:
        return jsonify({"message": "Course not found"}), 404
    return jsonify(item), 200

@app.route('/api/course/<course_id>/students', methods=['GET'])
def list_students_for_course(course_id):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression=Key('GSI1PK').eq(f"COURSE#{course_id}")
    )
    students = response.get('Items', [])
    return jsonify(students), 200


@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    data = request.json
    update_expression = "SET #name = :name, Email = :email"
    expression_attribute_names = {"#name": "Name"}
    expression_attribute_values = {":name": data['name'], ":email": data['email']}

    table.update_item(
        Key={'PK': f"USER#{user_id}", 'SK': f"PROFILE#{user_id}"},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )
    return jsonify({"message": "User profile updated successfully"}), 200


@app.route('/api/course/<course_id>', methods=['PUT'])
def update_course_details(course_id):
    data = request.json
    update_expression = "SET CourseTitle = :title, CourseDescription = :description, TeacherID = :teacher_id"
    expression_attribute_values = {
        ":title": data['title'],
        ":description": data['description'],
        ":teacher_id": data['teacher_id']
    }

    table.update_item(
        Key={'PK': f"COURSE#{course_id}", 'SK': f"METADATA#{course_id}"},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return jsonify({"message": "Course details updated successfully"}), 200


@app.route('/api/course/<course_id>/assign_teacher', methods=['POST'])
def assign_teacher_to_course(course_id):
    data = request.json
    teacher_id = data['teacher_id']

    update_expression = "SET TeacherID = :teacher_id"
    expression_attribute_values = {":teacher_id": teacher_id}

    table.update_item(
        Key={'PK': f"COURSE#{course_id}", 'SK': f"METADATA#{course_id}"},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return jsonify({"message": "Teacher assigned to course successfully"}), 200


def generate_token(user_id):
    token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       SECRET_KEY)
    return token


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression=Key('GSI1PK').eq(f"USER#{email}")
    )

    user = response.get('Items', [])
    if not user or not check_password_hash(user[0]['Password'], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user[0]['PK'].split('#')[1])
    return jsonify({"token": token}), 200


@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify({"message": "Token is invalid!"}), 401


if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0')