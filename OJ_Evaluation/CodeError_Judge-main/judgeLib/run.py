import os
import subprocess
import psutil
import shutil

def run(file_dir: str, input: str, timeLimit: float, memoryLimit: int) -> str:
    # file_dir is the path to the executable file, input is the sample input, timeLimit is the time limit, and memoryLimit is the memory limit.
    res = ''

    try:
        # run the program
        process = subprocess.Popen(
            [file_dir], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    except RuntimeError:
        res = 'RE'
    except MemoryError:
        res = 'MLE'
    except TimeoutError:
        res = 'TLE'
    except:
        res = 'CE'

    if res == '':
        # calculate memory usage
        memory_usage = psutil.Process(process.pid).memory_info().rss / (1024 ** 2)
        if memory_usage > memoryLimit:
            res = 'MLE'

    if res == '':
        try:
            output, error = process.communicate(
                input.encode('utf-8', 'ignore'), timeout=timeLimit)
        except subprocess.TimeoutExpired:
            res = 'TLE'
        except:
            res = 'RE'


    if res == '':
        # check if the program is something wrong
        if error:
            res = 'CE'

    # close the process
    process.terminate()
    process.wait()

    if res == '':
        output = output.decode('utf-8')
        output_lines = output.split('\n')
        cleaned_output = '\n'.join(line.strip() for line in output_lines)
        return cleaned_output
    else:
        return res
    

def runPy(file_dir: str, input: str, timeLimit: float, memoryLimit: int, test_id: int) -> str:
    # file_dir is the path to the .py (Python) file, input is the sample input, timeLimit is the time limit, and memoryLimit is the memory limit.
    res = ''
    
    try:
        # Run the Python script
        process = subprocess.Popen(
            ['python', file_dir], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    except RuntimeError:
        res = 'RE'
    except MemoryError:
        res = 'MLE'
    except TimeoutError:
        res = 'TLE'
    except:
        res = 'RE'

    if res == '':
        memory_usage = psutil.Process(process.pid).memory_info().rss / (1024 ** 2)
        if memory_usage > memoryLimit:
            res = 'MLE'

    if res == '':
        try:
            output, error = process.communicate(
                input.encode('utf-8', 'ignore'), timeout=timeLimit)
            stderr_output = error.decode('utf-8').strip()
            if stderr_output is not "":
                print("test",test_id+1,"Error occurred:")
                print(stderr_output,'\n')
        except subprocess.TimeoutExpired:
            res = 'TLE'
        except:
            res = 'RE'

    if res == '':
        if error:
            res = 'RE'

    process.terminate()
    process.wait()

    if res == '':
        output = output.decode('utf-8')
        output_lines = output.split('\n')
        cleaned_output = '\n'.join(line.strip() for line in output_lines)
        return cleaned_output
    else:
        return res

# def runPy(file_dir: str, input: str, timeLimit: float, memoryLimit: int, test_id: int) -> str:
#     res = ''
#     output = ''
#     error = ''

#     try:
#         process = subprocess.Popen(
#             ['python', file_dir],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             shell=False
#         )
#         output, error = process.communicate(input.encode('utf-8', 'ignore'), timeout=timeLimit)
#         process.wait()

#         memory_usage = psutil.Process(process.pid).memory_info().rss / (1024 ** 2)
#         if memory_usage > memoryLimit:
#             res = 'MLE'
#             print("Memory Limit Exceeded")

#         if process.returncode != 0:
#             res = 'RE'
#             print("test ",test_id,", Runtime error occurred:")
#             print(error.decode('utf-8'))  # Print the runtime error message
#         else:
#             output = output.decode('utf-8')
#             output_lines = output.split('\n')
#             cleaned_output = '\n'.join(line.strip() for line in output_lines)
#             return cleaned_output

#     except subprocess.TimeoutExpired:
#         res = 'TLE'
#         process.terminate()
#     except Exception as e:
#         res = 'RE'
#         print("Unexpected error occurred:", e)

#     return res


def runJava(file_dir: str, input: str, timeLimit: float, memoryLimit: int) -> str:
    res = ''
    print(file_dir)
    try:
        # Extract Java class and folder from file_dir
        java_class = os.path.splitext(os.path.basename(file_dir))[0]
        java_folder = os.path.dirname(file_dir)

        run_process = subprocess.Popen(
            ['java', '-cp', java_folder, java_class], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    except RuntimeError:
        res = 'RE'
    except MemoryError:
        res = 'MLE'
    except TimeoutError:
        res = 'TLE'
    except Exception as e:
        res = 'CE'
        print("Exception:", str(e))

    if res == '':
        memory_usage = psutil.Process(run_process.pid).memory_info().rss / (1024 ** 2)
        if memory_usage > memoryLimit:
            res = 'MLE'

    if res == '':
        try:
            output, error = run_process.communicate(
                input.encode('utf-8', 'ignore'), timeout=timeLimit)
        except subprocess.TimeoutExpired:
            res = 'TLE'
        except Exception as e:
            res = 'RE'
            print("Exception:", str(e))

    if res == '':
        if error:
            res = 'CE'
            try:
                error_str = error.decode('utf-8', 'ignore')
                print("Runtime Error:", error_str)
            except UnicodeDecodeError:
                error_str = error.decode('latin-1', 'ignore')
                print("Runtime Error (Non-UTF-8 Output):", error_str)

    run_process.terminate()
    run_process.wait()

    if res == '':
        output = output.decode('utf-8')
        output_lines = output.split('\n')
        cleaned_output = '\n'.join(line.strip() for line in output_lines)
        return cleaned_output
    else:
        return res