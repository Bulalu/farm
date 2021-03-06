import { useEthers } from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants } from "ethers"
import brownieConfig from "../brownie-config.json"

export const Main = () => {
    // Show token values from the wallet
    // Get the address of different tokens
    // Get the balance of the users wallet

    // send the brownie-config to our 'src' folder
    // send the build folder

    const { chainId} = useEthers()
    console.log("chainID",chainId)
    const networkName = chainId ? helperConfig[chainId] : "dev"
    console.log(networkName)
    console.log(chainId)

    const dappTokenAddress = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero
    const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau_token"] : constants.AddressZero
    
    // const weth_token = "0xc778417E063141139Fce010982780140Aa0cD5Ab"
    console.log(dappTokenAddress)
    console.log(wethTokenAddress)
    console.log(fauTokenAddress)

    return (
        <div>gm!</div>
    )

}