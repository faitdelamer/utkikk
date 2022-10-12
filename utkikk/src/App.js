import './App.css';
import './Table.css';
import React, { useState } from 'react';
import Table from "./Table";
import Pagenav from "./Pagenav";

export default function App() {
  
  const [data, setData] = useState({});
  const [meta, setMeta] = useState({});
  const [find, setFind] = useState("");
  const [size, setSize] = useState(10);
  const [side, setSide] = useState(1); // Ikke implementert skikkelig, neste på listen
  const [sort, setSort] = useState([""]); // Ikke implementert sortering i frontend, denne sender en liste
  const [order, setOrder] = useState(""); // ^ implementeres sammen med sortering
  const [getParams, setGetParams] = useState("") // ikke implementert
  const [argList, setArgList] = useState([]) // ikke implementert
  const headers = ["id", "First name", "Last name", "Age", "Street", "City", "State", "Lat", "Lon", "CCNO"];
  const tableLen = [{value: 10, text:"10"}, {value: 20, text:"20"}, {value: 50, text:"50"}, {value: 100, text:"100"}]
  const url = "http://localhost:5000/api/data?";
  
  const updSize = event => {
    setSize(event.target.value)
  }
  const updFind = event => {
    setFind(event.target.value)
  }

  React.useEffect(() => { //gjør query mot API. Denne må videre utvikles for å ta høyde for flere parametre. Tenkt å ha en array over parametre og slå de sammen med .join("&")
    fetch(url+"find="+find+"&size="+size+"&side="+side).then(res => res.json()).then(info => {
      setData(info.data);
      setMeta(info.info);
    });
  }, [find, size, side]); // effekten oppdateres når find og size oppdateres. Side neste, må ha solid logikk for å sørge for at sidetallet ikke oversiger max sider

  // React.useEffect(() => {
  //   if (meta.currentPage < side) {
  //     setSide(meta.currentPage)
  //   }
  // }, [])

  // rendering \
  return (
    <div className="App">
      <header className="App-header">
        <h1>Utkikk</h1>
      </header>
      <main className="App-main">
        <div className='table-wrapper'>
          <div className='container'>
            <div className='left'>
            <input type="text" placeholder="Søkefelt" className='sokefelt' value={find} onChange={updFind}></input>          
            </div>
            <div className='right'>
            <div className='left'>Tabellstørrelse:
            <select value={size} onChange={updSize}>
                {tableLen.map(opt => (
                  <option key={opt.value} value={opt.value}>
                    {opt.text}
                  </option>
                ))}
              </select>
            </div></div>
          </div>
        <Table header={headers} info={data}/>
          <div className='container'>
            <div className="left">
              {meta.totalResults ? <p>Antall rader: {meta.totalResults}</p> : null}
            </div>
            <div className="right">
                  <Pagenav side={side} size={meta.totalPages} setSide={setSide} />
                {/* {side > 3 && <div className='pgButton' value="1" key={1}>{1}</div>}
                {side > 4 && <div className='pgButton'>...</div>}
                {side > 2 && <div className='pgButton' key={side-2}>{side-2}</div>}
                {side > 1 && <div className='pgButton' key={side-1}>{side-1}</div>}
                {<div className='pgButton' key={side}>{side}</div>}
                {side+1 < meta.totalPages && <div className='pgButton' key={side+1}>{side+1}</div>}
                {side+2 < meta.totalPages && <div className='pgButton' key={side+2}>{side+2}</div>}
                {side+3 < meta.totalPages && <div className='pgButton'>...</div>}
                {meta.totalPages > side && <div className='pgButton' key={meta.totalPages}>{meta.totalPages}</div>} */}
              </div>
            </div>
        </div>
      </main>
    </div>
  );
}