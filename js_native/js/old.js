/**
 * Показывает список типов помещений, либо скрывает его 
 * @this {object Calculator} 
 */
/*
Calculator.prototype.showSelectList = function () {
   var that=this;
   var sel = this.elem.querySelector('#selectRoomType');
    if(!sel.classList.contains("in")) {
      sel.classList.add("in");
      for(let k in this.params.rooms) {
        var span = document.createElement('span');
        span.dataset.param=k;
        span.innerHTML=this.params.rooms[k].name;
        span.addEventListener('click',function() { that.addRoomBlock(this,sel);});
        sel.querySelector('.panel-body').appendChild(span);
      }
    }
    else {
      this.resetPanelCollapse(sel);
    }
}  
 */
/**
 * Добавляет блок с полями выбора конкретного тип помещения
 * @param {object HTMLElement} el элемент вызова с установленным blockId в dataset.param
 * @param {object HTMLElement} sel элемент со списком типов помещений 
 * @this {object Calculator} 
 */

/*
Calculator.prototype.addNewBlock = function (el,sel) {  
    var blockId=el.dataset.param;
    var divWrap=this.createBlock(blockId,this.params.rooms[blockId],true)
    this.elem.insertBefore(divWrap,this.elem.querySelector('.add-room-block'));
    this.resetPanelCollapse(sel);
}
*/

/**
 * Формирует элемент с основным блоком
 * @param {string} id идентификатор добавляемого блока
 * @param {object JSON} data объект с полями формы, выводимыми в блоке
 * @param {bool} isClose открыт/скрыт блок
 * @this {object Calculator} 
 * @return {object HTMLElement} элемент div
 */

/*
Calculator.prototype.createBlock = function(id,data,isClose) {
    var formDiv=document.createElement('div');
    if("formType" in data)
      formDiv.className=data.formType;
    for(let i in data.fields) {
      formDiv.appendChild(this.createField(i,data.fields[i]));
    }
    var div=this.printPanelGroup(id,data.name,formDiv,isClose);
    return div;
}
*/

/**
 * Формирует блок для списка выбора типа помещения
 * @return {object HTMLElement} элемент div
 */
/*

Calculator.prototype.createSelectBlock = function()
{
   var div = document.createElement('div');
   div.className='panel-group add-room-block';
   div.innerHTML='<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a class="add-room"><i class="glyphicon glyphicon-plus"></i> Добавить помещение</a></h4></div><div id="selectRoomType" class="panel-collapse collapse"><div class="panel-body"></div></div></div>';
   return div;
}
*/

/**
 * Формирует элемент PanelGroup
 * @param {string} id идентификатор элемента
 * @param {string} title заголовок элемента
 * @param {object DocumentFragment} content содержимое элемента
 * @param {bool} isClosedIcon есть иконка закрывания (х)?
 * @return {object HTMLElement} элемент div
 */

/*
Calculator.prototype.printPanelGroup = function(id,title,content,isClosedIcon) 
{
    var panelBody=document.createElement('div');
    panelBody.className='panel-body';
    panelBody.appendChild(content);
    
    var panelCollapse=document.createElement('div');
    panelCollapse.className='panel-collapse collapse in';
    panelCollapse.id=id;
    panelCollapse.appendChild(panelBody);  
    
    var a=document.createElement('a');
    a.dataset.toggle='collapse';
    a.dataset.parent='#'+id+'Wrap';
    a.setAttribute('href','#'+id);  
    a.innerHTML=title;
    
    var h4=document.createElement('h4');
    h4.className='panel-title';
    h4.appendChild(a);
    
    if(isClosedIcon) {
      var close=document.createElement('button');
      close.className='close';     
      close.setAttribute('type','button');
      close.innerHTML='&times;';
      close.addEventListener('click',this.removePanelGroup);
    }
    
    var panelHeading=document.createElement('div');
    panelHeading.className='panel-heading';
    if(isClosedIcon)
      panelHeading.appendChild(close);
    panelHeading.appendChild(h4);
    
    var panel=document.createElement('div');
    panel.className='panel panel-default';
    panel.appendChild(panelHeading);
    panel.appendChild(panelCollapse);  
    
    var panelWrap=document.createElement('div');
    panelWrap.className='panel-group';
    panelWrap.id=id+'Wrap';
    panelWrap.appendChild(panel);
    
    return panelWrap;
}
*/

/**
 * Сворачивает элемент PanelGroup
 * @param {object HTMLElement} el элемент
 */
/*

Calculator.prototype.resetPanelCollapse = function(el) { el.classList.remove("in"); el.querySelector('.panel-body').innerHTML='';}

*/
/**
 * Удаляет элемент PanelGroup
 * @this {object HTMLElement} элемент
 */

/*
Calculator.prototype.removePanelGroup = function() {this.parentNode.parentNode.parentNode.remove();}  

*/
