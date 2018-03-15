<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%! from clld_phylogeny_plugin.tree import Tree %>

<%block name="head">
    ${Tree.head(req)|n}
</%block>

<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<h2>${_('Parameter')} ${ctx.name}</h2>

% if ctx.description:
<p>${ctx.description}</p>
% endif

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

<div class="row-fluid">
    <div class="span4">
        ${tree.render() if tree else ''}
    </div>
    <div class="span8">
        ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
    </div>
</div>
