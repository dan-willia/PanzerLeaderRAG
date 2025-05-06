import pandas as pd

"""
For human evaluation of generated answers vs expected answers:
only machine-evaluated answers as 'false' are printed
"""

data = pd.read_csv("evaluation_edited.csv")

def print_output():
    for row in range(len(data)):
        if 'false' in str(data.loc[row,'3.5-turbo eval']).lower():
            query = data.loc[row,'Question']
            expected = data.loc[row,'Expected Answer']
            actual = data.loc[row,'3.5 Turbo']
            print(f"On question {row} ({query}):")
            print(f"EXPECTED ==> {expected}")
            print(f"GOT ==> {actual}")
            print()
        
def main():
    print_output()
    
if __name__ == '__main__':
    main()