async function tellToSolve() {
  let toSolve = "";
  for (var i = 0; i < 81; i++) {
    let val = document.getElementById("in_" + i).value;
    if (val != "") {
      toSolve += val;
    } else {
      toSolve += ".";
    }
  }
  let topText = document.getElementById("topText");
  let solved = await eel.solveIt(toSolve)();
  if (solved != "") {
    topText.innerHTML = "Easy peasy (˘⌣˘)";
    topText.classList.remove("error");
    topText.classList.add("success");
    for (let j = 0; j < 81; j++) {
      document.getElementById("in_" + j).value = solved[j];
    }
  } else {
    topText.innerHTML = "Cannot be solved. ⚆ _ ⚆";
    topText.classList.remove("success");
    topText.classList.add("error");
  }
}

function draw() {
  let toAdd = `
<colgroup id='col1'>
	<col />
	<col />
	<col />
</colgroup>
<colgroup id='col2'>
	<col />
	<col />
	<col />
</colgroup>
<colgroup id='col3'>
	<col />
	<col />
	<col />
</colgroup>`;
  for (let i = 0; i < 81; i++) {
    if (i == 0) toAdd += "<tbody id='tBodyTop'>";
    if (i == 27) toAdd += "</tbody><tbody id='tBodyMid'>";
    if (i == 54) toAdd += "</tbody><tbody id='tBodyBot'>";
    if (i == 0) {
      toAdd += "<tr>";
    } else if (i % 9 == 0 && i != 80) {
      toAdd += "</tr><tr>";
    }
    toAdd +=
      "<td><input type='text' oninput='changed(this)' onclick='changed(this)' onfocus='changed(this)' class='inputs' maxlength='2' oninput=\"this.value=this.value.replace(/[^1-9]/g,'')\" id='in_" +
      i +
      "'/></td>";

    if (i == 80) toAdd += "</tr>";

    if (i == 80) toAdd += "</tbody>";
  }
  document.getElementById("theTable").innerHTML = toAdd;
}
function clearThem() {
  for (let i = 0; i < 81; i++) {
    let id = "in_" + i;
    document.getElementById(id).value = "";
  }
}
function changed(element) {
  if (element.value[1]) {
    element.value = element.value[1];
  } else if (element.value[0]) {
    //pass
  } else {
    element.value = "";
  }
}
draw();
