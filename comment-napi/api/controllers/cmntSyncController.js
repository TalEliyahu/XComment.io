'use strict';

var modes='text';
//var script2Path='/Users/trx/projects/comments_remover/comments_remover_fork';
var script2Path='../';
var lang = 'Python';
var tmpfile;

var PythonShell = require('python-shell');
var bodyParser = require('body-parser')
var filemanager = require('easy-file-manager')

var fs = require('fs');
var path = require('path');


var path = "tmp"
var filename = "test.py"
var prefix = 'rc.'
var data; // buffered image




//create application/json parser
var jsonParser = bodyParser.json()


exports.sendContent = function(req, res) {
    //add args lang, payload2file
    if (!req.body) {
        console.log(req.body)
        return res.sendStatus(401)
};
    if (req.body.source) {
         filemanager.upload(path,filename,res.body.source,function(err){
            if (err) console.log(err);
        });


    var inPath = path.join(__dirname, '..', path, filename);

    console.log('The in path %j', inPath)


    }
    var options = {
        mode: modes,
        scriptPath: script2Path,
        args: [inPath, lang]
    };


    PythonShell.run('comments_remover.py', options, function(err, res) {
    outFile = prefix.concat(filename)
    var outPath = path.join(__dirname, '..', path, outFile)
    var outString = fs.readFileSync(outPath, 'utf8');



    if (err) throw err;
    // results is an array consisting of messages collected during execution
        console.log('results: %j', results);


    });

   res.send('Finished')
};


exports.getlist = function(req, res) {
    var options = {
        mode: modes,
        scriptPath: script2Path,
        args: ['-i']
    };


    PythonShell.run('comments_remover.py', options, function(err, results) {
    if (err) {
        throw err;
    };
    // results is an array consisting of messages collected during execution
    console.log('Finished');

    });
        res.send('Finished with : %j ', options)


};
