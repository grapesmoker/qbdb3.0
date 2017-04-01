module.exports = function(grunt) {

    grunt.initConfig({
	pkg: grunt.file.readJSON('package.json'),
	browserify: {
	    options: {
		browserifyOptions: {
		    paths: [
			'qbdb/static/js'
		    ]
		}
	    },
	    client: {
		src: ["qbdb/static/js/**/*.js"],
		dest: "qbdb/js/library.js"
	    }
	},
	handlebars: {
	    compile: {
		options: {
		    namespace: "JST",
		    processName: function(filePath) {
			return filePath.replace(/^qbdb\/static\/js\/templates\//, '').replace(/\.hbs$/, '')
		    },
		    commonjs: true
		},
		files: {
		    'papers/static/js/templates/templates.js': ['qbdb/static/js/templates/**/*.hbs']
		}
	    }
	}
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-handlebars');

    grunt.registerTask('default', ['handlebars', 'browserify:client'])
}