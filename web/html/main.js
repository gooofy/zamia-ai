
// globals
var cur_prompt = null;
var cur_ts = null;
var cur_id = 0;
var cur_ts_incomplete = true;
var selector_table = null;

function select_submission (sId) {
    console.log ("Audio selected: ", sId);
    cur_id = sId;
                   
    $('#audio').html ('<audio controls id="actrl" autoplay> <source id="asrc" src="/wav?id='+ sId +'" type="audio/wav"> Your browser does not support this audio format.</audio>');

    $.get ('/submission_get_details?id=' + sId, function( data ) {
        console.log ("details for sId=", sId, ': ', data);    

        cur_prompt = data['prompt'];

        $('#prompt-text').html (cur_prompt);

        if (data['reviewed']) {
            // audio quality

            switch (data['pcn']) {
            case 0:
                $('#pr-clean').prop('checked', true);
                break;
            case 1:
                $('#pr-accent').prop('checked', true);
                break;
            case 2:
                $('#pr-dialect').prop('checked', true);
                break;
            case 3:
                $('#pr-error').prop('checked', true);
                break;
            case 4:
                $('#pr-oov').prop('checked', true);
                break;
            }

            $('#truncated').prop('checked', data['truncated']);

            switch (data['audiolevel']) {
            case 0:
                $('#al-good').prop('checked', true);
                break;
            case 1:
                $('#al-low').prop('checked', true);
                break;
            case 2:
                $('#al-very-low').prop('checked', true);
                break;
            case 3:
                $('#al-distorted').prop('checked', true);
                break;
            }

            switch (data['noiselevel']) {
            case 0:
                $('#nl-low').prop('checked', true);
                break;
            case 1:
                $('#nl-noticable').prop('checked', true);
                break;
            case 2:
                $('#nl-high').prop('checked', true);
                break;
            }
        }

        $('#comment').val (data['comment']);

        // transcript table

        cur_ts = data['transcript'];

        var tt = $('#transcript-table').find('tbody');

        tt.html('');

        cur_ts_incomplete = false;

        for (var i = 0; i<cur_ts.length; i++) {

            var wentry = cur_ts[i];

            var w_tr = $('<tr/>');

            w_tr.append($('<td/>').html(wentry['word']));
            var w_td = $('<td/>');

            var ps = wentry['pronounciations'];
            for (var j = 0; j<ps.length; j++) {
                var p = ps[j];

                var p_radio = $('<input type="radio" name="wt' + i + '" value="' + p['pid'] + '"> [' + p['ipa'] + '] </input>');

                if (p['pid'] == wentry['selpid']) {
                    p_radio.prop('checked', true);
                }

                w_td.append(p_radio);

                // FIXME w_td.append($('<img id="wt' + j + '-edit" src="edit.png">'));
            }

            if (ps.length == 0)
                cur_ts_incomplete = true;

            // FIXME w_td.append($('<img id="wt001-edit" src="add.png" width=16px>'));

            w_tr.append(w_td);
            tt.append (w_tr);
        }
    }); 
}

$(document).ready(function(){
    selector_table = $('#dt_selector').dataTable( {
        "bProcessing": true,
        "bServerSide": true,
        "bAutoWidth" : false,
        "aoColumns": [
           { "sWidth": "0%" },
           { "sWidth": "35%" },
           { "sWidth": "60%" },
           { "sWidth": "5%"  },
           ],
        "aoColumnDefs": [{ "bVisible": false, "aTargets": [0] }],
        "aaSorting": [[ 3, "asc" ]],
        "sAjaxSource": "submissions",
        "fnDrawCallback": function ( oSettings ) {
            $('#dt_selector tbody tr').each( function () {
                $(this).click( function () {
                    var iPos = selector_table.fnGetPosition( this );
                    var aData = selector_table.fnGetData( iPos );
                    var sId = aData[0];
                    select_submission (sId);
                })
            })}
    } );

    $("#savebutton").click( function (event) {
        
        if (!cur_ts)
            return;

        if (cur_ts_incomplete) {
            alert("Transcript incomplete!");
            return;
        }

        var data = { 'sid': cur_id };

        data['pcn']        = $('input[name=pronounciation]:checked').val() 
        data['truncated']  = $('#truncated').is(":checked")
        data['audiolevel'] = $('input[name=audio-level]:checked').val() 
        data['noiselevel'] = $('input[name=noise]:checked').val() 
        data['comment']    = $('#comment').val() 

        // collect transcript info

        data['transcript'] = [];

        for (var i = 0; i<cur_ts.length; i++) {

            var wentry = cur_ts[i];

            //var ps = wentry['pronounciations'];
            //for (var j = 0; j<ps.length; j++) {
            //    var p = ps[j];
                data['transcript'].push( { 'pid': $('input[name=wt' + i + ']:checked').val(),
                                           'wid': wentry['wid'] } );
            //}
        }

        console.log ("savebutton data: ", data);

        $.ajax({
            url: '/save',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            //dataType: "JSON",
            //data: data,
            success: function(result) {
                console.log ("savebutton result: ", result) ;
                selector_table.fnReloadAjax();
            }
        });
    });

    // prompt popup

    $("#prompt-edit").click( function (event) {
        if (!cur_prompt)
            return;

        $("#pp-input").val (cur_prompt);

        $("#prompt-popup").show();
        var y = $(window).height() / 2 - $("#prompt-popup").height() / 2 + $(window).scrollTop();
        var x = $(window).width() / 2 - $("#prompt-popup").width() / 2;
        $("#prompt-popup").css({
            top: y,
            left: x
        });
    });

    $("#pp-close").click(function(e) {
        $("#prompt-popup").hide();
        return false;
    });

    $("#pp-save").click(function(e) {

        var cur_prompt = $("#pp-input").val();
        $("#prompt-popup").hide();

        data = { prompt: cur_prompt, sid: cur_id };

        $.ajax({
            url: '/setprompt?data=' + encodeURIComponent(JSON.stringify(data)),
            type: 'GET',
            success: function(result) {
                selector_table.fnReloadAjax ();
                select_submission (cur_id);
            }
        });


        return false;
    });

});
