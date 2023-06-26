import {FetchBasedHTTP} from "../../app/adapters/fetch-based-http";

describe(FetchBasedHTTP, () => {
    let http;
    beforeEach(() => {
        http = new FetchBasedHTTP();
    });
    describe('get', () => {
        it('responds with a successful response with data when fetch is success', async () => {
            global.fetch = jest.fn(() => Promise.resolve({
                status: 200,
                ok : true,
                json: () => Promise.resolve({some: "field"})
            }));

            const response = await http.get('/api/foo');

            expect(response.status).toEqual(200);
            expect(response.data).toEqual({some: "field"});
            expect(global.fetch).toHaveBeenCalledWith('/api/foo', {
                headers: {
                    "Content-Type": "application/json",
                }
            });
        });
        it('rejects with data when fetch is success', async () => {
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
        it('responds with a successful response with data when fetch is success', async () => {
            global.fetch = jest.fn(() => Promise.resolve({
                status: 200,
                ok : true,
                json: () => Promise.resolve({some: "field"})
            }));

            const response = await http.post('/api/foo', {some:"body"});

            expect(response.status).toEqual(200);
            expect(response.data).toEqual({some: "field"});
            expect(global.fetch).toHaveBeenCalledWith('/api/foo', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({some: "body"})
            });
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
