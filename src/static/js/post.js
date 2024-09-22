async function loadPost() {
    
    response = fetch('http://127.0.0.1:5000/api/posts/', {
        method: 'GET',
    })

}