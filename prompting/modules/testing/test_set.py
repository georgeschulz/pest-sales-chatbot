import pandas as pd

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

class TestSet:
    def __init__(self, test_set, function):
        self.test_set = test_set
        self.function = function

    def check(self, key):
        value = self.test_set[key]['prompt']
        response = self.function(value)
        if response == self.test_set[key]['expected']:
            print(GREEN + "/ PASS | Result: " + response + " | Expected: " + self.test_set[key]['expected'] + ' | Data ID: ' + str(key) + RESET)
            return 1
        else:
            print(RED + "X FAIL | Result: " + response + " | Expected: " + self.test_set[key]['expected'] + ' | Data ID: ' + str(key) + RESET)
            return 0
    
    def run(self, test_name, print_test_name=True, print_results=True, iter=1, results_loc=None):
        if print_test_name:
            print(BOLD + test_name + RESET + '\n')

        total_tokens = 0
        total_count = len(self.test_set) * iter
        correct_count = 0
        for i in range(iter):
            for key in self.test_set:
                correct_count += self.check(key)
        
        if print_results:
            print(BOLD + "Total: " + str(total_count) + " | Correct: " + str(correct_count) + " | Incorrect: " + str(total_count - correct_count) + ' | Accuracy: ' + str(correct_count/total_count) + RESET)

        if results_loc:
            #check if a file exists at results_loc called results.csv
            if os.path.isfile(results_loc + 'results.csv'):
                results = pd.read_csv(results_loc + 'results.csv')
            else:
                results = pd.DataFrame(columns=['test_name', 'total_count', 'correct_count', 'incorrect_count', 'accuracy'])
            
            new_results = pd.DataFrame([[test_name, total_count, correct_count, total_count - correct_count, correct_count/total_count]], columns=['test_name', 'total_count', 'correct_count', 'incorrect_count', 'accuracy'])
            combined = pd.concat([results, new_results])

            combined.to_csv(results_loc + 'results.csv', index=False)
            
    def __call__(self, indexes):
        for index in indexes:
            datapoint = self.test_set[index]
            print("ID: " + str(index) + " | " +  datapoint['prompt'])