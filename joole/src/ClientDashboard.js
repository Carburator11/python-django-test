import React from 'react';
import { LineChart, Line, CartesianGrid, XAxis } from 'recharts';

const testData = JSON.parse('{"Janvier":293,"Fevrier":223,"Mars":309,"Avril":261,"Mai":218,"Juin":197,"Juillet":254,"Aout":246,"Septembre":274,"Octobre":261,"Novembre":269,"Decembre":335}')
console.log("testData ", testData)

const ClientDashboard = ({data}) => {
    
    const inputData = data ? data : testData
    const input = []
    
    for (var key in inputData) {
        if (inputData.hasOwnProperty(key)) {
            input.push({
                month: key,
                uv: inputData[key]
            })
        }
    }
    return <div style={{textAlign: 'center'}}>
            <LineChart data={input} width={1300} height={300} >
             <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
             <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
              <XAxis dataKey="month" />
            </LineChart>
        </div>
}

export default ClientDashboard