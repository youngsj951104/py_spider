function getToken(num) {
    t=Date.parse(new Date())/1000
    CryptoJS = require('crypto-js')
    var window = global
    window.k = 'wdf2ff*TG@*(F4)*YH)g430HWR(*)' + 'wse';
    window.m = CryptoJS.enc.Utf8.parse(window.k);
    a = function (word) {
        var srcs = CryptoJS.enc.Utf8.parse(word);
        var encrypted = CryptoJS.AES.encrypt(srcs, window.m, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        return encrypted.toString();
    }
    window.s = a(t + '|' + num);
    window.a = window.s;
    return window.a
}
token=getToken(1)
console.log(token)