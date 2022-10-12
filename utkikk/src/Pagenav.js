import React from 'react';

export default function Pagenav({size, side, setSide}) {
    // får to ting her, nåværende side og maks sideantall
    // skal vise første og siste side
    // Skal vise dynamisk ± 2 sider fra gjeldende side

    // Dette kan nok løses med litt logikk men det får vente
    const pgpre = () => {setSide(side-1);};
    const pgone = () => {setSide(1);};
    const pgmtu = () => {setSide(side-2);};
    const pgmon = () => {setSide(side-1);};
    const pgpon = () => {setSide(side+1);};
    const pgptu = () => {setSide(side+2);};
    const pglst = () => {setSide(size);};
    const pgnxt = () => {setSide(side+1);};

    return (
        <div className='pgButtons'>
            {side > 1 && <div className='pgButton' onClick={pgpre}>←</div>}
            {side > 4 && <div className='pgButton' onClick={pgone}>{1}</div>}
            {side > 3 && <div className='pgButton'>...</div>}
            {side > 2 && <div className='pgButton' onClick={pgmtu}>{side-2}</div>}
            {side > 1 && <div className='pgButton' onClick={pgmon}>{side-1}</div>}
            <div className='pgButton' key={side}>{side}</div>
            {side < size && <div className='pgButton' onClick={pgpon}>{side+1}</div>}
            {side+1 < size && <div className='pgButton' onClick={pgptu}>{side+2}</div>}
            {side+2 < size && <div className='pgButton'>...</div>}
            {side+3 < size && <div className='pgButton' onClick={pglst}>{size}</div>}
            {side < size && <div className='pgButton' onClick={pgnxt}>→</div>}
        </div>
    )
} // ikke verdens peneste men det funker...