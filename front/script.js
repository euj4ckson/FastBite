const $=(element)=>document.querySelector(element),
    getId=(element)=>document.getElementById(element),
    attr=(element,attribute)=>element.getAttribute(attribute),
    _=null,
    menu=getId('burgerIcon'),
    products=$('menu').querySelectorAll('li'),
    btnAdd=$('.add2OrderBtn'),
    search=$('search'),
    searchInput=getId('searchValue'),
    clearFilterBtn=getId('clearFilterBtn'),
    orders=getId('ordersBtn'),
    toast=getId('toast'),
    order=getId('orderDetails'),
    closeToast=getId('closeToast'),
    filters=getId('quickFilters').querySelectorAll('#pizzas,#burgers,#beverages'),
    log=getId('log')
function addLog(action,item){
    let user = 'fulano',
        dt = new Date()
    const li = document.createElement('li')
    li.textContent=`${user} ${action} ${item} ${dt.getUTCHours()}:${dt.getUTCMinutes()} ${dt.getDate().toString().padStart(2,'0')}/${(dt.getMonth()+1).toString().padStart(2,'0')}/${dt.getFullYear()}`
    log.appendChild(li);
}
addLog('save','#123')
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
    element.style.display=element.style.display==='none'?'flex':'none'
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
    console.info('edit')
}
function deleteOrder(orderId){
    console.info('delete')
}
function getOrdersList(){
    console.info('full json orders list')
}
function getOrderDetails(){
    console.info('1 order details')
}
function getProducts(){
    console.info('json get from backend')
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
    toast.showModal()
    toast.style.background=states[type]
    toast.style.borderColor=states[`${type}Border`]
    toast.querySelector('span').textContent=msg
}
function filterList(list,input){
    list.forEach((_,index)=>list[index].style.display=list[index].textContent.toUpperCase().indexOf(input.value.toUpperCase())>-1?"flex":"none");
}
function clearFilter(input){
    input.value='';
}
searchInput.addEventListener("keyup",()=>filterList(products,searchInput))
clearFilterBtn.addEventListener('click',()=>{
    clearFilter(searchInput)
    filterList(products,searchInput)
})
menu.addEventListener('click',(e)=>changeSize(menu))
// search.addEventListener('click',()=>resizeElement(search,100))
orders.addEventListener('click',()=>toast.showModal())
// orders.addEventListener('click',()=>console.log(createOrder()))
btnAdd.addEventListener('click',()=>console.log(btnAdd))
closeToast.addEventListener('click',()=>toast.close())
order.addEventListener('click',()=>order.close())
filters.forEach((filter)=>{filter.addEventListener('click',(e)=>{filterList(e.target);setUIstate()})})