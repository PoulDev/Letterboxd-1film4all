let users = [];

const options = {
    root: null,
    rootMargin: '800px',
    threshold: 0
};

function addUser() {
    var username = document.getElementById("username").value;
    var userlist = document.getElementById("usernames");
    document.getElementById("username").value = "";

    var div = document.createElement("div");
    div.className = "user";

    var text = document.createElement("p");
    text.innerHTML = username;

    var remove = document.createElement("button");
    remove.innerHTML = `<i class="fa fa-trash"></i>`;
    remove.className = "remove";
    remove.onclick = function() {
        div.remove();
        users.splice(users.indexOf(username), 1);
    }

    div.appendChild(text);
    div.appendChild(remove);
    userlist.appendChild(div);
    users.push(username);
}

function submit() {
    localStorage.setItem("users", JSON.stringify(users));
    window.location.href = "/letterbox";
}

function loadTierlist() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (!entry.target.style.backgroundImage) {
                    fetch(`/film/${entry.target.data.id}/poster`)
                        .then(response => response.json())
                        .then(data => {
                            entry.target.style.backgroundImage = `url(${data.url2x})`;
                            entry.target.style.backgroundSize = "cover";
                            entry.target.style.backgroundPosition = "center";
                            entry.target.style.backgroundRepeat = "no-repeat";

                        })
                }
                console.log('Element is visible!', entry.target.data);
            }
        });
    }, options);


    users = JSON.parse(localStorage.getItem("users"))
    fetch("/letterbox", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ names: users })
    })
        .then(response => response.json())
        .then(data => {
            var tierlist = document.getElementById("tierlist");
            tierlist.innerHTML = "";
            for (var i = 0; i < data.length; i++) {
                if (data[i].length == 0) continue;
                var div = document.createElement("div");
                div.className = "tier";
                div.innerHTML = `<h2>Watched by ${i} users</h2>`;
                for (var j = 0; j < data[i].length; j++) {
                    if (data[i][j].length == 0) continue;
                    var div2 = document.createElement("div");
                    div2.className = "filmsRow";

                    var title = document.createElement("h3");
                    title.innerHTML = `${users.length - j} users want to watch those films`;

                    for (var k = 0; k < data[i][j].length; k++) {
                        var link = document.createElement("a");
                        link.target = "_blank";
                        link.href = `https://letterboxd.com/film/${data[i][j][k].id}`;

                        var film = document.createElement("div");
                        film.data = data[i][j][k];
                        film.className = "film";

                        var text = document.createElement("p");
                        text.innerText = data[i][j][k].name;

                        film.appendChild(text);

                        link.appendChild(film);
                        div2.appendChild(link);

                        observer.observe(film);
                    }
                    div.appendChild(title);
                    div.appendChild(div2);
                }
                tierlist.appendChild(div);
            }

            console.log(data);
        })
}
