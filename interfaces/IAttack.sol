pragma solidity ^0.8.0;

interface IAttack {
    
    // function signatures found using https://library.dedaub.com/decompile

    function start(uint256 varg0, uint256 varg1, uint256 varg2) external;

    function uniswapV2Call(address varg0, uint256 varg1, uint256 varg2, bytes calldata varg3) external;

    function tokensReceived(bytes4 varg0, bytes32 varg1, address varg2, address varg3, address varg4, uint256 varg5, bytes calldata varg6, bytes calldata varg7) external;

    function changeOwner(address varg0) external;

}

