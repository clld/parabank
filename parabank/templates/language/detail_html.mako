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


<h2>${_('Language')} ${ctx.name}</h2>

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

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.language_meta()}
</%def>

 <script>
var allTableCells = document.getElementsByTagName("td");
for(var i = 0, max = allTableCells.length; i < max; i++) {
    var node = allTableCells[i];

    //get the text from the first child node
    var currentText = node.childNodes[0].nodeValue;

    //check for '-' and assign this table cells background color
    if (currentText === "-")
        node.style.backgroundColor = "red";
}
</script>
