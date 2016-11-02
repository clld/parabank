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
</style>


<h2>${_('Language:')} ${ctx.name}</h2>

<h5>${ctx.description}</h5>
<br>
<input type="button" value="Reset" onClick="rainbow()">
<br>
<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#primary" data-toggle="tab">Contrast Colors</a></li>
        <li><a href="#secondary" data-toggle="tab">Addressing the Family</a></li>
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
    </div>
</div>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.language_meta()}
</%def>

<script>
// all the lables which should not be colored in:
var lableCells = ['eB', 'yB', 'eZ', 'yZ', 'my father (F)', 'my mother (M)', 'me (male)', 'me (female)', 'male', 'female',
            'male speaker (parent is younger sibling)', 'male speaker (parent is older sibling)',
            'female speaker (parent is younger sibling)', 'female speaker (parent is older sibling)',
            'male speaker (younger than cousin)', 'female speaker (younger than cousin)',
            'male speaker (older than cousin)', 'female speaker (older than cousin)'];

function getCssValuePrefix()
// different prefix for different browsers
{
    var rtrnVal = '';    //default to standard syntax
    var prefixes = ['-o-', '-ms-', '-moz-', '-webkit-'];

    // Create a temporary DOM object for testing
    var dom = document.createElement('div');

    for (var i = 0; i < prefixes.length; i++)
    {
        // Attempt to set the style
        dom.style.background = prefixes[i] + 'linear-gradient(#000000, #ffffff)';

        // Detect if the style was successfully set
        if (dom.style.background)
        {
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
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}

function increase_brightness(hex, percent){
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
function colorTheCells(colorList, cell)
{
    if (colorList.length > 0)
    {
        cell.style.backgroundColor = colorList[0]
    }
    if (colorList.length > 1)
    {
        cell.style.backgroundImage = getCssValuePrefix() +
                                        'linear-gradient(top left,' +
                                        colorList[0] + ' 50%, ' +
                                        colorList[1] +' 51%)'
    }

    if (colorList.length > 2)
    {
        cell.style.backgroundImage = getCssValuePrefix() +
                                        'linear-gradient(top left,' +
                                        colorList[0] + ' 32%, ' +
                                        colorList[1] + ' 33%, ' +
                                        colorList[1] + ' 65%, ' +
                                        colorList[2] +' 66%)'
    }

    if (colorList.length > 3)
    {
        cell.style.backgroundImage = getCssValuePrefix() +
                                        'linear-gradient(top left,' +
                                        colorList[0] + ' 24%, ' +
                                        colorList[1] + ' 25%, ' +
                                        colorList[1] + ' 50%, ' +
                                        colorList[2] +' 51%,' +
                                        colorList[2] +' 75%,' +
                                        colorList[3] +' 76%)'
    }
}

function rainbow()
// colors all relevant td depending on the content
// takes the value from a table cell and calculates a hex color code from it
// the background of the cell is set in the color code
// the color can be made lighter in increase_brightness function

{
    var divs = document.getElementsByClassName("parabox");
    for (var j = 0; j < divs.length; j++)
    {

        var cells = divs[j].getElementsByTagName('td');
        for (var k = 0, len = cells.length; k < len; k++)
        {
            var text = (cells[k].innerText);

            if (lableCells.indexOf(text) > -1)
            {
                cells[k].style.backgroundColor = "#F2F2F2";
                cells[k].style.borderRight = "thin solid #696969";

            } else {
                cells[k].style.border = "thin solid #696969";
                var textByWord = text.split(/[,/]/g);
                var colorList = [];
                for (var n = 0, len2 = textByWord.length; n < len2; n++)
                {
                    var backcolo = intToRGB(hashCode(textByWord[n].replace(" ","")));
                    var hex_colo = increase_brightness(backcolo, 50);
                    colorList.push(hex_colo);
                }
                colorTheCells(colorList, cells[k]);
            }
        }

        // divide up all cell content in individually clickable spans
        for (var l = 0, len3 = cells.length; l < len3; l++)
        {
            var text = (cells[l].innerText);
            var textByWord = text.split(/[,/]/g);
            var newContent = ""
            for (m = 0; m < textByWord.length; ++m)
            {
                textByWord[m] = "<span onclick='levenshteinSelect(this.innerText)'>" + textByWord[m] + "</span>";
                //alert(textByWord[m]);
            }
            newContent = textByWord.join();
            cells[l].innerHTML = newContent;
        }
    }
}

function getEditDistance(a, b)
// Compute the edit distance between the two given strings using Levenshtein

{
    var c; // Length of the longer of the two strings
    var matrix = [];
    var i; // Increment along the first column of each row
    var j; // Increment each column in the first row

    if(a.length >= b.length) {c = a.length}
    if (b.length > a.length) {c = b.length}

    for(i = 0; i <= b.length; i++){matrix[i] = [i]}
    for(j = 0; j <= a.length; j++){matrix[0][j] = j}

    // Fill in the rest of the matrix
    for(i = 1; i <= b.length; i++)
    {
        for(j = 1; j <= a.length; j++)
        {
            if(b.charAt(i - 1) == a.charAt(j - 1))
            {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, // substitution
                                 Math.min(matrix[i][j - 1] + 1, // insertion
                                          matrix[i - 1][j] + 1)); // deletion
            }
        }
    }

	/* Returns overlap of the two compared terms */
	var result = 1 - (matrix[b.length][a.length]) / c;

	// Round up to two digits after. 99 so that there is no 100 value (100 - 0) which results in black background
    return 99 - (100 * Math.round(result * 100) / 100);
}

function levenshteinSelect(baseValue)
// calculates the overlap between the clicked term and all the others
// fills the cells in the color. The darkness of the cell indicates the overlab percentage

{
    var divs = document.getElementsByClassName("parabox");
    for (var j = 0; j < divs.length; j++)
    {
        var cells = divs[j].getElementsByTagName('td');

        for (var k = 0, len = cells.length; k < len; k++)
        {
            var text = (cells[k].innerText);
            if (lableCells.indexOf(text) > -1)
            {
            } else {
                var colorList = [];
                var spans = cells[k].getElementsByTagName('span');
                for (var l = 0, len1 = spans.length; l < len1; l++)
                {
                    var oldValue = spans[l].innerText;

                    if (oldValue)
                    {
                        var newValue = getEditDistance(baseValue.replace(" ", ""), oldValue.replace(" ", ""));
                        colorList.push(increase_brightness('#FF1418', newValue));
                    } else {
                        colorList.push('#808080');
                    }
                }
                colorTheCells(colorList, cells[k]);
            }
        }
    }
}
rainbow();
</script>