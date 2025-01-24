import streamlit as st
import subprocess
import tempfile

import os

# Define interpreter paths based on the environment
# Check if running on Streamlit Cloud
is_deployed = os.environ.get("HOME", "").startswith("/home/appuser")

# Define interpreter paths based on the environment
INTERPRETER_PATHS = {
    "python": "./interpreters/python/python.exe" if not is_deployed else "python",
    "javascript": "./interpreters/nodejs/node.exe" if not is_deployed else "node"
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
        result = subprocess.run(
            [INTERPRETER_PATHS[language], temp_path],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    finally:
        temp_file.close()

# Streamlit Interface
st.title("Cross-Language Compiler")
st.subheader("Enter your code below:")

code_input = st.text_area("Code Input", height=300, placeholder="Write your Python, JavaScript, or Bash code here.")

if st.button("Run Code"):
    if code_input.strip():
        try:
            language = detect_language(code_input)
            st.write(f"Detected Language: {language.capitalize()}")
            output = execute_code(language, code_input)
            st.text_area("Output", output, height=200)
        except ValueError as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter code to compile!")
