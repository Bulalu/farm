import pytest
from brownie import network, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS,  get_account, get_contract, INITIAL_PRICE_FEED_VALUE
from scripts.deploy_farm_v2 import deploy_token_farm_and_dapp_token
import pytest
import brownie



def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    owner = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {"from": owner})

    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address
    
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {"from": non_owner})


def test_stake_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    owner = get_account()
    non_owner = get_account(index=1)
    bob = get_account(index=2)
    fau_token = get_contract("fau_token")
    weth_token = get_contract("weth_token")
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    staking_amount = 1 * 10**18
    
    
    weth_token.transfer(non_owner, staking_amount, {"from": owner})
    weth_token.transfer(bob, staking_amount*2, {"from": owner})

    balance_before_staking = dapp_token.balanceOf(token_farm)
    print("User balance before staking:", balance_before_staking)
    
    print(fau_token.balanceOf(owner))
    with brownie.reverts("Amount must be greater than zero"):
        token_farm.stakeTokens(0, weth_token.address, {"from": non_owner})

    with brownie.reverts("Token is currently not allowed"):
        token_farm.stakeTokens(staking_amount, non_owner, {"from": non_owner})

    # non owner
    weth_token.approve(token_farm, staking_amount, {"from": non_owner})
    token_farm.stakeTokens(staking_amount, weth_token.address, {"from": non_owner})

    weth_token.approve(token_farm, staking_amount * 2, {"from": bob})
    token_farm.stakeTokens(staking_amount * 2, weth_token.address, {"from": bob})

    assert(token_farm.stakingBalance(weth_token.address, bob) == staking_amount * 2)
    assert(token_farm.stakingBalance(weth_token.address, non_owner) == staking_amount)
    assert(token_farm.stakers(0) == non_owner)
    assert(token_farm.stakers(1) == bob)
    assert(weth_token.balanceOf(token_farm) == (staking_amount * 3))
    
    return token_farm, dapp_token, weth_token

def test_issue_token():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    owner = get_account()
    non_owner = get_account(index=1)
    bob = get_account(index=2)
    token_farm, dapp_token, weth_token = test_stake_tokens()
    
    print(dapp_token.balanceOf(non_owner))

    token_farm.issueTokens({"from": owner})

    print(dapp_token.balanceOf(non_owner))

    rewards_for_non_owner = (INITIAL_PRICE_FEED_VALUE * token_farm.stakingBalance(weth_token.address, non_owner))//10 ** 18
    rewards_for_bob = (INITIAL_PRICE_FEED_VALUE * token_farm.stakingBalance(weth_token.address, bob))//10 ** 18

    assert (dapp_token.balanceOf(non_owner) == rewards_for_non_owner )
    assert (dapp_token.balanceOf(bob) == rewards_for_bob )

    
def test_unstake_tokens():

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    owner = get_account()
    alice = get_account(index=1)
    bob = get_account(index=2)

    token_farm, dapp_token, weth_token = test_stake_tokens()

    bob_bal_before = weth_token.balanceOf(bob)
    alice_bal_before = weth_token.balanceOf(alice)
    print(bob_bal_before, alice_bal_before)

    bob_staking_bal = token_farm.stakingBalance(weth_token.address, bob)
    alice_staking_bal = token_farm.stakingBalance(weth_token.address, alice)
    token_farm.unstakeTokens(weth_token.address, {"from": bob})
    token_farm.unstakeTokens(weth_token.address, {"from": alice})

    assert( bob_staking_bal == weth_token.balanceOf(bob))
    assert( alice_staking_bal == weth_token.balanceOf(alice))

    with brownie.reverts("Yoo Nothing to unstake here bro, GET LOST"):
        token_farm.unstakeTokens(weth_token.address, {"from": owner})


def test_claim_rewards():

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    owner = get_account()
    alice = get_account(index=1)
    bob = get_account(index=2)

    token_farm, dapp_token, weth_token = test_stake_tokens()

    bob_bal_before = dapp_token.balanceOf(bob)
    alice_bal_before = dapp_token.balanceOf(alice)

    tx_alice = token_farm.claimRewards({"from": alice})
    tx_alice = token_farm.claimRewards({"from": alice})
    tx_alice = token_farm.claimRewards({"from": alice})
    assert "Rewards" in (tx_alice.events)
    assert tx_alice.events["Rewards"]["amount"] == token_farm.balanceOf(alice)
    print("dapp token balance",token_farm.balanceOf(bob))
    
    #check out this error
    
def test_calculate_share():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    owner = get_account()
    non_owner = get_account(index=1)
    bob = get_account(index=2)
    fau_token = get_contract("fau_token")
    weth_token = get_contract("weth_token")
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    staking_amount = 1 * 10**18
    
    
    weth_token.transfer(non_owner, staking_amount, {"from": owner})
    weth_token.transfer(bob, staking_amount*2, {"from": owner})

    with brownie.reverts("Insufficient Amount"):
        token_farm.calculateShares(staking_amount, weth_token, {"from": bob})
    
    # calculate_shares = token_farm.calculateShares(staking_amount, weth_token, {"from": bob})
    # print(calculate_shares)
   
    weth_token.approve(token_farm, staking_amount, {"from": non_owner})
    token_farm.stakeTokens(staking_amount, weth_token.address, {"from": non_owner})

    calculate_shares = token_farm.calculateShares(staking_amount,weth_token)
    print("Calculate Shares", calculate_shares)
