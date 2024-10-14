async function sendPost(user) {

    postTitle = document.getElementById('post-title');
    postContent = document.getElementById('post-content');
    data = new Date().toLocaleString().replace('/', '-').replace('/', '-').replace(',', '')
    response = await fetch('http://127.0.0.1:5000/api/posts', {

        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            title: `${postTitle.value}`,
            content: `${postContent.value}`,
            user: `${user}`,
            datetime: `${data}`
        })
    }).then( (res) => {

        if (!res.ok) {

            throw new Error(`HTTP ERROR STATUS ${res.status}`);

        }

        return res.json();

    });

    console.log(response);

}