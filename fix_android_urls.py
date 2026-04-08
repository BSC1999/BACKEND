import os
import re

JAVA_DIR = r"c:\Users\bharg\AndroidStudioProjects\final\app\src\main\java\com\simats\afinal"

target_strings = [
    r'(?:"http://10\.134\.178\.1:8000/api)([^"]*)(")',
    r'(?:"http://10\.134\.178\.1:8000/)([^"]*)(")',
]

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # We want to replace "http://10.134.178.1:8000/..." with com.simats.afinal.network.RetrofitClient.BASE_URL + "..."
    
    # Simple replace
    content = content.replace('"http://10.134.178.1:8000/', 'com.simats.afinal.network.RetrofitClient.BASE_URL + "')

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(file_path)}")

def main():
    for root, dirs, files in os.walk(JAVA_DIR):
        for file in files:
            if file.endswith('.java'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
