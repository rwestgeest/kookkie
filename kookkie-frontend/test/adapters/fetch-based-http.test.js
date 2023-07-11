/**
 * @jest-environment jsdom
 */
import {FetchBasedHTTP} from "../../app/adapters/fetch-based-http";

describe(FetchBasedHTTP, () => {
    let http;
    beforeEach(() => {
        http = new FetchBasedHTTP();
        document.cookie.split("; ").forEach((c) => {
            document.cookie = c.trim().split('=')[0] + '=;' + 'expires=Thu, 01 Jan 1970 00:00:00 UTC;';
        });
    });

    describe('get', () => {
        beforeEach(() =>{
            global.fetch = jest.fn(() => Promise.resolve({
                status: 200,
                ok : true,
                json: () => Promise.resolve({some: "field"})
            }));
        });

        it('calls the fetch api', async () => {
            const response = await http.get('/api/foo');
            expect(global.fetch).toHaveBeenCalledWith('/api/foo', {
                headers: {
                    "Content-Type": "application/json",
                }
            });
        });

        it('takes a XSRF-TOKEN from a cookkie for a next requests header', async () => {
            setCookies("some-cookie=blah", "XSRF-TOKEN=the-token", "some-ohter-cookkie=blah");

            await http.get('/api/foo');

            expect(global.fetch).toHaveBeenCalledWith('/api/foo', {
                headers: {
                    "Content-Type": "application/json",
                    "X-Xsrf-Token": "the-token"
                }
            });
        });


        it('responds with a successful response with data when fetch is success', async () => {
            const response = await http.get('/api/foo');

            expect(response.status).toEqual(200);
            expect(response.data).toEqual({some: "field"});
        });

        it('rejects with data when fetch is failure', async () => {
            global.fetch = jest.fn(() => Promise.resolve({
                status: 401,
                ok : false,
                json: () => Promise.resolve({reason: "reason"})
            }));

            const error = await http.get('/api/foo').catch((e) => e);

            expect(error).toEqual({reason: "reason"});
        });
    });
    describe('post', () => {
        beforeEach(() =>{
            global.fetch = jest.fn(() => Promise.resolve({
                status: 200,
                ok : true,
                json: () => Promise.resolve({some: "field"})
            }));
        });

        it('calls the fetch api', async () => {
            await http.post('/api/foo', {some:"body"});
            expect(global.fetch).toHaveBeenCalledWith('/api/foo', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({some: "body"})
            });
        });
        it('passes the X-Xsrf header when XSRF_TOKEN is in the cookies', async () => {
            setCookies("some-cookie=blah", "XSRF-TOKEN=the-token", "some-ohter-cookkie=blah");
            await http.post('/api/foo', {some:"body"});
            expect(global.fetch).toHaveBeenCalledWith('/api/foo', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Xsrf-Token": "the-token"
                },
                body: JSON.stringify({some: "body"})
            });
        });
        it('responds with a successful response with data when fetch is success', async () => {
            const response = await http.post('/api/foo', {some:"body"});

            expect(response.status).toEqual(200);
            expect(response.data).toEqual({some: "field"});
        });
        it('rejects with data when fetch is success', async () => {
            global.fetch = jest.fn(() => Promise.resolve({
                status: 401,
                ok : false,
                json: () => Promise.resolve({reason: "reason"})
            }));

            const error = await http.post('/api/foo').catch((e) => e);

            expect(error).toEqual({reason: "reason"});
        });
    });

});
function setCookies(...cookies) {
    for (var cookie of cookies) {
        document.cookie = cookie;
    }
}