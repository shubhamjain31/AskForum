// For adding new question
  $("#questionbtn").on('click',function(e){
  $("#question").empty();
  questionValue = document.getElementById('question').value;

  $.ajax({
        method:'POST',
        url:'/askaquestion/',

        data:{
          questionValue:questionValue,
        },
        success:function(e){
          
        },
        error:function(e){
          console.log("Fail");
        }
    });
});


//  for votes on questions
function votes(val){
  if (!is_flag().Result){
    alert('You need to login before voting')
  }
  else{
  var res = val.split("--");
  console.log(res);
  $.ajax({
    method:'POST',
    url:'/vote/',

    data:{
      questionId : res[1],
      action : res[0],
    },
    success:function(e){
      if(!e.flag){
        alert(e.Response);
      }
      else{
      $('#'+res[1]).html(parseInt($('#'+res[1]).html()) + parseInt(e.count))
      alert(e.Response);
      }
      
    },
    error:function(e){
      console.log("Fail");
    }
});
  } // else ends
}

// for answer votes

$('.vote').on('click',function(e){
  if (!is_flag().Result){
    alert('You need to login before voting')
  }
  else{
  var answerId = $(this).attr("data-href");
    console.log($(this).attr("name"),answerId);

  $.ajax({
    method:'POST',
    url:'/answervote/',
    data:{
      questionId:$(this).attr("data-value"),
      answerId:answerId,
      action:$(this).attr("name"),
    },
    success:function(e){
      if(!e.flag){
        alert(e.Response);
      }
      else{      
      $('#'+answerId).html(parseInt($('#'+answerId).html()) + parseInt(e.count))
      alert(e.Response);
      }
    },
    error:function(e){
      console.log('error')
    }
  })

 }
})


function is_flag(){
  var result = false;
  $.ajax({
    method:'POST',
    url:'/sessionval/',
    data:{},
    async: false,
    success:function(e){
      result = e;
    },
    error:function(e){
      console.log('error',e)
    }
  })
  return result;
}

// for validating question modal with session
$('#questionModalButton').on('click',function(e){
  // console.log(is_flag(result))
  if (!is_flag().Result){
    alert('Please Login to Continue!');
  }
  else{
    $('#exampleModalCenter').modal('show');
  }
})
  

// for validating answer textarea // form submit only with some valid value
$('#answerbtn').on('click',function(e){
  
  if(!$('#answertext').val().replace(/\s/g, "").length){
    alert('Answer Cannot be Blank');
    e.preventDefault();
  }
  else{
    if (is_flag()){
    $('#answersubmit').submit();
    }
    else{ 
      alert('Please login before answering.')
      e.preventDefault();
    }
    
  }
})

// "Answer" button show and hide
$("#answertext").keyup(function(){
  if(!$(this).val().replace(/\s/g, "").length){
    document.getElementById('answerbtn1').style.display = 'none';
  console.log("blank");
  }
  else{
    console.log($(this).val());
    document.getElementById('answerbtn1').style.display = 'block';
  }
});