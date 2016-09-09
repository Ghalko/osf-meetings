import Ember from 'ember';
import config from '../config/environment';

export
default Ember.Route.extend({
    beforeModel: function() {
        var refererUrl = window.location.toString();
        var nextQueryParam = '';
        if (refererUrl.indexOf(config.providers.osfMeetings.loginUrl) === -1) {
            // Make sure redirect url doesn't go back to login page
            // and cause infinite loop
            nextQueryParam = "?next=" + window.location;
        }
        
        window.location = config.providers.osfMeetings.apiLoginUrl + nextQueryParam;                      
    }
});