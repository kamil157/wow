var clipboard = new Clipboard('#btn-clipboard');

clipboard.on('success', function(e) {
    e.clearSelection();
    $(e.trigger).tooltip('show');
    setTimeout(function() {
        $(e.trigger).tooltip('hide');
    }, 1000);
});

$('input').change(function() {
    if (this.checked)
    {
        $(this.parentElement).addClass('checked');
    }
    else
    {
        $(this.parentElement).removeClass('checked');
    }
});