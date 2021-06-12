$(document).ready(function(){
    $("#filter-select").change(function(){
        $("form").submit();
    });

    $.ajax({
    type: 'GET',
    url:'getallcategories/',
        success: function (data){
        console.log(data);
            for(var key in data){
                console.log(data[key]['fields']['name']);
                var o = new Option(data[key]['fields']['name'], data[key]['pk']);
                $(o).html(data[key]['fields']['name']);
                $("#filter-select").append(o);
            }
            var selected_val = $("#filter-selected").val();
            if(selected_val!=''){
                $('#filter-select option[value='+selected_val+']').attr('selected', true);
            }
        }
    });

});