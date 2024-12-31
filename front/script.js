const $=(element)=>document.querySelector(element),
    getId=(element)=>document.getElementById(element),
    attr=(element,attribute)=>element.getAttribute(attribute),
    _=null,
    menu=getId('burgerIcon'),
    search=$('search'),
    btnAdd=$('.add2OrderBtn'),
    orders=getId('ordersBtn'),
    toast=getId('toast'),
    closeToast=getId('closeToast'),
    filters=getId('quickFilters').querySelectorAll('#pizzas,#burgers,#beverages')
function resizeElement(element,width,height=null){
    element.style.width=`${width}px`
    if(height)element.style.height=`${height}px`
}
function setUIstate(state='standard'){
    const colors={
        standard:'white',
        filter:'yellow',
        success:'green',
        error:'red'
    }
    document.querySelectorAll('body',menu,search).forEach((el)=>el.style.background=colors[state])
}
function toggleVisibility(element){
    element.style.display=element.style.display==='flex'?'none':'flex'
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
    // console.log(sizes[el].maxHeight);
    // let a = parseFloat(window.getComputedStyle(menu).width);
    // console.log(sizes[el].minHeight);
    // console.log(parseFloat(window.getComputedStyle(menu).width));
    // console.log(menu);
    // if(attr(menu,'width')==='opened'){console.log('is open')}
    // else console.log(('closed'));
}
function createOrder(){
    console.info('create')
}
function editOrder(){
    console.info('edit');
}
function deleteOrder(orderId){
    console.info('delete');
}
function getOrdersList(){
    console.info('full json orders list');
}
function getOrderDetails(){
    console.info('1 order details');
}
function changeToastState(msg,type=null){
    if(!type){toast.style.display='none';return}
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
    toast.style.display='flex'
    toast.style.background=states[type]
    toast.style.borderColor=states[`${type}Border`]
    toast.querySelector('span').textContent=msg
}
menu.addEventListener('click',(e)=>changeSize(menu))
search.addEventListener('click',()=>resizeElement(search,100))
orders.addEventListener('click',()=>console.log(createOrder()))
btnAdd.addEventListener('click',()=>console.log(btnAdd))
closeToast.addEventListener('click',()=>console.log(btnAdd))
filters.forEach((filter)=>{filter.addEventListener('click',(e)=>{setUIstate()})})