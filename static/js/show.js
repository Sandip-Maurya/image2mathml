
// console.log('Show.js is called')
var mathml_code_elm = document.getElementById('mathml-code');
var mathml_preview_elm = document.getElementById('mathml-preview');
var text = mathml_preview_elm.innerText;
mathml_preview_elm.innerHTML = text
// console.log(mathml_preview_elm.innerText)

document.getElementById('copy-btn').addEventListener('click', e => {
  mathml_code_elm.select();
  if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text);
    history.back()

  }
  else{
    // alert('Some error occured during click to copy process.')
    document.execCommand("copy");
    history.back()
  }
    
    // history.back()
    // setTimeout(() => {
    //   history.back()
    // }, 2000)

  })