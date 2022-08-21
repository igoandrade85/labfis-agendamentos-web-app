function filtraSemestre() {
  // Variables
  let dropdown, table, rows, cells, country, filter;
  dropdown = document.getElementById("filtra-semestre");
  table = document.getElementById("tabela");
  rows = table.getElementsByTagName("tr");
  filter = dropdown.value;

  // Loops through rows and hides those with countries that don't match the filter
  for (let row of rows) { // `for...of` loops through the NodeList
    cells = row.getElementsByTagName("td");
    semester = cells[0] || null; // gets the 2nd `td` or nothing
    // if the filter is set to 'All', or this is the header row, or 2nd `td` text matches filter
    if (filter === "Todos" || !semester || (filter === semester.textContent)) {
      row.style.display = ""; // shows this row
    }
    else {
      row.style.display = "none"; // hides this row
    }
  }
}

function pesquisaTema(row) {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("pesquisa-tema");
  filter = input.value.toUpperCase();
  table = document.getElementById("tabela");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[row];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function filtraArea() {
  // Variables
  let dropdown, table, rows, cells, semester, filter;
  dropdown = document.getElementById("filtra-area");
  table = document.getElementById("tabela");
  rows = table.getElementsByTagName("tr");
  filter = dropdown.value;

  // Loops through rows and hides those with countries that don't match the filter
  for (let row of rows) { // `for...of` loops through the NodeList
    cells = row.getElementsByTagName("td");
    semester = cells[0] || null; // gets the 2nd `td` or nothing
    // if the filter is set to 'All', or this is the header row, or 2nd `td` text matches filter
    if (filter === "Todas" || !semester || (filter === semester.textContent)) {
      row.style.display = ""; // shows this row
    }
    else {
      row.style.display = "none"; // hides this row
    }
  }
}

function setMinMAxDate(selectSemestreID, inputDataArray) {
  let inputData, year, semester;
  let selectSemestre = document.getElementById(selectSemestreID);
  [year, semester] = selectSemestre.value.split('.');
  for (i = 0; i < inputDataArray.length; i++) {
    inputData = document.getElementById(inputDataArray[i]);
    if (semester == '1') {
      if (i == 0) {
        inputData.value = `${year}-01-01`;
      } else {
        inputData.value = `${year}-07-31`;
      }
      inputData.setAttribute('min', `${year}-01-01`);
      inputData.setAttribute('max', `${year}-07-31`);
    } else if (semester == '2') {
      if (i == 0) {
        inputData.value = `${year}-08-01`;
      } else {
        inputData.value = `${year}-12-31`;
      }
      inputData.setAttribute('min', `${year}-08-01`);
      inputData.setAttribute('max', `${year}-12-31`);
    }
  }
}

window.onload = filtraSemestre();
window.onload = setMinMAxDate("select_semestre_novo", ["input_data_novo"]);
window.onload = setMinMAxDate("select_semestre_novo", ["input_data_inicial", "input_data_final"]);