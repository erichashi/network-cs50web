document.addEventListener('DOMContentLoaded', function() {
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#compose-content').value
        })
    })
    .then(response => response.json())
    .then(() => {
        load_all()
    })

    // Use buttons to toggle between views
    document.querySelector('#all-posts-button').addEventListener('click', () => load_all);
    
});

//views in index.html: id="all-post-view",  id="edit-view" id="new-post-view"

function load_all(){
  document.querySelector('#all-post-view').style.display = 'block';
  document.querySelector('#edit-view').style.display = 'none';
 
  document.querySelector('#compose-content').value = '';

  fetch(`/posts/all`)
  .then(response => response.json())
  .then(posts => {
    //posts is an arrany of post objects

    posts.forEach(current => {
      const poster = current.poster
      const content = current.content
      const timestamp = current.timestamp
      const likes = current.likes

      
      const post = document.createElement('div')
      post.className = 'post'
      
      
      post.innerHTML = `<strong>${poster}</strong>  ${content} ${likes} Likes <scan class='time'>${timestamp}</scan>` 
      document.querySelector('#all-post-view').append(post)
    })
    
  })
}

function compose_post(){
    document.querySelector('form').onsubmit = function() {
        fetch('/posts', {
          method: 'POST',
          body: JSON.stringify({
              content: document.querySelector('#compose-content').value
          })
        })
        .then(response => response.json())
        .then(() => {
          load_all()
        })
    }
}