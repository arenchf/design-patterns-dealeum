function sendComment(slug){
    text = $("textarea#write-comment").val()
    $.ajax({
        url : '/api/v1/deals/'+slug+"/comments",
        data: JSON.stringify({message:text}),
        contentType: "application/json",
        type : 'POST'
    }).done( function(data) {
            if(data['success'] === false){
                console.log("no success")
            }
            else{
                addComment(data['comment'])
            }
        }).fail((err)=>{
            console.log("fail")
        })
}

function addComment(commentJson){
    console.log("adding comment",commentJson)
}



function upvoteDeal(button,slug){
    $.ajax({
        url : '/api/v1/deals/'+slug+"/votes",
        type : 'PUT',
        dataType: "json",
        data: {"voteType":"upvote"}
    }).done( function(data) {
                console.log(data)
                points = $(button).parent().find('.deal-points i p').text()
                if(data['removed']===true){
                    $(button).parent().find('.deal-points i p').text(parseInt(points)-1)
                }else{
                    if(data['wasVoted']===true){
                        $(button).parent().find('.deal-points i p').text(parseInt(points)+2)
                    }
                    else{
                        $(button).parent().find('.deal-points i p').text(parseInt(points)+1)
                    }
                }
        })
}


function downvoteDeal(button,slug){
    $.ajax({
        url : '/api/v1/deals/'+slug+"/votes",
        type : 'PUT',
        dataType: "json",
        data: {"voteType":"downvote"}
    }).done( function(data) {
                console.log(data)
                points = $(button).parent().find('.deal-points i p').text()
                if(data['removed']===true){
                    $(button).parent().find('.deal-points i p').text(parseInt(points)+1)
                }else{
                    if(data['wasVoted']===true){
                        $(button).parent().find('.deal-points i p').text(parseInt(points)-2)
                    }
                    else{
                        $(button).parent().find('.deal-points i p').text(parseInt(points)-1)
                    }
                }
        })
}