export class FetchBasedHTTP {
    async get(url) {
        const response = {}
        const fetchResponse = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
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
        const fetchResponse = await fetch(url, {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                "Content-Type": "application/json",
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