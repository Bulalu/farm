import React from 'react';
import { ChainId, DAppProvider, Config } from '@usedapp/core';
import { Header } from './components/Header';
import { Container } from '@material-ui/core';
import { Main } from "./components/Main"

const config: Config = {
  supportedChains: [ChainId.Kovan, ChainId.Rinkeby]
  }


function App() {
  return (
    
    <DAppProvider config={config}>

      <Header />
      <Container maxWidth="md">
        <div className="App">
            Hello web3
        </div>
        <Main/>
      </Container>
      
    </DAppProvider>
   
  );
}

export default App;
