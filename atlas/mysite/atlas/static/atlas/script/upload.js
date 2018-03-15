(function(){
    console.log("LOADING UPLOAD JS")
    $('#helpbox').hide();



    $(document).on('ready', function() {


        $("#input-44").fileinput({
            uploadUrl: '/service/upload/',
            maxFilePreviewSize: 1024,
            showBrowse: true,
            allowedFileExtensions: ["txt", "csv", "text"],
            browseOnZoneClick: true,
            maxFileCount: 1
        });

        $("#input-441").fileinput({
            uploadUrl: '/service/upload/',
            maxFilePreviewSize: 1024,
            showBrowse: false,
            allowedFileExtensions: ["txt", "csv", "text"],
            browseOnZoneClick: true,
            maxFileCount: 1
        });
        $("#input-442").fileinput({
            uploadUrl: '/service/upload/',
            maxFilePreviewSize: 1024,
            showBrowse: false,
            allowedFileExtensions: ["txt", "csv", "text"],
            browseOnZoneClick: true,
            maxFileCount: 1
        });

        $("input:checkbox[name='opt1']").change(function() {
            if(this.checked) {
                $('#sd_upload').show();
            }
            else{
                $('#sd_upload').hide();
            }
        });

        $("input:checkbox[name='opt2']").change(function() {
            if(this.checked) {
                $('#td_upload').show();
            }
            else{
                $('#td_upload').hide();
            }
        });

        var step1_choice, step2_choice = "";

        $('#btnNext1').on("click", function(){
        console.log("inside button click 1");
            $('#td_panel').removeClass('hidden');
            $('#sd_panel').addClass('hidden');
        });

        $('#btnNext2').on("click", function(){
                console.log("inside button click 2");

            $('#data_panel').removeClass('hidden');
            $('#td_panel').addClass('hidden');
        });

        $('#help').click(function(){
            $('#helpbox').toggle('swing');
        });
    });



//    $('#fileupload').fileupload({
//        url: '/service/upload/',
//        dataType: 'json',
//        done: function (e, data) {
//            console.log("File uploaded");
//            if($('<p/>').text().length > 1){
//                $('<p/>').text("");
//            }
//            $('<p/>').text(data.files[0].name).appendTo('#files');
//        },
//        progressall: function (e, data) {
//            var progress = parseInt(data.loaded / data.total * 100, 10);
//            $('#progress .progress-bar').text(progress + '%');
//            $('#progress .progress-bar').css('width', progress + '%');
//        }
//    }).prop('disabled', !$.support.fileInput)
//        .parent().addClass($.support.fileInput ? undefined : 'disabled');

})();