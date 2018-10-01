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

% if ctx.description:
    <div class="well well-small alert alert-info">${ctx.description}</div>
% endif
             <div class="parabox">
                ${pronouns}
                </div>


${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.language_meta()}
</%def>
