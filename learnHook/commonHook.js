//定义新方法替换原方法
func_bk = func
//重写目标方法
func = function (arguments) {
    //my task;
    return old_func.apply(arguments)
}

//重写方法原型链抹去hook痕迹
func.prototype.func = func();

//对象属性hook方法
old_attr = obj.attr
Object.defineProperty(document, 'cookie', {
    set: function () {
        debugger;
        return;
    }


})

Object.defineProperty(window, 'cookie',
    {
        get: function () {
            debugger;
            return
        },
        set: function () {
            debugger;
            return;
        }

    }
)

//hook cookie
var cookie_cache = document.cookie;
    Object.defineProperty(document, 'cookie', {
        get: function() {
            console.log(cookie_cache);
            return cookie_cache;
        },
        set: function(val) {
            debugger;
            var cookie = val.split(";")[0];
            var ncookie = cookie.split("=");
            var flag = false;
            var cache = cookie_cache.split(";");
            cache = cache.map(function(a){
                if (a.split("=")[0] === ncookie[0]){
                    flag = true;
                    return cookie;
                }
                return a;
            })
            cookie_cache = cache.join(";");
            if (!flag){
                cookie_cache += cookie + ";";
            }
        },
    });