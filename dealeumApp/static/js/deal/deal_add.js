// action="/api/v1/deals" method="POST"


form = $("#add-deal-form")


function addDeal(){
    $.ajax({
        url: "/api/v1/deals",
        method:'POST',
        data:{
            'deal_url':$(form).find('#deal-url').val(),
            'title':$(form).find('#deal-title').val(),
            'new_price':$(form).find('#new-price').val(),
            'old_price':$(form).find('#old-price').val(),
            'message':$(form).find('textarea').val()
        }
    }).done(function(data, textStatus, xhr){
        if(xhr.status === 201){
            window.location.href = "/"
        }else{

        }
    })
}