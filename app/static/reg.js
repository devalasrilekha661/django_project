console.log("reg form js file");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("reg_form").addEventListener("submit", function(e) {

    e.preventDefault();

    let r_user = {
        n: document.getElementById("name").value,
        e: document.getElementById("email").value,
        ph: document.getElementById("phNum").value,
        p: document.getElementById("password").value,
        cp: document.getElementById("c_password").value,
        r: document.getElementById("role").value
    };

    fetch("http://127.0.0.1:8000/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(r_user)
    })
    .then(res => res.json())
    .then(res => {
        console.log(res);
        alert(res.msg);
    })
    .catch(err => console.log(err));
});
