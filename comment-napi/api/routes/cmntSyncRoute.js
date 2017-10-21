'use strict';
module.exports = function(app) {
    var cmntSync = require('../controllers/cmntSyncController');

    // input endpoint
    app.route('/input')
        .post(cmntSync.sendContent);


    // get supported programming langs
    app.route('/langs')
        .get(cmntSync.getlist);

    // for processing zip file
    //app.route('/processzip')
    //    .post(cmntSync.processZip)



};
