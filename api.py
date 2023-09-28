from flask import Flask, request, jsonify
import json

app = Flask(__name__)


# Function to write data to JSON file
def write_to_json(data, json_file_path):
  with open(json_file_path, "w") as json_file:
    json.dump(data, json_file)
    print(f"User input has been written to {json_file_path}.")


# Function to read data from JSON file
def read_from_json(json_file_path, password):
  try:
    with open(json_file_path, "r") as json_file:
      stored_data = json.load(json_file)
      if password in stored_data:
        return stored_data[password]
      else:
        return None
  except FileNotFoundError:
    return None


# Specify the JSON file path
json_file_path = "data.json"

# Check if the JSON file already exists
try:
  with open(json_file_path, "r") as json_file:
    data = json.load(json_file)
except FileNotFoundError:
  data = {}


# API route to receive user input
@app.route('/')
def index():
  return 'Hello from Flask!'


@app.route('/add_data', methods=['POST'])
def add_data():
  user_input = request.json.get("text")
  user = request.json.get("user")
  password = "cave"

  # Add the user input to the existing data dictionary
  if password in data:
    data[password].append("@"+user+":  " + user_input)
    
  else:
    data[password] = [user_input]

  # Write the updated data to the JSON file
  write_to_json(data, json_file_path)

  return jsonify({"message": "Data added successfully"})


# API route to retrieve messages
@app.route('/get_messages', methods=['GET'])
def get_messages():
  password = "cave"

  # Retrieve messages for the specified password
  messages = read_from_json(json_file_path, password)

  if messages:
    return jsonify({"messages": messages})
  else:
    return jsonify({"message": "No messages found for the given password"})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
