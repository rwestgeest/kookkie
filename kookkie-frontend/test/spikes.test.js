describe('spikes',  () => {
    class Base {
        foo(...params) {
            this.params = params;
            return this;
        }
    }

    describe('variable parameters', () => {
        it('is an object', () => {
            expect(new Base().foo(1,2,'three').params).toEqual([1, 2, "three"])
        });
        it('can be mocre concrete in override', () => {
            class Sub extends Base {
                foo(first, second) {
                    this.params = {first, second};
                    return this;
                }
            }
            expect(new Sub().foo(1,'two').params).toEqual({first : 1, second: "two"});
        });
        it('can pass them on to super', () => {
            class Sub2 extends Base {
                foo(first, second) {
                    super.foo(first, second)
                    return this;
                }
            }
            expect(new Sub2().foo(1,'two').params).toEqual([1, "two"]);
        });
    });
    describe('regular path expressions', () => {
        it ('replaces parameters with regexp parts', () => {
            const pathSpec = "#/foo/bar/:id/:name"
            const params = []
            const pathExp = pathSpec.replace(/:(\w+)/g, (match, param) => {
                params.push(param);
                return '([^\\/]+)'
            }).replace(/\//g, '\\/')
            expect(pathExp).toEqual('#\\/foo\\/bar\\/([^\\\\/]+)\\/([^\\\\/]+)')
            expect(params).toEqual(['id', 'name'])
        });
        it ('matches passed paramters', () => {
            const match = "#/foo/bar/some-id/some-name".match(new RegExp('#\\/foo\\/bar\\/([^\\\\/]+)/([^\\\\/]+)'))
            match.shift();
            expect(match.map((e) => e)).toEqual(['some-id', 'some-name'])
        });
    });
});