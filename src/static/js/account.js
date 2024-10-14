async function deleteAccount(id) {

    if(window.confirm('Are you sure you want to delete your account? This action is permanent.')) {

        response = await fetch(`http://127.0.0.1:5000/account/${id}`, {
            method: "DELETE"
        });

    }
}