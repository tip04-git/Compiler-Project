import subprocess
import tempfile
import os

# Paths to interpreters
INTERPRETER_PATHS = {
    "python": "./interpreters/python/python.exe",
    "javascript": "./interpreters/nodejs/node.exe",
    "bash": "C:/Program Files/Git/bin/bash.exe",  # Full path to bash.exe
}

# Detect the language
def detect_language(code):
    if "def " in code or "print(" in code:
        return "python"
    elif "console.log(" in code or "function " in code:
        return "javascript"
    elif "echo " in code or "#!/bin/bash" in code:
        return "bash"
    else:
        raise ValueError("Language not recognized")

# Execute the code using the respective interpreter
def execute_code(language, code):
    with tempfile.NamedTemporaryFile(delete=False, suffix={
        "python": ".py",
        "javascript": ".js",
        "bash": ".sh"
    }[language]) as temp_file:
        temp_file.write(code.encode())
        temp_file.flush()
        temp_path = temp_file.name

    try:
        subprocess.run([INTERPRETER_PATHS[language], temp_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        temp_file.close()

# Main function
def main():
    print("Welcome to the Cross-Language Compiler!")
    print("Enter your code below (end with 'END' on a new line):")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    code = "\n".join(lines)
    try:
        lang = detect_language(code)
        print(f"Detected language: {lang}")
        print("Executing your code...")
        execute_code(lang, code)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
