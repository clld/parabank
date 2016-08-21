<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%inherit file="../home_comp.mako"/>
<%! active_menu_item = "patterns" %>

<h3>Pattern: ${ctx.name}</h3>

<h5>${ctx.description}</h5>

${req.map.render()}

<h5>${ctx.languages}</h5>
<h5>${ctx}</h5>
<h5>${req}</h5>
<h5>${context}</h5>
<h5>${request}</h5>


${request.get_datatable('languages', h.models.Language, pattern=ctx).render()}