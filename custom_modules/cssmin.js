exports.task = {
  my_target: {
    files: [{
      expand: true,
      cwd: './peterpan/static/public/',
      src: [ '*.css', '!*.min.css' ], // 1
      dest: './peterpan/static/public/',
      ext: '.min.css'
    }]
  }
};
