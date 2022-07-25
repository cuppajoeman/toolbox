function permutations(currPermutation, elementsToPermute) {
  var generatedPermutations = []

  function copyWithoutElement(list, element) {
    var newList = [];
    for (var i = 0; i < list.length; i++) {
      if (list[i] != element) {
        newList.append(list[i]);
      } 
    }
    return newList;
  }

  if (elementsToPermute != []) {
    for (var i = 0; i < elementsToPermute.length; i++) {
      var element = elementsToPermute[i];
      nextPermutation = currPermutation.concat(element);
      var remainingElements = copyWithoutElement(elementsToPermute, element);
      
      generatedPermutations = generatedPermutations.concat(permutations(nextPermutation, remainingElements));
    }
    return generatedPermutations;
  } else {
    return [currPermutation];
  }
}
