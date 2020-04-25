(function() {
    var subheadings = document.getElementsByTagName("h2");
    for (var i = 0; i < subheadings.length; i++) {
        const element = subheadings[i];
        element.id = 'section-'+i;
    }
 
 })();
