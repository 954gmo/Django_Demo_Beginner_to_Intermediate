function check_all(source) {
    // get all records' checkboxes in the current page
    const checkboxes = document.getElementsByName('record');
    if(document.getElementById('all').checked){
        // selected all records in the current page
        for (let i = 0, n = checkboxes.length; i < n; i ++ ){
            checkboxes[i].checked = source.checked;
        }
        // update statistics
        $('#selected_amt').html(checkboxes.length);
        $('#txt_selected').html(checkboxes.length);
        if ($('#export').length) {
            $('#selected_records').html($('#selected_amt').html());
            $('#total_records').html($('#total').html());
        }
        if ($('#msg').length){
            $('#selected_records_msg').html($('#selected_amt').html());
            $('#total_records_msg').html($('#total').html());
        }
    }else{
        // dis-select all records in the current page
        for (let i = 0, n = checkboxes.length; i < n; i ++ ){
            checkboxes[i].checked = false;
        }
        // update statistics,
        $('#txt_selected').html('0');
        $('#selected_amt').html('0');
        if ($('#export').length) {
            $('#selected_records').html('0');
        }
        if ($('#msg').length){
            $('#selected_records_msg').html('0');
        }
    }
}

function check(){
    if (document.getElementById('all').checked){
        // dis-select the 'select all'
        document.getElementById('all').checked = false;
        // update statistics
        if ($('#export').length) {
            $('#selected_records').html('0');
        }
        if ($('#msg').length){
            $('#selected_records_msg').html('0');
        }
    }
    // update statistics, how many records are selected
    let count = document.querySelectorAll('input[name="record"]:checked').length.toString();
    document.getElementById('selected_amt').innerHTML = count;
    $('#txt_selected').html(count);
    if ($('#export').length) {
        $('#selected_records').html(count);
    }
    if ($('#msg').length){
        $('#selected_records_msg').html(count);
    }
}
