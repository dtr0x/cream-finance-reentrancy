import json

if __name__ == '__main__':
    with open('txdata/subcalls.json') as f:
        subcalls = json.load(f)
    attackInteractions = [s for s in subcalls if 'fromName' in s and s['fromName'] == 'Attack' or 'toName' in s and s['toName'] == 'Attack']
    print(json.dumps(attackInteractions, indent=4))
