const starknet = require("starknet");
const { RpcProvider, Contract, Account, ec, json, CallData, cairo, ERC20 } = starknet;

const provider = new RpcProvider({
    nodeUrl: "https://rpc.starknet.lava.build/lava-referer-cb6f2521-d467-40d9-a3a6-091bc7783813/",
});

let callCount = 0; // Contatore delle chiamate all'RPC

// get gas fee
const getTransactionByHash = async (txnHash) => {
    const result = await provider.getTransactionByHash(txnHash);
    console.log(result);
    callCount++; // Incrementa il contatore dopo ogni chiamata all'RPC
    console.log("Call count:", callCount);
}

const retryEvery5Seconds = async () => {
    const txnHash = "0x03bb60523d2e4349d159a0403e2194f3f06cfa3e4efb97347856e70ac8e650a9";
    while (true) {
        try {
            await getTransactionByHash(txnHash);
        } catch (error) {
            console.log("An error occurred, retrying in 5 seconds...");
        }
        await new Promise(resolve => setTimeout(resolve, 5000));
    }
}

retryEvery5Seconds();
