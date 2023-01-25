$('#like').click(function(){
      $.ajax({
               type: "POST",
               url: "{% url 'like-image' img_id=img_obj.id%}",
               data: {'csrfmiddlewaretoken': '{{ csrf_token }}'},
               dataType: "json",
               success: function(response) {
                      alert(response.message);
                      alert('Сейчас лайков ' + response.likes_count);
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    })