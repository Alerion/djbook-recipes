Ext.ux.MainViewport = Ext.extend(Ext.Viewport, {
    renderTo: Ext.getBody(),
    initComponent: function(){
        var config = {
            layout: 'border',
            defaults: {
                frame: true
            },
            items: [{
                region: 'center',
                html: '',
                tbar: [{
                    text: 'Say Hello',
                    handler: this.sayHello,
                    scope: this
                }]
            },{
                region: 'west',
                html: 'West',
                width: 350
            }]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.MainViewport.superclass.initComponent.apply(this, arguments);
    },//initComponent
    sayHello: function(){
        Ext.Msg.prompt('Name', 'Please enter your name:', function(btn, text){
            if (btn == 'ok') {
                MainApi.hello(text, function(response){
                    Ext.ux.msg('Success', response.msg, Ext.Msg.INFO);
                })
            }
        })
    }                    
});