pragma solidity ^0.8.6;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DappToken is ERC20 {
    
    constructor() public ERC20("Dapp Token", "DAPP"){
       
    }

    function mint(uint256 amount) public {
        _mint(msg.sender, amount);
    }
}