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
</style>


<h2>${_('Language:')} ${ctx.name}</h2>

<h5>${ctx.comment}</h5>
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
// takes the value from a table cell and calculates a hex color code from it
// the background of the cell is set in the color code
// the color can be made lighter in increase_brightness function

// var primary = document.getElementById('primary');
// var cells = primary.getElementsByTagName('td');

var cells = document.getElementsByTagName('td');

function hashCode(str) { // java String#hashCode
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
var ls = ['eB', 'yB', 'eZ', 'yZ', 'my father (F)', 'my mother (M)', 'me (male)', 'me (female)', 'male', 'female',
          'male speaker (parent is younger sibling)', 'male speaker (parent is older sibling)',
          'female speaker (parent is younger sibling)', 'female speaker (parent is older sibling)',
          'male speaker (younger than cousin)', 'female speaker (younger than cousin)',
          'male speaker (older than cousin)', 'female speaker (older than cousin)'];

for (var i=0, len=cells.length; i<len; i++){
    var text = (cells[i].innerText);
    if (ls.indexOf(text) > -1) {
        cells[i].style.backgroundColor = "#F2F2F2";
        //cells[i].style.borderColor= "#F2F2F2";
    }

    else {
        var backcolor = intToRGB(hashCode(text));
        var hex_color = increase_brightness('#' + backcolor, 50);
        cells[i].style.backgroundColor = hex_color;
    }
}
</script>
