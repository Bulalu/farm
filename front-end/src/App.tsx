import React from 'react';
import { ChainId, DAppProvider, Config } from '@usedapp/core';
import { Header } from './components/Header';

const config: Config = {
  supportedChains: [ChainId.Kovan, ChainId.Rinkeby]
  }


function App() {
  return (
    
    <DAppProvider config={config}>

      <Header />
      <div className="App">
          Hello web3
      </div>

    </DAppProvider>
   
  );
}

export default App;
