function asset(rootDir){
  $.ajax({
    url: rootDir + "include/asset.html", // ディレクトリー変更
    cache: false,
    async: false,
    dataType: 'html',
    success: function(html){
      html = html.replace(/\{\$root\}/g, rootDir);
      document.write(html);
    }
  });
}

function header(rootDir){
  $.ajax({
    url: rootDir + "include/header.html", // ディレクトリー変更
    cache: false,
    async: false,
    dataType: 'html',
    success: function(html){
      html = html.replace(/\{\$root\}/g, rootDir);
      document.write(html);
    }
  });
}

function footer(rootDir){
  $.ajax({
    url: rootDir + "include/footer.html", // ディレクトリー変更
    cache: false,
    async: false,
    dataType: 'html',
    success: function(html){
      html = html.replace(/\{\$root\}/g, rootDir);
      document.write(html);
    }
  });
}

function check(rootDir){
  $.ajax({
    url: rootDir + "include/check.html", // ディレクトリー変更
    cache: false,
    async: false,
    dataType: 'html',
    success: function(html){
      html = html.replace(/\{\$root\}/g, rootDir);
      document.write(html);
    }
  });
}

function show_modal(link, value){
  $("#link").attr("href", link)
  $("#value").text(value)
  $('#myModal').modal()
}

$(document).ready(function() {
  var pagetop = $('.pagetop');
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      pagetop.fadeIn();
    } else {
      pagetop.fadeOut();
    }
  });
  pagetop.click(function () {
    $('body, html').animate({ scrollTop: 0 }, 500);
    return false;
  });
});
