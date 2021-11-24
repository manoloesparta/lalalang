import './Editor.css'

const placeholder = `let fact = fun(num) {
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

function Editor() {

  const handleTab = (e) =>  {
    const source = document.getElementById('source')
    if(e.key == 'Tab') {
      const value = source.value
      const [start, end] = [source.selectionStart, source.selectionEnd]
      source.value = value.slice(0, start) + '\t' + value.slice(end)
      source.selectionStart = source.selectionEnd = start + 1
      e.preventDefault();
    }
  }

  return (
    <div className="column is-half">
      <div className="field">
        <div className="control">
            <textarea 
              id="source" 
              className="textarea is-medium is-info" 
              placeholder={placeholder}
              onKeyDown={handleTab}/>
        </div>
      </div>
    </div>
  )
}

export default Editor;