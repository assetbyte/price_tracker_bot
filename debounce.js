const fetchURL = (url) => {
    console.log(`fetching: ${url}`)
}

function debounce(callback, delay) {
  let timer; 

  return function (...args) {
    clearTimeout(timer);

    timer = setTimeout(() => {
      callback(...args);
    }, delay); 
  };
}

const fetching = debounce(fetchURL, 300)
fetching(1)
fetching(2) 
fetching(3)
fetching(4)
fetching(5)
