const $=(element)=>document.querySelector(element),
    attr=(element,attribute)=>element.getAttribute(attribute),
    _ = null,
    menu = $('nav'),
    search = $('search')
function resize(element,width,height=null){
    element.style.width=`${width}px`
    if(height)element.style.height=`${height}px`
}
function toggleSize(element){
    if(attr(menu,'data-size')==='opened'){console.log('is open')}
    else console.log(('closed'));
    //not passing e.target properly
}
console.log(menu, menu.getAttribute('data-size'));
menu.setAttribute('data-size','closed');
menu.addEventListener('click',(e)=>toggleSize(e.target))
search.addEventListener('click',()=>resize(search,100))