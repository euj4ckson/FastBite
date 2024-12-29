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
    let el = 'menu';
    console.log(sizes[el].);
    // let a = parseFloat(window.getComputedStyle(menu).width);
    // console.log(sizes[el].minHeight);
    console.log(parseFloat(window.getComputedStyle(menu).width));
    console.log(menu);
    // if(attr(menu,'width')==='opened'){console.log('is open')}
    // else console.log(('closed'));
}
console.log(menu, menu.getAttribute('data-size'));
menu.setAttribute('data-size','closed');
menu.addEventListener('click',(e)=>toggleSize(menu))
search.addEventListener('click',()=>resize(search,100))
