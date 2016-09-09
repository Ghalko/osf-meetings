import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo } from 'ember-data/relationships';
import { validator, buildValidations } from 'ember-cp-validations';

var Validations = buildValidations({
    title: {
        description: 'Title',
        validators: [
            validator('presence', true),
            validator('unique-submission-title'),
            validator('length', {
                min: 4
            }),
        ]
    },
    description: {
        description: 'Description',
        validators: [
            validator('presence', true),
            validator('length', {
                min: 10
            })
        ]
    },
}, {
    debounce: 500,
});


export default Model.extend(Validations, {
    conference : belongsTo('conference'),
    title : attr('string'),
    description : attr('string'),
    canEdit: attr('boolean'),
    nodeId: attr('string'),
    category: attr('string', { defaultValue : 'project' }),
    dateCreated: attr(),
    contributor : belongsTo('user'),
    fileId: attr('string'),
    fileUrl: attr('string')
});
