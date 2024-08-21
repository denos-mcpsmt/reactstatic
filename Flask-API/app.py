from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import uuid
import time
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

SECRET_KEY = 'DUMMYEXAMPLEKEY'

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000', region_name='us-west-2')



def create_user_table():
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {'AttributeName': 'PK', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'SK', 'KeyType': 'RANGE'}  # Sort key
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
    table.meta.client.get_waiter('table_exists').wait(TableName='Users')
    print("Users table created successfully.")


# Create the Courses table
def create_courses_table():
    table = dynamodb.create_table(
        TableName='Courses',
        KeySchema=[
            {
                'AttributeName': 'CourseID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'CourseID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Category',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='Courses')

    print(f"Table {table.table_name} created successfully!")

# Ensure the Users table exists
def ensure_table_exists(table_name):
    try:
        # Check if the table exists by trying to describe it
        table = dynamodb.Table(table_name)
        table.load()
        print(f"Table '{table_name}' already exists.")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # Table does not exist, create it
            print(f"Table '{table_name}' does not exist. Creating...")
            return False
        else:
            # Some other error occurred
            print(f"Unexpected error occurred: {e}")
            raise

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    print("here")
    # Check if user already exists
    table = dynamodb.Table('Users')
    table.load()
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression=Key('GSI1PK').eq(f"USER#{email}")
    )
    if response.get('Items'):
        return jsonify({"message": "User already exists"}), 400

    # Hash the password for security
    hashed_password = generate_password_hash(password, method='scrypt')

    # Create a new user ID
    user_id = str(uuid.uuid4())

    # Create the user item
    item = {
        'PK': f"USER#{user_id}",
        'SK': f"PROFILE#{user_id}",
        'GSI1PK': f"USER#{email}",
        'GSI1SK': f"PROFILE#{user_id}",
        'Name': name,
        'Email': email,
        'Password': hashed_password,
        'AccountType': 'regular'  # You can customize this as needed
    }

    # Store the user in the database
    table.put_item(Item=item)

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201


# Function to add course to DynamoDB (same as before)
def add_course(course_id, teacher, students, schedule, fee, category):
    table = dynamodb.Table('Courses')

    table.put_item(
        Item={
            'CourseID': course_id,
            'Teacher': teacher,
            'EnrolledStudents': students,
            'Schedule': schedule,
            'Fee': fee,
            'Category': category
        }
    )
    print(f"Course {course_id} added successfully!")

@app.route('/api/course', methods=['POST'])
def create_course():
    try:
        # Parse the incoming JSON data
        data = request.get_json()

        # Extract details from the JSON payload
        course_id = data['course_id']
        teacher = data['teacher']
        students = data['students']
        schedule = data['schedule']
        fee = data['fee']
        category = data['category']

        # Add the course to DynamoDB
        add_course(course_id, teacher, students, schedule, fee, category)

        # Return a success response
        return jsonify({'message': 'Course created successfully!'}), 201

    except Exception as e:
        # Handle errors and return an appropriate response
        return jsonify({'error': str(e)}), 400

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




@app.route('/', methods=['GET'])
def home():
    return jsonify({"messge":"Hello this is Darren"}), 401


if not ensure_table_exists('Users'):
    create_user_table()

if not ensure_table_exists('Courses'):
    create_courses_table()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')