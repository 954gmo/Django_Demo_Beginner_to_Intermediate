$(document).ready(function (){

    let files_to_upload = [];
    let single_file_group = [];
    let multi_file_group = [];

    $('#msg_all, #msg_selected').click(function (e) {
        let form_data = new FormData();

        if (e.target.id === 'msg_all'){
            const q = document.getElementById('searchbar').value;
            const f = document.getElementById('from_date').value;
            const t = document.getElementById('to_date').value;
            const stores =document.getElementsByName('store');
            let store = [];
            for (let i = 0, n = stores.length; i < n; i ++ ){
                if(stores[i].checked){
                    store.push(stores[i].id);
                }
            }
            form_data.append('q', q);
            form_data.append('f', f);
            form_data.append('t', t);
            form_data.append('s', store.join(','));
        }else{
            const checked_items = document.querySelectorAll('input[name="record"]:checked');
            let ids = []
            for (let i=0; i < checked_items.length; i++){
                ids.push(checked_items[i].id);
            }
            form_data.append('ids', ids.join(','));
        }

        files_to_upload = multi_file_group.concat(single_file_group);
        for (const file in files_to_upload){
            if (typeof(file) != "undefined"){
                console.log(files_to_upload[file]);
                form_data.append('files', files_to_upload[file]);
            }
        }

        let msg = document.getElementById('msg_content').value;
        form_data.append('action', 'send_msg');
        form_data.append('msg', msg);

        e.preventDefault();
        $.ajax({
            url: '/mgmt_cust_info/send_msg',
            type: 'POST',
            data: form_data,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (data){
                console.log(data);
            },
            error: function (data) {
                console.log(data);
            }
        });
    });

    $('#multi_files').change(function (e) {
        multi_file_group = [];
        $('ul.multi_file_list').html('');

        for (let i=0; i < this.files.length; i++){
            $('ul.multi_file_list').append(`<li class="list-group-item">
                                                <button class="multi_group" id="f-${i}" >delete</button>
                                                <strong>${this.files[i].name}</strong>
                                            </li>`);
            multi_file_group.push(this.files[i]);
        }
    })

    $('form button.add').click(function(e) {
        e.preventDefault();
        let nb_attachments = $('form input').length;
        let $input = $('<input type="file" name=attachment-' + nb_attachments + '>');
        $input.on('change', function(evt) {
            let f = evt.target.files[0];
            $('form').append($(this));
            $('ul.file_selected').append(`<li class="list-group-item">
                                                <button  class="single_group" id="sf-${nb_attachments}" >delete</button>
                                                <strong>${f.name}</strong>
                                           </li>`);
            single_file_group.push(f);
        });
        $input.hide();
        $input.trigger('click');
    });

    $(document).on('click', '.multi_group', function (e) {
        delete multi_file_group[parseInt(e.target.id.split('-')[1])];
        this.parentElement.remove();
    });

    $(document).on('click', '.single_group', function (e){
        delete single_file_group[parseInt(this.id.split('-')[1])];
        this.parentElement.remove();
    });
});


