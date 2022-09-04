$(document).ready(function () {
    $('#save').click(function (e){
        e.preventDefault();
        $.post(
            window.location.pathname.replace('edit', 'save'),
            {
                'first_name': $('#first_name').val(),
                'last_name': $('#last_name').val(),
                'email': $('#email').val(),
                'user_type': $('#user_type').val(),
                'is_active': $('#is_active').is(':checked'),
                'id': $('#op_id').html(),
            },
            function (data) {
                if (data['status'] === 200){
                    let m = document.getElementById('msg');
                    let dm = document.getElementById('msg-div');
                    m.innerHTML = 'Operator Profile Updated!';
                    dm.style.display = 'block';
                    setTimeout(function(){
                        m.innerHTML = '';
                        dm.style.display = 'none';
                    }, 3000);
                }
            });
    });
    $('#chk_change_password').click(function (e) {
        if($(this).is(":checked")){
            $('#password_change_div').show();
        }else{
            $('#password_change_div').hide();
        }
    });

    $('#change_password').click(function (e) {
        if ($('#new_password1').val() !== $('#new_password2').val()){
            $('#warning').show();
            return;
        }
        $('#warning').hide();
        e.preventDefault();
        $.post(
            '/operator/change_password',
            {
                'new': $('#new_password1').val(),
                'id': $('#op_id').html(),
            },
            function (data) {
                if (data['status'] === 200){
                    $('#msg_pass').show();
                    $('#new_password1').val('');
                    $('#new_password2').val('');
                    setTimeout(function(){
                        $('#msg_pass').hide();
                    }, 3000);
                }
            });
    });
});
