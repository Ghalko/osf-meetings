import Ember from 'ember';

export default Ember.Route.extend({
    info: false,
    init: function(){
        this.controllerFor('index').set('info', false);
        Ember.$('#submission-instructions').hide(); 
    },
    model(params) {
        return Ember.RSVP.hash({
            conf : this.store.findRecord('conference', params.conference_id),
            allSubmissions : this.store.query('submission', {
                conference: params.conference_id
            })
        });
    },
    isEqual: function(p1, p2) {
        return (p1 === p2);
    },
    actions: {
        //component reusable
        toggleInfo() {
            let curInfo = this.controllerFor('index').get('info');
            if (curInfo === true){
                Ember.$('#submission-instructions').hide(400);
            }
            else {
                Ember.$('#submission-instructions').show(400);
            }
            this.controllerFor('index').set('info', !curInfo);
        },
    }
});
