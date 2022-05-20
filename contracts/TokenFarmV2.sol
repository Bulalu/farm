pragma solidity ^0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import  "@openzeppelin/contracts/token/ERC20/IERC20.sol"; 
import  "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "./DappToken.sol";

contract TokenFarmV2 is Ownable, DappToken{

    using SafeERC20 for IERC20;

    // mapping token address -> staker address -> amount
    mapping(address => mapping(address => uint256)) public stakingBalance;
    mapping(address => uint256) public uniqueTokensStaked;
    mapping(address => address) public tokenPriceFeedMapping;
   
    address[] public stakers;
    address[] public allowedTokens;
    address public rewardToken;

    // total supply of minted shares
    uint256 public totalSupplyShares;

    event Rewards(uint256 amount, address user);

    constructor(address _rewardToken){
        rewardToken = (_rewardToken);
    }

    function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }
    // users can also claim instead of looping and sending them on yo own
    function issueTokens() public onlyOwner {
        // Issue tokens to all stakers
        for( uint256 stakersIndex = 0; stakersIndex < stakers.length; stakersIndex ++){

            address recepient = stakers[stakersIndex];
            uint256 userTotalValue = getUserTotalValue(recepient);
            // send tokens rewards based on TVL
            IERC20(rewardToken).safeTransfer(recepient, userTotalValue);
        }
    }

    function claimRewards() public {
        // claim rewards for every token type (DAI, FAU) staked
        // should mint new tokens dapp tokens
        // balanceofstaked should be greater than 0 
        uint256 rewards = getUserTotalValue(msg.sender);
        require(rewards > 0, "Nothing to Claim" );

        emit Rewards(rewards, msg.sender);
        _mint(msg.sender, rewards);
    }

    function calculateShares(uint256 _amount, address _token) public returns(uint256 dunno) {
        


        uint256 farmBalance = IERC20(_token).balanceOf(address(this));
        require(farmBalance > 0, "Insufficient Amount");
        if (totalSupplyShares == 0) { 
            totalSupplyShares = _amount;
        }

        dunno = (_amount * totalSupplyShares) / farmBalance;

        return dunno;


    }
    
    function farmBalance(address _token) public view returns(uint256 _balance) {
        
        _balance = IERC20(_token).balanceOf(address(this));
        return _balance;
    }
    // get total for all tokens staked eth/dai/usdc
    function getUserTotalValue(address _user) internal view returns(uint256 amount){
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "Nothing staked bruh");
        for(uint256 allowedTokensIndex = 0; allowedTokensIndex < allowedTokens.length; allowedTokensIndex++){
            
            totalValue = totalValue + getUserSingleTokenValue(_user, allowedTokens[allowedTokensIndex]);
        }

        return totalValue;
        
        
    }

    function getUserSingleTokenValue(address _user, address _token) public view returns(uint256){
        if (uniqueTokensStaked[_user] == 0) {
            return 0;
        }

        // price of the token * stakingBalance[_token][user]
        (uint256 price, uint256 decimal) = getTokenPrice(_token);
        // 10 * 10**18 ETH
        // ETH/USD -> $3000 * 10**18?
        // 10 * 10**18 * 3000 / 10** DECIMALS
        uint256 rewards = (stakingBalance[_token][_user] * price / (10**uint256(decimal)));
        return rewards;

    }

    function getTokenPrice(address _token) public view returns(uint256 price, uint256 decimals){
        // priceFeedAddress
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        (,int256 price,,,) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);

    }
    function stakeTokens(uint256 _amount, address _token) public {
        
        require(_amount > 0, "Amount must be greater than zero");
        require(tokenIsAllowed(_token), "Token is currently not allowed");
        
        IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);
        updateUniqueTokensStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] = stakingBalance[_token][msg.sender] + _amount;
       
        if (uniqueTokensStaked[msg.sender] == 1){
            stakers.push(msg.sender);
        }
    }

    function unstakeTokens(address _token) public {

        // should burn them dapp tokens
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Yoo Nothing to unstake here bro, GET LOST");
        
        
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender] = uniqueTokensStaked[msg.sender] - 1;

        IERC20(_token).safeTransfer(msg.sender, balance);

    }
    // @dev checks to see if the user has already staked or not
    // so that you will add the users twice on the staker mapping
    // sure there is other ways this could be done
    function updateUniqueTokensStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }

    function addAllowedTokens(address _token) public onlyOwner{
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

