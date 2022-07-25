function chooseRandomWithoutReplacement(items, num_elements) {
  // faster way to remove an array item when you don't care about array order
  function removeArrayItem(i) {
    var val = items.pop();
    if (i < items.length) {
      items[i] = val;
    }
  }

  function makeRandom() {
    var rand = items[Math.floor(Math.random() * items.length)];
    removeArrayItem(rand);
    return rand;
  }

  var choices = [];

  for (var i = 0; i < num_elements; i++) {
    choices.push(makeRandom()); 
  }

  return choices;

}

