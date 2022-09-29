from brownie import *
import json
from contextlib import redirect_stdout

def recompile():
    globals()['Exploit'] = \
        compile_source(open('contracts/Exploit.sol').read()).Exploit

# this logic allows staying in the brownie console and
# iteratively testing call execution during contract development

def main():
    if not history:
        chain.snapshot()
    else:
        chain.revert()
        recompile()
    with redirect_stdout(None):
        attacker = accounts.add()
    exploit = Exploit.deploy({'from': attacker})
    exploit.start()
    history[-1].call_trace(True)

