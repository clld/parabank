<%inherit file="app.mako"/>

##
## define app-level blocks:
## #263681
<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}"
       style="padding-top: 7px; padding-bottom: 2px;">
        <img width="34" src="${request.static_url('parabank:static/logo.png')}"/>
    </a>
</%block>

${next.body()}
