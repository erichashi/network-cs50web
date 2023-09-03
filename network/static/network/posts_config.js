document.addEventListener('DOMContentLoaded', () => {

    document.addEventListener('click', event => {
        const element = event.target

        //Edit Post
        if (element.className === 'edit-button') {
            try {
                const parent = element.parentElement

                parent.querySelector('#edit-container').style.display = 'flex'
                
                const content = parent.querySelector('#p-content-value').innerText;
                parent.querySelector('#edit-textarea').value = content

                parent.querySelector('#p-content').style.display = 'none';
                
                const id = parent.querySelector('#post-id').innerText;

                parent.querySelector('#save-button').addEventListener('click', async () => {

                    await fetch(`/api/posts/${id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            content: document.querySelector('#edit-textarea').value
                        })
                    })

                parent.querySelector('#p-content-value').innerHTML = parent.querySelector('#edit-textarea').value;
                
                parent.querySelector('#p-content').style.display = 'flex';

                parent.querySelector('#edit-container').style.display = 'none';

                })
                
            } catch (error) {console.log(error)}
            
        } 
        
        //Like Post
        else if (element.className === 'fa fa-heart' || element.className === 'fa fa-heart-o') {

            const parent = element.parentElement
            const id = parent.querySelector('#post-id').innerText;

            const l = parent.querySelector('span').innerText 
            const likes = parseInt(l)

            if(element.className === 'fa fa-heart'){
                element.className = 'fa fa-heart-o'
                like(id, likes - 1)

                parent.querySelector('span').innerText = likes - 1
                
            } else {
                element.className = 'fa fa-heart'
                like(id, likes + 1)
                parent.querySelector('span').innerText = likes + 1

            }
     
        }
    })
})

function like(id, value){
    return fetch(`/api/posts/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            likes: value
        })
    })
}


    


