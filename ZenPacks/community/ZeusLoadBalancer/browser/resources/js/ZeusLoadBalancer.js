(function(){
var ZC = Ext.ns('Zenoss.component');
ZC.registerName('ZeusPool', _t('ZXTM Pool'), _t('ZXTM Pools'));
ZC.registerName('ZeusVirtualServer', _t('Virtual Server'), _t('Virtual Servers'));

ZC.ZeusPoolPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'ZeusPool',
            sortInfo: {
                field: 'name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'poolName'},
                {name: 'poolAlgorithm'},
                {name: 'poolNodes'},
                {name: 'poolDraining'},
                {name: 'poolFailPool'},
                {name: 'poolPersistence'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 80
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
            },{
                id: 'poolAlgorithm',
                dataIndex: 'poolAlgorithm',
                header: _t('Algorithm'),
                width: 100
            },{
                id: 'poolNodes',
                dataIndex: 'poolNodes',
                header: _t('Nodes'),
                width: 100
            },{
                id: 'poolDraining',
                dataIndex: 'poolDraining',
                header: _t('Draining'),
                width: 100
            },{
                id: 'poolFailPool',
                dataIndex: 'poolFailPool',
                header: _t('Failure Pool'),
                width: 220
            },{
                id: 'poolPersistence',
                dataIndex: 'poolPersistence',
                header: _t('Persistence'),
                width: 100
            }]
        });
        ZC.ZeusPoolPanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('ZeusPoolPanel', ZC.ZeusPoolPanel);

ZC.ZeusVirtualServerPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'ZeusVirtualServer',
            sortInfo: {
                field: 'name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'vsName'},
                {name: 'vsPort'},
                {name: 'vsProtocol'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
            },{
                id: 'vsPort',
                dataIndex: 'vsPort',
                header: _t('Port'),
                width: 220
            },{
                id: 'vsProtocol',
                dataIndex: 'vsProtocol',
                header: _t('Protocol'),
                width: 220
            }]
        });
        ZC.ZeusVirtualServerPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ZeusVirtualServerPanel', ZC.ZeusVirtualServerPanel);

})();
