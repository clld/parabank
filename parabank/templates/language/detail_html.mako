<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<style>
td {
    border: 1px solid lightblue;
    padding-right: 5px;
    padding-left: 5px;
    background: white;
}

th {
    height:26px;
    font-weight: bold;
    background: #F2F2F2;
}

div.parabox {
    padding: 10px;
    background: #F2F2F2;
    border: 1px solid lightblue;
}
span {
    cursor: pointer;
}

.control-group {
	display: inline-block;
    width: 100%;
	margin: 10px;
	padding: 0px;
	text-align: left;
	vertical-align: top;
}

.control {
	font-size: 16px;
	position: relative;
	display: block;
	margin-bottom: 15px;
	padding-left: 30px;
	cursor: pointer;
}

.control input {
	position: absolute;
	z-index: -1;
	opacity: 0;
}
.control__indicator {
	position: absolute;
	top: 2px;
	left: 0;
	width: 15px;
	height: 15px;
	background: #e6e6e6;
    border: 1px solid darkgray;
}

/* Check mark */
.control__indicator:after {
	position: absolute;
	display: none;
	content: '';
}

/* Show check mark */
.control input:checked ~ .control__indicator:after {
	display: block;
}

/* Checkbox tick */
.control--checkbox .control__indicator:after {
	top: 2px;
	left: 5px;
	width: 3px;
	height: 8px;
	transform: rotate(45deg);
	border: solid #fff;
	border-width: 0 2px 2px 0;
}

/* Disabled tick colour */
.control--checkbox input:disabled ~ .control__indicator:after {
	border-color: #7b7b7b;
}

.control--radio .control__indicator {
	border-radius: 50%;
}
/* Hover and focus states */
.control:hover input ~ .control__indicator,
.control input:focus ~ .control__indicator {
	background: #ccc;
}

/* Checked state */
.control input:checked ~ .control__indicator {
	background: #2aa1c0;
}

/* Hover state whilst checked */
.control:hover input:not([disabled]):checked ~ .control__indicator,
.control input:checked:focus ~ .control__indicator {
	background: #0e647d;
}

/* Check mark */
.control__indicator:after {
	position: absolute;
	display: none;
	content: '';
}

/* Show check mark */
.control input:checked ~ .control__indicator:after {
	display: block;
}

/* Radio button inner circle */
.control--radio .control__indicator:after {
	top: 4px;
	left: 4px;
	width: 7px;
	height: 7px;
	border-radius: 50%;
	background: #fff;
}
.top6 {
    display:flex;
    background: #F2F2F2;
    border: 1px solid lightblue;
    padding: 5px;
    padding-top: 25px;
}
.in6 {

    margin-left: 15px;
    padding-bottom: 5px;

}


input[type=button] {
    width: 148px;
    vertical-align: center;
}

input[type=text] {
    width: 90%;
    vertical-align: middle;
}

</style>


<h2>${_('Language:')} ${ctx.name}</h2>

<h5>${ctx.description}</h5>
<br>
<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#primary" data-toggle="tab">Kinship</a></li>
        <!-- <li><a href="#secondary" data-toggle="tab">Addressing the Family</a></li> -->
        <li><a href="#pronouns" data-toggle="tab">Pronouns</a></li>
        <li><a href="#verbagreement" data-toggle="tab">Verb Agreement</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="primary" class="tab-pane active">
            Color for maximum contrast
            <div class="parabox">
                <h4>Siblings</h4>
                ${siblings}
                </div>
            <br>

            <div class="parabox">
                <h4>Cousins</h4>
                ${cousins}
                </div>
            <br>

            <div class="parabox">
                <h4>Parents, Aunts & Uncles</h4>
                ${parents}
                </div>
            <br>

            <div class="parabox">
                <h4>Grandparents & Grandchildren</h4>
                ${grand}
                </div>
            <br>

            <div class="parabox">
                <h4>Sons & Daughters, Nephews & Nieces</h4>
                ${sons}
                </div>
            <br>

            <div class="parabox">
                <h4>In-Laws</h4>
                ${inlaws}
                </div>
            <br>
        </div>
        <div id="secondary" class="tab-pane">
            <div class="parabox">
                <h4>Family members (on the left) addressing other family members</h4>
                ${levenshtein_siblings}
                </div>
        </div>
        <div id="pronouns" class="tab-pane">
            <div class="parabox">
                <h4>Pronouns</h4>
                ${pronouns}
                </div>
        </div>
        <div id="verbagreement" class="tab-pane">
            <div class="parabox">
                <h4>Verb Agreement</h4>
                ${verb_agreement}
                </div>
            <br>

            <div class="parabox">
                <h4>Verb Agreement</h4>
                ${verb_agreement2}
                </div>
        </div>
    </div>
</div>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.language_meta()}
    <div class="in6">
        <h4>Editor</h4>
        <input type="button" value="Reset" onClick="reloadPage()">
        <input type="button" value="Max. contrast" onClick="rainbow()"><br>

        <hr>
        <input type="button" value="Cut first letter" onClick="removeFirstLetter()">
        <input type="button" value="Cut last letter" onClick="removeLastLetter()"><br>
        <input type="button" value="Cut first word" onClick="removeFirstWord()">
        <input type="button" value="Cut last word" onClick="removeLastWord()"><br>

        <input type="button" value="abc only" onClick="onlyABC()">
        <input type="button" value="(blank)" onClick=""><br>
        <hr>
        <input type="text" id="substring" placeholder="ab-, -bc-, -de"><br>
        <input type="button" value="Remove Substring" onClick="removeSubstring()"><br>
        <hr>

    </div>


    <div class="in6">
        <div class="control-group">

            <h4>Highlight Similarity</h4>
            <p>Highlight the similarity of terms by clicking on them.</p>
            <label class="control control--radio">Levenshtein Distance
                <input type="radio" name="comMeth" value="Leventhe" checked="checked">
                <div class="control__indicator"></div>
            </label>
            <label class="control control--radio">Overlap of Word Beginning
                <input type="radio" name="comMeth" value="Beginning">
                <div class="control__indicator"></div>
            </label>
            <label class="control control--radio">Overlap of Word Ending
                <input type="radio" name="comMeth" value="Ending">
                <div class="control__indicator"></div>
            </label>
            <label class="control control--radio">Length of Shared Substring
                <input type="radio" name="comMeth" value="Substring">
                <div class="control__indicator"></div>
            </label>
        </div>
    </div>
<hr>
    <div class="in6">

        <div class="control-group">

            <h4>Ignore certain Letters</h4>
            <p>Ignore vowels or selected how many letters at the BEGINNING <br> of
                a term will be ignored when a term in the table is clicked.</p>

            <label class="control control--checkbox" >Ignore Vowels in Terms
                <input type="checkbox" name="vowels" value="yes">
                <div class="control__indicator"></div>
            </label>
            <hr>

            <label class="control control--radio">First Letter
                <input type="radio" name="beginning" value="1">
                <div class="control__indicator"></div>
            </label>
            <label class="control control--radio">First 2 Letter
                <input type="radio" name="beginning" value="2">
                <div class="control__indicator"></div>
            </label>
            <label class="control control--radio">First 3 Letter
                <input type="radio" name="beginning" value="3">
                <div class="control__indicator"></div>
            </label>
            <label class="control control--radio">No Letter is Ignored
                <input type="radio" name="beginning" value="0" checked="checked">
                <div class="control__indicator"></div>
            </label>
        </div>
    </div>

    <div class="in6">
        <div class="control-group">

            <p>Selected how many letters at the END of a term will <br>
                be ignored when a term in the table is clicked.</p>
        <label class="control control--radio">Last Letter
            <input type="radio" name="ending" value="1">
            <div class="control__indicator"></div>
        </label>
        <label class="control control--radio">Last 2 Letters
            <input type="radio" name="ending" value="2">
            <div class="control__indicator"></div>
        </label>
        <label class="control control--radio">Last 3 Letters
            <input type="radio" name="ending" value="3">
            <div class="control__indicator"></div>
        </label>
            <label class="control control--radio">No Letter is ignored
            <input type="radio" name="ending" value="0" checked="checked">
            <div class="control__indicator"></div>
        </label>
        </div>

    </div>


</%def>

<script>
// all the lables which should not be colored in:
var lableCells = ['eB', 'yB', 'eZ', 'yZ', 'father (F)', 'mother (M)', 'ego (male)', 'ego (female)', 'male', 'female',
                  'male speaker (parent is younger sibling)', 'male speaker (parent is older sibling)',
                  'female speaker (parent is younger sibling)', 'female speaker (parent is older sibling)',
                  'male speaker (younger than cousin)', 'female speaker (younger than cousin)',
                  'male speaker (older than cousin)', 'female speaker (older than cousin)',
                  '1st (excl) Person Singular', '1st (excl) Person Dual','1st (excl) Person Plural',
                  '1st (incl) Person Dual', '1st (incl) Person Plural', '2nd Person Singular',
                  '2nd Person Dual', '2nd Person Plural','3rd Person Singular Gender 1',
                  '3rd Person Singular Gender 2', '3rd Person Dual','3rd Person Plural',];

function reloadPage() {
    location.reload();
}

function getCssValuePrefix() {
    // different prefix for different browsers
    var rtrnVal = '';    //default to standard syntax
    var prefixes = ['-o-', '-ms-', '-moz-', '-webkit-'];
    var dom = document.createElement('div'); // Create a temporary DOM object for testing

    for (var i = 0; i < prefixes.length; i++) {
        // Attempt to set the style
        dom.style.background = prefixes[i] + 'linear-gradient(#000000, #ffffff)';

        // Detect if the style was successfully set
        if (dom.style.background) {
            rtrnVal = prefixes[i];
        }
    }
    dom = null;
    delete dom;
    return rtrnVal;
}

function hashCode(str) { // java String#hashCode
    // turn string into number
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
}

function intToRGB(i){
    // turns number into hexColor
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}

function increaseBrightness(hex, percent){
    // strip the leading # if it's there
    hex = hex.replace(/^\s*#|\s*$/g, '');

    var r = parseInt(hex.substr(0, 2), 16),
        g = parseInt(hex.substr(2, 2), 16),
        b = parseInt(hex.substr(4, 2), 16);

    return '#' +
       ((0|(1<<8) + r + (256 - r) * percent / 100).toString(16)).substr(1) +
       ((0|(1<<8) + g + (256 - g) * percent / 100).toString(16)).substr(1) +
       ((0|(1<<8) + b + (256 - b) * percent / 100).toString(16)).substr(1);
}

function colorTheCells(cellColorList, cell) {
    // divides the cell background and colors in the sections

    if (cellColorList.length > 0) {
        cell.style.backgroundColor = cellColorList[0]
    }

    if (cellColorList.length > 1) {
        cell.style.backgroundImage = getCssValuePrefix() +
                                     'linear-gradient(top left,' +
                                     cellColorList[0] + ' 50%, ' +
                                     cellColorList[1] +' 51%)';
    }

    if (cellColorList.length > 2) {
        cell.style.backgroundImage = getCssValuePrefix() +
                                     'linear-gradient(top left,' +
                                     cellColorList[0] + ' 32%, ' +
                                     cellColorList[1] + ' 33%, ' +
                                     cellColorList[1] + ' 65%, ' +
                                     cellColorList[2] +' 66%)';
    }

    if (cellColorList.length > 3) {
        cell.style.backgroundImage = getCssValuePrefix() +
                                     'linear-gradient(top left,' +
                                     cellColorList[0] + ' 24%, ' +
                                     cellColorList[1] + ' 25%, ' +
                                     cellColorList[1] + ' 50%, ' +
                                     cellColorList[2] +' 51%,' +
                                     cellColorList[2] +' 75%,' +
                                     cellColorList[3] +' 76%)';
    }
}

function levenstheinDistance(a, b) {
    // Compute the edit distance between the two given strings using Levenshtein

    var c; // Length of the longer of the two strings
    var matrix = [];
    var i; // Increment along the first column of each row
    var j; // Increment each column in the first row

    if(a.length >= b.length) {c = a.length}
    if (b.length > a.length) {c = b.length}

    for(i = 0; i <= b.length; i++){matrix[i] = [i]}
    for(j = 0; j <= a.length; j++){matrix[0][j] = j}

    // Fill in the rest of the matrix
    for(i = 1; i <= b.length; i++) {
        for(j = 1; j <= a.length; j++) {

            if(b.charAt(i - 1) == a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];

            } else {
                matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, // substitution
                               Math.min(matrix[i][j - 1] + 1,     // insertion
                               matrix[i - 1][j] + 1));            // deletion
            }
        }
    }

	/* Returns overlap of the two compared terms */
	var result = 1 - (matrix[b.length][a.length]) / c;

	// Round up to two digits after. 99 so that there is no 100 value (100 - 0) which results in black background
    return 99 - (100 * Math.round(result * 100) / 100);
}

function longestCommonSubstring(string1, string2){
	// init max value
	var longestCommonSubstring = 0;
	// init 2D array with 0
	var table = [],
            len1 = string1.length,
            len2 = string2.length,
            row, col;
	for(row = 0; row <= len1; row++){
		table[row] = [];
		for(col = 0; col <= len2; col++){
			table[row][col] = 0;
		}
	}
	// fill table
        var i, j;
	for(i = 0; i < len1; i++){
		for(j = 0; j < len2; j++){
			if(string1[i] === string2[j]){
				if(table[i][j] === 0){
					table[i+1][j+1] = 1;
				} else {
					table[i+1][j+1] = table[i][j] + 1;
				}

				if(table[i+1][j+1] > longestCommonSubstring){
					longestCommonSubstring = table[i+1][j+1];
				}

			} else {
				table[i+1][j+1] = 0;
			}
		}
	}
    longestCommonSubstring = 15 * longestCommonSubstring;
    if (longestCommonSubstring > 99) {longestCommonSubstring = 99}
    if (longestCommonSubstring < 1) {longestCommonSubstring = 1}
	return increaseBrightness('#FF1418', 100 - longestCommonSubstring);
}

function getTableCells() {
    // get all parabox divs and table cells in them
    var cells = [];
    var divs = document.getElementsByClassName("parabox");
    for (var j = 0; j < divs.length; j++)
    {
        var cellsInP = divs[j].getElementsByTagName('td');
        for (var p = 0; p < cellsInP.length; p++) {
            cells.push(cellsInP[p])
        }
    }
    return cells;
}

function getAllSpans() {
    var cells = getTableCells();
    var allSpans = [];
    for (var h = 0, len3 = cells.length; h < len3; h++)
    {
        var spans = cells[h].getElementsByTagName("span");
        for (var k = 0, len1 = spans.length; k < len1; k++) {
            allSpans.push(spans[k]);
        }
    }
    return allSpans;
}

function getRadioButton(theButtonGroup) {
    // goes throught radio button group and returns the selected one
    var groupList = document.getElementsByName(theButtonGroup);

    for (var i = 0, length = groupList.length; i < length; i++) {

        if (groupList[i].checked) {state = groupList[i].value}
    }
    return state;
}

function getCheckboxes(checkboxName){
    // get states of checkboxes
    var checkedValue = null;
    var inputElements = document.getElementsByName(checkboxName);
    for(var i=0; inputElements[i]; ++i){
        if(inputElements[i].checked){
            checkedValue = inputElements[i].value;
            break;
        }
    }
    return checkedValue;
}

function removeVowels(value) {
    // removes all occurences of the vowels from a string
    value = value.replaceAll("a", "")
                 .replaceAll("e", "")
                 .replaceAll("i", "")
                 .replaceAll("o", "")
                 .replaceAll("u", "")
                 .replaceAll("y", "");
    return value;
}

String.prototype.replaceAll = function(search, replace) {
    // if replace is not sent, return original string otherwise it will
    // replace search string with 'undefined'.
    if (replace === undefined) {
        return this.toString();
    }

    return this.replace(new RegExp('[' + search + ']', 'g'), replace);
};

function findColorList(clickedValue, currentCell) {
    // get radio selection, clicked clickedValue and current cell to calculate the background color

    var beginningValue = getRadioButton('beginning');      // radio buttons for cutting beginning letters
    var endingValue = - getRadioButton('ending');            // radio buttons for cutting ending letters ( "-" as value from back)
    var ignoreVowels = getCheckboxes("vowels");             // checkbox to remove all vowels from calculation
    var cellColorList = [];                                // populated with a hexColor value for each term in cell
    var spans = currentCell.getElementsByTagName('span');  // list of individual spans

    for (var l = 0, len1 = spans.length; l < len1; l++) {

        var colorToPush;

        if (endingValue == 0) {endCut = 99} // work around for string can't be cut to -0th index
        else {endCut = endingValue}

        var oldValue = spans[l].innerText.replace(" ", "") // removes the leading space
                                         .slice(beginningValue)
                                         .slice(0, endCut);

        var shortClickValue = clickedValue.slice(beginningValue)
                                     .slice(0, endCut);

        if (ignoreVowels == 'yes') {
            oldValue = removeVowels(oldValue);
            shortClickValue = removeVowels(shortClickValue)
            }

        if (oldValue) {
            cellColorList.push(compareMethod(shortClickValue, oldValue));

        } else {cellColorList.push('#808080')}  // no value in span
    }
    colorTheCells(cellColorList, currentCell);
}

function compareMethod(shortClickValue, oldValue) {

    var comMethValue = getRadioButton('comMeth');          // radio buttons for comparison method
    var colorToPush;

    if (comMethValue == 'Leventhe') {
        colorToPush = increaseBrightness('#FF1418', levenstheinDistance(shortClickValue, oldValue));

    } else if (comMethValue == 'Beginning') {
        colorToPush = compareBeginning(shortClickValue, oldValue);

    } else if (comMethValue == 'Ending') {
        colorToPush = compareEnding(shortClickValue, oldValue);

    } else {
        colorToPush = longestCommonSubstring(shortClickValue, oldValue);
    }
    return colorToPush;
};

function compareBeginning(shortClickValue, oldValue) {
    // calculates how much the beginning 1, 2, 3 letters overlap

    if (shortClickValue.slice(0, 3) == oldValue.slice(0, 3)) {
    colorToPush = increaseBrightness('#FF1418', 1);
    } else {

        if (shortClickValue.slice(0, 2) == oldValue.slice(0, 2)) {
            colorToPush = increaseBrightness('#FF1418', 33);
        } else {

            if (shortClickValue.slice(0, 1) == oldValue.slice(0, 1)) {
            colorToPush = increaseBrightness('#FF1418', 66);

            } else {
                colorToPush = increaseBrightness('#FF1418', 99);
            }
        }
    }
    return colorToPush;
}

function compareEnding(shortClickValue, oldValue) {
    // calculates how much the ending -3, -2, -1 letters overlap

    if (shortClickValue.slice(-3) == oldValue.slice(-3)) {
        colorToPush = increaseBrightness('#FF1418', 1);
    } else {

        if (shortClickValue.slice(-2) == oldValue.slice(-2)) {
            colorToPush = increaseBrightness('#FF1418', 33);
        } else {

            if (shortClickValue.slice(-1) == oldValue.slice(-1)) {
                colorToPush = increaseBrightness('#FF1418', 66);
            } else {

                colorToPush = increaseBrightness('#FF1418', 99);
            }
        }
    }
    return colorToPush;
}

function levenshteinSelect(clickedValueRaw) {
    // calculates the overlap between the clicked term and all the others
    // fills the cells in the color. The darkness of the cell indicates the overlab percentage

    if (lableCells.indexOf(clickedValueRaw) > -1) { // cell is a lable cell
    } else {

        var clickedValue = clickedValueRaw.replace(" ", "");   // innerText of table cell
        var cells = getTableCells();                           // all table cells in document

        for (var k = 0, len = cells.length; k < len; k++) {

            var text = (cells[k].innerText);

            if (lableCells.indexOf(text) > -1){ // cell is a lable cell
            } else {
                currentCell = cells[k];
                // color in the table cells depending on the values
                findColorList(clickedValue, currentCell);
            }
        }
    }
}

function removeSubstring() {

    var subRemove = document.getElementById('substring').value;
    var subClean = subRemove.replaceAll("-", "");
    var subLength = subClean.length;
    var spans = getAllSpans();

    for (var l = 0, len1 = spans.length; l < len1; l++) {

        var raw = spans[l].innerText;
        var cleanShort = raw.trim().slice(1);

        if (subRemove.startsWith("-")) {
            if (subRemove.endsWith("-")) {

                if (cleanShort.indexOf(subClean) > -1) {
                    if (raw.indexOf(subClean) + subLength < raw.length) {
                        spans[l].innerText = raw.replace(subClean, "")
                    }
                }

            } else {
                if (raw.endsWith(subClean)) {
                    spans[l].innerText = raw.slice(0, - (subLength))
                }
            }

        } else if (subRemove.endsWith("-")) {
            if (raw.trim().startsWith(subClean)) {
                spans[l].innerText = raw.replace(subClean, "");
            }

        } else {
            spans[l].innerText = raw.replace(subClean, "");
            }
    }
}

function removeFirstLetter() {
    var spans = getAllSpans();
    for (var l = 0, len1 = spans.length; l < len1; l++) {

        if (spans[l].innerText[0] == " ") {
            spans[l].innerText = " " + spans[l].innerText.substr(2)
        } else {
            spans[l].innerText = spans[l].innerText.substr(1);
        }
    }
}

function removeFirstWord() {
    var spans = getAllSpans();
    for (var k = 0, len1 = spans.length; k < len1; k++) {

        var values = spans[k].innerText.trim().split(' ');
        if (values.length > 1) {
            var valueOut = [];
            for (var m = 1, len2 = values.length; m < len2; m++) {
                valueOut.push(values[m]);
            }
            spans[k].innerText = ' ' + valueOut.join(' ').trim();
        }
    }
}

function removeLastWord() {
    var spans = getAllSpans();
    for (var k = 0, len1 = spans.length; k < len1; k++) {

        var values = spans[k].innerText.trim().split(' ');
        if (values.length > 1) {
            var valueOut = [];
            for (var m = 0, len2 = values.length; m < len2 - 1; m++) {
                valueOut.push(values[m]);
            }
            spans[k].innerText = ' ' + valueOut.join(' ').trim();
        }
    }
}

function removeLastLetter() {
    var spans = getAllSpans();
    for (var l = 0, len1 = spans.length; l < len1; l++) {
        spans[l].innerText = spans[l].innerText.slice(0, -1);
    }
}

function onlyABC(){
    var spans = getAllSpans();
    for (var l = 0, len1 = spans.length; l < len1; l++) {
        var patt1 = /[a-z ]+/g;
        spans[l].innerText = spans[l].innerText.replace(/[1234567890.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
    }
}

function rainbow() {

    var cells = getTableCells();    // all table cells in document

    for (var g = 0, len = cells.length; g < len; g++) {
        var text = (cells[g].innerText);
        var cellColorList = [];
        if (lableCells.indexOf(text) > -1){         // cell is a lable cell

        } else {

            var spans = cells[g].getElementsByTagName('span');
            for (var l = 0, len1 = spans.length; l < len1; l++) {
                var backclr = intToRGB(hashCode(spans[l].innerText));
                var hexclr = increaseBrightness(backclr, 50);
                cellColorList.push(hexclr);
            }
        }

        colorTheCells(cellColorList, cells[g]);
    }
}



function spanCells() {

    var cells = getTableCells();

    for (var k = 0, len = cells.length; k < len; k++) {

        var text = (cells[k].innerText);


        if (lableCells.indexOf(text) > -1) {  // all label cells are grayed
            cells[k].style.backgroundColor = "#F2F2F2";
            cells[k].style.borderRight = "thin solid #696969";

        } else {

            var textByWord = text.split(/[,/]/g);


            cells[k].style.border = "thin solid #696969";

            for (var n = 0, len2 = textByWord.length; n < len2; n++) {

                textByWord[n] = "<span onclick='levenshteinSelect(this.innerText)'>" + textByWord[n] + "</span>";
            }
        cells[k].innerHTML = textByWord.join();
        }
    }
    rainbow()
}

spanCells()


</script>