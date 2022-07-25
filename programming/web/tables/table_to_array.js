function tableToArray(tableId) {
  /*
   * Takes the id of an html table
   * and converts it into a two
   * dimensional javascript array
   */

  tableList = [];
  tableRows = document.getElementById(tableId).rows;

  for (var i = 0; i < tableRows.length; i++) {
    rowList = []
    row = tableRows[i].cells;
    for (var j = 0; j < row.length; j++) {
      rowList.push(row[j].innerText);
    }
    tableList.push(rowList)
  }

  return tableList
}

function removeNewlines(arr) {
  /* 
   * Takes a 2d array of strings
   * and converts "\n" to ""
   */
  for (var i = 0; i < arr.length; i++) {
    for (var j = 0; j < arr[i].length; j++) {
      if (arr[i][j] == "\n") {
        arr[i][j] = "";
      }
    }
  }
}
