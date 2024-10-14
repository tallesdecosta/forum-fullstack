addEventListener('scrollend', () => {

    getPosts();
});

async function getPosts() {

    try {
        
        response = await fetch('/api/posts', {
            method: 'GET',
        }).then( (res) => {

            if (!res.ok) {

                return 'a';

            }

            return res.json();

        });

        console.log(response)

        if(response != 'none'){

            createPostsElements(response);
        }

        

    } catch (error) {

        displayError(error);
        throw(error);

    };

};


function createPostsElements(json) {

    
    for (item in json) {
        
        console.log(json)
        postsWrapper = document.getElementById("posts-wrapper");

        post = document.createElement("article");
        post.setAttribute('published', json[item].was_made);
        post.classList.add('post');  
        post.classList.add('flex');
        post.classList.add('justify-content-center');
        post.classList.add('gap-20px');
        postImage = document.createElement('img');
        postImage.src = `static/img/avatars/${json[item].image_path}`;
        postImage.classList.add('post-img');
        post.appendChild(postImage)
        console.log(postImage.src);
        
        post.appendChild(document.createElement('div'));
        infoWrapper = post.childNodes[1];
        infoWrapper.classList.add('flex');
        infoWrapper.classList.add('collumn');
        infoWrapper.classList.add('gap-20px');
        infoWrapper.appendChild(document.createElement('div'));
        infoWrapper.appendChild(document.createElement('div'));
        infoWrapper.appendChild(document.createElement('div'));

        titleWrapper = infoWrapper.childNodes[0];
        titleWrapper.classList.add('flex');
        titleWrapper.classList.add('justify-content-between');
        title = document.createElement('h2');
        title.textContent = json[item].title;
        avatar = document.createElement('img');
        titleWrapper.appendChild(title);
        avatar.src = `static/img/avatars/${json[item].image_path}`;
        avatar.classList.add('post-avatar');
        titleWrapper.appendChild(avatar);

        tagWrapper = infoWrapper.childNodes[1];
        
        
        tagWrapper.appendChild(document.createElement('button'));
        tagWrapper.appendChild(document.createElement('button'));
        tagWrapper.appendChild(document.createElement('button'));

        tagWrapper.childNodes[0].classList.add('tag');
        tagWrapper.childNodes[0].textContent = 'tag';

        tagWrapper.childNodes[1].classList.add('tag');
        tagWrapper.childNodes[1].textContent = 'tag';

        tagWrapper.childNodes[2].classList.add('tag');
        tagWrapper.childNodes[2].textContent = 'tag';

        metricsWrapper = infoWrapper.childNodes[2];
        metricsWrapper.classList.add('flex');
        metricsWrapper.classList.add('gap-30px');
        likes = document.createElement('p');
        comments = document.createElement('p');

        likes.textContent = `${json[item].likes} likes`;
        comments.textContent = `${json[item].comments} comments`;
        
        metricsWrapper.appendChild(likes);
        metricsWrapper.appendChild(comments);
        post.addEventListener('click', directPost)
        post.id = `${json[item].post_id}`
        postsWrapper.appendChild(post);
    }
};

function displayError(error) {

    console.log(error)

}

function showUserMenu() {

    menu = document.getElementById('menu');

    if (menu.classList.contains('open-menu')){

        document.getElementById('menu').classList.remove('open-menu');

    } else {

        document.getElementById('menu').classList.add('open-menu');

    }
    
}

function directPost() {

    post = document.getElementById(`${this.id}`);
    url = `http://127.0.0.1:5000/feed/post/${post.id}`;
    window.location.href = url; 
}

function desktopQuery(query) {
    
    newestBtn = document.getElementById('newest-btn');

    popular = document.getElementById('popular-btn');
    
    following = document.getElementById('following-btn');

    if (query.matches) { 

      newestBtn.childNodes[3].textContent = 'Newest and Recent'
      popular.childNodes[3].textContent = 'Popular of the day'

    } else {

       newestBtn.childNodes[3].textContent = 'Newest'
      popular.childNodes[3].textContent = 'Popular'

    }

  }
  
  // Create a MediaQueryList object
  var query = window.matchMedia("(min-width: 1440px)")
  
  desktopQuery(query)

  // Attach listener function on state changes
  query.addEventListener("change", function() {
    desktopQuery(query);
  });