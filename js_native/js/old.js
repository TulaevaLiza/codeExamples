/**
 * ���������� ������ ����� ���������, ���� �������� ��� 
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
 * ��������� ���� � ������ ������ ����������� ��� ���������
 * @param {object HTMLElement} el ������� ������ � ������������� blockId � dataset.param
 * @param {object HTMLElement} sel ������� �� ������� ����� ��������� 
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
 * ��������� ������� � �������� ������
 * @param {string} id ������������� ������������ �����
 * @param {object JSON} data ������ � ������ �����, ���������� � �����
 * @param {bool} isClose ������/����� ����
 * @this {object Calculator} 
 * @return {object HTMLElement} ������� div
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
 * ��������� ���� ��� ������ ������ ���� ���������
 * @return {object HTMLElement} ������� div
 */
/*

Calculator.prototype.createSelectBlock = function()
{
   var div = document.createElement('div');
   div.className='panel-group add-room-block';
   div.innerHTML='<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a class="add-room"><i class="glyphicon glyphicon-plus"></i> �������� ���������</a></h4></div><div id="selectRoomType" class="panel-collapse collapse"><div class="panel-body"></div></div></div>';
   return div;
}
*/

/**
 * ��������� ������� PanelGroup
 * @param {string} id ������������� ��������
 * @param {string} title ��������� ��������
 * @param {object DocumentFragment} content ���������� ��������
 * @param {bool} isClosedIcon ���� ������ ���������� (�)?
 * @return {object HTMLElement} ������� div
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
 * ����������� ������� PanelGroup
 * @param {object HTMLElement} el �������
 */
/*

Calculator.prototype.resetPanelCollapse = function(el) { el.classList.remove("in"); el.querySelector('.panel-body').innerHTML='';}

*/
/**
 * ������� ������� PanelGroup
 * @this {object HTMLElement} �������
 */

/*
Calculator.prototype.removePanelGroup = function() {this.parentNode.parentNode.parentNode.remove();}  

*/
