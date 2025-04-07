# Example: main.py
def validate_file(data, context):
    file_name = data['name']
    if file_name.endswith(".csv"):
        print(f"Valid file: {file_name}")
        # Move to processed folder logic here
