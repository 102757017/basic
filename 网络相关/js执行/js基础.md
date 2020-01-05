# 基础

## 时间戳

```
// 时间戳转本地时间
var time2 = new Date().toLocaleString()
console.log(time2)

// 生成时间戳2 
var time3 = Date.now()
console.log(time3)
```

输出结果

```
"Sun Jan 05 2020 19:22:20 GMT+0800 (中国标准时间)"

1578223264041
```



## 布尔值

> 默认 False 有：**`false` `undefuned` `null` `0` `-0` `NaN` `''` 空字符串**

## 定义变量

变量必须以字母开头
变量也能以 $ 和 _ 符号开头
在 JavaScript 中函数就是变量

```
// str
var str1 = JSON.stringify({x:2})
console.log(str1)
```

> 多个变量同时赋值, 以**逗号**分隔，分号结尾

```
var a = 'hi', b = 1+2,c
// 格式化之后可能显示为, 在; 号为一句的结尾
var a = 'hi',
b = 1 + 2
,c;
console.log(a,b,c)
```

输出结果

```
{“x”:2}

hi 3 undefined

1
```

> 变量补充定义, 将会以最后一次定义为准

```
var a ='';
var a= 1;
console.log(a)
// 输出 1
// var 是局部变量, 不设置 var 就是全局变量
```

> 尾部补充定义, 因为是解释性语言可以这样操作的

```
console.log(w)
var w = '这是w'
console.log(w)
	
// 作用域
function test(){
	var k = '作用域测试';
	function abc(){
		console.log(k)
	}
	abc();
}
```

## jothor编码

> jothor编码 利用 js 弱类型进行转换

-  \+ 号会是一个弱类型转换, 比如 str + int 就会将int 强制转换为 str
-  [] 就会被强制转换为0, 从而得到想要的类型

```
var s = +[];
console.log('jothor编码', s)
// 输出 jothor编码 0
```

## =  赋值

## ==  会自动转换类型并比较

## === 绝对等于（值和类型均相等）

## !== 不绝对等于（值和类型有一个不相等，或两个都不相等）

> 赋值 一个 = 号只代表赋值操作

```
var a = 0, b = 1;
if (a=b){
	console.log('一个 = 号只代表赋值操作编码')
}
	
// == 与 === 
if(1=='1'){
	console.log('== 会自动转换类型并比较')
}
	
if(1===1){
	console.log('=== 不会自动转换类型并比较')
```

```
一个 = 号只代表赋值操作编码
== 会自动转换类型并比较
=== 不会自动转换类型并比较
```

## 逻辑运算符

> `&&` 与
>
> || 或
>
> ！非

**注意: || 或的时候,遇到 false值会跳过,直到遇到第一个为true的值并返回，如果都为false返回最后一个,如下:**

```
var u;
var b = u || 0 || "" || 100 || 200;
console.log(b)
// && 与: 遇到 false 就返回
var i = 100 && 0 && 200;
console.log(i)
var a = 0;
(1 == 1) && (a = 100);  // 这种情况 相当于是一个如果真
console.log(a)
```

```
100
0
100
```

## 三元运算

```
var a = 100;
a ? console.log('真'): console.log('假')
// 输出 真
```

## 对象

| 对象       | 例子                        |
| :--------- | :-------------------------- |
| 内置对象   | `数组` `函数` `日期`        |
| 宿主对象   | `DOM` `Windows` `navigator` |
| 自定义对象 | `{}` 或者 `new Object`      |

> 继承属性 Object.prototype 最顶层的原型对象,所有对象都会继承的.包括内置对象也会继承.

```
Object.prototype.x2 = 100
var obj = {x:1,y:2};
console.log(obj.x2)
// 输出 100
```

# 编码

## escape

> **`escape()`** 函数可对字符串进行编码，这样就可以在所有的计算机上读取该字符串。

该方法不会对 ASCII 字母和数字进行编码，也不会对下面这些 ASCII 标点符号进行编码： `* @ - _ + . / 。` 其他所有的字符都会被转义序列替换。

例如

```
>escape ('hello 这文被转换')
<"hello%20%u8FD9%u6587%u88AB%u8F6C%u6362"
>unescape("hello%20%u8FD9%u6587%u88AB%u8F6C%u6362")
<"hello 这文被转换"
```

解码： **`unescape()`**

## encodeURIComponent URL 编码

-  编码 `encodeURIComponent()`
-  解码 `decodeURIComponent()`

```
>encodeURIComponent("https://blog.zhangkunzhi.com/语法基础")
<"https%3A%2F%2Fblog.zhangkunzhi.com%2F%E8%AF%AD%E6%B3%95%E5%9F%BA%E7%A1%80"
>decodeURIComponent("https%3A%2F%2Fblog.zhangkunzhi.com%2F%E8%AF%AD%E6%B3%95%E5%9F%BA%E7%A1%80")
<"https://blog.zhangkunzhi.com/语法基础"
```



# DOM元素控制

向 id="demo" 的 HTML 元素输出文本 "你好 Dolly" ：

```
document.getElementById("demo").innerHTML = "你好 Dolly";
```



# 引用外部index.js文件

```
<script src="index.js"></script>
 <script>
    window.onload = function(){
        aa();    //调用index.js中的aa函数
    }</script>
```

# 引用 jQuery库

<script src="http://apps.bdimg.com/libs/jquery/2.1.1/jquery.min.js">
jQuery 语法是通过选取 HTML 元素，并对选取的元素执行某些操作。
jQuery基础语法： $(selector).action()

```
$("#id")            //ID选择器， 选取id="id"的元素
$("div")            //元素选择器 选取所有<div>标签的元素
$(".classname")     //类选择器  选取class="classname"的元素
$(".classname,.classname1,#id1")     //组合选择器
$(this)				//选取当前 HTML 元素
```

更多实例查询http://www.runoob.com/jquery/jquery-selectors.html

```
$(document).ready(function(){
   // 这是为了防止文档在完全加载（就绪）之前运行 jQuery 代码，即在 DOM 加载完成后才可以对 DOM 进行操作。
});
```



# jQuery-AJAX

jQuery-AJAX是与服务器交换数据的技术，它在不重载全部页面的情况下，实现了对部分网页的更新。

```
$.get(URL,callback)
	URL 参数规定您希望请求的 URL
	callback 参数是请求成功后所执行的函数名

$.getJSON()

$.post(URL,data,callback);
```