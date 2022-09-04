$(document).ready(function (e) {
    const all_store = $('#all_store');
    const stores_checkboxes = $('input[name=store]');
    all_store.change(function (e) {
       if($(this).is(':checked')){
           stores_checkboxes.each(function () {
               $(this).prop('checked', true);
           });
           search();
       }else{
           stores_checkboxes.each(function () {
              $(this).prop('checked', false);
           });
           sig_alert("Please Select a store or all store before searching");
       }
    });

    stores_checkboxes.each(function (){
        $(this).click(function (e) {
            const checked_cnt = $('input[name=store]:checked').length;
            if(stores_checkboxes.length === checked_cnt){
                all_store.prop('checked', true);
                search();
            }else if (checked_cnt){
                all_store.prop('checked', false);
                search();
            }else{
                all_store.prop('checked', false);
                sig_alert("Please Select a store or all store before searching");
            }
        });
    });

    const all_shift = $('#all_shift');
    const shift_checkboxes = $('input[name=shift]');

    if (all_shift.length){
        all_shift.change(function (e) {
            if($(this).is(':checked')){
                if (shift_checkboxes.length){
                    shift_checkboxes.each(function (){
                        $(this).prop('checked', true);
                    });
                }
                search();
            }else{
                if (shift_checkboxes.length){
                    shift_checkboxes.each(function () {
                       $(this).prop('checked', false);
                    });
                    sig_alert("Please Select a shift or all shift before searching");
                }
            }
        })
    }
    if (shift_checkboxes.length){
        shift_checkboxes.each(function () {
            $(this).change(function (e){
                const shift_cnt = $('input[name=shift]:checked').length;
                if (shift_checkboxes.length === shift_cnt){
                    all_shift.prop('checked', true);
                    search();
                }else if(shift_cnt){
                    all_shift.prop('checked', false);
                    search();
                }else{
                    all_shift.prop('checked', false);
                    sig_alert("Please Select a shift or all shift before searching");
                }
            });
        });
    }

    $('#searchbar').keyup(function (e) {
        search();
    });

    $('#from_date, #to_date').change(function () {
        search();
    });

    $('#filter_by_date').click(function () {
        search();
    });

    $('#reset_date_filter').click(function () {
       $('#all_store').prop('checked', true);
       stores_checkboxes.each(function (){
           $(this).prop('checked', true);
       });
       $('#searchbar').val('');
       $('#from_date').val('');
       $('#to_date').val('');
       if($('#all_shift').length){
           $('#all_shift').prop('checked', true);
           shift_checkboxes.each(function () {
              $(this).prop('checked', true);
           });
       }
       search();
    });

    $('#txt_qr_code').click(function(e) {
        const checked_items = document.querySelectorAll('input[name="record"]:checked');
        let ids = []
        for (let i=0; i < checked_items.length; i++){
            ids.push(checked_items[i].id);
        }
        if (ids.length === 0){
            sig_alert("Please Select Customer to Send QR code, if any");
            return;
        }
        let form_data = new FormData();
        form_data.append('ids', ids.join(','));
        e.preventDefault();
        $.ajax({
            url: '/txt_QR_code/',
            type: 'POST',
            data: form_data,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (data){
                 $('#msg').html(`QR code Sent to Customer(s) ${ids.join(',')}`);
                    $('#msg-div').show();
                    setTimeout(function () {
                        $('#msg-div').hide();
                    }, 3000);
            },
            error: function (data) {
                sig_alert("Server Internal Error, Please Report the Issue!");
            }
        });
    });
});

function pagination_ajax(url) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            pagination_result(this.responseText);
        }
    };
    xhttp.open('GET', window.location.pathname + url);
    xhttp.send();
}

function search(){

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            pagination_result(this.responseText);
        }
    };

    xhttp.open('GET',  action_url());
    xhttp.send();
}

function action_url(act_type='search'){
    // if store element is present
    if ($('#all_store').length){
        // if no store selected, alert and quit the search
        const store_checked_cnt = $('input[name=store]:checked').length;
        if (store_checked_cnt === 0){
            sig_alert("Please Select a store or all store before searching");
            return;
        }
    }



    // if shifts is enabled but no shift is selected, alert and quit the search
    // otherwise check which shift is selected
    let shift = [];
    const shifts = $('input[name=shift]');
    if(shifts.length){
        if($('input[name=shift]:checked').length === 0){
             sig_alert("Please Select a shift or all shift before searching");
             return;
        }
        shifts.each(function () {
           if($(this).is(':checked')){
               shift.push($(this).attr('id'));
           }
        });
    }

    const q = document.getElementById('searchbar').value;
    const from_date = document.getElementById('from_date').value;
    const to_date = document.getElementById('to_date').value;

    const stores = $('input[name=store]');
    let store = [];
    for (let i = 0, n = stores.length; i < n; i ++ ){
            if(stores[i].checked){
                store.push(stores[i].id);
            }
    }
    // stores.each(function () {
    //    if($(this).is(':checked')){
    //        store.push($(this).attr('id'));
    //    }
    // });
    return `${window.location.pathname}${act_type}?q=${q}&f=${from_date}&t=${to_date}&s=${store.join(',')}&st=${shift.join(',')}`;
}

function pagination_result(responseText) {
    $('#search_result').html(responseText);
    $('#total_records').html($('#total').html());
    $('#selected_records').html($('#selected_amt').html());
    if($('#msg-h2').length){
        $('#total_records_msg').html($('#total').html());
        $('#selected_records_msg').html($('#selected_amt').html());
    }
}

$(document).ready(function () {
    $('#export_all').click(function (e){
        if ($('#total_records').html() === '0'){
            sig_alert("empty result set of  no records are selected");
            return;
        }
        exportation(action_url('export'));
    });

    $('#export_selected').click(function (e) {
        if ($('#selected_records').html() === '0'){
            alert("empty result set of  no records are selected");
            return;
        }
        const checked_items = document.querySelectorAll('input[name="record"]:checked');

        let ids = []
        for (let i=0; i < checked_items.length; i++){
            ids.push(checked_items[i].id);
        }
        exportation(`${window.location.pathname}export?ids=${ids.join(',')}`);
    });
});

function exportation(url){
        const xhttp = new XMLHttpRequest();
        xhttp.responseType = 'blob';
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                let blob = this.response;
                let filename = '';
                let disposition = xhttp.getResponseHeader('Content-Disposition');
                if (disposition && disposition.indexOf('attachment') !== -1){
                    let filename_regex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    let matches = filename_regex.exec(disposition);
                    if (matches !== null && matches[1]){
                        filename = matches[1].replace(/['"]/g, '');
                    }
                }
                if (typeof window.navigator.msSaveBlob !== 'undefined'){
                    window.navigator.msSaveBlob(blob, filename);
                }else{
                    let URL = window.URL || window.webkitURL;
                    let downloadURL = URL.createObjectURL(blob);
                    if (filename){
                        let a = document.createElement('a');
                        if (typeof a.download === 'undefined'){
                            window.location.href = downloadURL;
                        }else{
                            a.href = downloadURL;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                        }
                    }else{
                        window.location.href = downloadURL;
                    }
                }
            }
        };
        xhttp.open('GET', url, true);
        xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhttp.send();
}

