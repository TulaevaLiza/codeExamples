
var FLAG_ADD_MODE=true;

/**
 * Класс калькулятор для оценки стоимости работ (внутренней отделки помещений)
 * @param {object} настройки для калькулятора, 
 * 		содержит 
 * 		elem {object HTMLElement} контейнер для калькулятора на странице 
 * 		params {object JSON} объект полей калькулятора
 * 		contentWrap {object} объект который описывает стиль вывода калькулятора на странице (вкладки/сворачивание)
 * @constructor
 */

function Calculator(options) {
  this.elem=options.elem;
  this.params=options.params;
  this.data={};
  this.contentWrap=new Tabs();
}

/**
 * Инициализация объекта, вывод формы на дисплей
 * @this {object Calculator} 
 */

Calculator.prototype.init = function () {
/*  this.contentWrap.add("main",document.createTextNode(this.params.main.name),this.createHTML(this.params.main),false);  
  this.contentWrap.add("add",this.createDropdown('+','add-room',this.params.rooms),null,false,FLAG_ADD_MODE);  
  this.elem.appendChild(this.contentWrap.createHTML());
  console.log(this.contentWrap); */

    var that=this;
    this.elem.appendChild(this.createBlock("main",this.params.main,false));
    this.elem.appendChild(this.createSelectBlock());
    this.elem.querySelector('.add-room').addEventListener('click',function() { that.showSelectList();});

}

/**
 * Формирует HTML элемент с полями формы
 * @param {object JSON} data объект с полями формы для вывода
 * @this {object Calculator} 
 * @return {object HTMLElement} элемент div
 */

Calculator.prototype.createHTML = function(data) {
    var formDiv=document.createElement('div');
    formDiv.classList.add('form-container');
    if("formType" in data)
      formDiv.classList.add(data.formType);
    for(let i in data.fields) {
      formDiv.appendChild(this.createField(i,data.fields[i]));
    }
    return formDiv;
}

/**
 * Формирует выпадающий список
 * @param {string} name заголовок списка
 * @param {string} cl класс блока со списком
 * @param {object JSON} data объект с блоками, из которых будет сформирован список
 * @this {object Calculator} 
 * @return {object HTMLElement} элемент div
 */

Calculator.prototype.createDropdown = function(name,cl,data) {
  var div=document.createElement('div');
  div.classList.add('dropdown');
  div.classList.add(cl);
  var a=document.createElement('a');
  a.dataset.toggle='dropdown';
  a.innerHTML=name+' <b class="caret"></b>';
  a.href='#';
  div.appendChild(a);
  var ul=document.createElement('ul');
  ul.classList.add('dropdown-menu');

  for(let k in data) {
    li = document.createElement('li');
    li.innerHTML=data[k].name;
//    li.addEventListener('click',function() { that.addRoomBlock(this,sel);});
    ul.appendChild(li);
  }
  div.appendChild(ul);

  return div;
}


//

/**
 * Показывает список типов помещений, либо скрывает его 
 * @this {object Calculator} 
 */

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

/**
 * Добавляет блок с полями выбора конкретного тип помещения
 * @param {object HTMLElement} el элемент вызова с установленным blockId в dataset.param
 * @param {object HTMLElement} sel элемент со списком типов помещений 
 * @this {object Calculator} 
 */
Calculator.prototype.addNewBlock = function (el,sel) {  
    var blockId=el.dataset.param;
    var divWrap=this.createBlock(blockId,this.params.rooms[blockId],true)
    this.elem.insertBefore(divWrap,this.elem.querySelector('.add-room-block'));
    this.resetPanelCollapse(sel);
}

/**
 * Добавляет блок с дополнительными полями в конце родительского блока
 * @param {object HTMLElement} el элемент вызова с установленным subblockId в id или htmlFor
 * @this {object Calculator} 
 */

Calculator.prototype.showSubBlock = function (el) {
    var subblockId=el.nodeName=='LABEL'?el.htmlFor:el.id;
    var checked=el.querySelector('input').checked;
    var subblock=el.closest('.form-container').querySelector('#'+subblockId+'Wrap');
 
    if(checked && subblock==null)
      el.closest('.form-container').appendChild(this.createSubBlock(subblockId,this.params.subblocks[subblockId]));
    if(!checked && subblock!=null)
      subblock.remove();
} 

/**
 * Добавляет блок с дополнительными полями после ссылки вызова
 * @param {object HTMLElement} el элемент вызова с установленным subblockId в id
 * @this {object Calculator} 
 */

Calculator.prototype.showSubBlockAfterLink = function (el) {
    var subblockId=el.id;
    var subblock=el.parentNode.querySelector('#'+subblockId+'Wrap');
 
    if(subblock==null)
      el.parentNode.appendChild(this.createSubBlock(subblockId,this.params.subblocks[subblockId]));
    if(subblock!=null)
      subblock.remove();
}


/**
 * Формирует элемент fieldset с дополнительным блоком
 * @param {string} id идентификатор добавляемого блока
 * @param {object JSON} data объект с полями формы, выводимыми в блоке
 * @return {object HTMLElement} элемент fieldset
 */

Calculator.prototype.createSubBlock = function(id,data) {
    var frag = document.createElement('fieldset');
    frag.id=id+'Wrap';
    frag.className='sub-form';
    var h=document.createElement('legend');
    h.className='subblock-title';
    h.innerHTML=data.name;
    frag.appendChild(h);
    for(let i in data.fields) {
      frag.appendChild(this.createField(i,data.fields[i]));
    }
    return frag;
}

/**
 * Формирует элемент с основным блоком
 * @param {string} id идентификатор добавляемого блока
 * @param {object JSON} data объект с полями формы, выводимыми в блоке
 * @param {bool} isClose открыт/скрыт блок
 * @this {object Calculator} 
 * @return {object HTMLElement} элемент div
 */

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

/**
 * Формирует поле формы
 * @param {string} fieldId идентификатор добавляемого поля
 * @param {object JSON} field объект с параметрами поля
 * @return {object HTMLElement} элемент div
 */

Calculator.prototype.createField = function(fieldId,field) {
    var formGroup=document.createElement('div');
    formGroup.classList.add('form-group');
    switch(field.type) {
      case "select":
        formGroup.appendChild(this.createSelect(fieldId,field));
        break;
      case "checkbox":
        formGroup.appendChild(this.createCheckbox(fieldId,field));
        break;
      case "link":
	formGroup.classList.add('subblock');
        formGroup.appendChild(this.createLink(fieldId,field));
        break;
      default:
        formGroup.appendChild(this.createTextInput(fieldId,field));
    }
    return formGroup;
}

/**
 * Формирует поле формы типа ссылка
 * @param {string} fieldId идентификатор добавляемого поля
 * @param {object JSON} fieldParam объект с параметрами поля
 * @return {object DocumentFragment} 
 */

Calculator.prototype.createLink = function(fieldId,fieldParam) {
    var that=this;
    var out = document.createDocumentFragment();
    var a = document.createElement('a');
    a.id=fieldId;
    a.innerHTML='<i class="glyphicon glyphicon-plus"></i> '+fieldParam.name;
    if("click" in fieldParam)
      a.addEventListener("click",function() { that[fieldParam.click](this);});
    out.appendChild(a);
    if("isShow" in fieldParam) {
	if(fieldParam.isShow)
		this[fieldParam.click].call(a);	
     }  
    return out;
}


/**
 * Формирует поле формы типа Checkbox
 * @param {string} fieldId идентификатор добавляемого поля
 * @param {object JSON} fieldParam объект с параметрами поля
 * @return {object DocumentFragment} 
 */
Calculator.prototype.createCheckbox = function(fieldId,fieldParam) {
    var that=this;
    var out = document.createDocumentFragment();
    var label = document.createElement('label');
    label.htmlFor=fieldId;
    label.innerHTML='<input type="checkbox" id="'+fieldId+'"'+("required" in fieldParam?' '+fieldParam.required:'')+'> '+fieldParam.name;
    if("click" in fieldParam)
      label.addEventListener("click",function() { that[fieldParam.click](this);});
    out.appendChild(label);
    return out;
}


/**
 * Формирует поле формы типа Список
 * @param {string} fieldId идентификатор добавляемого поля
 * @param {object JSON} fieldParam объект с параметрами поля
 * @return {object DocumentFragment} 
 */
Calculator.prototype.createSelect = function(fieldId,fieldParam) {
     var out = document.createDocumentFragment();
    var label = document.createElement('label');
    label.htmlFor=fieldId;
    if(fieldParam.printName==false)
	    label.className='sr-only';
    if("name" in fieldParam)
      label.innerHTML=fieldParam.name;
    out.appendChild(label);
  
    var select=document.createElement('select');
    select.className='form-control';
    select.id=fieldId;
    if("required" in fieldParam)	
	    input.setAttribute('required','required');
    if("fieldWidth" in fieldParam)
      select.style.width=fieldParam.fieldWidth;
    if("data" in fieldParam)
    for(let i=0; i<fieldParam.data.length; i++) {
      var option = new Option(fieldParam.data[i],i);
      select.appendChild(option);
    }
    out.appendChild(select);
    if("sub" in fieldParam){
      var span = document.createElement('span');
      span.innerHTML=' '+fieldParam.sub;
      span.className='sub';
      out.appendChild(span);
    }

    return out;
}

/**
 * Формирует поле формы типа Текст
 * @param {string} fieldId идентификатор добавляемого поля
 * @param {object JSON} fieldParam объект с параметрами поля
 * @return {object DocumentFragment} 
 */

Calculator.prototype.createTextInput = function(fieldId,fieldParam) 
{
    var out = document.createDocumentFragment();
    var label = document.createElement('label');
    label.htmlFor=fieldId;
    if("name" in fieldParam)
      label.innerHTML=fieldParam.name;
    out.appendChild(label);
    
    var input=document.createElement('input');
    input.className='form-control';
    input.type='text';
    input.id=fieldId;
    if("required" in fieldParam)	
	    input.setAttribute('required','required');
    if("placeholder" in fieldParam)
      input.placeholder=fieldParam.placeholder;
    if("fieldWidth" in fieldParam)
      input.style.width=fieldParam.fieldWidth;
    
    out.appendChild(input);
    
    if("sub" in fieldParam){
      var span = document.createElement('span');
      span.innerHTML=' '+fieldParam.sub;
      span.className='sub';
      out.appendChild(span);
    }
    return out;
}

/**
 * Формирует блок для списка выбора типа помещения
 * @return {object HTMLElement} элемент div
 */

Calculator.prototype.createSelectBlock = function()
{
   var div = document.createElement('div');
   div.className='panel-group add-room-block';
   div.innerHTML='<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a class="add-room"><i class="glyphicon glyphicon-plus"></i> Добавить помещение</a></h4></div><div id="selectRoomType" class="panel-collapse collapse"><div class="panel-body"></div></div></div>';
   return div;
}

/**
 * Формирует элемент PanelGroup
 * @param {string} id идентификатор элемента
 * @param {string} title заголовок элемента
 * @param {object DocumentFragment} content содержимое элемента
 * @param {bool} isClosedIcon есть иконка закрывания (х)?
 * @return {object HTMLElement} элемент div
 */

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

/**
 * Сворачивает элемент PanelGroup
 * @param {object HTMLElement} el элемент
 */

Calculator.prototype.resetPanelCollapse = function(el) { el.classList.remove("in"); el.querySelector('.panel-body').innerHTML='';}

/**
 * Удаляет элемент PanelGroup
 * @this {object HTMLElement} элемент
 */

Calculator.prototype.removePanelGroup = function() {this.parentNode.parentNode.parentNode.remove();}  


/**
 * Добавляет в вкладки Tabs еще одну вкладку
 * @param {string} id идентификатор вкладки
 * @param {string} title заголовок вкладки
 * @param {object DocumentFragment} content содержимое вкладки
 * @param {bool} isClosedIcon есть иконка закрывания (х)?
 * @return {object DocumentFragment} 
 */

Calculator.prototype.phintTab = function(id,title,content,isClosedIcon) {
  if(!("tab-nav" in this.contentWrap)) {
    this.contentWrap=new Tabs();	
  }	
  this.contentWrap.addTab(id,title,content,isClosedIcon);
  var tabPanel=this.contentWrap.createTabHtml(this.elem);
  return tabPanel;
}



/**
 * Класс вкладки Tabs
 * @param {object} настройки для калькулятора, 
 * 		содержит 
 * 		tabContent {object} ассоциативный массив объектов элементов вкладок {'id {string}':{'nav':{string},'close':{bool},'content':{object DocumentFragment},'avtive':{bool}},{},..}
 * @constructor
 */

function Tabs() {
  this.tabContent=new Object();
}

/**
 * Добавляет в вкладки Tabs еще одну вкладку
 * @param {string} id идентификатор вкладки
 * @param {string} title заголовок вкладки
 * @param {object DocumentFragment} content содержимое вкладки
 * @param {bool} isClosedIcon есть иконка закрывания (х)?
 */

Tabs.prototype.add = function (id,title,content,isClosedIcon,addMode = false) {
  var blockId=id+'Wrap';
  var i=1;
  while(blockId in this.tabContent) {
    blockId=id+'Wrap'+i;
    i++;
  }


  this.tabContent[blockId]=new Object();
  this.tabContent[blockId].nav=title;
  this.tabContent[blockId].close=isClosedIcon;
  this.tabContent[blockId].content=content;
  if(addMode==false) {
    this.setNoActive();
    this.tabContent[blockId].active=true;
  }
  else {
    this.tabContent[blockId].active=false;
  }
  this.tabContent[blockId].addMode=addMode;
}

/**
 * Создает фрагмент документа с вкладками
 * @return {object DocumentFragment}
 */

Tabs.prototype.createHTML = function () {
  var that=this;
  var out = document.createElement('div');
  out.className='tabs';
  var tabNav = document.createElement('ul');
  tabNav.className='nav nav-tabs';
  var tab = document.createElement('div');
  tab.className='tab-content';
  var li,a,div,close,li_last,div_last;
  for(let id in this.tabContent) {
    li=document.createElement('li');
    if(this.tabContent[id].active===true) {
      li.className='active';
    }
    a=document.createElement('a');
    a.href='#'+id;
    a.dataset.toggle='tab';
    a.appendChild(this.tabContent[id].nav);
    li.appendChild(a);

    if(this.tabContent[id].close) {
      close=document.createElement('button');
      close.id=id;     
      close.className='close';     
      close.setAttribute('type','button');
      close.innerHTML='&times;';
      close.addEventListener('click',function() { that.removeTab(this);});
      li.appendChild(close);
    }

    if(this.tabContent[id].addMode===true) {
       li_last=li;
    }
    else {
      tabNav.appendChild(li); 
    }

    div=document.createElement('div');
    if(this.tabContent[id].active===true) {
      div.className='tab-pane active';
    }
    else {
      div.className='tab-pane';
    }
    div.id=id;
    if(this.tabContent[id].content!==null) {
      div.appendChild(this.tabContent[id].content);
    }
    if(this.tabContent[id].addMode===true) {
       div_last=div;
    }
    else {
      tab.appendChild(div);
    }
  }
  if(li_last)
    tabNav.appendChild(li_last); 
  if(div_last)
    tab.appendChild(div_last);

  out.appendChild(tabNav);
  out.appendChild(tab);
  return out;
}

/**
 * Устанавливает все вкладки не активными
 */

Tabs.prototype.setNoActive = function () {
  for(let id in this.tabContent) {
	this.tabContent[id].active=false;
  }
}

/**
 * Удаляет вкладку и перерисовывает оставшиеся
 * @param  el - ссылка в навигации удаляемой вкладки c id = id вкладки
 * @this - объект Tabs
 */

Tabs.prototype.removeTab = function (el) {
  var id=el.id;
  delete this.tabContent[id];
  el.closest('.tabs').innerHTML='';
  el.closest('.tabs').appendChild(this.createTabHTML());
}


/**
 *загрузка параметров блоков и полей калькулятора ajax запросом к скрипту, извлекающему их из базы данных	
 */

var $params;

$.ajax({
         url:"../load_params_string.php",
	 async:false,
	 error:function (jqXHR,status,err) {
		console.log(jqXHR,status,err);
	 },
         success:function (result){
//	    console.log(result);
            params=JSON.parse(result);
	    console.log(params);
	 }
});   

var calc=new Calculator({'elem':document.getElementById('calc'),'params':params});
calc.init();