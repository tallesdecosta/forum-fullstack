

async function getPosts() {

    try {
        
        response = await fetch('http://127.0.0.1:5000/api/posts', {
            method: 'GET',
        }).then( (res) => {

            if (!res.ok) {

                return 'a';

            }

            return res.json();

        });
        console.log(response)
        createPostsElements(response);

    } catch (error) {

        displayError(error);
        throw(error);

    };

};

async function sendPost() {

    postContent = document.getElementById('post-content');

    response = await fetch('http://127.0.0.1:5000/api/posts', {

        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            title: `${postContent.value}`,
            content: `${postContent.value}`,
            user: `${username}`,
            datetime: `${new Date().toLocaleString()}`
        })
    }).then( (res) => {

        if (!res.ok) {

            throw new Error(`HTTP ERROR STATUS ${res.status}`);

        }

        return res.json();

    });

    console.log(response);

}

function createPostsElements(json) {

    
    for (item in json) {
        console.log(item)
        postsWrapper = document.getElementById("posts-wrapper");

        post = document.createElement("article");
        post.classList.add('post');
        post.classList.add('flex');
        post.classList.add('gap-20px');
        postImage = document.createElement('img');
        postImage.src = `static/img/${json[item].image_path}`;
        postImage.classList.add('post-img');
        post.appendChild(postImage);
        
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
        title = document.createElement('h3');
        title.textContent = json[item].title;
        avatar = document.createElement('img');
        titleWrapper.appendChild(title);
        avatar.src = json[item].avatar_path;
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