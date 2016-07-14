<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%inherit file="../home_comp.mako"/>
<%! active_menu_item = "patterns" %>
<h3>Pattern</h3>

${ctx.render()}
