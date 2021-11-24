import { useState } from 'react'
import './Result.css'

function Result() {

  const [result, setResult] = useState('No current result')
  const [today, setToday] = useState('Today')

  const API = 'https://1ak8gy9914.execute-api.us-east-1.amazonaws.com/Prod/'

  const handleCompile = async () => {
    const source = document.getElementById('source')
    try {
      const config = {method: 'POST', body: JSON.stringify({'source': source.value})}
      const response = await fetch(API, config)
      if(response.status == 200) {
        const json = await response.json()
        setResult(json.output)
      }
    } catch {
      setResult('Invalid input (or error found)')
    }
    setToday(new Date().toISOString())
  }

  return (
    <div className="column is-half">
      <div className="card">
        <div className="card-content">
          <p id="result" className="title">{result}</p>
          <p id="time" className="subtitle">{today}</p>
        </div>
      </div>
      <button 
        id="compile" 
        className="button is-warning"
        onClick={handleCompile}>Compile</button>
    </div>
  )
}

export default Result;