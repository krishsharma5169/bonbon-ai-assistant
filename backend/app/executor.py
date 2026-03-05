import subprocess
import tempfile
import os

def execute_python(code: str, input_data: str = None):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode())
        filename = tmp.name

    try:
        result = subprocess.run(
            ["python", filename],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5
        )

        success = result.returncode == 0
        output = result.stdout if success else result.stderr

        return success, output

    except Exception as e:
        return False, str(e)

    finally:
        os.remove(filename)