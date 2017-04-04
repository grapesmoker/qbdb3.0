module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        browserify: {
            options: {
                browserifyOptions: {
                    paths: [
                        'qbdb/static/js'
                    ]
                    //standalone: 'qbdb'
                },
                transform: ['browserify-shim']
            },
            client: {
                transform: ['browserify-shim'],
                src: ['qbdb/static/js/**/*.js'],
                dest: "static/js/qbdb.js"
            }
        },
        'browserify-jst': {
            compile: {
                options: {
                    processName: function (filePath) {
                        return filePath.replace(/^qbdb\/static\/js\/templates\//, '').replace(/\.html$/, '')
                    }
                },
                src: 'qbdb/static/js/templates/**/*.html',
                dest: 'qbdb/static/js/templates/jst.js'
            }
        },
        handlebars: {
            compile: {
                options: {
                    namespace: "JST",
                    processName: function (filePath) {
                        return filePath.replace(/^qbdb\/static\/js\/templates\//, '').replace(/\.hbs$/, '')
                    },
                    commonjs: true
                },
                files: {
                    'papers/static/js/templates/templates.js': ['qbdb/static/js/templates/**/*.hbs']
                }
            }
        },
        watch: {
            scripts: {
                files: ['qbdb/static/js/**/*.js'],
                tasks: ['browserify:client']
            },
            templates: {
                files: ['qbdb/static/js/templates/**/*.html'],
                tasks: ['browserify-jst', 'browserify:client']
            }
        }
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-handlebars');
    grunt.loadNpmTasks('grunt-browserify-jst');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['browserify-jst', 'browserify:client'])
};