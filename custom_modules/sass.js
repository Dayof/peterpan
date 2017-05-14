exports.task = {
  dist: {
    options: {
      style: 'expanded',
      lineNumbers: true, // 1
      sourcemap: 'none'
    },
    files: [{
      expand: true, // 2
      cwd: './peterpan/static/sass',
      src: [ '**/*.scss' ],
      dest: './peterpan/static/public',
      ext: '.css'
    }]
  }
};
