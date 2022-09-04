
$(document).ready(function () {
    $('#del').click(function (e){
        const id = $('#cust').html();
        const first_name = $('#first_name').val();
        const last_name = $('#last_name').val();
        const phone = $('#phone').val();
        const text = `Deleting is NOT Reversible! You are deleting customer ${id}, ${first_name}, ${last_name}, ${phone}, Please confirm before you click 'OK' to execute deletion! `;
        if (confirm(text) === false){
            return;
        }
        e.preventDefault();
        $.post(
            window.location.pathname.replace('edit', 'del'),
            {
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'id': id,
            },
            function (data) {
                if (data['status'] === 200){
                    $('#edit_customer').html('');
                    $('#msg').html(`Customer ${id} Disabled!`);
                    $('#msg-div').show();

                    setTimeout(function(){
                        $('#msg-div').hide();
                    }, 3000);
                }else{
                    sig_alert("Server Internal Error, Please Report the Issue!");
                }
            });
    });

    $('#save').click(function (e){
        e.preventDefault();
        if (($('#id_periods').val() !== '') && (!$.trim($('#log_info').val()))){
            $('#warning').show();
            return;
        }
        $.post(
            window.location.pathname.replace('edit', 'save'),
            {
                'first_name': $('#first_name').val(),
                'last_name': $('#last_name').val(),
                'phone': $('#phone').val(),
                'id': $('#cust').html(),
                'periods': $('#id_periods').val(),
                'msg': $('#log_info').val(),
            },
            function (data) {
                if (data['status'] === 200){
                    $('#msg').html('Customer Profile Updated!');
                    $('#msg-div').show();
                    setTimeout(function(){
                        $('#msg-div').hide();
                    }, 3000);
                    if ($('#id_periods').val()){
                        let row = $('<tr></tr>');
                        let d = new Date($.now());
                        $('<td></td>').text(d.toDateString() + ' ' + d.toLocaleTimeString()).appendTo(row);
                        let d2 = new Date();
                        d2.setDate(d.getDate() + parseInt($('#id_periods').val()));
                        $('<td></td>').text(
                            d2.toDateString() + ' ' + d.toLocaleTimeString()
                        ).appendTo(row)
                        $('<td></td>').text($('#log_info').val()).appendTo(row);
                        row.prependTo($('#notes_log'));
                        $('#warning').hide();
                        $('#cust_status').html(`Customer is Dis-activated for ${$('#id_periods').find(':selected').text()}`);
                        $('#log_info').val('');
                    }

                }else{
                    sig_alert("Server Internal Error, Please Report the Issue!");
                }
            });
    });
});

