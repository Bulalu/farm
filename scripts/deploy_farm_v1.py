from scripts.helpful_scripts import get_account, get_contract
from brownie import DappToken, TokenFarm, config, network
from web3 import Web3


#balance that will remain in our dapptoken contract
KEPT_BALANCE = Web3.toWei(100, "ether")

def deploy_token_farm_and_dapp_token():
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    dapp_token.mint(1000000000000000000000000, {"from":account})
    token_farm = TokenFarm.deploy(dapp_token.address, {"from": account}, publish_source = config["networks"][network.show_active()]["verify"])

   
    tx = dapp_token.transfer(token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account})
    tx.wait(1)

    # dapp_token, weth_token, fau_token/dai
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed")
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)

    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(token, dict_of_allowed_tokens[token], {"from": account})
        set_tx.wait(1)

def main():
    deploy_token_farm_and_dapp_token()


dapp_token_Address_rinkeby = "0xddac861531d7d52E7758FB4FA317c8Aec5cc8599"
token_farm_Address_rinkeby = "0xA49eF7D22Be1d1831087F85237aF13ce5BE2e590 "