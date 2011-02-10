Ext.ns('Ext.ux.stores');

Ext.ux.stores.ProjectStore = new Ext.data.DirectStore({
    root: 'data',
    storeId: 'projects',
    totalProperty: 'count',
    fields: [
        'id',
        'name',
        'description'
    ],
    api: {
        read: ProjectApi.read
    }          
});

Ext.ns('Ext.ux.tpl');

Ext.ux.tpl.ProjectTpl = new Ext.XTemplate(
    '<tpl for=".">',
        '<div class="project-wrap" pr_id="{id}">',
            '<h3>{name}</h3>',
            '<p>{description}</p>',
        '</div>',
    '</tpl>'
);

Ext.ux.ProjectsView = Ext.extend(Ext.DataView, {
    singleSelect: true,
    store: 'projects',
    tpl: Ext.ux.tpl.ProjectTpl,
    emptyText: 'No projects',
    loadingText: 'Loading...',
    itemSelector: 'h3',
    initComponent: function(){
        Ext.ux.ProjectsView.superclass.initComponent.call(this);
        this.on('selectionchange', this.onSelect, this);
    },
    afterRender: function(){
        Ext.ux.ProjectsView.superclass.afterRender.apply(this, arguments);
        this.reload();
    },
    reload: function(){
        this.store.load();
    },
    onSelect: function(view, selected){
        if (selected.length){
            var r = this.getRecord(selected[0])
            alert(r.get('name'))
        }
    }
});

Ext.ux.ProjectsPanel = Ext.extend(Ext.Panel, {
    autoScroll: true,
    title: 'Projects',
    initComponent: function(){
        this.projects_view = new Ext.ux.ProjectsView();
        var config = {
            items: this.projects_view ,
            bbar: new Ext.PagingToolbar({
                store: 'projects',
                displayInfo: true,
                pageSize: PROJECTS_ON_PAGE
            })            
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.ProjectsPanel.superclass.initComponent.apply(this, arguments);             
    }
});

Ext.reg('ext:ux:projects-panel', Ext.ux.ProjectsPanel);