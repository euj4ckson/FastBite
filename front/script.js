const $=(element)=>document.querySelector(element),
    log=(msg)=>console.log(msg),
    getClass=(element)=>document.querySelector(`.${element}`),
    getId=(element)=>document.getElementById(element),
    attr=(element,attribute)=>element.getAttribute(attribute),
    _=null,
    menu=getId('burgerIcon'),
    products=$('menu').querySelectorAll('li'),
    cardBtnAdd=getClass('add2OrderBtn'),
    search=$('search'),
    searchInput=getId('searchValue'),
    clearFilterBtn=getId('clearFilterBtn'),
    orders=getId('ordersBtn'),
    toast=getId('toast'),
    order=getId('orderDetails'),
    orderBtnRemove=getClass('btnRemoveUnit'),
    orderBtnAdd=getClass('btnAddUnit'),
    orderBtnDelete=getClass('btnDeleteItem'),
    opc=getClass('orderProductCount'),
    orderBtnClose=getClass('orderBtnClose'),
    closeToast=getId('closeToast'),
    filters=getId('quickFilters').querySelectorAll('#pizzas,#burgers,#beverages'),
    logs=getId('logs')
function addLog(action,item){
    let user = 'fulano',
        dt = new Date()
    const li = document.createElement('li')
    li.textContent=`${user} ${action} ${item} ${dt.getUTCHours()}:${dt.getUTCMinutes()} ${dt.getDate().toString().padStart(2,'0')}/${(dt.getMonth()+1).toString().padStart(2,'0')}/${dt.getFullYear()}`
    logs.appendChild(li);
}
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
orderBtnRemove.addEventListener('click',(e)=>{
    let actualValue = parseInt(opc.textContent)
    if(actualValue===0){
        deleteOrderItem(e.target.parentNode.parentNode.id)
        return
    }
    opc.textContent =parseInt(opc.textContent)-1
})
function deleteOrderItem(itemId){
    //call view function update order items
    getId(itemId).remove();
}
orderBtnAdd.addEventListener('click',()=>{
    opc.textContent =parseInt(opc.textContent)+1
})
orderBtnDelete.addEventListener('click',(e)=>{
    deleteOrderItem(e.target.parentNode.parentNode.id)
})
orderBtnDelete.querySelector('img').addEventListener('click',(e)=>{
    deleteOrderItem(e.target.parentNode.parentNode.parentNode.id)
})
orders.addEventListener('click',()=>{order.showModal();})
cardBtnAdd.addEventListener('click',()=>console.log(cardBtnAdd))
orderBtnClose.addEventListener('click',()=>{order.close()})
closeToast.addEventListener('click',()=>toast.close())
filters.forEach((filter)=>{filter.addEventListener('click',(e)=>{filterList(e.target);setUIstate()})})
