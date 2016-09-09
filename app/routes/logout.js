import Ember from 'ember';

export default Ember.Route.extend({
	beforeModel: function() {
        window.location = "http://localhost:8000/accounts/logout/";
    }
});
