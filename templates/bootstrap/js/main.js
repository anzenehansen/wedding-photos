$("#sort-pics").click(function(e){
    $("#video").hide();
    $("#photo").show();
});

$("#sort-video").click(function(e){
    $("#video").show();
    $("#photo").hide();
});

$("#sort-all").click(function(e){
    $("#video").show();
    $("#photo").show();
});

/** Videos really shouldn't be a slideshow, so we disable it for videos and allow it for pics **/
$(".video").prettyPhoto({theme: 'facebook'});
$(".photo").prettyPhoto({theme: 'facebook',slideshow:5000, autoplay_slideshow:true});
