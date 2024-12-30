const $=(element)=>document.querySelector(element),
    getId=(element)=>document.getElementById(element),
    attr=(element,attribute)=>element.getAttribute(attribute),
    _ = null,
    menu = $('nav'),
    search = $('search'),
    btnAdd = $('.add2OrderBtn'),
    orders = getId('ordersBtn'),
    toast = getId('toast')
function resizeElementElement(element,width,height=null){
    element.style.width=`${width}px`
    if(height)element.style.height=`${height}px`
}

function toggleVisibility(element){
    // console.log(
        // document.querySelectorAll('menu,search')
    // );
    // let elementIsVisible =
    // element.style.display = 
    // console.log(window.getComputedStyle(menu).display)
    // attr(menu,'display')
    // element.style.display='flex'
}
function changeSize(element){
    const sizes = {
        search: {
            minWidth: 50,
            minHeight: 50,
            maxWidth: 300,
            maxHeight: 50,
        },
        menu: {
            minWidth: 50,
            minHeight: 50,
            maxWidth: 300,
            maxHeight: 300,
        }
    }
    // let el = 'menu';
    // console.log(sizes[el].maxHeight);
    // let a = parseFloat(window.getComputedStyle(menu).width);
    // console.log(sizes[el].minHeight);
    // console.log(parseFloat(window.getComputedStyle(menu).width));
    // console.log(menu);
    // if(attr(menu,'width')==='opened'){console.log('is open')}
    // else console.log(('closed'));
}
function createOrder(){
    console.log('create')
    showToast('saved','success')
}
function editOrder(){
    console.log('edit');
}
function deleteOrder(orderId){
    console.log('delete');
}
function getOrdersList(){
    console.log('full json orders list');
}
function getOrderDetails(){
    console.log('1 order details');
}
function showToast(msg,type=null){
    // Standard: Blue - INFO
    const state = {
        info:'lightblue',
        success: 'green',
        warning: 'yellow',
        error: 'red',
    }
    toast.style.display='flex';
    toast.style.background=!type?state.info:state[type];
    toast.textContent=msg
}
// console.log(menu, menu.getAttribute('data-size'));
// menu.setAttribute('data-size','closed');
menu.addEventListener('click',(e)=>changeSize(menu))
// search.addEventListener('click',()=>resizeElement(search,100))
orders.addEventListener('click',()=>console.log(createOrder()))
btnAdd.addEventListener('click',()=>console.log(btnAdd))