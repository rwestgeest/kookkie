

export class FetchBasedHTTP {
    async get(url) {
        const response = {}
        const fetchResponse = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                "X-Xsrf-Token": xsrf_token_from_cookie()
            }
        });
        if (!fetchResponse.ok) {
            const data = await fetchResponse.json()
            throw (data);
        }
        response.status = fetchResponse.status;
        response.data = await fetchResponse.json();
        return response;
    }

    async post(url, body) {
        const response = {}
        console.log(document.cookie);
        const fetchResponse = await fetch(url, {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                "Content-Type": "application/json",
                "X-Xsrf-Token": xsrf_token_from_cookie()
            }
        });
        if (!fetchResponse.ok) {
            const data = await fetchResponse.json()
            throw (data);
        }
        response.status = fetchResponse.status;
        response.data = await fetchResponse.json();
        return response;
    }

}

function xsrf_token_from_cookie() {
    const token = document.cookie
        .split("; ")
        .find(row => row.startsWith("XSRF-TOKEN="))
        ?.split("=")[1];
    return token;
}