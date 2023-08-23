$(document).on('click', '[data-delete]', function () {
    var url = $(this).attr('data-delete');
    $.ajax('/delete', {
        method: 'post',
        data: { url: url },
        success: function (data) {
            if (data.status != 'success') {
                alert(data.message);
                return;
            }
            loadFileList();
        },
    });
});
function download() {
    var url = $('#url').val();
    var name = $('#name').val();
    $.ajax('/download', {
        method: 'post',
        data: {
            name: name,
            url: url,
        },
        success: function (data) {
            if (data.status != 'success') {
                alert(data.message);
                return;
            }
            loadFileList();
        },
    });
}
function loadFileList() {
    $.ajax('/list', {
        method: 'post',
        success: function (data) {
            if (data.status != 'success') {
                alert(data.message);
                return;
            }
            $('#links>li').remove();
            for (var i = 0; i < data.data.length; i++) {
                var file = data.data[i];
                var template =
                    $('#links').html() +
                    '<li class="w3-bar w3-padding">' +
                    '    <span class="w3-bar-item w3-left">' +
                    file.name.replace('static/files/', '') +
                    '</span>' +
                    '    <span class="w3-bar-item w3-right">' +
                    '        <span class="w3-text-grey">' +
                    file.size +
                    ' &nbsp; </span>' +
                    '        <a href="' +
                    file.name +
                    '" class="w3-btn w3-teal w3-round"> <span class="fa fa-download"></span></a>' +
                    '        <span data-delete="' +
                    file.name +
                    '" class="w3-btn w3-red w3-round"> <span class="fa fa-trash"></span></span>' +
                    '    </span>' +
                    '</li>';
                $('#links').html(template);
            }
        },
    });
}

function getLink() {
    var url = $('#yt-url').val();
    $('#youtube-links>li').remove();
    $.ajax('/links', {
        method: 'post',
        data: {
            url: url,
        },
        success: function (data) {
            if (data.status != 'success') {
                alert(data.message);
                return;
            }
            for (let i = 0; i < data.data.length; i++) {
                var stream = data.data[i];
                var html =
                    $('#youtube-links').html() +
                    '<li class="w3-bar w3-padding"> <span class="w3-bar-item w3-left">' +
                    stream.resolution +
                    '</span>' +
                    '<span class="w3-bar-item w3-right">' +
                    '<span class="w3-text-grey">' +
                    stream.filesize +
                    ' &nbsp; </span>' +
                    '<a href="' +
                    stream.url +
                    '" class="w3-btn w3-teal w3-round">' +
                    '<span class="fa fa-download"></span>' +
                    ' </a>' +
                    ' </span>' +
                    '</li>';
                $('#youtube-links').html(html);
            }
        },
    });
}

$(loadFileList);
