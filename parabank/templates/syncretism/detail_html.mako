<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "syncretisms" %>

<h3>Syncretism: ${ctx.name}</h3>

<h5>${ctx.description}</h5>

${req.map.render()}

<%util:table items="${ctx.languages}" args="item" options="${dict(bInfo=True)}">
    <%def name="head()">
        <th>Language</th>
        <th>Latitude</th>
        <th>Longitude</th>


    </%def>
    <td>${h.link(request, item)}</td>
    <td>${item.latitude}</td>
    <td>${item.longitude}</td>
</%util:table>
