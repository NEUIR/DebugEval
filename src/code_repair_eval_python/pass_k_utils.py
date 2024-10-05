import numpy as np
import json

def read_jsonl_file(file_path):
    """
    Read data from file_path, and return a list of data
    :param file_path: The file path to read
    :return: The data read from file_path
    """
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            responses_success = item['responses_success']
            if responses_success == 'True':
                success = 1
            else:
                success = 0
            new_line = {'success':success}
            results.append(new_line)
    return results
def estimate_pass_at_k(num_samples, num_correct, k):
    """Estimates pass@k of each problem and returns them in an array."""

    def estimator(n: int, c: int, k: int) -> float:
        """Calculates 1 - comb(n - c, k) / comb(n, k)."""
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    import itertools

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array(
        [estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
    )


def calculate_pass_at_k(results, k_list=[1, 5]):
    # Calculate pass@k.
    total, correct = [], []
    for result in results:
        passed = [result["success"]]
        total.append(len(passed))
        correct.append(sum(passed))
    total = np.array(total)
    correct = np.array(correct)

    ks = k_list
    pass_at_k = {f"pass@{k}": estimate_pass_at_k(total, correct, k).mean()
                 for k in ks if (total >= k).all()}
    # print(pass_at_k)
    return pass_at_k

def pass_at_k(n,c,k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@k
    """
    if n<k: # k can't be bigger than n
        return float('nan')
    elif n-c<k:
        return 1.0
    else:
        return 1.0-np.prod(1.0-k/np.arange(n-c+1,n+1))

if __name__ == '__main__':
    file_path = ''
    results = read_jsonl_file(file_path)
    pass_1 = calculate_pass_at_k(results)
    print(pass_1)
