/*
*/

chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    return {redirectUrl: chrome.extension.getURL("js/pk.js")}; //是你要替换的js脚本
  },
  {
    urls: ["https://www.seagame.com/mxj/js/pk.js?ver=2.34"],  //你要拦截的url地址
    types: ["script"]       //拦截类型为script，
  },
  ["blocking"] //类型blocking为拦截,
);

chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    return {redirectUrl: chrome.extension.getURL("js/bbs.js")}; //是你要替换的js脚本
  },
  {
    urls: ["https://www.seagame.com/mxj/js/bbs.js?ver=2.34"],  //你要拦截的url地址
    types: ["script"]       //拦截类型为script，
  },
  ["blocking"] //类型blocking为拦截,
);