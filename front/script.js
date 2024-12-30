const $=(element)=>document.querySelector(element),
    getId=(element)=>document.getElementById(element),
    attr=(element,attribute)=>element.getAttribute(attribute),
    _=null,
    menu=getId('burgerIcon'),
    search=$('search'),
    btnAdd=$('.add2OrderBtn'),
    orders=getId('ordersBtn'),
    toast=getId('toast'),
    filters=getId('quickFilters').querySelectorAll('#pizzas,#burgers,#beverages')
function resizeElement(element,width,height=null){
    element.style.width=`${width}px`
    if(height)element.style.height=`${height}px`
}
function setUIcolor(state='standard'){
    const colors={
        standard:'white',
        filter:'yellow',
        success:'green',
        error:'red'
    }
    document.querySelectorAll('body',menu,search).forEach((el)=>el.style.background=colors[state])
    // document.body.style.background
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
    showToast('saved','info')
}
function editOrder(){
    // console.warn('edit');
    // console.error('edit');
    // console.info('edit');
}
editOrder();
function deleteOrder(orderId){
    console.log('delete');
}
function getOrdersList(){
    console.log('full json orders list');
}
function getOrderDetails(){
    console.log('1 order details');
}
function showToast(msg,type=info){
    const states = {
        info:'#d4f4ff',
        infoBorder:'#00bbff',
        success:'#ccffd5',
        successBorder:'#007526',
        warning:'#ffef76',
        warningBorder:'#ffe100',
        error:'#ff7b76',
        errorBorder:'#ff0800',
    }
    resizeElement(toast,200);
    // Standard: Blue - INFO
    toast.style.display='flex';
    toast.style.background=states[type];
    toast.style.borderColor=states[`${type}Border`];
    toast.textContent=msg
}
// console.log(menu, menu.getAttribute('data-size'));
// menu.setAttribute('data-size','closed');
menu.addEventListener('click',(e)=>changeSize(menu))
// search.addEventListener('click',()=>resizeElement(search,100))
orders.addEventListener('click',()=>console.log(createOrder()))
btnAdd.addEventListener('click',()=>console.log(btnAdd))
filters.forEach((filter)=>{filter.addEventListener('click',(e)=>{setUIcolor()})})