function clipboardTooltip(selector) {
    var clipboard = new Clipboard(selector);
    clipboard.on('success', function (e) {
        e.clearSelection();
        $(e.trigger).tooltip('show');
        setTimeout(function() {
            $(e.trigger).tooltip('hide');
        }, 1000);
    });
}

clipboardTooltip('#btn-clipboard-copy')
clipboardTooltip('#btn-clipboard-profileset')

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