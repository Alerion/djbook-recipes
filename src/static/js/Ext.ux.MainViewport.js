Ext.ux.MainViewport = Ext.extend(Ext.Viewport, {
    public_attr: 1,
    renderTo: Ext.getBody(),
    initComponent: function(){
        //initComponent это конструктор компонента. 
        //Сдесь может определить необходимыне нам параметры Ext.Viewport
        var config = {
            private_attr: 2,
            layout: 'border',
            defaults: {
                frame: true
            },
            //центральная панель
            items: [{
                region: 'center',
                html: '',
                //тулбар с кнопкой и обработчиком this.sayHello
                tbar: [{
                    text: 'Say Hello',
                    handler: this.sayHello,
                    scope: this
                }]
            },{
                //еще одна панель
                region: 'east',
                width: 350,
                xtype: 'ext:ux:projects-panel'
            },{
                region: 'north',
                contentEl: 'header',
                height: 40                
            }]
        }
        //В this.initialConfig находяться опции передаваемые при создании компонента.
        //Тоесть сдеась мы их просто затираем параметрами из config.
        //Таким образом можно опредеть публичные и приватные атриубуты.
        //Например public_attr по-умолчанию равен 1, но пользователь может его переопределить,
        //передав в констурктор Ext.ux.MainViewport. private_attr же всегда будет
        //установлен в 2.
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        //Вызываем родительский метод, наследование все таки :)
        Ext.ux.MainViewport.superclass.initComponent.apply(this, arguments);
    },//initComponent
    sayHello: function(){
        //после нажатия кнопки показываем окошко для ввода имени
        Ext.Msg.prompt('Name', 'Please enter your name:', function(btn, text){
            if (btn == 'ok') {
                //Вызываем метод hello класса на сервере.
                MainApi.hello(text, function(response){
                    //callback, показываем сообщение с сервера.
                    Ext.ux.msg('Success', response.msg, Ext.Msg.INFO);
                });
            }
        })
    }                    
});