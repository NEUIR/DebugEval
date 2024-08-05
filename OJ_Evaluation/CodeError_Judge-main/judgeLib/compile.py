import os
import subprocess

def compile(filename: str, test_id: int) -> bool:
    if filename.endswith('.c'):
        return compile_c(filename[:-2])
    elif filename.endswith('.cpp'):
        return compile_cpp(filename[:-4])
    elif filename.endswith('.java'):
        return compile_java(filename[:-5])
    else:
        return False

# def compile_c(filename: str) -> bool:
#     try:
#         subprocess.run(['gcc', filename+'.c', '-o', filename+'.exe'],
#                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         return True
#     except subprocess.CalledProcessError:
#         return False
def compile_c(filename: str) -> bool:
    try:
        result = subprocess.run(['gcc', filename+'.c', '-o', filename+'.exe'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Compilation failed with error:")
            print(result.stderr)
            return False
        else:
            return True
    except FileNotFoundError:
        print("GCC compiler not found or filename is invalid.")
        return False


# def compile_cpp(filename: str) -> bool:
#     try:
#         subprocess.run(['g++', filename+'.cpp', '-o', filename+'.exe'],
#                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         return True
#     except subprocess.CalledProcessError:
#         return False

def compile_cpp(filename: str) -> bool:
    try:
        result = subprocess.run(['g++', filename+'.cpp', '-o', filename+'.exe'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Compilation failed with error:")
            print(result.stderr)
            return False
        else:
            return True
    except FileNotFoundError:
        print("G++ compiler not found or filename is invalid.")
        return False


def compile_java(filename: str) -> bool:
    original_directory = os.getcwd()  # Save the current working directory.
    java_directory = os.path.dirname(filename)
    
    try:
        os.chdir(java_directory)  # Switch to the directory where the Java source file is located.
        subprocess.run(['javac', filename + '.java'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    finally:
        os.chdir(original_directory)  # Restore the original working directory.