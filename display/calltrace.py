import json

if __name__ == '__main__':
    with open('txdata/calltrace.out') as f:
        for l in f:
            print(l, end='')
