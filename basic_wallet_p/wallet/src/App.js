import React, {useState} from 'react';
import axios from 'axios';

function App() {

  const [minedata, setMineData ] = useState({
     id: '',
     total: 0,
     transactions: [],

  })


  const handleSubmit = ()=>{
    axios.get('http://localhost:5000/chain')
    .then( res => {
      const transactions = res.data.chain
      // console.log(res.data.chain);
      transactions.map(block =>{ 
        // console.log(block.transaction)
        block.transaction.map(tran=> {
          setMineData({...block, transactions })
        })})
       console.log(transactions)   
    })
    

  }
  return (
    <div className="App">
      <header className="App-header">
       <h1>Mining Wallet</h1> 
       <input 
            type='text'
            name='id'
            placeholder='Enter I.D.'
            // value={}
            ></input>
        <button onClick={handleSubmit}>YOU MINE THEM COINS</button> 
      </header>
    </div>
  );
}

export default App;
