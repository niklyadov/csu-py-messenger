const login = (() => {

    let that = {}
    const TOKEN = "Bearer"

    that.getLoggedUser = async () => {
        const currentToken = localStorage.getItem(TOKEN)
        return await fetch('/user/', {method: 'GET', headers: { Authorization: `Bearer ${currentToken}` }})
                .then(response => {
                    if (response.ok) {
                        let data = response.json()

                        localStorage.setItem("USER_ID", data.id)
                        localStorage.setItem("USER_NAME", data.name)
                        localStorage.setItem("USER_LOGIN", data.login)
                        return data
                    } else {
                        console.error(response);
                        return null;
                    }
                })
    }

    that.authorize = async (login, password) => {
        const formData = new FormData();
            formData.append('username', login);
            formData.append('password', password);

        return await fetch('/auth/login/', {method: 'POST', body: formData})
            .then(r => r.json())
            .then(data => {
                localStorage.setItem(TOKEN, data.access_token)
                return true;
            });
    }

    that.requestLoginAndPassword = async () => {
        let login = prompt("Login:", "test");
        let password = prompt("Password", "test");

        if(!!login && !!password && await that.authorize(login, password)) {
            
            alert("Success login!");
            return true;

        } else {

            alert("Incorrect login or password");
            return false;
        }
    }

    return {
        getLoggedUser: () => that.getLoggedUser(),
        isAuthorized: () => !!that.getLoggedUser(),
        requestLoginAndPasswordIfNotLoggedIn: async () => {
            let loggedUser = await that.getLoggedUser();
            if(!!loggedUser) {
                return true;
            }

            return await that.requestLoginAndPassword();;
        },
        logout: () => {
            localStorage.removeItem(TOKEN)
        }
    }

})();