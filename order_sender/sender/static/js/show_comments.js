function reply_click(clicked_id)
{
    var unzip = clicked_id.replace(/\D/g,'');
    var x = document.getElementById(unzip);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}