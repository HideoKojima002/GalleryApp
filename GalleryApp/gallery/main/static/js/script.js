<script>
  $('#like_{{img_obj.id}}').click(function(){
           $.ajax({
                    type: "POST",
                    url: "{% url 'like-image' img_id=img_obj.id%}",
                    data: {'csrfmiddlewaretoken': '{{ csrf_token }}'},
                    dataType: "json",
                    success: function(response) {

                          let likeButton = $('#like_{{img_obj.id}}');
                          let likesCount = likeButton.find('.likes-count');
                          likesCount.text(response['likes_count']);

                     },
                     error: function(rs, e) {
                            alert(rs.responseText);
                     }
               });
  })
</script>