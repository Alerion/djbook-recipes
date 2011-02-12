Ext.ns('Ext.ux.stores');    //Объявляем namespace

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
        read: ProjectApi.read    //Метод Ext.Direct, который возвращает данные
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
    singleSelect: true,    //только один элемент может быть выбран
    store: 'projects',    //id нашего Store для загрузки данных, можно передать сам Store
    tpl: Ext.ux.tpl.ProjectTpl,    //шаблон для рендеринга элемента 
    emptyText: 'No projects',
    loadingText: 'Loading...',    
    itemSelector: 'h3',    //DOM-элемент который будет отвечать за выбор элемента
    autoScroll: true,    //обображаем скролл, если элементы не влязят в панель
    initComponent: function(){
        Ext.ux.ProjectsView.superclass.initComponent.call(this);
        this.on('selectionchange', this.onSelect, this);    //добавляем обработчик выбора элемента
    },
    afterRender: function(){
        //этод метод выполняеться после рендеринга компонента
        //можно использовать пости для всех компонентов ExtJs(Ext.Panel, Ext.Window и др.)
        Ext.ux.ProjectsView.superclass.afterRender.apply(this, arguments);
        this.reload();
    },
    reload: function(){
        //обновляем данные с сервера
        this.store.load();
    },
    onSelect: function(view, selected){
        //обработчик выбора элемента
        //проверяем выбран ли элемент т.к. метод вызываеться если выбор снят
        if (selected.length){
            //В selected[0] будет DOM-елемент, который указали в itemSelector
            //метод Ext.data.Store.getRecord возвращает запись соответствующую
            //записаь для этого элемента
            var r = this.getRecord(selected[0])
            //Показываем имя проекта, 
            //аналогично можно получить id, description или другое поле 
            alert(r.get('name'))
        }
    }
});

Ext.ux.ProjectsPanel = Ext.extend(Ext.Panel, {
    autoScroll: true,
    title: 'Projects',
    initComponent: function(){
        this.projects_view = new Ext.ux.ProjectsView();    //сохраним на будущее
        var config = {
            items: this.projects_view,
            bbar: new Ext.PagingToolbar({    //paginator
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