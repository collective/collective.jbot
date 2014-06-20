jQuery(function($) {

    $().ready(function() {
        var $parent = $('.link-parent');
        $parent.attr('href', portal_url + '/plone_control_panel');

        var WINDOW_BASE = window.location.protocol + '//' + window.location.host;

        var WINDOWED_HEIGHT = '300px';
        var FULLSCREEN_HEIGHT = '600px';

        // Editor management

        var extensionModes = {
            css: "ace/mode/css",
            js: "ace/mode/javascript",
            htm: "ace/mode/html",
            html: "ace/mode/html",
            xml: "ace/mode/xml"
        };
        var defaultMode = "ace/mode/text";

        function getExtension(path) {
            var m = path.match(/.(\w+)$/);
            if(m == null) return null;
            return m[1].toLowerCase();
        }

        function isHTMLFile(path) {
            var extension = getExtension(path);
            return extension == 'html' || extension == 'htm';
        }

        // See http://stackoverflow.com/questions/1694295/jquery-background-color-animate-not-working/5718151
        function animateHighlight(node, highlightColor, duration) {
            var highlightBg = highlightColor || "#FFFFE3";
            var animateMs = duration || 750;
            var originalBg = $(node).css("background-color");

            if (!originalBg || originalBg == highlightBg)
                originalBg = "#FFFFFF"; // default to white

            $(node)
                .css("backgroundColor", highlightBg)
                .animate({ backgroundColor: originalBg }, animateMs, null, function () {
                    $(node).css("backgroundColor", originalBg);
                });
        };

        if($.browser.msie) {
            $(".ie-warning").show();
        }
        var RESOURCES = null;
        $.ajax({
          url: portal_url + '/@@available-resources',
          success: function(data){
            RESOURCES = data;
          }
        });
        var $searchContainer = $('#search-resources');
        var $results = $('ul', $searchContainer);
        var handler = function(e){
          e.preventDefault();
          $results.empty();
          var val = $('input', $searchContainer).val().toLowerCase();
          for(var i=0; i<RESOURCES.length; i++){
            if(RESOURCES[i].toLowerCase().indexOf(val) !== -1){
              var el = document.createElement('li');
              var $el = $(el);
              var customize = document.createElement('a');
              var $customize = $(customize);
              $customize.html('Customize');
              $customize.attr('href', '#');
              $customize.attr('data-resource', RESOURCES[i]);
              $customize.click(function(e){
                e.preventDefault();
                $.ajax({
                  url: portal_url + '/@@customize-jbot-resource',
                  type: 'POST',
                  data: {
                    _authenticator: $('[name="_authenticator"]').val(),
                    resource: $(this).attr('data-resource')
                  },
                  success: function(){
                    window.location.reload();
                  },
                  error: function(){
                    alert('error customizing');
                  }
                });
              });
              $el.html(RESOURCES[i] + ' - ');
              $el.append($customize);
              $results.append($el);
            }
          }
        };
        $('button', $searchContainer).click(handler);
        $('form', $searchContainer).submit(handler);
        $("#search-resources-btn").overlay({
          closeOnClick: false,
          onBeforeLoad: function() {
            $('input', $searchContainer).focus();
          },
          onBeforeClose: function() {
          }
        });
  });
});

