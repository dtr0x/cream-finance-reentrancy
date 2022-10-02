# Cream Finance Reentrancy 
A reconstruction of the reentrancy exploit described [here](https://rekt.news/cream-rekt/). Specifically, this code reproduces transaction [0xa9a1b8ea288eb9ad315088f17f7c7386b9989c95b4d13c81b69d5ddad7ffe61e](https://etherscan.io/tx/0xa9a1b8ea288eb9ad315088f17f7c7386b9989c95b4d13c81b69d5ddad7ffe61e) in which the attacker profits 9,740,000 AMP tokens and around 41 WETH. By carefully reconstructing the transaction using Brownie, an attack contract can be written close to the original. Doing so allows us to gain a deeper understanding of the vulnerability by analyzing the function calls in Solidity. 

## Methodology
### Retrieving data
Initially we can get the transaction hash, attacker address, and attack contract address from etherscan, along with the transaction input data. The chain is forked at the block before the attack. We add these parameters to our configuration in `brownie-config.yaml`. Additionally, the attack contract bytecode is run through a decompiler (such as [Dedaub](https://library.dedaub.com/decompile)) to get a rough idea of the function signatures, which are added to the interface `IAttack.sol`. We then send the transaction payload to the attacker contract from the attacker address to make sure we can replay the attack on our forked chain without issue. In doing so, we retrieve some highly important data which provides enough insight to reconstruct the attack contract (given in `txdata` folder):
* **call trace**: contract execution flow of the entire transaction
* **subcalls**: similar to call trace but useable as a python dict
* **trace**: details of every EVM instruction in the execution (not included due to size), useful for obtaining bytecode of any contracts created along the way

This preliminary step is done via `scripts/get_exploit_data.py`, which also retrieves and saves the Solidity source files of verified contracts which are a helpful reference to understand external calls. 

### Iterative development
Next we construct an attack contract, for which the primary reference is stepping through the call trace, call by call. Convenience added to do so:
```
python -m display.calltrace | less
```
Additionally, subcalls filtered to only show those that are from/to the attack contract can be viewed with
```
python -m display.subcalls | less
```
Equipped with our call trace in view, it's time to start writing `Exploit.sol`. We'll fire up `brownie console`, and test each addition to the contract by running `scripts/testdev.py`. This will recompile the contract and reset the chain, which is much quicker than having to exit the console and refork the chain every time. We also have to keep an eye out for any `CREATE`/`CREATE2` instructions in the call trace. In this particular attack, we have one, so it is necessary to inspect the full trace object to get the bytecode of the created contract and reconstruct it as well. 

### Deploy the exploit
The final result can be found in `contracts/Exploit.sol`. To test our reproduced attack, run 
```
brownie run exploit
```
which should produce the following output:
```
Running 'scripts/exploit.py::main'...
==================== Deploying exploit contract: ====================
Transaction sent: 0xd157a52f235363981182b290c39166b190355f1b85b9cb496dcaee638be2388f
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 0
  Exploit.constructor confirmed   Block: 13125072   Gas used: 1048890 (8.74%)
  Exploit deployed at: 0xf1b46CceBF14B15c3fdC6f71b72da1ae39734bEC

==================== Attacker balances before: ====================
AMP: 0.00
WETH: 0.00
==================== Starting exploit: ====================
Transaction sent: 0x6f809a9438cb07e80018b977af8392779d5233e440af41f4104a77af0594b9d9
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 1
  Exploit.start confirmed   Block: 13125073   Gas used: 1734425 (14.45%)

==================== Attacker balances after: ====================
AMP: 9740000.00
WETH: 41.08
Terminating local RPC client...
```

