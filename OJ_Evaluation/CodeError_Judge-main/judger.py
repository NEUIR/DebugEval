import judgeLib
import os

def judge(code_path, input_path, answer_path, timeLimit, memoryLimit, showDetails):
    test_cnt = len(os.listdir(input_path))
    AC_cnt = 0
    result = ''
    for i in range(test_cnt):
        # res, input, output, expected = judgeLib.judge(file_dir=code_path, input_dir=input_path+'/'+str(i+1)+'.in', answer_dir=answer_path+'/'+str(i+1)+'.out', timeLimit=timeLimit, memoryLimit=memoryLimit)
        res, input, output, expected = judgeLib.judge(file_dir=code_path, input_dir=os.path.join(input_path,str(i+1)+'.in'), answer_dir=os.path.join(answer_path, str(i+1)+'.out'), timeLimit=timeLimit, memoryLimit=memoryLimit, test_id=i) 
        if res=='AC':
            AC_cnt += 1
        elif result=='':
            result = res
        
        if showDetails:
            print('-------------------------')
            print('Sample ',i+1)
            if res=='AC':
                print("Test Result:\033[92m{}\033[0m".format(res))
            else:
                print("Test Result:\033[91m{}\033[0m".format(res))
            print('Input:\n', input)
            print('Output:\n', output)
            print('Expected:\n' ,expected)
            
    
    print("===========================")
    if result=='':
        result = 'AC'
        print("Test Result:\033[92m{}\033[0m".format(result))
    else:
        print("Test Result:\033[91m{}\033[0m".format(result))
    print("pass/total: ",AC_cnt,'/',test_cnt,'\n===============================')
    return result