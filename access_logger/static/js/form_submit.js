let fabricCanvas = new fabric.Canvas('signature', { isDrawingMode: true });

let submitBtn = document.getElementById('submit-btn');

submitBtn.addEventListener("click", () => {
  let content = {};
  [...document.querySelectorAll('input')].forEach(e => {content[e.name] = e.value});
  content['signature'] = document.getElementById('signature').toDataURL();
  console.log(content);

  const xhr = new XMLHttpRequest();

  if (location.pathname.endsWith('entry.html')) {
    xhr.open("POST", '/log_entry', true);
  }
  else {
    if (location.pathname.endsWith('exit.html')) {
      xhr.open("POST", '/log_exit', true);
    }
    else {
      window.alert('Error, this page is neither entry.html nor exit.html!');
      return;
    }
  }

  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onreadystatechange = function() { // Call a function when the state changes.
      if(xhr.readyState === XMLHttpRequest.DONE) {
        const status = xhr.status;
        if (status === 0 || (status >= 200 && status < 400)) {
          window.location = '/static/index.html';
        } else {
          window.alert('Error, cannot send the form!');
        }
      }
  };
  xhr.send(JSON.stringify(content));

}, false);

document.getElementById('clear-btn').addEventListener("click", () => {
  window.location.reload();
}, false);
