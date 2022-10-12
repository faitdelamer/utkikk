import React from 'react';

export default function Table({header, info}) {
    // lager en tabell ut fra prop 1 (header 1d object) og prop 2 (info 2d object)
    return (
        <table className='fl-table'>
            <thead>
                <tr>
                {header.map(todo=><th>{todo}</th>)}
                </tr>
            </thead>
            <tbody>
                {Object.keys(info).map(row =>
                <tr>
                    {Object.keys(info[row]).map(data => <td>{info[row][data]}</td>)}
                </tr>)}
            </tbody>
        </table>
    )
}