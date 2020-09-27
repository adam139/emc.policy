// add tag to under documentByLine

define([
    'pat-base',
    'mockup-patterns-structure-url/pattern-structureupdater',
], function(Base) {
    'use strict';
    var Pattern = Base.extend({
      name: 'structureupdater_emc',  // Give it another name than the original pattern
      trigger: '.template-folder_contents',
      parser: 'mockup',
      init: function() {
        $('body').on('context-info-loaded', function (e, data) {
          // Do our task
          if (data.object ) {
          var $subject = data.object.Subject;
          
          
            if ($subject.length != 0 && !this.$el.hasClass("tagged"))  {
              var $stag = '<ul id="subject"><li class="first"><span class="glyphicon glyphicon-tags" aria-hidden="true"></span></li>';
              var $etag = '</ul>';
              var out = '';
              for(var j = 0,len = $subject.length; j < len; j++){
                 out = out + '<li><a class ="btn btn-default" href="#">' + $subject[j] + '</a></li>';
                 //console.log($subject[j]);
               }
               var $tags = $stag + out + $etag;
               $('#plone-document-byline').before(data.object &&  $tags);
               this.$el.addClass("tagged");
            }
          }
        }.bind(this));
      }
    });
    return Pattern;
});