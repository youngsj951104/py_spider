function yt(t) {
    function e(t) {
        var e = t.replace(/\r\n/g, "\n");

        function i(t) {
            return String.fromCharCode(t)
        }

        for (var n = [], a = 0; a < e.length; a += 1) {
            var r = e.charCodeAt(a);
            r < 128 ? n.push(i(r)) : r > 2047 ? n.push(i(r >> 12 | 224), i(r >> 6 & 63 | 128), i(63 & r | 128)) : n.push(i(r >> 6 | 192), i(63 & r | 128))
        }
        return n.join("")
    }

    function i(t) {
        var e = t.length
            , i = 16 * ((e + 8 - (e + 8) % 64) / 64 + 1)
            , n = Array(i - 1)
            , a = 0;
        while (a <= e) {
            var r = (a - a % 4) / 4
                , c = a % 4 * 8
                , o = a === e ? 128 : t.charCodeAt(a);
            n[r] |= o << c,
                a += 1
        }
        return n[i - 2] = e << 3,
            n[i - 1] = e >>> 29,
            n
    }

    function n(t, e) {
        return t << e | t >>> 32 - e
    }

    function a(t, e) {
        var i = 2147483648 & t
            , n = 2147483648 & e
            , a = 1073741824 & t
            , r = 1073741824 & e
            , c = (1073741823 & t) + (1073741823 & e);
        return a & r ? 2147483648 ^ c ^ i ^ n : a | r ? 1073741824 & c ? 3221225472 ^ c ^ i ^ n : 1073741824 ^ c ^ i ^ n : c ^ i ^ n
    }

    function r(t) {
        var e = t.FN
            , i = t.a
            , r = t.b
            , c = t.c
            , o = t.d
            , s = t.x
            , l = t.s
            , A = t.ac
            , u = a(i, a(a(e(r, c, o), s), A));
        return a(n(u, l), r)
    }

    function c(t) {
        for (var e = "", i = 0; i <= 3; i += 1) {
            var n = t >>> 8 * i & 255
                , a = "0".concat(n.toString(16));
            e += a.substr(a.length - 2, 2)
        }
        return e
    }

    var o = 1732584193
        , s = 4023233417
        , l = 2562383102
        , A = 271733878
        , u = [[7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]]
        , d = "16b05af49e38d27c58be147ad0369cf207e5c3a18f6d4b29".split("").map((function (t) {
                return parseInt(t, 16)
            }
        ))
        ,
        h = [3614090360, 3905402710, 606105819, 3250441966, 4118548399, 1200080426, 2821735955, 4249261313, 1770035416, 2336552879, 4294925233, 2304563134, 1804603682, 4254626195, 2792965006, 1236535329, 4129170786, 3225465664, 643717713, 3921069994, 3593408605, 38016083, 3634488961, 3889429448, 568446438, 3275163606, 4107603335, 1163531501, 2850285829, 4243563512, 1735328473, 2368359562, 4294588738, 2272392833, 1839030562, 4259657740, 2763975236, 1272893353, 4139469664, 3200236656, 681279174, 3936430074, 3572445317, 76029189, 3654602809, 3873151461, 530742520, 3299628645, 4096336452, 1126891415, 2878612391, 4237533241, 1700485571, 2399980690, 4293915773, 2240044497, 1873313359, 4264355552, 2734768916, 1309151649, 4149444226, 3174756917, 718787259, 3951481745];

    function g(t) {
        var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0;
        return (t + e) % 4
    }

    function v(t, e, i) {
        return t & e | ~t & i
    }

    function b(t, e, i) {
        return t & i | e & ~i
    }

    function p(t, e, i) {
        return t ^ e ^ i
    }

    function f(t, e, i) {
        return e ^ (t | ~i)
    }

    var m = e(t)
        , y = i(m);

    function I(t) {
        var e = o
            , i = s
            , n = l
            , c = A
            , m = [o, A, l, s];
        h.forEach((function (e, i) {
                var n = i % 16
                    , a = i / 16 << 0
                    , c = i < 16 ? i : d[i - 16]
                    , o = [v, b, p, f][a];
                m[g(n)] = r({
                    FN: o,
                    a: m[g(n)],
                    b: m[g(n, 3)],
                    c: m[g(n, 2)],
                    d: m[g(n, 1)],
                    x: y[t + c],
                    s: u[a][n % 4],
                    ac: e
                })
            }
        )),
            o = a(m[0], e),
            s = a(m[3], i),
            l = a(m[2], n),
            A = a(m[1], c)
    }

    for (var E = 0; E < y.length; E += 16)
        I(E);
    return (c(o) + c(s) + c(l) + c(A)).toLowerCase()
}

function getSign(pts) {
    var i = "7hfsyhGFDSJh28sh';d3hfsf8jgkkaoctai.qq.com"
    var l = yt(pts + i)
    return l
}