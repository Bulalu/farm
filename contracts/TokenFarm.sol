pragma solidity ^0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import  "@openzeppelin/contracts/token/ERC20/IERC20.sol"; 11

contract TokenFarm is Ownable{
    // mapping token address -> staker address -> amount
    mapping(address => mapping(address => uint256)) public stakingBalance;
// stakeTokens
// unstakeTokens
// issueTokens (rewards)
// addAllowedTokens
// getEthValue
    address[] public allowedTokens;
    function stakeTokens(uint256 _amount, address _token) public {
        // what tokens can they stake?
        // how much can they stake?
        require(_amount > 0, "Amount must be greater than zero");
        require(tokenIsAllowed(_token), "Token is currently not allowed");
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        stakingBalance[msg.sender][_token] = stakingBalance[msg.sender][_token] + _amount;
    }

    function addAllowedTokens(address _token) public onlyOwner{
        // who can this functions
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public view returns (bool) {
        for( uint256 allowedTokensIndex=0; allowedTokensIndex < allowedTokens.length; allowedTokensIndex ++)
            if(allowedTokens[allowedTokensIndex] == _token){
                return true;
            }
        return false;
    }
}

