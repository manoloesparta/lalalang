import './styles.css'

const API = 'https://compile.manoloesparta.com'

const SAMPLE_CODE = `let fact = fun(num) {
  let factIter = fun(actual, acc) {
    if(actual == 1) {
      return acc;
    }
    return factIter(actual - 1, actual * acc);
  }
  return factIter(num, 1);
}

let result = fact(4);
println(result);`

const sourceCode = document.getElementById('source')
sourceCode.setAttribute('placeholder', SAMPLE_CODE)
sourceCode.addEventListener('keydown', (e) => {
  if(e.key == 'Tab') {
    const value = sourceCode.value
    const [start, end] = [sourceCode.selectionStart, sourceCode.selectionEnd]
    sourceCode.value = value.slice(0, start) + '\t' + value.slice(end)
    sourceCode.selectionStart = sourceCode.selectionEnd = start + 1
    e.preventDefault();
  }
})

const result = document.getElementById('result')
const time = document.getElementById('time')
const compileButton = document.getElementById('compile')

compileButton.addEventListener('click', async () => {
  try {
    const config = { 
      'method': 'POST',
      'body': JSON.stringify({'source': sourceCode.value})
    }
    const response = await fetch(API, config)
    const json = await response.json()
    console.log(json)
    result.innerHTML = json.output
  } catch {
    result.innerHTML = 'Invalid input (or error found)'
  }
  const today = new Date()
  time.innerHTML = today.toISOString()
})