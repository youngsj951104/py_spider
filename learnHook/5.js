// ==UserScript==
// @name         scu.edu
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http://scu.edu.cn/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    function SekiroClient(wsURL) {
        this.wsURL = wsURL;
        this.handlers = {};
        this.socket = {};
        this.base64 = false;
        // check
        if (!wsURL) {
            throw new Error('wsURL can not be empty!!')
        }
        this.webSocketFactory = this.resolveWebSocketFactory();
        this.connect()
    }

    SekiroClient.prototype.resolveWebSocketFactory = function () {
        if (typeof window === 'object') {
            var theWebSocket = window.WebSocket ? window.WebSocket : window.MozWebSocket;
            return function (wsURL) {

                function WindowWebSocketWrapper(wsURL) {
                    this.mSocket = new theWebSocket(wsURL);
                }

                WindowWebSocketWrapper.prototype.close = function () {
                    this.mSocket.close();
                };

                WindowWebSocketWrapper.prototype.onmessage = function (onMessageFunction) {
                    this.mSocket.onmessage = onMessageFunction;
                };

                WindowWebSocketWrapper.prototype.onopen = function (onOpenFunction) {
                    this.mSocket.onopen = onOpenFunction;
                };
                WindowWebSocketWrapper.prototype.onclose = function (onCloseFunction) {
                    this.mSocket.onclose = onCloseFunction;
                };

                WindowWebSocketWrapper.prototype.send = function (message) {
                    this.mSocket.send(message);
                };

                return new WindowWebSocketWrapper(wsURL);
            }
        }
        if (typeof weex === 'object') {
            // this is weex env : https://weex.apache.org/zh/docs/modules/websockets.html
            try {
                console.log("test webSocket for weex");
                var ws = weex.requireModule('webSocket');
                console.log("find webSocket for weex:" + ws);
                return function (wsURL) {
                    try {
                        ws.close();
                    } catch (e) {
                    }
                    ws.WebSocket(wsURL, '');
                    return ws;
                }
            } catch (e) {
                console.log(e);
                //ignore
            }
        }
        //TODO support ReactNative
        if (typeof WebSocket === 'object') {
            return function (wsURL) {
                return new theWebSocket(wsURL);
            }
        }
        // weex ?????? PC???????????????ebsocket API??????????????????????????????????????????????????????????????????
        throw new Error("the js environment do not support websocket");
    };

    SekiroClient.prototype.connect = function () {
        console.log('sekiro: begin of connect to wsURL: ' + this.wsURL);
        var _this = this;
        // ??????heck close?????????
        // if (this.socket && this.socket.readyState === 1) {
        //     this.socket.close();
        // }
        try {
            this.socket = this.webSocketFactory(this.wsURL);
        } catch (e) {
            console.log("sekiro: create connection failed,reconnect after 2s");
            setTimeout(function () {
                _this.connect()
            }, 2000)
        }

        this.socket.onmessage(function (event) {
            _this.handleSekiroRequest(event.data)
        });

        this.socket.onopen(function (event) {
            console.log('sekiro: open a sekiro client connection')
        });

        this.socket.onclose(function (event) {
            console.log('sekiro: disconnected ,reconnection after 2s');
            setTimeout(function () {
                _this.connect()
            }, 2000)
        });
    };

    SekiroClient.prototype.handleSekiroRequest = function (requestJson) {
        console.log("receive sekiro request: " + requestJson);
        var request = JSON.parse(requestJson);
        var seq = request['__sekiro_seq__'];

        if (!request['action']) {
            this.sendFailed(seq, 'need request param {action}');
            return
        }
        var action = request['action'];
        if (!this.handlers[action]) {
            this.sendFailed(seq, 'no action handler: ' + action + ' defined');
            return
        }

        var theHandler = this.handlers[action];
        var _this = this;
        try {
            theHandler(request, function (response) {
                try {
                    _this.sendSuccess(seq, response)
                } catch (e) {
                    _this.sendFailed(seq, "e:" + e);
                }
            }, function (errorMessage) {
                _this.sendFailed(seq, errorMessage)
            })
        } catch (e) {
            console.log("error: " + e);
            _this.sendFailed(seq, ":" + e);
        }
    };

    SekiroClient.prototype.sendSuccess = function (seq, response) {
        var responseJson;
        if (typeof response == 'string') {
            try {
                responseJson = JSON.parse(response);
            } catch (e) {
                responseJson = {};
                responseJson['data'] = response;
            }
        } else if (typeof response == 'object') {
            responseJson = response;
        } else {
            responseJson = {};
            responseJson['data'] = response;
        }


        if (Array.isArray(responseJson)) {
            responseJson = {
                data: responseJson,
                code: 0
            }
        }

        if (responseJson['code']) {
            responseJson['code'] = 0;
        } else if (responseJson['status']) {
            responseJson['status'] = 0;
        } else {
            responseJson['status'] = 0;
        }
        responseJson['__sekiro_seq__'] = seq;
        var responseText = JSON.stringify(responseJson);
        console.log("response :" + responseText);


        if (responseText.length < 1024 * 6) {
            this.socket.send(responseText);
            return;
        }

        if (this.base64) {
            responseText = this.base64Encode(responseText)
        }

        //???????????????????????????????????
        var segmentSize = 1024 * 5;
        var i = 0, totalFrameIndex = Math.floor(responseText.length / segmentSize) + 1;

        for (; i < totalFrameIndex; i++) {
            var frameData = JSON.stringify({
                    __sekiro_frame_total: totalFrameIndex,
                    __sekiro_index: i,
                    __sekiro_seq__: seq,
                    __sekiro_base64: this.base64,
                    __sekiro_is_frame: true,
                    __sekiro_content: responseText.substring(i * segmentSize, (i + 1) * segmentSize)
                }
            );
            console.log("frame: " + frameData);
            this.socket.send(frameData);
        }
    };

    SekiroClient.prototype.sendFailed = function (seq, errorMessage) {
        if (typeof errorMessage != 'string') {
            errorMessage = JSON.stringify(errorMessage);
        }
        var responseJson = {};
        responseJson['message'] = errorMessage;
        responseJson['status'] = -1;
        responseJson['__sekiro_seq__'] = seq;
        var responseText = JSON.stringify(responseJson);
        console.log("sekiro: response :" + responseText);
        this.socket.send(responseText)
    };

    SekiroClient.prototype.registerAction = function (action, handler) {
        if (typeof action !== 'string') {
            throw new Error("an action must be string");
        }
        if (typeof handler !== 'function') {
            throw new Error("a handler must be function");
        }
        console.log("sekiro: register action: " + action);
        this.handlers[action] = handler;
        return this;
    };

    SekiroClient.prototype.encodeWithBase64 = function () {
        this.base64 = arguments && arguments.length > 0 && arguments[0];
    };

    SekiroClient.prototype.base64Encode = function (s) {
        if (arguments.length !== 1) {
            throw "SyntaxError: exactly one argument required";
        }

        s = String(s);
        if (s.length === 0) {
            return s;
        }

        function _get_chars(ch, y) {
            if (ch < 0x80) y.push(ch);
            else if (ch < 0x800) {
                y.push(0xc0 + ((ch >> 6) & 0x1f));
                y.push(0x80 + (ch & 0x3f));
            } else {
                y.push(0xe0 + ((ch >> 12) & 0xf));
                y.push(0x80 + ((ch >> 6) & 0x3f));
                y.push(0x80 + (ch & 0x3f));
            }
        }

        var _PADCHAR = "=",
            _ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
            _VERSION = "1.1";//Mr. Ruan fix to 1.1 to support asian char(utf8)

        //s = _encode_utf8(s);
        var i,
            b10,
            y = [],
            x = [],
            len = s.length;
        i = 0;
        while (i < len) {
            _get_chars(s.charCodeAt(i), y);
            while (y.length >= 3) {
                var ch1 = y.shift();
                var ch2 = y.shift();
                var ch3 = y.shift();
                b10 = (ch1 << 16) | (ch2 << 8) | ch3;
                x.push(_ALPHA.charAt(b10 >> 18));
                x.push(_ALPHA.charAt((b10 >> 12) & 0x3F));
                x.push(_ALPHA.charAt((b10 >> 6) & 0x3f));
                x.push(_ALPHA.charAt(b10 & 0x3f));
            }
            i++;
        }


        switch (y.length) {
            case 1:
                var ch = y.shift();
                b10 = ch << 16;
                x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 0x3F) + _PADCHAR + _PADCHAR);
                break;

            case 2:
                var ch1 = y.shift();
                var ch2 = y.shift();
                b10 = (ch1 << 16) | (ch2 << 8);
                x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 0x3F) + _ALPHA.charAt((b10 >> 6) & 0x3f) + _PADCHAR);
                break;
        }

        return x.join("");
    };

    function guid() {
        function S4() {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        }

        return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
    }

    var client = new SekiroClient("ws://localhost:5603/websocket?group=rs&clientId=" + guid());
    client.registerAction("Match10_getdata", function (request, resolve, reject) {
        var url = "/api/challenge5";
        call = function (num) {
            var list = {
                "page": request['page'],
                "token": window.token,
            };
            $.ajax({
                url: url,
                dataType: "json",
                async: true,
                data: list,
                type: "POST",
                beforeSend: function (request) {
                    (function () {
                        var httpRequest = new XMLHttpRequest();
                        var url = '/cityjson';
                        httpRequest.open('POST', url, false);
                        httpRequest.send()
                    })()
                },
                success: function (data) {
                    window[data.k['k'].split('|')[0]] = parseInt(data.k['k'].split('|')[1]);
                    var s = '<tr class="odd">';
                    datas = data.data;
                    resolve(datas)
                    $.each(datas, function (index, val) {
                        var html = '<td class="info">' + val.value + '</td>';
                        s += html
                    });
                    $('.data').text('').append(s + '</tr>')
                },
                complete: function () {
                    $("#page").paging({
                        nowPage: num,
                        pageNum: 100,
                        buttonNum: 7,
                        canJump: 1,
                        showOne: 1,
                        callback: function (num) {
                            call(num)
                        },
                    })
                },
                error: function () {
                    alert('???????????????')
                    location.reload()
                }
            })
        };
        call(1)
    });
})();